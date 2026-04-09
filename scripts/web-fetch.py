#!/usr/bin/env python3
"""
Web content fetcher for anything-to-notebooklm skill.
Supports WeChat articles (--stealth) and regular web pages.
Usage: python3 web-fetch.py <url> [--stealth] [max_chars]
"""
import sys
import os
import subprocess
import json
import re

def fetch_with_jina(url):
    """Use Jina Reader as fallback."""
    try:
        result = subprocess.run(
            ["curl", "-s", f"https://r.jina.ai/{url}"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and len(result.stdout) > 100:
            return result.stdout
    except Exception:
        pass
    return None

def fetch_with_scrapling(url, stealth=False):
    """Use scrapling (headless browser) for JS-rendered or anti-scraping sites."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fetch_py = os.path.join(script_dir, "..", "web-content-fetcher", "scripts", "fetch.py")
    
    if not os.path.exists(fetch_py):
        return None
    
    cmd = [sys.executable, fetch_py, url]
    if stealth:
        cmd.append("--stealth")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass
    return None

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else None
    if not url:
        print("Usage: web-fetch.py <url> [--stealth] [max_chars]", file=sys.stderr)
        sys.exit(1)
    
    stealth = "--stealth" in sys.argv
    max_chars = None
    
    for arg in sys.argv[2:]:
        if arg == "--stealth":
            continue
        if arg.isdigit():
            max_chars = int(arg)
    
    # Detect WeChat → force stealth
    if "mp.weixin.qq.com" in url:
        stealth = True
    
    content = fetch_with_scrapling(url, stealth)
    
    if not content or len(content) < 100:
        content = fetch_with_jina(url)
    
    if not content:
        print(f"Failed to fetch content from {url}", file=sys.stderr)
        sys.exit(1)
    
    if max_chars and len(content) > max_chars:
        content = content[:max_chars]
    
    print(content)

if __name__ == "__main__":
    main()
