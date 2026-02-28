import json
import time
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def analyze_company(company_name: str, content: str) -> dict:
    print(f"\n🤖 Analyzing {company_name}...")

    prompt = f"""You are analyzing job listings from {company_name}'s career page.
Focus ONLY on Software Engineering, Backend, Infrastructure, Platform, or Technical roles.
Ignore sales, marketing, legal, HR, and finance roles completely.

Here is the content:
{content[:4000]}

Extract information and return ONLY a JSON object with these exact fields, no explanation:

{{
  "company": "{company_name}",
  "software_engineering_roles": ["list only SWE/technical job titles you see, ignore sales/marketing"],
  "required_skills": ["technical skills mentioned e.g. Python, Go, Kafka, Kubernetes"],
  "experience_levels": ["Junior/Mid/Senior/Staff - only ones you see"],
  "locations": ["cities or Remote mentioned"],
  "domain_focus": "what engineering domain e.g. payments, trading, infra, fraud",
  "candidate_traits": ["culture or personality traits the company emphasizes"],
  "notable_observations": "any unique patterns about this company hiring"
}}

Return ONLY the JSON. No markdown, no explanation, no code blocks."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            },
            timeout=120
        )

        raw_text = response.json()["response"].strip()

        # Strip markdown code blocks if model adds them
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]

        insights = json.loads(raw_text)
        print(f"  ✅ {company_name} — done")
        return insights

    except json.JSONDecodeError:
        print(f"  ⚠️  {company_name} — JSON parse failed, attempting recovery...")
        try:
            fixed = raw_text.strip()
            if not fixed.endswith("}"):
                fixed += "\n}"
            insights = json.loads(fixed)
            print(f"  ✅ {company_name} — recovered successfully")
            return insights
        except:
            print(f"  ❌ {company_name} — recovery failed")
            return {
                "company": company_name,
                "error": "JSON parse failed",
                "raw": raw_text if 'raw_text' in locals() else "no response"
            }

    except Exception as e:
        print(f"  ❌ {company_name} — error: {e}")
        return {"company": company_name, "error": str(e)}


def print_summary(insights: list):
    print(f"\n{'='*55}")
    print(f"  📊 INSIGHTS SUMMARY")
    print(f"{'='*55}")

    for insight in insights:
        if "error" in insight:
            print(f"\n❌ {insight['company']} — failed")
            continue

        print(f"\n🏢 {insight['company'].upper()}")
        print(f"  Domain   : {insight.get('domain_focus', 'N/A')}")

        roles = insight.get('software_engineering_roles', [])
        if roles:
            print(f"  Roles    : {', '.join(roles[:3])}")

        skills = insight.get('required_skills', [])
        if skills:
            print(f"  Skills   : {', '.join(skills[:5])}")

        levels = insight.get('experience_levels', [])
        if levels:
            print(f"  Levels   : {', '.join(levels)}")

        traits = insight.get('candidate_traits', [])
        if traits:
            print(f"  Culture  : {', '.join(traits[:3])}")


def main():
    print("=" * 55)
    print("  🧠 STEP 3 — AI ANALYSIS WITH OLLAMA (LOCAL)")
    print(f"  Model: {MODEL}")
    print("=" * 55)

    # Load cleaned data from Step 2
    try:
        with open("fintech_cleaned.json", "r") as f:
            companies = json.load(f)
    except FileNotFoundError:
        print("❌ fintech_cleaned.json not found!")
        print("   Run fintech_scraper_v2.py first")
        return

    all_insights = []

    for company in companies:

        # Skip companies with too little content
        if company.get("cleaned_length", 0) < 100:
            print(f"\n⏭️  Skipping {company['company']} — not enough content")
            continue

        insights = analyze_company(company["company"], company["content"])
        all_insights.append(insights)

        # ✅ Save after EVERY company — crash safe
        with open("fintech_insights.json", "w") as f:
            json.dump(all_insights, f, indent=2)
        print(f"  💾 Saved progress ({len(all_insights)} companies so far)")

        time.sleep(1)

    print_summary(all_insights)
    print(f"\n  ✅ Analyzed {len(all_insights)} companies")
    print(f"  💾 Final results saved to fintech_insights.json")


if __name__ == "__main__":
    main()