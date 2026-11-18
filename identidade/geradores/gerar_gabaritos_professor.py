"""Kit do professor LE3D: gabaritos para imprimir (A4 retrato, 210 × 297 mm, traço preto).

Benchmark: "Material Oficina de Gamificação Pedagógica — Lab Escola 3D" (Canva, 23 págs.), 18/11/2026.
Gramática: P&B, traço 0,4 mm, cantos levemente arredondados, faixa de cabeçalho fixa
(título em display + atividade entre parênteses + logo em traço à direita).

  cabecalho.svg                faixa de cabeçalho (título editável no Canva)
  dado-planificado.svg         dado com abas de cola
  cartas_{4,6,12}.svg          grades de cartas com campos sugeridos
  fichas-sorteio.svg           8 cartas + 8 fichas redondas
  quebra-cabeca_{3,5,8}x.svg   quebra-cabeça com encaixes
  tabuleiro_{serpentina,moldura,anel,colmeia}.svg
  ficha-pistas.svg             ficha de pistas (Investigadores do Conhecimento)

Uso: py gerar_gabaritos_professor.py <identidade/geradores> <saída>. Determinístico. Unidades em mm.
"""
import json, math, sys
from pathlib import Path

VET, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
W, H, M = 210, 297, 12           # página e margem
TR = 0.4                         # traço
PRETO = "#150E1F"
FONTE_T = "'Big Shoulders Display', 'Bebas Neue', sans-serif"
FONTE_R = "'Source Sans 3', 'Source Sans Pro', sans-serif"

ic = json.loads((VET / "icone-le3d.json").read_text(encoding="utf-8"))
IV, IS, IH = ic["vertices"], ic["segmentos"], ic["sistema"]["altura_linhas_centrais"]
IW = max(p[0] for p in (IV.values() if isinstance(IV, dict) else IV))


def logo(x, y, larg):
    e = larg / IW
    d = " ".join(f"M{x + IV[i][0] * e:.2f} {y + (IH - IV[i][1]) * e:.2f}L{x + IV[j][0] * e:.2f} {y + (IH - IV[j][1]) * e:.2f}" for i, j in IS)
    t = (f'<text x="{x + larg + 2}" y="{y + 3.2}" font-family="{FONTE_T}" font-weight="700" font-size="3.4" letter-spacing="0.4" fill="{PRETO}">'
         f'<tspan x="{x + larg + 2}">LAB</tspan><tspan x="{x + larg + 2}" dy="3.6">ESCOLA</tspan><tspan x="{x + larg + 8}" dy="3.6">3D</tspan></text>')
    return f'<path d="{d}" stroke="{PRETO}" stroke-width="0.35" stroke-linecap="round" stroke-linejoin="round"/>' + t


def cab(titulo, atividade):
    return (f'<text x="{M}" y="{M + 6}" font-family="{FONTE_T}" font-size="7" fill="{PRETO}">'
            f'<tspan font-weight="700">{titulo}</tspan> <tspan font-weight="400">({atividade})</tspan></text>'
            + logo(W - M - 30, M - 1, 15))


def salvar(nome, corpo, nota, titulo=None, atividade="Nome da atividade"):
    topo = cab(titulo, atividade) if titulo else ""
    (OUT / nome).write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<!-- {nota} · kit do professor LE3D · gerado por gerar_gabaritos_professor.py (github.com/labescola3d/prototipos/tree/main/identidade/geradores) · não editar à mão -->\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n'
        f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>\n{topo}\n'
        f'<g fill="none" stroke="{PRETO}" stroke-width="{TR}" stroke-linejoin="round">\n{corpo}</g>\n</svg>\n', encoding="utf-8")


def rect(x, y, w, h, r=1.5):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}"/>\n'


def rot(x, y, txt, tam=3):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONTE_R}" font-size="{tam}" fill="{PRETO}" stroke="none">{txt}</text>\n'


