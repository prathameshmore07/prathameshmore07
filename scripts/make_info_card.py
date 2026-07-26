from pathlib import Path

OUTPUT = Path("assets/svg/info-card.svg")

rows = [
    ("user", "Prathamesh More"),
    ("role", "Full Stack Developer"),
    ("focus", "AI | Cybersecurity"),
    ("languages", "Python • TS • JS • C++"),
    ("frontend", "Next.js • React • Tailwind"),
    ("backend", "FastAPI • Node • Express"),
    ("database", "MongoDB • PostgreSQL • Supabase"),
    ("projects", "CRAVE • FlowState • Retro Arcade"),
    ("building", "AI Agents & Security Tools"),
    ("github", "@prathameshmore07"),
]

width = 780
height = 40 + len(rows) * 34

svg = [
f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="0 0 {width} {height}">

<defs>
<style>
    .title {{
        font-family: "JetBrains Mono", "Cascadia Code", "Courier New", monospace;
        font-size: 18px;
        fill: #58a6ff;
        font-weight: bold;
    }}

    .key {{
        font-family: "JetBrains Mono", "Cascadia Code", "Courier New", monospace;
        font-size: 16px;
        fill: #7ee787;
    }}

    .value {{
        font-family: "JetBrains Mono", "Cascadia Code", "Courier New", monospace;
        font-size: 16px;
        fill: #c9d1d9;
    }}
</style>
</defs>

<rect width="100%" height="100%" rx="12" fill="#0d1117"/>

<text x="20" y="28" class="title">
$ neofetch
</text>
'''
]

y = 60

for i, (k, v) in enumerate(rows):
    delay = round(i * 0.15, 2)

    svg.append(f'''
<text
    x="20"
    y="{y}"
    class="key"
    opacity="0">

    <animate
        attributeName="opacity"
        begin="{delay}s"
        dur="0.4s"
        from="0"
        to="1"
        fill="freeze"/>

    {k} :
</text>

<text
    x="185"
    y="{y}"
    class="value"
    opacity="0">

    <animate
        attributeName="opacity"
        begin="{delay}s"
        dur="0.4s"
        from="0"
        to="1"
        fill="freeze"/>

    {v}
</text>
''')

    y += 32

svg.append("</svg>")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(svg), encoding="utf-8")

print(f"✅ Saved: {OUTPUT}")