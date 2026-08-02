import cv2
import numpy as np
import os

# Configuration
# Read color original to sample exact petal/leaf colors
COLOR_IMAGE = "image.jpg" if os.path.exists("image.jpg") else "image.png"
GRAY_IMAGE = "source-prepped.png"
OUTPUT_SVG = "avi-ascii.svg"

# Grid width (controls horizontal density)
GRID_WIDTH = 115 

# ASCII Character Ramp
RAMP = " .`'-_:=+*!|/r(l1Z4X#%@"

def rgb_to_hex(r, g, b):
    """Converts RGB pixel tuple to HTML hex string."""
    return f"#{r:02x}{g:02x}{b:02x}"

def image_to_colored_ascii(gray_path, color_path, width=115):
    img_gray = cv2.imread(gray_path, cv2.IMREAD_GRAYSCALE)
    img_color = cv2.imread(color_path)

    if img_gray is None or img_color is None:
        raise FileNotFoundError(f"Missing input images. Check '{gray_path}' and '{color_path}'.")

    # Resize color to match grayscale dimensions if needed
    img_color = cv2.resize(img_color, (img_gray.shape[1], img_gray.shape[0]))
    
    h, w = img_gray.shape
    aspect_ratio = h / w
    
    # --- HEIGHT FIX ---
    # Lowered multiplier from 0.52 to 0.38 to significantly reduce total rows/height
    height = int(width * aspect_ratio * 0.38)
    
    resized_gray = cv2.resize(img_gray, (width, height), interpolation=cv2.INTER_CUBIC)
    resized_color = cv2.resize(img_color, (width, height), interpolation=cv2.INTER_CUBIC)
    
    ascii_grid = []
    ramp_len = len(RAMP)
    
    for r in range(height):
        row_data = []
        for c in range(width):
            pixel_val = resized_gray[r, c]
            b, g, r_val = resized_color[r, c]  # OpenCV reads BGR
            
            # Map brightness to character
            char_idx = int((255 - pixel_val) / 255 * (ramp_len - 1))
            char = RAMP[char_idx]
            
            # Escape XML special characters
            if char == " ": char = "&#160;"
            elif char == "&": char = "&amp;"
            elif char == "<": char = "&lt;"
            elif char == ">": char = "&gt;"
            
            hex_color = rgb_to_hex(r_val, g, b)
            row_data.append((char, hex_color))
            
        ascii_grid.append(row_data)
        
    return ascii_grid, width, height

def generate_svg(ascii_grid, cols, rows):
    # Tightened character and line geometry for compact display
    char_width = 6.2   
    line_height = 8.5  # Reduced from 10.0 to make overall container shorter
    
    view_width = int(cols * char_width + 20)
    view_height = int(rows * line_height + 30)
    
    duration_per_line = 0.02
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_width} {view_height}" width="{view_width}" height="{view_height}">')
    svg_lines.append('  <style>')
    svg_lines.append('    .ascii { font-family: "Fira Code", "Courier New", monospace; font-size: 8.5px; white-space: pre; font-weight: 500; }')
    svg_lines.append('    .line { opacity: 0; animation: typeIn 0.01s forwards; }')
    svg_lines.append('    @keyframes typeIn { to { opacity: 1; } }')
    svg_lines.append('  </style>')
    
    # Terminal Container
    svg_lines.append('  <rect width="100%" height="100%" rx="8" fill="#0d1117" stroke="#30363d"/>')
    
    # Terminal Window Buttons
    svg_lines.append('  <circle cx="20" cy="18" r="4" fill="#ff5f56"/>')
    svg_lines.append('  <circle cx="32" cy="18" r="4" fill="#ffbd2e"/>')
    svg_lines.append('  <circle cx="44" cy="18" r="4" fill="#27c93f"/>')
    
    svg_lines.append('  <g class="ascii">')
    
    y = 35
    for idx, row in enumerate(ascii_grid):
        delay = round(idx * duration_per_line, 2)
        
        # Group contiguous characters of the same color into single tspans to keep SVG lightweight
        spans_html = ""
        curr_color = None
        curr_text = ""
        
        for char, color in row:
            if color != curr_color:
                if curr_text:
                    spans_html += f'<tspan fill="{curr_color}">{curr_text}</tspan>'
                curr_color = color
                curr_text = char
            else:
                curr_text += char
                
        if curr_text:
            spans_html += f'<tspan fill="{curr_color}">{curr_text}</tspan>'
            
        svg_lines.append(f'    <text x="12" y="{y}" class="line" style="animation-delay: {delay}s;">{spans_html}</text>')
        y += line_height
        
    svg_lines.append('  </g>')
    svg_lines.append('</svg>')
    
    return "\n".join(svg_lines)

def main():
    print(f"Generating colored ASCII SVG from {COLOR_IMAGE}...")
    ascii_grid, cols, rows = image_to_colored_ascii(GRAY_IMAGE, COLOR_IMAGE, width=GRID_WIDTH)
    
    svg_content = generate_svg(ascii_grid, cols, rows)
    
    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Successfully generated {OUTPUT_SVG} with full color & shortened height!")

if __name__ == "__main__":
    main()