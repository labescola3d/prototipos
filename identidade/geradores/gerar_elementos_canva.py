"""Gera em SVG os 7 elementos gráficos garimpados nas artes do LE3D no Canva (18/11/2026).

Não são cópias das artes: são reconstruções paramétricas, a partir do kit vetorial
(icone-le3d.json, cubo-le3d.json) e das cores da marca, para virarem ferramenta.

  1 padrao-icones_{roxo,laranja}.svg   ícone LE3D em traço, repetido como textura (padrão sem emenda)
  2 reticula-pontos_{laranja,branco}.svg · grade-pontos_laranja.svg   pontos em degradê de canto / em grade
  3 mancha-organica_{1,2,3}{,_contorno}.svg   mancha para máscara de foto, cheia e com contorno laranja
  4 canto-icone.svg · canto-cubo.svg   traço grande cortado no canto superior direito (girar para os outros)
  5 etiqueta-destaque_{laranja,roxo}.svg   caixa arredondada para frase curta
  6 marca-texto_laranja.svg   faixa irregular para pôr atrás de uma palavra
  7 setas-sequencia.svg   três setas brancas com sombra roxa

Uso: py gerar_elementos_canva.py <identidade/geradores> <saída>
Determinístico (sem acaso): rodar de novo dá o mesmo arquivo.
"""
import json, math, sys
from pathlib import Path

VET, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
ROXO, LARANJA, BRANCO, CINZA = "#3026AD", "#E3630D", "#FFFFFF", "#F2F2F2"


def tint(hexc, p):  # regra da rampa da marca: mistura com branco, TRUNCANDO o canal
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{int(c + (255 - c) * p):02X}" for c in (r, g, b))


def salvar(nome, w, h, corpo, nota, fundo=None):
    bg = f'  <rect width="{w}" height="{h}" fill="{fundo}"/>\n' if fundo else ""
    (OUT / nome).write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<!-- {nota} · candidato a elemento gráfico LE3D (garimpo do Canva, 18/11/2026) · '
        'gerado por gerar_elementos_canva.py (github.com/labescola3d/prototipos/tree/main/identidade/geradores) · não editar à mão -->\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">\n'
        + bg + corpo + "</svg>\n", encoding="utf-8")


# ── geometria do kit ──────────────────────────────────────────────
ic = json.loads((VET / "icone-le3d.json").read_text(encoding="utf-8"))
IV, IS, IH = ic["vertices"], ic["segmentos"], ic["sistema"]["altura_linhas_centrais"]
cb = json.loads((VET / "cubo-le3d.json").read_text(encoding="utf-8"))
CV, CS = cb["vertices"], cb["segmentos"]
CH = max(p[1] for p in CV.values())


def d_icone(esc, dx, dy):  # y para cima -> SVG
    return " ".join(f"M{dx + IV[i][0] * esc:.2f} {dy + (IH - IV[i][1]) * esc:.2f}"
                    f"L{dx + IV[j][0] * esc:.2f} {dy + (IH - IV[j][1]) * esc:.2f}" for i, j in IS)


def d_cubo(esc, dx, dy):
    return " ".join(f"M{dx + CV[a][0] * esc:.2f} {dy + (CH - CV[a][1]) * esc:.2f}"
                    f"L{dx + CV[b][0] * esc:.2f} {dy + (CH - CV[b][1]) * esc:.2f}" for a, b in CS)


def traco(d, cor, w, extra=""):
    return f'  <path d="{d}" stroke="{cor}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>\n'


# 1 · padrão de ícones (ladrilho em tijolo: linhas alternadas deslocadas meia célula)
for nome, fundo in (("roxo", ROXO), ("laranja", LARANJA)):
    esc, cw, ch = 0.12, 160, 130           # ícone com 120 px de largura numa célula de 160 × 130
    linha = tint(fundo, 0.2)
    tile = (traco(d_icone(esc, 20, 15), linha, 2.4) + traco(d_icone(esc, 20 + cw / 2, 15 + ch), linha, 2.4)
            + traco(d_icone(esc, 20 - cw / 2, 15 + ch), linha, 2.4))
    corpo = (f'  <defs><pattern id="p" width="{cw}" height="{2 * ch}" patternUnits="userSpaceOnUse">\n'
             + tile.replace("  <path", "    <path") + "  </pattern></defs>\n"
             f'  <rect width="1080" height="1350" fill="{fundo}"/>\n  <rect width="1080" height="1350" fill="url(#p)"/>\n')
    salvar(f"padrao-icones_{nome}.svg", 1080, 1350, corpo,
           f"Padrão de ícones LE3D sobre {nome}; traço = cor de fundo a 20% de branco")

