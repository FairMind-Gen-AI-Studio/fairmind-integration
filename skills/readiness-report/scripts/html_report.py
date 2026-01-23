#!/usr/bin/env python3
"""
HTML Report Generator for Agent Readiness.

Generates self-contained HTML reports with FairMind branding.
Inspired by factory.ai agent readiness report design.
"""

from typing import Any

# FairMind brand colors
FAIRMIND_TEAL = "#00594C"
FAIRMIND_TEAL_LIGHT = "#007A68"
FAIRMIND_TEAL_DARK = "#003D34"

# Base64-encoded FairMind logo (PNG)
FAIRMIND_LOGO_BASE64 = "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"


def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _get_status_html(status: str) -> str:
    """Get status indicator HTML with appropriate styling."""
    if status == "pass":
        return '<span class="status pass">&#x2713;</span>'
    elif status == "fail":
        return '<span class="status fail">&#x2717;</span>'
    else:
        return '<span class="status skip">&#x2014;</span>'


def _get_top_strengths(data: dict, n: int = 3) -> list[tuple[str, float, list[str]]]:
    """Get top performing pillars with example passing criteria."""
    pillar_scores = []
    for pillar_name, pillar in data["pillars"].items():
        if pillar["total"] > 0:
            pct = pillar["percentage"]
            passing = [c["id"] for c in pillar["criteria"] if c["status"] == "pass"][:3]
            pillar_scores.append((pillar_name, pct, passing))
    pillar_scores.sort(key=lambda x: x[1], reverse=True)
    return pillar_scores[:n]


def _get_top_opportunities(data: dict, n: int = 5) -> list[tuple[str, str, str]]:
    """Get highest priority improvement opportunities."""
    opportunities = []
    for pillar_name, pillar in data["pillars"].items():
        for criterion in pillar["criteria"]:
            if criterion["status"] == "fail":
                opportunities.append(
                    (criterion["id"], criterion["level"], criterion["reason"], pillar_name)
                )
    opportunities.sort(key=lambda x: x[1])
    return [(o[0], o[2], o[3]) for o in opportunities[:n]]