# cabeçalho isolado
salvar("cabecalho.svg", "", "Faixa de cabeçalho das fichas", "TÍTULO DA FICHA")

# dado planificado (cruz) com abas
a, x0, y0 = 45, (W - 45 * 4) / 2, 50
faces = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2)]
dado = "".join(rect(x0 + c * a, y0 + l * a, a, a, 0) for c, l in faces)
def aba(x1, y1, x2, y2, dx, dy, k=7):
    return (f'<path d="M{x1:.1f} {y1:.1f} L{x1 + dx * k + (x2 - x1) * 0.15:.1f} {y1 + dy * k + (y2 - y1) * 0.15:.1f} '
            f'L{x2 + dx * k - (x2 - x1) * 0.15:.1f} {y2 + dy * k - (y2 - y1) * 0.15:.1f} L{x2:.1f} {y2:.1f}" stroke-dasharray="1.5 1"/>\n')
X, Y = x0, y0
dado += aba(X + a, Y, X + 2 * a, Y, 0, -1)                    # topo da face de cima
dado += aba(X + a, Y, X + a, Y + a, -1, 0) + aba(X + 2 * a, Y, X + 2 * a, Y + a, 1, 0)
dado += aba(X + a, Y + 3 * a, X + 2 * a, Y + 3 * a, 0, 1)
dado += aba(X + a, Y + 2 * a, X + a, Y + 3 * a, -1, 0) + aba(X + 2 * a, Y + 2 * a, X + 2 * a, Y + 3 * a, 1, 0)
dado += aba(X + 4 * a, Y + a, X + 4 * a, Y + 2 * a, 1, 0)
dado += rot(M, 250, "Desenhe a pista, a numeração ou os pontos em cada face; recorte, dobre nas linhas e cole nas abas tracejadas.", 3)
salvar("dado-planificado.svg", dado, "Dado planificado com abas de cola", "DADO")

# grades de cartas
for n, (cols, lins) in {4: (2, 2), 6: (2, 3), 12: (4, 3)}.items():
    g, gw, gh = 4, (W - 2 * M - 4 * (cols - 1)) / cols, (H - 40 - M - 4 * (lins - 1)) / lins
    s = ""
    for l in range(lins):
        for c in range(cols):
            x, y = M + c * (gw + g), 30 + l * (gh + g)
            s += rect(x, y, gw, gh, 2.5)
            s += f'<path d="M{x + 3:.1f} {y + 4:.1f} h{gw * 0.25:.1f} M{x + gw * 0.35:.1f} {y + 4:.1f} h{gw * 0.6:.1f}"/>\n'
            s += rect(x + 3, y + 7, gw - 6, gh * 0.45, 1.5) + rect(x + 3, y + 10 + gh * 0.45, gw - 6, gh * 0.45 - 13, 1.5)
            s += f'<circle cx="{x + gw - 8:.1f}" cy="{y + 13:.1f}" r="{min(gw, gh) * 0.05:.1f}"/>\n'
            if n == 4 and l == 0 and c == 0:
                s += rot(x + 3, y + 3, "Categoria", 2.4) + rot(x + gw * 0.35, y + 3, "Objeto / Lugar / Pessoa", 2.4)
                s += rot(x + 6, y + 12, "Imagem representativa", 2.6) + rot(x + 6, y + 15 + gh * 0.45, "Informações / Conteúdos", 2.6)
    salvar(f"cartas_{n}.svg", s, f"Grade de {n} cartas com campos sugeridos", "LAYOUT DE CARTAS")

# fichas de sorteio
s = rot(M, 32, "Cartas", 3.5)
cw = (W - 2 * M - 3 * 5) / 4
for l in range(2):
    for c in range(4):
        s += rect(M + c * (cw + 5), 36 + l * 60, cw, 55, 1.5)
s += rot(M, 168, "Fichas para sortear", 3.5)
for l in range(2):
    for c in range(4):
        s += f'<circle cx="{M + cw / 2 + c * (cw + 5):.1f}" cy="{195 + l * 50:.1f}" r="{cw / 2 - 1:.1f}"/>\n'
