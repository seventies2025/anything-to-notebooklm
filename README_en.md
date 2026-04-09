# Anything to NotebookLM

**Transform any content into any format using AI.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[English](README.md) | [中文](README_zh.md)

---

## What Is This?

A **Claude Code/OpenClaw Skill** that converts **any content source** into **any output format** powered by [Google NotebookLM](https://notebooklm.google.com/).

```
You: Turn this WeChat article into a podcast
AI: ✅ 8-minute podcast generated → podcast.mp3

You: Make a mind map from this EPUB book
AI: ✅ Mind map generated → mindmap.json

You: Create a PPT from this YouTube video
AI: ✅ 25-slide presentation generated → slides.pdf
```

**How it works**: Fetch content from multiple sources → Upload to NotebookLM → AI generates your desired format.

---

## Supported Content Sources (15+ formats)

| Category | Sources |
|----------|---------|
| **Social** | WeChat articles (anti-scraping bypass), YouTube videos (auto-captions) |
| **Web** | Any webpage, search queries (auto-summarize) |
| **Documents** | Word (.docx), PowerPoint (.pptx), Excel (.xlsx), PDF (incl. scanned OCR), EPUB, Markdown |
| **Media** | Images (JPEG/PNG/GIF - OCR), Audio (WAV/MP3 - transcription) |
| **Data** | CSV, JSON, XML, ZIP archives (batch processing) |

**Powered by**: [Microsoft markitdown](https://github.com/microsoft/markitdown)

---

## Supported Output Formats

| Format | Use Case | Time | Example Trigger |
|--------|----------|------|-----------------|
| 🎙️ **Podcast** | Commute listening | 2-5 min | "Generate podcast", "Make audio" |
| 📊 **PPT/Slides** | Team presentations | 1-3 min | "Make PPT", "Create slides" |
| 🗺️ **Mind Map** | Structure thinking | 1-2 min | "Draw mind map", "Generate brain map" |
| 📝 **Quiz** | Self-testing | 1-2 min | "Generate quiz", "Create questions" |
| 🎬 **Video** | Visualization | 3-8 min | "Make a video" |
| 📄 **Report** | Deep analysis | 2-4 min | "Generate report", "Write summary" |
| 📈 **Infographic** | Data visualization | 2-3 min | "Make infographic" |
| 📋 **Flashcards** | Memorization | 1-2 min | "Make flashcards" |

**Pure natural language — no commands to remember!**

---

## Quick Start

### Requirements

- ✅ Python 3.9+
- ✅ Git (pre-installed on macOS/Linux)

That's it! All other dependencies install automatically.

### Installation (3 Steps)

```bash
# 1. Clone to Claude skills directory
cd ~/.claude/skills/
git clone https://github.com/joeseesun/anything-to-notebooklm
cd anything-to-notebooklm

# 2. Install all dependencies
./install.sh

# 3. Configure MCP per the prompts, then restart Claude Code
```

### First-Time Setup

```bash
# NotebookLM authentication (one-time only)
notebooklm login
notebooklm list  # verify success

# Environment check (optional)
./check_env.py
```

---

## Usage Examples

### Example 1: Article → Podcast

```
You: Generate a podcast from this article https://mp.weixin.qq.com/s/abc123

AI executes:
  ✓ Fetch WeChat article content
  ✓ Upload to NotebookLM
  ✓ Generate podcast (2-5 min)

✅ Result: /tmp/article_podcast.mp3 (8 min, 12.3 MB)
💡 Use case: Listen to in-depth articles during commute
```

### Example 2: EPUB → PPT

```
You: Make a PPT from this book /Users/joe/Books/sapiens.epub

AI executes:
  ✓ Extract ebook content (150K chars)
  ✓ AI refine key points
  ✓ Generate professional PPT

✅ Result: /tmp/sapiens_slides.pdf (25 pages, 3.8 MB)
💡 Use case: Use directly for book club presentations
```

### Example 3: YouTube → Quiz

```
You: Generate a quiz from this YouTube video https://youtube.com/watch?v=abc

AI executes:
  ✓ Extract video subtitles
  ✓ AI analyze key knowledge points
  ✓ Auto-generate questions

✅ Result: /tmp/video_quiz.md (15 questions: 10 MCQ + 5 essay)
💡 Use case: Test your learning retention
```

### Example 4: Multi-Source → Report

```
You: Generate a report from these sources:
  - https://example.com/article1
  - https://youtube.com/watch?v=xyz
  - /Users/joe/research.pdf

AI executes:
  ✓ Aggregate 3 different sources
  ✓ AI integrated analysis
  ✓ Generate comprehensive report

✅ Result: /tmp/multi_source_report.md (7 sections, 15.2 KB)
💡 Use case: Comprehensive topic research report
```

### Example 5: Scanned Image → Text

```
You: Convert this scanned image to text /Users/joe/scan.jpg

AI executes:
  ✓ OCR recognize text in image
  ✓ Extract as plain text
  ✓ Generate structured document

✅ Result: /tmp/scan_document.txt (95%+ accuracy)
💡 Use case: Digitize scanned documents
```

---

## Key Features

### 🧠 Smart Detection
Automatically identify input type — no manual specification needed:

```
https://mp.weixin.qq.com/s/xxx   → WeChat article
https://youtube.com/watch?v=xxx  → YouTube video
/path/to/file.epub               → EPUB ebook
"Search 'AI trends'"              → Search query
```

### 🚀 Fully Automated
From fetching to generation, seamless pipeline:

```
Input → Fetch → Convert → Upload → Generate → Download
        ‾‾‾‾‾‾‾‾‾‾全自动‾‾‾‾‾‾‾‾‾‾
```

### 🌐 Multi-Source Integration
Mix multiple content sources:

```
Article + Video + PDF + Search results → Comprehensive Report
```

### 🔒 Local-First Processing
Sensitive content processed locally:

```
WeChat article → Local MCP fetch → Local conversion → NotebookLM
```

---

## Architecture

```
┌─────────────────────────────────────┐
│         User Natural Language        │
│  "Generate podcast from this article"│
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│          Claude Code Skill           │
│  • Smart content source detection    │
│  • Auto-invoke appropriate tools     │
└──────────────┬──────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
┌──────────┐     ┌─────────────┐
│ WeChat   │     │ Other       │
│ MCP fetch│     │ markitdown  │
└─────┬────┘     └──────┬──────┘
      │                 │
      └────────┬────────┘
               │
               ▼
┌─────────────────────────────────────┐
│          NotebookLM API             │
│  • Upload content sources            │
│  • AI generate target formats       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Generated Files              │
│  .mp3 / .pdf / .json / .md          │
└─────────────────────────────────────┘
```

---

## Advanced Usage

### Add to Existing Notebook

```
Add this article to my [AI Research] notebook https://example.com
```

### Batch Processing

```
Generate podcasts from all these articles:
1. https://mp.weixin.qq.com/s/abc123
2. https://example.com/article2
3. /Users/joe/notes.md
```

### ZIP Batch Conversion

```
Convert all documents in this ZIP to podcast /path/to/files.zip
```

Auto-extract, detect, convert, and merge.

---

## Troubleshooting

### MCP Tools Not Found

```bash
# Test MCP server
python ~/.claude/skills/anything-to-notebooklm/wexin-read-mcp/src/server.py

# Reinstall dependencies
cd ~/.claude/skills/anything-to-notebooklm/wexin-read-mcp
pip install -r requirements.txt
playwright install chromium
```

### NotebookLM Auth Failed

```bash
notebooklm login     # Re-authenticate
notebooklm list      # Verify
```

### Environment Check

```bash
./check_env.py       # 13-point check
./install.sh         # Reinstall
```

---

## Contributing

PRs, Issues, and suggestions welcome!

## FAQ

<details>
<summary><b>Q: Which languages are supported?</b></summary>

A: NotebookLM supports multiple languages; Chinese and English work best.
</details>

<details>
<summary><b>Q: Who voices the podcast?</b></summary>

A: Google AI voice synthesis. English has two AI hosts in dialogue; Chinese is single narrator.
</details>

<details>
<summary><b>Q: Any content length limits?</b></summary>

A:
- Minimum: ~500 characters
- Maximum: ~500,000 characters
- Recommended: 1,000-10,000 for best results
</details>

<details>
<summary><b>Q: Can I use it commercially?</b></summary>

A:
- This Skill: MIT license, free to use
- Generated content: Subject to NotebookLM Terms of Service
- Original content: Subject to original content copyright
- Recommendation: For personal learning only
</details>

<details>
<summary><b>Q: Why is MCP needed?</b></summary>

A: WeChat articles have anti-scraping protections. MCP uses browser simulation to bypass them. Other sources (webpages, YouTube, PDF) don't need MCP.
</details>

---

## License

[MIT License](LICENSE)

## Acknowledgments

- [Google NotebookLM](https://notebooklm.google.com/) - AI content generation
- [Microsoft markitdown](https://github.com/microsoft/markitdown) - Document conversion
- [wexin-read-mcp](https://github.com/Bwkyd/wexin-read-mcp) - WeChat fetching
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) - NotebookLM CLI

## Contact

- **Issues**: [GitHub Issues](https://github.com/joeseesun/anything-to-notebooklm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/joeseesun/anything-to-notebooklm/discussions)

---

<div align="center">

**If you find this useful, please give it a ⭐ Star!**

Made with ❤️ by [Joe](https://github.com/joeseesun)

</div>
