from pathlib import Path
from html import escape

def create_thumbnail_svg(path, title):
    text = escape(title[:28])
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<rect width="1280" height="720" fill="#8ed8ff"/>
<circle cx="180" cy="150" r="100" fill="#ffd86b"/>
<circle cx="1050" cy="560" r="150" fill="#9be28f"/>
<rect x="90" y="260" width="1100" height="220" rx="55" fill="#ffffff" opacity=".92"/>
<text x="640" y="395" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="72" font-weight="700" fill="#17324d">{text}</text>
<text x="640" y="455" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="30" fill="#2d5877">Original Preschool 3D Adventure</text>
</svg>"""
    Path(path).write_text(svg, encoding="utf-8")
    return str(path)
