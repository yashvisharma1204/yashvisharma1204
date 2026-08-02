import datetime
import requests
from bs4 import BeautifulSoup
import svgwrite

USERNAME = "yashvisharma1204"  # GitHub username
OUTPUT_SVG = "heatmap.svg"

# GitHub dark theme color scale (least -> most active)
COLOR_LEVELS = [
    "#161b22",  # Level 0: 0 commits
    "#0e4429",  # Level 1: 1-3 commits
    "#006d32",  # Level 2: 4-6 commits
    "#26a641",  # Level 3: 7-9 commits
    "#39d353"   # Level 4: 10+ commits
]

def fetch_contributions(username):
    """Scrapes contribution data directly from GitHub's profile page."""
    url = f"https://github.com/users/{username}/contributions"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch contributions for user {username}. Status: {response.status_code}")
        
    soup = BeautifulSoup(response.content, "html.parser")
    days = soup.find_all("td", class_="ContributionCalendar-day")
    
    contribution_data = []
    for day in days:
        date_str = day.get("data-date")
        count_attr = day.get("data-level", "0")
        
        if date_str:
            level = int(count_attr) if count_attr.isdigit() else 0
            contribution_data.append((date_str, level))
            
    return contribution_data

def generate_heatmap_svg(contributions, output_path):
    """Generates a terminal-styled contribution heatmap SVG."""
    # Heatmap layout geometry
    box_size = 11
    box_gap = 3
    margin_x = 35
    margin_y = 40
    
    # Calculate grid dimensions based on ~52 weeks
    weeks = len(contributions) // 7 + 1
    width = margin_x + (weeks * (box_size + box_gap)) + 20
    height = margin_y + (7 * (box_size + box_gap)) + 25

    dwg = svgwrite.Drawing(output_path, size=(width, height), viewBox=f"0 0 {width} {height}")
    
    # Styling
    dwg.defs.add(dwg.style("""
        .bg { fill: #0d1117; stroke: #30363d; rx: 8px; }
        .header { font-family: 'Fira Code', monospace; font-size: 12px; fill: #58a6ff; font-weight: bold; }
        .day-label { font-family: 'Fira Code', monospace; font-size: 9px; fill: #8b949e; }
        .legend-text { font-family: 'Fira Code', monospace; font-size: 9px; fill: #8b949e; }
    """))

    # Terminal Background
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), class_="bg"))
    
    # Header Title
    dwg.add(dwg.text(f"~/contributions --user={USERNAME}", insert=(15, 22), class_="header"))

    # Day labels (Mon, Wed, Fri)
    day_names = ["Mon", "Wed", "Fri"]
    day_indices = [1, 3, 5]
    for idx, name in zip(day_indices, day_names):
        y_pos = margin_y + (idx * (box_size + box_gap)) + 9
        dwg.add(dwg.text(name, insert=(8, y_pos), class_="day-label"))

    # Render Heatmap Cells
    col = 0
    row = 0
    for date_str, level in contributions:
        x = margin_x + col * (box_size + box_gap)
        y = margin_y + row * (box_size + box_gap)
        
        color = COLOR_LEVELS[min(level, 4)]
        dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), rx=2, fill=color))
        
        row += 1
        if row >= 7:
            row = 0
            col += 1

    # Footer Legend
    legend_start_x = width - 130
    legend_y = height - 12
    dwg.add(dwg.text("Less", insert=(legend_start_x - 28, legend_y + 8), class_="legend-text"))
    
    for idx, color in enumerate(COLOR_LEVELS):
        lx = legend_start_x + (idx * (box_size + box_gap))
        dwg.add(dwg.rect(insert=(lx, legend_y), size=(box_size, box_size), rx=2, fill=color))
        
    dwg.add(dwg.text("More", insert=(legend_start_x + (5 * (box_size + box_gap)) + 4, legend_y + 8), class_="legend-text"))

    dwg.save()

def main():
    print(f"Fetching GitHub contribution data for @{USERNAME}...")
    try:
        contributions = fetch_contributions(USERNAME)
        print(f"Fetched {len(contributions)} days of contribution data.")
        
        print("Building heatmap SVG...")
        generate_heatmap_svg(contributions, OUTPUT_SVG)
        print(f"Successfully generated {OUTPUT_SVG}!")
    except Exception as e:
        print(f"Error generating heatmap: {e}")

if __name__ == "__main__":
    main()