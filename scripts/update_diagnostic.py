import subprocess
import re

OUTPUT_SVG = "agent_diagnostic.svg"

# Theme Palette
GREEN = "#3fb950"
BLUE = "#58a6ff"
PURPLE = "#d2a8ff"
TEXT = "#c9d1d9"
DIM = "#484f58"
BG = "#0d1117"
STROKE = "#30363d"

def get_local_commits():
    """Reads the last 5 commit summaries directly from your local git log."""
    try:
        cmd = ["git", "log", "-n", "5", "--pretty=format:%h|%s"]
        output = subprocess.check_output(cmd, text=True).strip().split('\n')
        entries = []
        for line in output:
            if '|' in line:
                sha, msg = line.split('|', 1)
                msg_clean = re.sub(r'[^\w\s\(\)\[\]\.,@-]', '', msg)
                entries.append((sha, msg_clean, GREEN, "[PASS]"))
        return entries if entries else [("0000000", "Initial commit", GREEN, "[PASS]")]
    except Exception:
        return [("LOCAL", "Working directory sync active", GREEN, "[PASS]")]

def generate_svg(log_entries):
    width = 540
    row_h = 18
    
    # Calculate exact total height with the added cd command
    header_h = 105
    logs_h = len(log_entries) * row_h
    footer_h = 45
    total_height = header_h + logs_h + footer_h

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_height}" width="{width}" height="{total_height}">')
    svg.append('  <style>')
    svg.append('    .term-font { font-family: "Fira Code", monospace; font-size: 11px; }')
    svg.append('    .log-line { opacity: 0; animation: fadeIn 0.15s forwards; }')
    svg.append('    @keyframes fadeIn { to { opacity: 1; } }')
    svg.append('  </style>')
    
    # Terminal Container Background
    svg.append(f'  <rect width="100%" height="100%" rx="8" fill="{BG}" stroke="{STROKE}"/>')
    svg.append('  <circle cx="15" cy="15" r="4" fill="#ff5f56"/>')
    svg.append('  <circle cx="28" cy="15" r="4" fill="#ffbd2e"/>')
    svg.append('  <circle cx="41" cy="15" r="4" fill="#27c93f"/>')
    
    # --- COMMANDS ---
    y = 38
    svg.append(f'  <text x="15" y="{y}" class="term-font" fill="{GREEN}">yashvi@lpu:~$ <tspan fill="{TEXT}">cd research-agent</tspan></text>')
    
    y += 20
    svg.append(f'  <text x="15" y="{y}" class="term-font" fill="{GREEN}">yashvi@lpu:~/research-agent$ <tspan fill="{TEXT}">./agent_diagnostics.sh --repo research-agent</tspan></text>')
    
    y += 22
    svg.append(f'  <text x="15" y="{y}" class="term-font" fill="{PURPLE}">[AGENT HEALTH CHECK] Diagnostic Mode: verbose</text>')
    
    y += 18
    svg.append(f'  <text x="15" y="{y}" class="term-font" fill="{DIM}">TIMESTAMP      EVENT_ID     SUMMARY                                      STATUS</text>')
    
    # --- LOG ENTRIES ---
    for idx, (sha, summary, color, status) in enumerate(log_entries):
        delay = idx * 0.04
        y += row_h
        summary_clean = (summary[:38] + '..') if len(summary) > 38 else summary.ljust(40)
        
        svg.append(f'  <g class="log-line" style="animation-delay: {delay}s;">')
        svg.append(f'    <text x="15" y="{y}" class="term-font" fill="{DIM}">2026-08-02 </text>')
        svg.append(f'    <text x="120" y="{y}" class="term-font" fill="{BLUE}">REF:{sha}</text>')
        svg.append(f'    <text x="205" y="{y}" class="term-font" fill="{TEXT}">{summary_clean}</text>')
        svg.append(f'    <text x="480" y="{y}" class="term-font" fill="{color}">{status}</text>')
        svg.append('  </g>')

    # --- FOOTER PROMPT ---
    y += 18
    svg.append(f'  <line x1="15" y1="{y}" x2="{width - 15}" y2="{y}" stroke="{STROKE}" stroke-dasharray="2 2"/>')
    y += 18
    svg.append(f'  <text x="15" y="{y}" class="term-font" fill="{GREEN}">yashvi@lpu:~/research-agent$ <tspan fill="{TEXT}">_</tspan></text>')

    svg.append('</svg>')
    return "\n".join(svg)

def main():
    entries = get_local_commits()
    svg_data = generate_svg(entries)
    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg_data)
    print(f"Successfully generated {OUTPUT_SVG} with directory navigation!")

if __name__ == "__main__":
    main()