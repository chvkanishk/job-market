import json
import requests
from collections import Counter

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def load_insights() -> list:
    """Load the AI analysis results from Step 3"""
    try:
        with open("fintech_insights.json", "r") as f:
            data = json.load(f)
        # Filter out failed companies
        valid = [d for d in data if "error" not in d]
        print(f"✅ Loaded {len(valid)} company insights")
        return valid
    except FileNotFoundError:
        print("❌ fintech_insights.json not found!")
        print("   Run ai_analyzer.py first")
        return []


def find_patterns_locally(insights: list) -> dict:
    """
    Find patterns using pure Python — no AI needed.
    Count frequencies across all companies.
    """
    print("\n🔍 Finding patterns across companies...")

    all_skills = []
    all_levels = []
    all_locations = []
    all_traits = []
    all_domains = []
    all_roles = []

    for company in insights:
        all_skills.extend(company.get("required_skills", []))
        all_levels.extend(company.get("experience_levels", []))
        all_locations.extend(company.get("locations", []))
        all_traits.extend(company.get("candidate_traits", []))
        all_roles.extend(company.get("software_engineering_roles", []))
        domain = company.get("domain_focus", "")
        if domain:
            all_domains.append(domain)

    return {
        "top_skills":    Counter(all_skills).most_common(10),
        "top_levels":    Counter(all_levels).most_common(5),
        "top_locations": Counter(all_locations).most_common(8),
        "top_traits":    Counter(all_traits).most_common(8),
        "top_domains":   Counter(all_domains).most_common(5),
        "top_roles":     Counter(all_roles).most_common(10),
        "total_companies": len(insights)
    }


def ask_ollama_for_patterns(insights: list) -> str:
    """
    Send all company insights to Ollama and ask for
    high-level pattern analysis in plain English
    """
    print("\n🤖 Asking Ollama for deep pattern analysis...")

    # Prepare a compact summary of all companies
    summary = []
    for company in insights:
        summary.append({
            "company": company.get("company"),
            "skills": company.get("required_skills", []),
            "traits": company.get("candidate_traits", []),
            "levels": company.get("experience_levels", []),
            "domain": company.get("domain_focus", ""),
            "observations": company.get("notable_observations", "")
        })

    prompt = f"""You are a career intelligence analyst specializing in fintech companies.

Here is data from {len(insights)} fintech company career pages:

{json.dumps(summary, indent=2)}

Analyze this data and provide insights on:
1. What technical skills are most in demand across fintech companies?
2. What kind of engineer do fintech companies typically look for?
3. What cultural traits do fintech companies value most?
4. What makes fintech hiring different from other tech sectors?
5. What advice would you give to a backend engineer targeting fintech roles?

Write your analysis in clear, plain English. Be specific and actionable.
Format with numbered sections matching the questions above."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            },
            timeout=180
        )
        return response.json()["response"].strip()
    except Exception as e:
        return f"Ollama analysis failed: {e}"


def print_pattern_report(patterns: dict, ollama_analysis: str):
    """Print the full pattern report"""

    n = patterns["total_companies"]

    print(f"\n{'='*55}")
    print(f"  📊 FINTECH HIRING PATTERN REPORT")
    print(f"  Based on {n} companies")
    print(f"{'='*55}")

    print(f"\n🛠️  TOP TECHNICAL SKILLS:")
    for skill, count in patterns["top_skills"]:
        bar = "█" * count
        print(f"  {skill:<35} {bar} ({count}/{n})")

    print(f"\n🎯 MOST SOUGHT EXPERIENCE LEVELS:")
    for level, count in patterns["top_levels"]:
        bar = "█" * count
        print(f"  {level:<35} {bar} ({count}/{n})")

    print(f"\n📍 TOP LOCATIONS:")
    for loc, count in patterns["top_locations"]:
        print(f"  {loc:<35} ({count} companies)")

    print(f"\n🧠 CANDIDATE TRAITS COMPANIES VALUE:")
    for trait, count in patterns["top_traits"]:
        bar = "█" * count
        print(f"  {trait:<35} {bar} ({count}/{n})")

    print(f"\n🏦 ENGINEERING DOMAINS:")
    for domain, count in patterns["top_domains"]:
        print(f"  {domain:<35} ({count} companies)")

    print(f"\n💼 MOST COMMON JOB TITLES:")
    for role, count in patterns["top_roles"][:7]:
        print(f"  {role}")

    print(f"\n{'='*55}")
    print(f"  🤖 OLLAMA DEEP ANALYSIS")
    print(f"{'='*55}")
    print(f"\n{ollama_analysis}")


def save_report(patterns: dict, ollama_analysis: str):
    """Save the full report to files"""

    # Save as JSON for further processing
    report = {
        "patterns": {
            "top_skills":    patterns["top_skills"],
            "top_levels":    patterns["top_levels"],
            "top_locations": patterns["top_locations"],
            "top_traits":    patterns["top_traits"],
            "top_domains":   patterns["top_domains"],
            "top_roles":     patterns["top_roles"],
        },
        "ollama_analysis": ollama_analysis
    }
    with open("fintech_patterns.json", "w") as f:
        json.dump(report, f, indent=2)

    # Save as readable text report
    with open("fintech_report.txt", "w") as f:
        f.write("FINTECH HIRING INTELLIGENCE REPORT\n")
        f.write("=" * 55 + "\n\n")
        f.write("TOP SKILLS:\n")
        for skill, count in patterns["top_skills"]:
            f.write(f"  {skill} — {count}/{patterns['total_companies']} companies\n")
        f.write("\nDEEP ANALYSIS:\n")
        f.write(ollama_analysis)

    print(f"\n💾 Saved fintech_patterns.json")
    print(f"💾 Saved fintech_report.txt")


def main():
    print("=" * 55)
    print("  🔍 STEP 4 — PATTERN FINDER")
    print("=" * 55)

    # Load insights from Step 3
    insights = load_insights()
    if not insights:
        return

    # Find patterns using Python counters
    patterns = find_patterns_locally(insights)

    # Get deep analysis from Ollama
    ollama_analysis = ask_ollama_for_patterns(insights)

    # Print full report
    print_pattern_report(patterns, ollama_analysis)

    # Save everything
    save_report(patterns, ollama_analysis)


if __name__ == "__main__":
    main()