from pathlib import Path
from PIL import Image

INPUT = Path("assets/images/source-prepped.png")
OUTPUT = Path("assets/svg/avi-ascii.svg")

WIDTH = 100
ASCII = " .`:-=+*#%@"

img = Image.open(INPUT).convert("L")

w, h = img.size
aspect = h / w

HEIGHT = int(WIDTH * aspect * 0.55)

img = img.resize((WIDTH, HEIGHT))

pixels = list(img.getdata())

lines = []

for y in range(HEIGHT):
    row = ""
    for x in range(WIDTH):
        pixel = pixels[y * WIDTH + x]
        index = pixel * (len(ASCII) - 1) // 255
        row += ASCII[index]
    lines.append(row)

font_size = 8
line_height = 10

svg_height = line_height * len(lines) + 20
svg_width = WIDTH * 6

svg = []

svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">')

svg.append('<rect width="100%" height="100%" fill="#0d1117"/>')

svg.append(
    '<text x="10" y="20" '
    'font-family="Courier New, monospace" '
    f'font-size="{font_size}" '
    'fill="#d0d0d0">'
)

for i, line in enumerate(lines):
    svg.append(
        f'<tspan x="10" dy="{line_height}">{line}</tspan>'
    )

svg.append("</text>")
svg.append("</svg>")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(svg), encoding="utf-8")

print("Saved:", OUTPUT)