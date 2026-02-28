import asyncio
import json
import re
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

FINTECH_COMPANIES = [
    {"name": "Coinbase",  "url": "https://boards.greenhouse.io/coinbase"},
    {"name": "Affirm",    "url": "https://boards.greenhouse.io/affirm"},
    {"name": "Robinhood", "url": "https://boards.greenhouse.io/robinhood"},
    {"name": "Stripe",    "url": "https://boards.greenhouse.io/stripe"},
    {"name": "Brex",      "url": "https://boards.greenhouse.io/brex"},
    {"name": "Ramp",      "url": "https://boards.greenhouse.io/rampfinancial"},
    {"name": "Chime",     "url": "https://boards.greenhouse.io/chime"},
    {"name": "Carta",     "url": "https://boards.greenhouse.io/carta"},
    {"name": "Marqeta",   "url": "https://boards.greenhouse.io/marqeta"},
]

# ─────────────────────────────────────────────
# NOISE PATTERNS TO REMOVE
# These are common patterns found in navigation,
# footers, and other non-job content
# ─────────────────────────────────────────────
NOISE_PATTERNS = [
    r'\[Skip to.*?\].*?\n',          # Skip navigation links
    r'\[Sign in\].*?\n',             # Sign in links
    r'\[Sign up\].*?\n',             # Sign up links
    r'!\[.*?\]\(.*?\)',              # Images (markdown format)
    r'\[!\[.*?\]\(.*?\)\].*?\n',    # Image links
    r'©.*?\n',                       # Copyright lines
    r'Privacy.*?Terms.*?\n',         # Privacy/Terms lines
    r'Cookie.*?\n',                  # Cookie notices
    r'\* \* \*',                     # Horizontal rules
]

# Keywords that indicate job-related content
JOB_SIGNALS = [
    'engineer', 'developer', 'software', 'backend', 'frontend',
    'infrastructure', 'platform', 'data', 'security', 'product',
    'manager', 'director', 'analyst', 'intern', 'remote', 'salary',
    'qualifications', 'requirements', 'responsibilities', 'experience',
    'job-boards.greenhouse.io', 'boards.greenhouse.io/robinhood/jobs',
    'stripe.com/jobs/listing'
]


def clean_content(raw_markdown: str, company_name: str) -> str:
    """
    Remove noise from scraped markdown and keep only job-relevant content.
    Works in 3 passes:
      Pass 1 - Remove known noise patterns using regex
      Pass 2 - Keep only lines that contain job-related signals
      Pass 3 - Remove excessive blank lines
    """
    if not raw_markdown:
        return ""

    # ── Pass 1: Remove known noise patterns ──
    cleaned = raw_markdown
    for pattern in NOISE_PATTERNS:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

    # ── Pass 2: Filter line by line ──
    lines = cleaned.split('\n')
    job_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip empty lines for now (add back later)
        if not line_stripped:
            continue
            
        # Skip lines that are pure navigation (just a link, nothing else)
        if re.match(r'^\[.*?\]\(https?://.*?\)$', line_stripped):
            # But keep it if it looks like a job link
            if any(signal in line_stripped.lower() for signal in JOB_SIGNALS):
                job_lines.append(line_stripped)
            continue
        
        # Skip very short lines that are likely menu items (under 15 chars)
        if len(line_stripped) < 15 and not line_stripped.startswith('#'):
            continue
        
        # Keep lines with job-related signals
        if any(signal in line_stripped.lower() for signal in JOB_SIGNALS):
            job_lines.append(line_stripped)
            continue
            
        # Keep section headers (## headings)
        if line_stripped.startswith('#'):
            job_lines.append(line_stripped)
            continue

    # ── Pass 3: Join and remove excessive blank lines ──
    result = '\n'.join(job_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)  # Max 2 consecutive newlines

    return result.strip()


def count_jobs(content: str) -> int:
    """Rough estimate of job count from cleaned content"""
    # Count lines that look like job titles (contain job keywords)
    job_title_signals = ['engineer', 'developer', 'manager', 'director', 
                         'analyst', 'intern', 'lead', 'architect']
    count = 0
    for line in content.split('\n'):
        if any(s in line.lower() for s in job_title_signals):
            count += 1
    return count


async def scrape_company(crawler, company):
    print(f"\n🔍 Scraping {company['name']}...")

    try:
        config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
        result = await crawler.arun(url=company["url"], config=config)

        if result.success:
            raw = result.markdown
            cleaned = clean_content(raw, company['name'])
            job_count = count_jobs(cleaned)
            
            # Warn if content is suspiciously short (likely wrong page)
            if len(cleaned) < 100:
                print(f"  ⚠️  {company['name']} — content too short, may be wrong URL")
            else:
                print(f"  ✅ {company['name']} — cleaned {len(raw):,} → {len(cleaned):,} chars | ~{job_count} job mentions")

            return {
                "company":        company["name"],
                "url":            company["url"],
                "raw_length":     len(raw),
                "cleaned_length": len(cleaned),
                "content":        cleaned,
                "scraped_at":     datetime.now().isoformat()
            }
        else:
            print(f"  ❌ {company['name']} — failed to fetch page")
            return None

    except Exception as e:
        print(f"  ❌ {company['name']} — error: {e}")
        return None


async def main():
    print("=" * 55)
    print("  🚀 FINTECH SCRAPER v3 — With Content Cleaning")
    print("=" * 55)

    results = []

    async with AsyncWebCrawler() as crawler:
        for company in FINTECH_COMPANIES:
            data = await scrape_company(crawler, company)
            if data:
                results.append(data)
            await asyncio.sleep(2)

    # Save cleaned results
    with open("fintech_cleaned.json", "w") as f:
        json.dump(results, f, indent=2)

    # Print summary
    print(f"\n{'='*55}")
    print(f"  📊 SUMMARY")
    print(f"{'='*55}")
    total_raw = sum(r['raw_length'] for r in results)
    total_clean = sum(r['cleaned_length'] for r in results)
    reduction = ((total_raw - total_clean) / total_raw * 100) if total_raw else 0
    print(f"  Companies scraped : {len(results)}/{len(FINTECH_COMPANIES)}")
    print(f"  Raw content size  : {total_raw:,} chars")
    print(f"  Clean content size: {total_clean:,} chars")
    print(f"  Noise removed     : {reduction:.1f}%")
    print(f"\n  💾 Saved to fintech_cleaned.json")
    print(f"{'='*55}")


if __name__ == "__main__":
    asyncio.run(main())