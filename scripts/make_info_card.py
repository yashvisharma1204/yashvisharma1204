import svgwrite

def build_card():
    # Expanded height from 320px to 650px to align with the ASCII portrait
    dwg = svgwrite.Drawing('info-card.svg', size=('490px', '650px'), viewBox='0 0 490 650')
    
    # Custom CSS for terminal aesthetics & staggered fade-in animations
    style = """
        .term-text { font-family: 'Fira Code', 'Courier New', monospace; font-size: 12.5px; fill: #c9d1d9; }
        .label { fill: #58a6ff; font-weight: bold; }
        .accent { fill: #3fb950; font-weight: bold; }
        .header { fill: #d2a8ff; font-weight: bold; }
        .dim { fill: #484f58; }
        .line { opacity: 0; animation: fadeIn 0.4s forwards; }
        @keyframes fadeIn { to { opacity: 1; } }
    """
    dwg.defs.add(dwg.style(style))
    
    # Terminal Container Box
    dwg.add(dwg.rect(insert=(0, 0), size=('490', '650'), rx=8, ry=8, fill='#0d1117', stroke='#30363d'))
    
    # Header Window Controls
    dwg.add(dwg.circle(center=(20, 20), r=5, fill='#ff5f56'))
    dwg.add(dwg.circle(center=(35, 20), r=5, fill='#ffbd2e'))
    dwg.add(dwg.circle(center=(50, 20), r=5, fill='#27c93f'))
    dwg.add(dwg.text("yashvi@dev-box: ~", insert=(70, 24), class_="term-text dim"))

    lines = [
        # --- Section 1: Profile Info ---
        ("yashvi@lpu ~ $ ", "whoami", "cmd"),
        ("----------------------------------------", "", "dim"),
        ("NAME       : ", "Yashvi Sharma", "info"),
        ("ROLE       : ", "SDE Intern @ Nielsen", "info"),
        ("PREV       : ", "Ex-Data Science Intern @ Futurense", "info"),
        ("EDU        : ", "B.Tech CSE (AI & Data Eng) @ LPU", "info"),
        ("EXPLORING  : ", "Machine Learning • NLP • Scalable Backend", "info"),
        ("INTERESTS  : ", "Deep Learning • Optimization • Open Source", "info"),
        ("OUTSIDE    : ", "Binge Watching • Research • Strategy Games", "info"),
        
        ("----------------------------------------", "", "dim"),
        
        # --- Section 2: Stack Details ---
        ("yashvi@lpu ~ $ ", "cat stack.json", "cmd"),
        ("TECH_STACK : ", "", "header"),
        ("  Languages  => ", "[ Java, Python, SQL, C++ ]", "info"),
        ("  Frameworks => ", "[ Spring Boot, PyTorch, FastAPI ]", "info"),
        ("  Data / ML  => ", "[ Spark, AWS, OpenCV, HuggingFace ]", "info"),
        ("  Tools      => ", "[ Git, Docker, Linux, Maven ]", "info"),
        
        ("----------------------------------------", "", "dim"),
        
        # --- Section 3: Current Status ---
        ("yashvi@lpu ~ $ ", "./status.sh", "cmd"),
        ("  [STATUS]   ", "Researching ML Techniques", "info"),
        ("  [LOCATION] ", "New Delhi, India 🇮🇳", "info"),
    ]
    
    y_pos = 55
    for idx, (col1, col2, line_type) in enumerate(lines):
        delay = round(idx * 0.08, 2)
        g = dwg.g(class_="line", style=f"animation-delay: {delay}s;")
        
        if line_type == "cmd":
            g.add(dwg.text(col1, insert=(20, y_pos), class_="term-text accent"))
            g.add(dwg.text(col2, insert=(150, y_pos), class_="term-text"))
        elif line_type == "dim":
            g.add(dwg.text(col1, insert=(20, y_pos), class_="term-text dim"))
        elif line_type == "header":
            g.add(dwg.text(col1, insert=(20, y_pos), class_="term-text header"))
        else: # Regular info rows
            g.add(dwg.text(col1, insert=(20, y_pos), class_="term-text label"))
            g.add(dwg.text(col2, insert=(140, y_pos), class_="term-text"))
            
        dwg.add(g)
        y_pos += 24

    dwg.save()
    print("Updated info-card.svg height and contents successfully.")

if __name__ == '__main__':
    build_card()