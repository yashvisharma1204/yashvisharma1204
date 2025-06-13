import random

# Zen elements
rows = 4
width = 40
elements = ['🌱', '🪨', '🌾', '🍃', '⛰️', ' ']

# Zen quotes
quotes = [
    "Breathe in calm. Breathe out stress.",
    "Stillness speaks volumes.",
    "Let the flow guide you.",
    "Code in harmony.",
    "Focus is the gateway to peace.",
    "Grow slow, grow steady."
]

garden = []
for _ in range(rows):
    line = ''.join(random.choice(elements) for _ in range(width))
    garden.append(line)

with open("zen_garden.txt", "w") as f:
    for line in garden:
        f.write(line + "\n")
    f.write(f"\n“{random.choice(quotes)}”\n")
