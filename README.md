# 🏦 Fintech Hiring Intelligence System

> An end-to-end AI pipeline that scrapes, analyzes, and visualizes software engineering job listings across top fintech companies — running **100% free and locally** on your machine.

---

## 📌 What This Project Does

This system automatically:
1. **Scrapes** career pages from top fintech companies
2. **Cleans** the raw content by removing navigation noise
3. **Analyzes** each company's job listings using a local AI model
4. **Finds patterns** across all companies
5. **Generates** a beautiful HTML dashboard with all insights

No paid APIs. No cloud services. Everything runs on your local machine.

---

## 🏗️ Architecture

```
Career Pages (Greenhouse ATS)
        ↓
   Crawl4AI (Web Scraper)
        ↓
  Content Cleaner (Python)
        ↓
  LLaMA 3.2 via Ollama (Local AI)
        ↓
   Pattern Finder (Python)
        ↓
   HTML Dashboard (Report)
```

---

## 🏢 Companies Targeted (Phase 1)

| Company | ATS | Status |
|---|---|---|
| Coinbase | Greenhouse | ✅ |
| Affirm | Greenhouse | ✅ |
| Robinhood | Greenhouse | ✅ |
| Stripe | Greenhouse | ✅ |
| Brex | Greenhouse | ✅ |
| Chime | Greenhouse | ✅ |
| Carta | Greenhouse | ✅ |
| Marqeta | Greenhouse | ✅ |

---

## 📁 Project Structure

```
scraper/
│
├── fintech_scraper_v2.py     # Step 1 — Scrapes career pages using Crawl4AI
├── ai_analyzer.py            # Step 2 — Analyzes job listings with LLaMA 3.2
├── pattern_finder.py         # Step 3 — Finds trends across all companies
├── generate_report.py        # Step 4 — Generates the HTML dashboard
│
├── fintech_cleaned.json      # Cleaned scraped content (auto-generated)
├── fintech_insights.json     # AI-extracted insights per company (auto-generated)
├── fintech_patterns.json     # Cross-company patterns (auto-generated)
├── fintech_report.html       # Final visual dashboard (auto-generated)
└── fintech_report.txt        # Plain text report (auto-generated)
```

---

## ⚙️ Tech Stack

| Tool | Purpose | Cost |
|---|---|---|
| **Python 3.11** | Core language | Free |
| **Crawl4AI** | AI-powered web scraping | Free / Open Source |
| **Ollama** | Run AI models locally | Free |
| **LLaMA 3.2** | Job description analysis | Free / Open Source |
| **Playwright** | Headless browser (via Crawl4AI) | Free |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11+
- Windows / Mac / Linux
- NVIDIA GPU recommended (runs on CPU too)

### Step 1 — Clone and Set Up Environment

```bash
# Create project folder
mkdir scraper
cd scraper

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### Step 2 — Install Python Dependencies

```bash
pip install crawl4ai requests
crawl4ai-setup
crawl4ai-doctor
```

### Step 3 — Install Ollama & Download Model

Download Ollama from [https://ollama.com](https://ollama.com) and install it.

Then pull the LLaMA model:

```bash
ollama pull llama3.2
```

Verify GPU is being used:

```bash
ollama ps
# Should show: PROCESSOR = 100% GPU
```

---

## ▶️ How to Run

Run each script in order:

```bash
# Step 1 — Scrape career pages
python fintech_scraper_v2.py

# Step 2 — Analyze with AI
python ai_analyzer.py

# Step 3 — Find patterns
python pattern_finder.py

# Step 4 — Generate dashboard
python generate_report.py

# Open the dashboard
start fintech_report.html       # Windows
open fintech_report.html        # Mac
```

---

## 📊 Key Findings

From analyzing 8 fintech companies:

- **Python** appears in 60%+ of backend engineering roles
- **Go** is the second most demanded language at 50%
- **Kubernetes & Kafka** are the dominant infrastructure tools
- **Senior and Staff** levels dominate — fintech rarely hires juniors
- **Remote** is the most common location offering
- **High performance, ownership, and urgency** are the most valued cultural traits

---

## 🔍 How Each Script Works

### `fintech_scraper_v2.py`
Uses **Crawl4AI** to visit each company's Greenhouse career page. Returns clean markdown text instead of raw HTML. Applies a 3-pass content filter to remove navigation menus, footers, and other noise — reducing content size by ~51%.

### `ai_analyzer.py`
Sends each company's cleaned content to **LLaMA 3.2** running locally via Ollama. The model extracts structured JSON with: job titles, required skills, experience levels, locations, domain focus, candidate traits, and key observations. Saves progress after each company so a crash won't lose your work.

### `pattern_finder.py`
Uses Python's `Counter` to find frequency patterns across all companies. Also sends a summary to LLaMA for a plain-English deep analysis with career advice for backend engineers targeting fintech.

### `generate_report.py`
Reads all the insights and generates a polished **HTML dashboard** with skill bar charts, experience level pills, location breakdown, trait tags, and individual company cards. Opens directly in your browser.

---

## 🗺️ Roadmap

- [x] Phase 1 — Greenhouse ATS companies (~8 companies)
- [ ] Phase 2 — Lever ATS companies (Netflix, Lyft, Reddit)
- [ ] Phase 3 — Workday companies (Google, Amazon, Microsoft)
- [ ] Phase 4 — Custom career pages (Apple, Meta, Stripe)
- [ ] Add PostgreSQL storage for historical tracking
- [ ] Schedule weekly re-scraping with cron
- [ ] Build Spring Boot REST API to query insights
- [ ] Add job URL tracker for direct apply links

---

## 💼 Resume Description

> **Fintech Hiring Intelligence System** | Python, Crawl4AI, LLaMA 3.2, Ollama
>
> Built an end-to-end AI pipeline that scrapes and analyzes SWE job listings across 8+ top fintech companies including Stripe, Coinbase, Affirm, and Robinhood. Used Crawl4AI for intelligent web scraping with 51% noise reduction and LLaMA 3.2 (running locally via Ollama) for structured insight extraction from unstructured job descriptions. Generated an interactive HTML dashboard revealing cross-company hiring patterns. Designed modular architecture with crash-safe incremental saving across scraping, cleaning, analysis, and reporting layers.

---

## ⚠️ Notes

- Always respect `robots.txt` and rate limit your requests
- Job listings change frequently — re-run weekly for fresh data
- The `RequestsDependencyWarning` from urllib3 is harmless and can be ignored
- If a company shows "Page not found" they have moved to a different ATS

---

## 👤 Author

Built as a portfolio project to demonstrate AI integration, distributed pipeline design, and backend engineering skills targeting the fintech industry.
