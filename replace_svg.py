import re

with open('index.html', 'r') as f:
    content = f.read()

with open('lion.svg', 'r') as f:
    new_svg = f.read()

# Replace the lion SVGs
def replace_svg_match(match):
    svg_content = match.group(0)
    # Check if this SVG is one of the lion logos by looking at its content.
    if 'fill="#4A0E1C"' in svg_content and 'opacity="0.55"' in svg_content or 'viewBox="0 0 80 80"' in svg_content and 'rx="12"' in svg_content:
        # It's a lion logo. We need to preserve the class if it exists.
        class_match = re.search(r'class="([^"]+)"', svg_content)
        if class_match:
            class_str = f' class="{class_match.group(1)}"'
            return new_svg.replace('<svg viewBox="0 0 160 160"', f'<svg{class_str} viewBox="0 0 160 160"')
        else:
            return new_svg
    return svg_content

# The file contains 4 lion logos. They have a distinct structure.
# Let's write a python script to replace them explicitly.
# Wait, let's just find them by parsing the HTML.
from bs4 import BeautifulSoup

soup = BeautifulSoup(content, 'html.parser')
svgs = soup.find_all('svg')
for svg in svgs:
    # Identify the lion logos based on elements they contain
    if svg.find('g', attrs={'stroke': '#C9A84C', 'opacity': '0.65'}) or svg.find('g', attrs={'stroke': '#C9A84C', 'opacity': '0.55'}):
        # This is a lion logo!
        new_svg_soup = BeautifulSoup(new_svg, 'html.parser')
        new_svg_tag = new_svg_soup.svg

        # Copy original attributes
        for attr, value in svg.attrs.items():
            if attr not in ['viewBox', 'xmlns', 'fill']:
                new_svg_tag[attr] = value

        # Replace the tag
        svg.replace_with(new_svg_tag)

with open('index.html', 'w') as f:
    f.write(str(soup))
