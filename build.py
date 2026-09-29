"""Assemble index.html from page.html + the generated map SVG."""
from pathlib import Path
root = Path(__file__).parent
page = (root / "page.html").read_text()
svg = (root / "assets/_map.svg").read_text()
(root / "index.html").write_text(page.replace("<!--MAP-->", svg))
print("wrote index.html")

# Artifact preview copy: the viewer supplies its own doctype/html/head/body skeleton.
import re
art = (root / "index.html").read_text()
for tag in ["<!doctype html>", '<html lang="en">', "<head>", "</head>", "<body>", "</body>", "</html>"]:
    art = art.replace(tag, "")
art = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>', "", art)
(root / "artifact.html").write_text(art.strip() + "\n")
print("wrote artifact.html")
