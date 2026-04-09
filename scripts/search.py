#!/usr/bin/env python3
"""
Search aggregator for anything-to-notebooklm skill.
Uses Tavily (via existing web search) to summarize results for a topic.
Usage: python3 search.py "<query>" [--count 5] [--output FILE]
"""
import sys
import os
import subprocess
import json

def search_tavily(query, count=5):
    """Use Tavily CLI or direct API to search."""
    try:
        result = subprocess.run(
            ["tavily", "search", query, "--max-results", str(count)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout
    except FileNotFoundError:
        pass

    # Fallback: use curl to call Tavily API directly
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if api_key:
        import urllib.request
        data = json.dumps({"query": query, "max_results": count}).encode()
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=data,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                result = json.loads(resp.read())
                results = result.get("results", [])
                return json.dumps(results, indent=2, ensure_ascii=False)
        except Exception:
            pass

    # Last resort: jinaai search
    try:
        result = subprocess.run(
            ["curl", "-s", f"https://r.jina.ai/https://duckduckgo.com/?q={query}&format=json"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except Exception:
        pass

    return None

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    query = args[0] if args else None
    if not query:
        print("Usage: search.py <query> [--count N] [--output FILE]", file=sys.stderr)
        sys.exit(1)

    count = 5
    output = None

    for f in flags:
        if f.startswith("--count="):
            count = int(f.split("=")[1])
        elif f == "--output" and flags.index(f) + 1 < len(args):
            output = args[flags.index(f) + 1]

    result = search_tavily(query, count)
    if not result:
        print("Search failed. Check Tavily API key or network.", file=sys.stderr)
        sys.exit(1)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(result)

    print(result)

if __name__ == "__main__":
    main()
