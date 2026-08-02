# scripts/make_info_card.py
import svgwrite

def build_card():
    dwg = svgwrite.Drawing('info-card.svg', size=('490px', '320px'))
    
    # Custom CSS for staggered fade-in animations
    style = """
        .term-text { font-family: 'Fira Code', 'Courier New', monospace; font-size: 13px; fill: #c9d1d9; }
        .label { fill: #58a6ff; font-weight: bold; }
        .accent { fill: #3fb950; }
        .line { opacity: 0; animation: fadeIn 0.5s forwards; }
        @keyframes fadeIn { to { opacity: 1; } }
    """
    dwg.defs.add(dwg.style(style))
    
    # Terminal Container Box
    dwg.add(dwg.rect(insert=(0, 0), size=('490', '320'), rx=8, ry=8, fill='#0d1117', stroke='#30363d'))
    
    lines = [
        ("yashvi@lpu ~ $ ", "whoami", True),
        ("----------------------------------------", "", False),
        ("NAME       : ", "Yashvi Sharma", False),
        ("ROLE       : ", "SDE Intern @ Nielsen", False),
        ("PREV       : ", "Ex-Data Science Intern @ Futurense", False),
        ("EDU        : ", "B.Tech CSE (AI & Data Eng) @ LPU", False),
        ("EXPLORING  : ", "Machine Learning • NLP • Scalable Backend", False),
        ("INTERESTS  : ", "Deep Learning • Optimization • Open Source", False),
        ("OUTSIDE    : ", "Binge Watching • Research • Strategy Games", False),
    ]
    
    y_pos = 35
    for idx, line in enumerate(lines):
        delay = idx * 0.15
        g = dwg.g(class_="line", style=f"animation-delay: {delay}s;")
        
        if line[2]: # Command prompt line
            g.add(dwg.text(line[0], insert=(20, y_pos), class_="term-text accent"))
            g.add(dwg.text(line[1], insert=(140, y_pos), class_="term-text"))
        else:
            g.add(dwg.text(line[0], insert=(20, y_pos), class_="term-text label"))
            g.add(dwg.text(line[1], insert=(120, y_pos), class_="term-text"))
            
        dwg.add(g)
        y_pos += 28

    dwg.save()

if __name__ == '__main__':
    build_card()