salvar("fichas-sorteio.svg", s, "Cartas e fichas redondas para sorteio", "OPÇÕES DE ALEATORIEDADE")

# quebra-cabeça (bordas com encaixe; sentido do encaixe determinístico)
def borda(x1, y1, x2, y2, sinal):
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy * sinal, ux * sinal
    p = lambda t, h: (x1 + ux * L * t + nx * L * h, y1 + uy * L * t + ny * L * h)
    q = [p(0.38, 0), p(0.36, 0.12), p(0.5, 0.22), p(0.64, 0.12), p(0.62, 0)]
    return (f"L{q[0][0]:.2f} {q[0][1]:.2f} C{p(0.42, 0.06)[0]:.2f} {p(0.42, 0.06)[1]:.2f} {q[1][0]:.2f} {q[1][1]:.2f} {p(0.38, 0.16)[0]:.2f} {p(0.38, 0.16)[1]:.2f} "
            f"C{p(0.40, 0.24)[0]:.2f} {p(0.40, 0.24)[1]:.2f} {p(0.60, 0.24)[0]:.2f} {p(0.60, 0.24)[1]:.2f} {p(0.62, 0.16)[0]:.2f} {p(0.62, 0.16)[1]:.2f} "
            f"C{q[3][0]:.2f} {q[3][1]:.2f} {p(0.58, 0.06)[0]:.2f} {p(0.58, 0.06)[1]:.2f} {q[4][0]:.2f} {q[4][1]:.2f} L{x2:.2f} {y2:.2f}")
for n in (3, 5, 8):
    lado = W - 2 * M; t = lado / n; x0, y0 = M, 40
    s = rect(x0, y0, lado, lado, 0)
    for i in range(1, n):
        for j in range(n):   # linhas verticais e horizontais internas, peça a peça
            sg = 1 if (i * 7 + j * 3) % 2 else -1
            s += f'<path d="M{x0 + i * t:.2f} {y0 + j * t:.2f} ' + borda(x0 + i * t, y0 + j * t, x0 + i * t, y0 + (j + 1) * t, sg) + '"/>\n'
            sg = 1 if (i * 5 + j * 11) % 2 else -1
            s += f'<path d="M{x0 + j * t:.2f} {y0 + i * t:.2f} ' + borda(x0 + j * t, y0 + i * t, x0 + (j + 1) * t, y0 + i * t, sg) + '"/>\n'
    salvar(f"quebra-cabeca_{n}x{n}.svg", s, f"Quebra-cabeça {n} × {n} com encaixes", "QUEBRA-CABEÇAS")

# tabuleiros
# serpentina: 3 colunas de casas ligadas por curvas
s, cw, ch, colx, top, n = "", 26, 16, [30, 92, 154], 50, 12
for k, x in enumerate(colx):
    s += rect(x, top, cw, ch * n, 0)
    s += "".join(f'<path d="M{x} {top + i * ch} h{cw}"/>\n' for i in range(1, n))
    if k < 2:
        cx = (x + colx[k + 1] + cw) / 2; r1, r2 = (colx[k + 1] + cw - x) / 2, (colx[k + 1] - x - cw) / 2
        yb = top if k % 2 == 0 else top + ch * n; sw = 1 if k % 2 == 0 else 0
        s += f'<path d="M{x} {yb} A{r1} {r1} 0 0 {sw} {colx[k + 1] + cw} {yb} M{x + cw} {yb} A{r2} {r2} 0 0 {sw} {colx[k + 1]} {yb}"/>\n'
        sg = -1 if k % 2 == 0 else 1
        for a_ in (45, 90, 135):
            ar = math.radians(a_)
            s += f'<path d="M{cx - r2 * math.cos(ar):.1f} {yb + sg * r2 * math.sin(ar):.1f} L{cx - r1 * math.cos(ar):.1f} {yb + sg * r1 * math.sin(ar):.1f}"/>\n'
