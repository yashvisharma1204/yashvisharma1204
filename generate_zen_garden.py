import random
rows = 10
cols = 80

elements = ['🌱', '🪨', '🌾', '🍃', '⛰️']
density = 0.1  

quotes = [
    "Breathe in calm. Breathe out stress.",
    "Stillness speaks volumes.",
    "Let the flow guide you.",
    "Code in harmony.",
    "Focus is the gateway to peace.",
    "Grow slow, grow steady."
]

garden = [[' ' for _ in range(cols)] for _ in range(rows)]

num_items = int(rows * cols * density)
for _ in range(num_items):
    r = random.randint(0, rows - 1)
    c = random.randint(0, cols - 1)
    garden[r][c] = random.choice(elements)

with open("zen_garden.txt", "w") as f:
    for row in garden:
        f.write("".join(row) + "\n")
    f.write(f"\n“{random.choice(quotes)}”\n")