# 2 · retícula de pontos (canto superior direito; o raio cai com a distância ao canto)
for nome, cor in (("laranja", LARANJA), ("branco", BRANCO)):
    passo, pts = 22, []
    for gy in range(0, 520, passo):
        for gx in range(0, 520, passo):
            x, y = 520 - gx, gy + (passo / 2 if (gx // passo) % 2 else 0)
            dist = math.hypot(gx, gy) / 520
            r = 8.5 * max(0.0, 1 - dist) ** 1.4
            if r > 0.9:
                pts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
    salvar(f"reticula-pontos_{nome}.svg", 540, 540, f'  <g fill="{cor}">' + "".join(pts) + "</g>\n",
           f"Retícula de pontos {nome}, degradê a partir do canto superior direito")
pts = [f'<circle cx="{30 + c * 44 + (22 if l % 2 else 0)}" cy="{30 + l * 38}" r="5"/>'
       for l in range(10) for c in range(5)]
salvar("grade-pontos_laranja.svg", 260, 400, f'  <g fill="{tint(LARANJA, 0.0)}" fill-opacity="0.55">' + "".join(pts) + "</g>\n",
       "Grade regular de pontos em quincôncio, como a do botton")


# 3 · manchas orgânicas: Catmull-Rom fechado sobre raios fixos (sem acaso)
def mancha(raios, cx=500, cy=500, base=380):
    n = len(raios)
    P = [(cx + base * r * math.cos(2 * math.pi * k / n - math.pi / 2),
          cy + base * r * math.sin(2 * math.pi * k / n - math.pi / 2)) for k, r in enumerate(raios)]
    d = f"M{P[0][0]:.1f} {P[0][1]:.1f}"
    for k in range(n):
        p0, p1, p2, p3 = P[k - 1], P[k], P[(k + 1) % n], P[(k + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + "Z"


FORMAS = {1: [1.0, 1.12, 0.92, 1.05, 0.8, 0.98, 1.15, 0.86],
          2: [1.1, 0.85, 1.0, 1.18, 0.9, 0.95, 0.82],
          3: [0.95, 1.15, 1.05, 0.78, 1.0, 1.12, 0.88, 1.02, 0.84]}
for k, r in FORMAS.items():
    d = mancha(r)
    salvar(f"mancha-organica_{k}.svg", 1000, 1000, f'  <path d="{d}" fill="{ROXO}"/>\n',
           f"Mancha orgânica {k}, cheia — usar como máscara de foto")
    salvar(f"mancha-organica_{k}_contorno.svg", 1000, 1000,
           f'  <path d="{d}" fill="{ROXO}" stroke="{LARANJA}" stroke-width="14" stroke-linejoin="round"/>\n',
           f"Mancha orgânica {k} com contorno laranja, como em 'Você sabia?'")

# 4 · ícone e cubo cortados no canto (traço branco; recorte pelo próprio viewBox)
salvar("canto-icone.svg", 1000, 1000, traco(d_icone(0.9, 380, -200), BRANCO, 9),
       "Ícone LE3D em traço branco, cortado no canto superior direito (girar 90° para os outros cantos)")
salvar("canto-cubo.svg", 1000, 1000, traco(d_cubo(0.75, 470, -190), BRANCO, 9),
       "Cubo LE3D em traço branco, cortado no canto superior direito (girar 90° para os outros cantos)")

# 5 · etiqueta de destaque
for nome, cor in (("laranja", LARANJA), ("roxo", ROXO)):
    salvar(f"etiqueta-destaque_{nome}.svg", 640, 150,
           f'  <rect x="0" y="0" width="640" height="150" rx="32" fill="{cor}"/>\n',
           f"Etiqueta de destaque {nome}: caixa de 640 × 150, raio 32; texto em branco por cima")

# 6 · marca-texto (borda levemente irregular, como pincelada)
topo = [(0, 14), (80, 8), (190, 12), (300, 6), (420, 11), (520, 7), (600, 13)]
base = [(604, 86), (500, 92), (380, 88), (260, 94), (140, 89), (40, 93), (-4, 84)]
d = "M" + " L".join(f"{x} {y}" for x, y in topo + base) + "Z"
salvar("marca-texto_laranja.svg", 600, 100, f'  <path d="{d}" fill="{LARANJA}"/>\n',
       "Marca-texto laranja: faixa para pôr atrás de uma palavra; esticar na horizontal à vontade")

# 7 · setas em sequência
seta = "M0 0 L46 50 L0 100 L22 100 L68 50 L22 0Z"
corpo = "".join(f'  <path d="{seta}" transform="translate({18 + k * 92} {26})" fill="{ROXO}"/>\n'
                f'  <path d="{seta}" transform="translate({10 + k * 92} {18})" fill="{BRANCO}"/>\n' for k in range(3))
salvar("setas-sequencia.svg", 300, 150, corpo, "Três setas brancas com sombra roxa deslocada")

print("ok", len(list(OUT.glob("*.svg"))), "svg")