salvar("tabuleiro_serpentina.svg", s, "Tabuleiro em serpentina", "TIPOS DE TABULEIRO")

# moldura
x0, y0, w, h, b = 20, 40, 170, 230, 26
s = rect(x0, y0, w, h, 0) + rect(x0 + b, y0 + b, w - 2 * b, h - 2 * b, 0)
s += "".join(f'<path d="M{x0 + px} {y0 + py} L{x0 + qx} {y0 + qy}"/>\n' for px, py, qx, qy in
             [(0, 0, b, b), (w, 0, w - b, b), (0, h, b, h - b), (w, h, w - b, h - b)])
nh, nv = 7, 10
s += "".join(f'<path d="M{x0 + b + i * (w - 2 * b) / nh:.1f} {y0} v{b} M{x0 + b + i * (w - 2 * b) / nh:.1f} {y0 + h - b} v{b}"/>\n' for i in range(1, nh))
s += "".join(f'<path d="M{x0} {y0 + b + i * (h - 2 * b) / nv:.1f} h{b} M{x0 + w - b} {y0 + b + i * (h - 2 * b) / nv:.1f} h{b}"/>\n' for i in range(1, nv))
salvar("tabuleiro_moldura.svg", s, "Tabuleiro em moldura retangular", "TIPOS DE TABULEIRO")

# anel
cx, cy, R, r, n = W / 2, 160, 90, 50, 20
s = f'<circle cx="{cx}" cy="{cy}" r="{R}"/>\n<circle cx="{cx}" cy="{cy}" r="{r}"/>\n'
s += "".join(f'<path d="M{cx + r * math.cos(2 * math.pi * i / n):.1f} {cy + r * math.sin(2 * math.pi * i / n):.1f} L{cx + R * math.cos(2 * math.pi * i / n):.1f} {cy + R * math.sin(2 * math.pi * i / n):.1f}"/>\n' for i in range(n))
salvar("tabuleiro_anel.svg", s, "Tabuleiro em anel, 20 casas", "TIPOS DE TABULEIRO")

# colmeia (19 hexágonos dentro de um hexágono)
def hexa(cx, cy, r):
    return "M" + " L".join(f"{cx + r * math.cos(math.radians(60 * k + 30)):.2f} {cy + r * math.sin(math.radians(60 * k + 30)):.2f}" for k in range(6)) + "Z"
cx, cy, r = W / 2, 160, 15
s = f'<path d="{hexa(cx, cy, 95)}"/>\n'
for q in range(-2, 3):
    for rr in range(-2, 3):
        if abs(q + rr) > 2:
            continue
        x = cx + r * math.sqrt(3) * (q + rr / 2); y = cy + r * 1.5 * rr
        s += f'<path d="{hexa(x, y, r - 1)}"/>\n'
salvar("tabuleiro_colmeia.svg", s, "Tabuleiro em colmeia, 19 casas hexagonais", "TIPOS DE TABULEIRO")

# ficha de pistas
s = rect(M, 28, W - 2 * M, 130, 2) + rect(M + 6, 70, 95, 80, 1) + rect(M + 112, 46, 68, 52, 1) + rect(M + 112, 112, 68, 38, 1)
s += rot(M + 125, 42, "Pista visual", 4) + rot(M + 128, 108, "Descrição", 4)
s += rect(M, 164, W - 2 * M, 112, 2)
s += "".join(rot(M + 6, 176 + i * 24, t, 3.6) for i, t in enumerate(["Pista 1 —", "Pista 2 —", "Pista 3 —", "Curiosidade —"]))
s += rot(M, 285, "Frente: silhueta · Verso: desenho ou foto (colagem)", 2.8)
salvar("ficha-pistas.svg", s, "Ficha de pistas", "FICHA DE PISTAS", "Investigadores do Conhecimento")

print("ok", len(list(OUT.glob("*.svg"))), "svg")
