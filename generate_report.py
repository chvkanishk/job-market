import json
from collections import Counter
from datetime import datetime


def load_data():
    with open("fintech_insights.json", "r") as f:
        insights = json.load(f)
    valid = [d for d in insights if "error" not in d]
    return valid


def build_counters(insights):
    all_skills, all_levels, all_locations, all_traits, all_domains, all_roles = [], [], [], [], [], []
    for c in insights:
        all_skills.extend(c.get("required_skills", []))
        all_levels.extend(c.get("experience_levels", []))
        all_locations.extend(c.get("locations", []))
        all_traits.extend(c.get("candidate_traits", []))
        all_roles.extend(c.get("software_engineering_roles", []))
        d = c.get("domain_focus", "")
        if d:
            all_domains.append(d.lower().strip())

    return {
        "skills":    Counter(all_skills).most_common(8),
        "levels":    Counter(all_levels).most_common(5),
        "locations": Counter(all_locations).most_common(6),
        "traits":    Counter(all_traits).most_common(6),
        "domains":   Counter(all_domains).most_common(5),
        "roles":     Counter(all_roles).most_common(8),
    }


def generate_html(insights, counters):
    n = len(insights)
    date = datetime.now().strftime("%B %d, %Y")

    # Build skill bars
    max_skill = counters["skills"][0][1] if counters["skills"] else 1
    skill_bars = ""
    for skill, count in counters["skills"]:
        pct = int((count / n) * 100)
        width = int((count / max_skill) * 100)
        skill_bars += f"""
        <div class="bar-row">
            <span class="bar-label">{skill}</span>
            <div class="bar-track">
                <div class="bar-fill" style="width:{width}%"></div>
            </div>
            <span class="bar-pct">{pct}%</span>
        </div>"""

    # Build level pills
    level_pills = ""
    for level, count in counters["levels"]:
        pct = int((count / n) * 100)
        level_pills += f'<div class="pill">{level} <span class="pill-count">{pct}%</span></div>'

    # Build location list
    location_items = ""
    for loc, count in counters["locations"]:
        location_items += f'<div class="loc-item"><span class="loc-dot">◆</span>{loc}<span class="loc-num">{count}</span></div>'

    # Build trait tags
    trait_tags = ""
    for trait, count in counters["traits"]:
        if trait.lower() not in ["culture", "personality traits"]:
            trait_tags += f'<span class="trait-tag">{trait}</span>'

    # Build company cards
    company_cards = ""
    colors = ["#00d4ff", "#ff6b35", "#7c3aed", "#10b981", "#f59e0b", "#ef4444", "#3b82f6", "#ec4899"]
    for i, company in enumerate(insights):
        color = colors[i % len(colors)]
        roles = company.get("software_engineering_roles", [])[:3]
        skills = company.get("required_skills", [])[:4]
        domain = company.get("domain_focus", "N/A")
        levels = ", ".join(company.get("experience_levels", [])[:3])
        obs = company.get("notable_observations", "")

        roles_html = "".join(f"<li>{r}</li>" for r in roles)
        skills_html = "".join(f'<span class="skill-chip">{s}</span>' for s in skills)

        company_cards += f"""
        <div class="company-card">
            <div class="card-accent" style="background:{color}"></div>
            <div class="card-body">
                <div class="card-header">
                    <h3 class="company-name">{company['company']}</h3>
                    <span class="domain-badge">{domain}</span>
                </div>
                <div class="card-section">
                    <p class="section-label">TOP ROLES</p>
                    <ul class="role-list">{roles_html}</ul>
                </div>
                <div class="card-section">
                    <p class="section-label">KEY SKILLS</p>
                    <div class="skill-chips">{skills_html}</div>
                </div>
                <div class="card-section">
                    <p class="section-label">LEVELS HIRING</p>
                    <p class="levels-text">{levels}</p>
                </div>
                {f'<div class="card-obs">{obs}</div>' if obs else ''}
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fintech Hiring Intelligence Report</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --bg: #0a0a0f;
    --surface: #13131a;
    --surface2: #1a1a24;
    --border: #2a2a3a;
    --text: #e8e8f0;
    --muted: #6b6b80;
    --accent: #00d4ff;
    --accent2: #ff6b35;
    --green: #10b981;
  }}

  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Syne', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }}

  /* HERO */
  .hero {{
    padding: 80px 60px 60px;
    position: relative;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(135deg, #0a0a0f 0%, #0d0d1a 100%);
  }}
  .hero::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(0,212,255,0.05) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(255,107,53,0.05) 0%, transparent 50%);
    pointer-events: none;
  }}
  .hero-tag {{
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 20px;
  }}
  .hero h1 {{
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -2px;
    margin-bottom: 16px;
  }}
  .hero h1 span {{ color: var(--accent); }}
  .hero-sub {{
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: var(--muted);
    margin-top: 24px;
  }}
  .hero-stats {{
    display: flex;
    gap: 40px;
    margin-top: 40px;
    flex-wrap: wrap;
  }}
  .stat-block {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}
  .stat-num {{
    font-size: 36px;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: -2px;
    font-family: 'Space Mono', monospace;
  }}
  .stat-label {{
    font-size: 12px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 2px;
  }}

  /* LAYOUT */
  .container {{
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 60px;
  }}
  .section {{
    padding: 60px 0;
    border-bottom: 1px solid var(--border);
  }}
  .section-title {{
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 8px;
  }}
  .section-heading {{
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -1px;
    margin-bottom: 40px;
  }}

  /* GRID */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }}
  .grid-3 {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }}

  /* PANELS */
  .panel {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px;
  }}
  .panel-title {{
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 24px;
  }}

  /* SKILL BARS */
  .bar-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
  }}
  .bar-label {{
    font-size: 13px;
    color: var(--text);
    width: 160px;
    flex-shrink: 0;
    font-family: 'Space Mono', monospace;
  }}
  .bar-track {{
    flex: 1;
    height: 6px;
    background: var(--border);
    border-radius: 3px;
    overflow: hidden;
  }}
  .bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 3px;
    transition: width 1s ease;
  }}
  .bar-pct {{
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: var(--accent);
    width: 36px;
    text-align: right;
  }}

  /* PILLS */
  .pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }}
  .pill {{
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 8px 16px;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .pill-count {{
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: var(--accent);
  }}

  /* LOCATIONS */
  .loc-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
  }}
  .loc-item:last-child {{ border-bottom: none; }}
  .loc-dot {{ color: var(--accent); font-size: 8px; }}
  .loc-num {{
    margin-left: auto;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: var(--accent);
    background: rgba(0,212,255,0.1);
    padding: 2px 8px;
    border-radius: 4px;
  }}

  /* TRAITS */
  .trait-tag {{
    display: inline-block;
    background: rgba(255,107,53,0.1);
    border: 1px solid rgba(255,107,53,0.3);
    color: var(--accent2);
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 13px;
    margin: 4px;
  }}

  /* COMPANY CARDS */
  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 20px;
  }}
  .company-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
  }}
  .company-card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent);
  }}
  .card-accent {{
    height: 4px;
    width: 100%;
  }}
  .card-body {{ padding: 24px; }}
  .card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }}
  .company-name {{
    font-size: 20px;
    font-weight: 700;
    letter-spacing: -0.5px;
  }}
  .domain-badge {{
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
    color: var(--muted);
    background: var(--surface2);
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 4px;
    text-transform: uppercase;
  }}
  .card-section {{ margin-bottom: 16px; }}
  .section-label {{
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 8px;
  }}
  .role-list {{
    list-style: none;
    font-size: 13px;
    color: var(--text);
    line-height: 1.8;
  }}
  .role-list li::before {{
    content: '→ ';
    color: var(--accent);
    font-family: 'Space Mono', monospace;
  }}
  .skill-chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .skill-chip {{
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.2);
    color: var(--accent);
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-family: 'Space Mono', monospace;
  }}
  .levels-text {{
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: var(--green);
  }}
  .card-obs {{
    margin-top: 12px;
    padding: 10px;
    background: var(--surface2);
    border-left: 2px solid var(--accent2);
    font-size: 12px;
    color: var(--muted);
    border-radius: 0 6px 6px 0;
    line-height: 1.6;
  }}

  /* FOOTER */
  .footer {{
    padding: 40px 60px;
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1px;
  }}

  @media (max-width: 768px) {{
    .hero, .container, .footer {{ padding-left: 24px; padding-right: 24px; }}
    .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
    .bar-label {{ width: 100px; }}
  }}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-tag">▸ Fintech Intelligence Report</div>
  <h1>Who Are Fintech<br>Companies <span>Hiring?</span></h1>
  <p style="color:var(--muted); font-size:15px; margin-top:16px; max-width:500px; line-height:1.6;">
    AI-powered analysis of software engineering job listings across top fintech companies.
  </p>
  <div class="hero-stats">
    <div class="stat-block">
      <span class="stat-num">{n}</span>
      <span class="stat-label">Companies Analyzed</span>
    </div>
    <div class="stat-block">
      <span class="stat-num">{sum(len(c.get("software_engineering_roles",[])) for c in insights)}</span>
      <span class="stat-label">SWE Roles Found</span>
    </div>
    <div class="stat-block">
      <span class="stat-num">{len(counters["skills"])}</span>
      <span class="stat-label">Unique Skills</span>
    </div>
  </div>
  <p class="hero-sub">Generated {date} · Powered by Crawl4AI + LLaMA 3.2</p>
</div>

<div class="container">

  <!-- SKILLS + LEVELS -->
  <div class="section">
    <p class="section-title">▸ Technical Landscape</p>
    <h2 class="section-heading">What Skills Do They Want?</h2>
    <div class="grid-2">
      <div class="panel">
        <p class="panel-title">Top Technical Skills</p>
        {skill_bars}
      </div>
      <div style="display:flex; flex-direction:column; gap:24px;">
        <div class="panel">
          <p class="panel-title">Experience Levels Hiring</p>
          <div class="pills">{level_pills}</div>
        </div>
        <div class="panel">
          <p class="panel-title">Top Locations</p>
          {location_items}
        </div>
      </div>
    </div>
  </div>

  <!-- TRAITS -->
  <div class="section">
    <p class="section-title">▸ Culture & Fit</p>
    <h2 class="section-heading">What Kind of Person Do They Want?</h2>
    <div class="panel">
      <p class="panel-title">Candidate Traits Fintech Companies Emphasize</p>
      <div>{trait_tags}</div>
    </div>
  </div>

  <!-- COMPANY CARDS -->
  <div class="section">
    <p class="section-title">▸ Company Breakdown</p>
    <h2 class="section-heading">Company by Company</h2>
    <div class="cards-grid">
      {company_cards}
    </div>
  </div>

</div>

<div class="footer">
  Built with Python · Crawl4AI · LLaMA 3.2 (Ollama) · {date}
</div>

</body>
</html>"""
    return html


def main():
    print("=" * 55)
    print("  📊 STEP 5 — GENERATING HTML REPORT")
    print("=" * 55)

    insights = load_data()
    if not insights:
        return

    counters = build_counters(insights)
    html = generate_html(insights, counters)

    with open("fintech_report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Report generated successfully!")
    print(f"💾 Saved to fintech_report.html")
    print(f"\n👉 Open it by running:")
    print(f"   start fintech_report.html")


if __name__ == "__main__":
    main()