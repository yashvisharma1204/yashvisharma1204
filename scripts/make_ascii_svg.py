import cv2
import numpy as np

# Configuration
INPUT_IMAGE = "source-prepped.png"
OUTPUT_SVG = "avi-ascii.svg"

# Keep the detailed grid (Resolution looks good in your example)
GRID_WIDTH = 130 

# Extended detailed ramp
RAMP = " .`'-_:=+*!|/r(l1Z4X#%@"

def image_to_ascii(image_path, width=130):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not find {image_path}. Please run prep_photo.py first.")

    h, w = img.shape
    aspect_ratio = h / w
    # Multiplier keeps the flower proportions correct
    height = int(width * aspect_ratio * 0.52)
    
    resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    
    ascii_rows = []
    ramp_len = len(RAMP)
    for row in resized:
        line = ""
        for pixel in row:
            index = int((255 - pixel) / 255 * (ramp_len - 1))
            line += RAMP[index]
        ascii_rows.append(line)
        
    return ascii_rows, width, height

def generate_svg(ascii_rows, cols, rows):
    # --- GEOMETRY FIX ---
    # Shrink font geometry to fit high-detail grid without clipping
    char_width = 6.2   # Prevents character overlap
    line_height = 10.0  
    
    # Calculate necessary viewbox width based on grid and character size
    # GridWidth(130) * CharWidth(6.2) = 806. Add small padding.
    view_width = int(cols * char_width + 15)
    view_height = int(rows * line_height + 25)
    
    # Optional: If you want to scale the entire image down to fit perfectly 
    # side-by-side with the card (e.g., 370px width), use the display_width configuration.
    # Otherwise, the SVG will naturally take up its natural width (821px).
    display_width = view_width 
    display_height = view_height
    
    duration_per_line = 0.03 # Typing speed
    
    svg_lines = []
    # Start SVG with updated ViewBox and optimized display size
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_width} {view_height}" width="{display_width}" height="{display_height}">')
    svg_lines.append('  <style>')
    
    # Fira Code recommended for cleanest monospace rendering on GitHub
    svg_lines.append('    .ascii { font-family: "Fira Code", "Courier New", monospace; font-size: 9px; fill: #a6adba; white-space: pre; font-weight: 500; }')
    svg_lines.append('    .line { opacity: 0; animation: typeIn 0.01s forwards; }')
    svg_lines.append('    @keyframes typeIn { to { opacity: 1; } }')
    svg_lines.append('  </style>')
    
    # Terminal background container (expanded for updated dimensions)
    svg_lines.append(f'  <rect width="100%" height="100%" rx="8" fill="#0d1117" stroke="#30363d"/>')
    svg_lines.append('  <g class="ascii">')
    
    # Starting vertical position
    y = 20
    for idx, line in enumerate(ascii_rows):
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        delay = round(idx * duration_per_line, 2)
        
        # Horizontal padding increased (x="10") to contain leftmost edges
        svg_lines.append(
            f'    <text x="10" y="{y}" class="line" style="animation-delay: {delay}s;">{escaped_line}</text>'
        )
        y += line_height
        
    svg_lines.append('  </g>')
    svg_lines.append('</svg>')
    
    return "\n".join(svg_lines)

def main():
    print(f"Correcting ASCII geometry for {INPUT_IMAGE} (Detail level: {GRID_WIDTH})...")
    ascii_rows, cols, rows = image_to_ascii(INPUT_IMAGE, width=GRID_WIDTH)
    
    svg_content = generate_svg(ascii_rows, cols, rows)
    
    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Successfully generated {OUTPUT_SVG}. Inspect the edges now!")

if __name__ == "__main__":
    main()