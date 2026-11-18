"""Separa os elementos gráficos dos banners do site (labescola3d.rio.br, uploads/2024/10).

Entrada: identidade/geradores/originais-site/*.svg (cópia íntegra dos banners, 17/11/2026).
Saída:   identidade/elementos/site-2024/
  - fita-organica_<banner>.svg  — só as 18 linhas da fita, fundo transparente
  - quadrados_<banner>.svg      — só os quadrados vazados laranja, na posição original
  - moldura-degrade_{vertical,horizontal}.svg — cartão do site, reconstruído com os
    parâmetros medidos em carrossel-1.svg (vertical) e Group-5-2.svg (horizontal)

Uso: py extrair_elementos_site.py <pasta site-2024>
"""
import re, sys
from pathlib import Path

BASE = Path(sys.argv[1]); ORIG = BASE / "originais"
CAB = '<?xml version="1.0" encoding="UTF-8"?>\n<!-- {nota} · extraído de labescola3d.rio.br em 17/11/2026 por extrair_elementos_site.py (github.com/labescola3d/prototipos/tree/main/identidade/geradores) · não editar à mão -->\n'

for svg in sorted(ORIG.glob("*.svg")):
    s = svg.read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    paths = re.findall(r"<path\b[^>]*?(?:/>|></path>)", s)
    fita = [p for p in paths if 'stroke="#353C8E"' in p]
    quad = [p for p in paths if 'stroke="#E3620E"' in p]
    w, h = vb.split()[2:]
    for nome, lista, nota in (("fita-organica", fita, "Fita orgânica LE3D — 18 linhas #353C8E, traço 0,321"),
                              ("quadrados", quad, "Quadrados vazados LE3D — #E3620E, traço 1,2272")):
        (BASE / f"{nome}_{svg.stem}.svg").write_text(
            CAB.format(nota=nota) +
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}" fill="none">\n'
            f'  <g clip-path="url(#c)">\n    ' + "\n    ".join(lista) + "\n  </g>\n"
            f'  <defs><clipPath id="c"><rect width="{w}" height="{h}"/></clipPath></defs>\n</svg>\n', encoding="utf-8")
    print(svg.stem, "fita", len(fita), "quadrados", len(quad))

MOLD = {
    "vertical": (1000, 600, 19.5, (500, 0, 500, 600), ("#E3620E", "#3026AD"), "carrossel-1.svg: laranja no topo, roxo embaixo"),
    "horizontal": (1589, 630, 29.5, (0, 315, 1589, 315), ("#3026AD", "#E3630D"), "Group-5-2.svg: roxo à esquerda, laranja à direita"),
}
for nome, (w, h, rx, (x1, y1, x2, y2), (c1, c2), nota) in MOLD.items():
    (BASE / f"moldura-degrade_{nome}.svg").write_text(
        CAB.format(nota=f"Moldura com contorno em degradê — {nota}") +
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">\n'
        f'  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="#F2F2F2" stroke="url(#g)"/>\n'
        f'  <defs><linearGradient id="g" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" gradientUnits="userSpaceOnUse">'
        f'<stop stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>\n</svg>\n', encoding="utf-8")
print("molduras ok")