def generate_html_report(data: dict) -> str:
    """Generate a self-contained HTML report with FairMind branding."""
    repo_name = data["repo_name"]
    pass_rate = data["pass_rate"]
    achieved = data["achieved_level"]
    total_passed = data["total_passed"]
    total = data["total_criteria"]
    languages = data.get("languages", ["Unknown"])
    repo_type = data.get("repo_type", "application")
    level_scores = data["level_scores"]

    # Build level progress HTML
    level_bars = []
    for level in range(1, 6):
        score = level_scores.get(str(level), level_scores.get(level, 0))
        is_achieved = achieved > 0 and level <= achieved
        level_class = "achieved" if is_achieved else ("passed" if score >= 80 else "")
        level_bars.append(f'''
            <div class="level-item {level_class}">
                <div class="level-label">L{level}</div>
                <div class="level-bar">
                    <div class="level-fill" style="width: {score}%"></div>
                </div>
                <div class="level-score">{score:.0f}%</div>
            </div>
        ''')

    # Build strengths HTML
    strengths = _get_top_strengths(data)
    strengths_html = ""
    for i, (pillar_name, pct, passing) in enumerate(strengths, 1):
        passing_str = ", ".join(f'<code>{p}</code>' for p in passing) if passing else ""
        strengths_html += f'''
            <div class="card">
                <div class="card-number">{i:02d}</div>
                <div class="card-title">{_escape_html(pillar_name)} <span class="pct">{pct:.0f}%</span></div>
                <div class="card-detail">{passing_str}</div>
            </div>
        '''

    # Build opportunities HTML
    opportunities = _get_top_opportunities(data)
    opportunities_html = ""
    for i, (crit_id, reason, pillar) in enumerate(opportunities, 1):
        opportunities_html += f'''
            <div class="card opportunity">
                <div class="card-number">{i:02d}</div>
                <div class="card-title"><code>{_escape_html(crit_id)}</code></div>
                <div class="card-detail">{_escape_html(reason)}</div>
                <div class="card-pillar">{_escape_html(pillar)}</div>
            </div>
        '''

    # Build criteria sections HTML
    criteria_sections = ""
    for pillar_name, pillar in data["pillars"].items():
        pct = pillar["percentage"]
        passed = pillar["passed"]
        pillar_total = pillar["total"]

        criteria_rows = ""
        for criterion in pillar["criteria"]:
            status_html = _get_status_html(criterion["status"])
            criteria_rows += f'''
                <div class="criterion">
                    {status_html}
                    <code class="criterion-id">{_escape_html(criterion["id"])}</code>
                    <span class="criterion-score">{criterion["score"]}</span>
                    <span class="criterion-reason">{_escape_html(criterion["reason"])}</span>
                </div>
            '''

        criteria_sections += f'''
            <details class="pillar-section">
                <summary>
                    <span class="pillar-name">{_escape_html(pillar_name)}</span>
                    <span class="pillar-score">{passed}/{pillar_total} ({pct:.0f}%)</span>
                </summary>
                <div class="criteria-list">
                    {criteria_rows}
                </div>
            </details>
        '''

    # Build full HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Readiness Report: {_escape_html(repo_name)}</title>
    <style>
        :root {{
            --teal: {FAIRMIND_TEAL};
            --teal-light: {FAIRMIND_TEAL_LIGHT};
            --teal-dark: {FAIRMIND_TEAL_DARK};
            --pass: #22c55e;
            --fail: #ef4444;
            --skip: #94a3b8;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}

        /* Header */
        header {{
            background: var(--teal);
            color: white;
            padding: 2rem;
            margin-bottom: 2rem;
        }}
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        .logo {{ height: 40px; }}
        .header-meta {{
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
        }}
        .header-meta span {{ opacity: 0.9; }}

        /* Hero */
        .hero {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .hero-title {{
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        .hero-stats {{
            display: flex;
            gap: 3rem;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--teal);
        }}
        .stat-label {{
            color: var(--text-muted);
            font-size: 0.875rem;
        }}

        /* Level Progress */
        .level-progress {{
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
            flex-wrap: wrap;
        }}
        .level-item {{
            flex: 1;
            min-width: 100px;
            text-align: center;
        }}
        .level-label {{
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-muted);
        }}
        .level-item.achieved .level-label {{ color: var(--teal); }}
        .level-bar {{
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
        }}
        .level-fill {{
            height: 100%;
            background: var(--teal-light);
            border-radius: 4px;
            transition: width 0.3s;
        }}
        .level-item.achieved .level-fill {{ background: var(--teal); }}
        .level-score {{
            font-size: 0.875rem;
            margin-top: 0.25rem;
            color: var(--text-muted);
        }}

        /* Grid */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        .section-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--teal-dark);
        }}

        /* Cards */
        .card {{
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            border-left: 4px solid var(--pass);
        }}
        .card.opportunity {{ border-left-color: var(--fail); }}
        .card-number {{
            font-size: 0.75rem;
            color: var(--text-muted);
            font-weight: 600;
        }}
        .card-title {{
            font-weight: 600;
            margin: 0.25rem 0;
        }}
        .card-title .pct {{ color: var(--teal); }}
        .card-detail {{
            font-size: 0.875rem;
            color: var(--text-muted);
        }}
        .card-pillar {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.5rem;
        }}

        /* Criteria */
        .pillar-section {{
            background: var(--card-bg);
            border-radius: 8px;
            margin-bottom: 0.75rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        .pillar-section summary {{
            padding: 1rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
        }}
        .pillar-section summary:hover {{ background: var(--bg); }}
        .pillar-score {{
            color: var(--text-muted);
            font-weight: normal;
        }}
        .criteria-list {{
            padding: 0 1rem 1rem;
            border-top: 1px solid var(--border);
        }}
        .criterion {{
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border);
            font-size: 0.875rem;
        }}
        .criterion:last-child {{ border-bottom: none; }}
        .status {{
            font-weight: bold;
            width: 1.5rem;
            flex-shrink: 0;
        }}
        .status.pass {{ color: var(--pass); }}
        .status.fail {{ color: var(--fail); }}
        .status.skip {{ color: var(--skip); }}
        .criterion-id {{
            font-family: 'SF Mono', Monaco, monospace;
            background: var(--bg);
            padding: 0.125rem 0.375rem;
            border-radius: 4px;
            font-size: 0.8125rem;
            white-space: nowrap;
        }}
        .criterion-score {{
            color: var(--text-muted);
            white-space: nowrap;
        }}
        .criterion-reason {{
            color: var(--text-muted);
            flex: 1;
        }}

        code {{
            font-family: 'SF Mono', Monaco, monospace;
            background: var(--bg);
            padding: 0.125rem 0.375rem;
            border-radius: 4px;
            font-size: 0.8125rem;
        }}

        footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.875rem;
        }}
        footer a {{ color: var(--teal); }}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <img src="data:image/png;base64,{FAIRMIND_LOGO_BASE64}" alt="FairMind" class="logo">
            <div class="header-meta">
                <span>{', '.join(languages)}</span>
                <span>{repo_type}</span>
            </div>
        </div>
    </header>

    <div class="container">
        <section class="hero">
            <h1 class="hero-title">{_escape_html(repo_name)}</h1>
            <div class="hero-stats">
                <div class="stat">
                    <div class="stat-value">{pass_rate:.0f}%</div>
                    <div class="stat-label">Pass Rate</div>
                </div>
                <div class="stat">
                    <div class="stat-value">L{achieved if achieved > 0 else '—'}</div>
                    <div class="stat-label">Achieved Level</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{total_passed}/{total}</div>
                    <div class="stat-label">Criteria Passing</div>
                </div>
            </div>
            <div class="level-progress">
                {''.join(level_bars)}
            </div>
        </section>

        <div class="grid">
            <section>
                <h2 class="section-title">Strengths</h2>
                {strengths_html}
            </section>
            <section>
                <h2 class="section-title">Opportunities</h2>
                {opportunities_html}
            </section>
        </div>

        <section>
            <h2 class="section-title">All Criteria</h2>
            {criteria_sections}
        </section>
    </div>

    <footer>
        Generated by <a href="https://fairmind.ai">FairMind</a> Agent Readiness Report
    </footer>
</body>
</html>'''

    return html
