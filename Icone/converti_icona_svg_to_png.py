import cairosvg

# Conversione del file SVG in PNG
path_svg = "cross-circle.svg"
path_png = "cross-circle.png"
cairosvg.svg2png(url=path_svg, write_to=path_png)