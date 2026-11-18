"""Lote 2 do garimpo do Canva (18/11/2026): 8 elementos de marca + variante roxa da retícula.

Fontes: mood board SIAC, template do principal, Conexões Lab Escola, Pitch Deck, cabeçalho "gestão".
Reconstruções paramétricas com as cores da marca (amarelo do mosaico -> laranja).

  8  mosaico-triangulos.svg            triângulos isométricos roxo/lilás/laranja com hachura
  9  chevrons_{esquerda,direita}.svg   « » em traço, moldura de título
  10 faixas-diagonais_laranja.svg      linhas paralelas a 45°
  11 mascara-diagonal.svg              recorte de foto em losangos/faixas (usar como máscara)
  12 linhas-circuito_laranja.svg       trilhas que se cruzam, com nós
  13 explosao_{laranja,roxo}.svg       estrela de pontas com sombra deslocada
  14 bauhaus-modulo.svg                quartos de círculo, semicírculos, quadrados e pontos
  15 ondas-concentricas.svg · brilho-4-pontas.svg
  +  reticula-pontos_roxo.svg          variante lilás da retícula, para fundo roxo

Uso: py gerar_elementos_canva_lote2.py <saída>. Determinístico.
"""
import math, sys
from pathlib import Path

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
ROXO, LARANJA, BRANCO, PRETO, CINZA = "#3026AD", "#E3630D", "#FFFFFF", "#150E1F", "#F2F2F2"


def tint(h, p):
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{int(c + (255 - c) * p):02X}" for c in (r, g, b))


def shade(h, p):
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{int(c * (1 - p)):02X}" for c in (r, g, b))


LILAS = tint(ROXO, 0.3)
ROXO_ESC = shade(ROXO, 0.2)


def salvar(nome, w, h, corpo, nota):
    (OUT / nome).write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<!-- {nota} · candidato a elemento gráfico LE3D (garimpo do Canva, lote 2, 18/11/2026) · '
        'gerado por gerar_elementos_canva_lote2.py (github.com/labescola3d/prototipos/tree/main/identidade/geradores) · não editar à mão -->\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">\n'
        + corpo + "</svg>\n", encoding="utf-8")


# 8 · mosaico de triângulos isométricos (grade de colunas; cada coluna = triângulos apontando esq/dir)
L = 100                      # largura da coluna
H = L * 2 / math.sqrt(3)     # altura do triângulo (lado) na grade isométrica vertical
cores = {"l": LILAS, "r": ROXO, "o": LARANJA, "e": ROXO_ESC}
# cada linha: colunas 0..5; em cada coluna, par (triângulo p/ direita, triângulo p/ esquerda); "." = vazio
padrao = [
    "lr lo or .. el o.",
    "ol .l rl ol re ..",
    "e. lo .o er .. ..",
    "lr o. le .. .. ..",
    "oe lr .. .. .. ..",
    "lo e. .. .. .. ..",
    "o. .. .. .. .. ..",
    "e. .. .. .. .. ..",
]
padrao = [linha.split() for linha in padrao]
tri, hach = [], []
for lin, cols in enumerate(padrao):
    for col, par in enumerate(cols):
        x0 = col * L
        for lado, ch in enumerate(par):
            if ch == ".":
                continue
            if lado == 0:   # base na linha x0, ápice à direita
                y = lin * H + (col % 2) * H / 2
                pts = [(x0, y), (x0, y + H), (x0 + L, y + H / 2)]
            else:           # base na linha x0+L, ápice à esquerda
                y = lin * H + ((col + 1) % 2) * H / 2
                pts = [(x0 + L, y), (x0 + L, y + H), (x0, y + H / 2)]
            c = cores[ch]
            d = "M" + " L".join(f"{x:.1f} {yy:.1f}" for x, yy in pts) + "Z"
            tri.append(f'<path d="{d}" fill="{c}"/>')
            cx, cy = sum(p[0] for p in pts) / 3, sum(p[1] for p in pts) / 3
            hach.append(f'<path d="M{cx - 26:.1f} {cy - 20:.1f}L{cx + 26:.1f} {cy + 20:.1f}"/>')
W = 6 * L
salvar("mosaico-triangulos.svg", W, int(len(padrao) * H + H / 2),
       "  <g>" + "".join(tri) + f'</g>\n  <g stroke="{PRETO}" stroke-opacity="0.45" stroke-width="2">' + "".join(hach) + "</g>\n",
       "Mosaico de triângulos isométricos roxo, lilás e laranja, com hachura")

# 9 · chevrons em traço
def chev(direita):
    s = []
    for k in range(4):
        x = 10 + k * 28
        if direita:
            s.append(f'<path d="M{x} 10 L{x + 40} 50 L{x} 90"/>')
        else:
            s.append(f'<path d="M{x + 40} 10 L{x} 50 L{x + 40} 90"/>')
    return f'  <g stroke="{BRANCO}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">' + "".join(s) + "</g>\n"
salvar("chevrons_direita.svg", 150, 100, chev(True), "Chevrons » em traço branco, à direita do título")
salvar("chevrons_esquerda.svg", 150, 100, chev(False), "Chevrons « em traço branco, à esquerda do título")

# 10 · faixas diagonais
lin = "".join(f'<path d="M{-200 + k * 110} 1000 L{800 + k * 110} 0"/>' for k in range(0, 12, 1) if k % 3 != 2)
salvar("faixas-diagonais_laranja.svg", 1000, 1000,
       f'  <g stroke="{LARANJA}" stroke-width="12" stroke-linecap="round">{lin}</g>\n',
       "Faixas diagonais laranja a 45°, sobre foto tratada em roxo")

# 11 · máscara diagonal (losangos e faixas inclinadas; preto = área visível)
form = [
    "M0 0 L420 0 L0 420Z",
    "M500 0 L760 0 L260 500 L0 500 L0 500Z",
    "M330 640 L640 330 L950 640 L640 950Z",
    "M0 600 L120 600 L0 720Z",
]
salvar("mascara-diagonal.svg", 1000, 1000, "".join(f'  <path d="{d}" fill="{PRETO}"/>\n' for d in form),
       "Máscara de foto em diagonal: usar as formas como recorte da foto")

# 12 · linhas de circuito
trilhas = [
    "M20 60 H260 L300 100 H560 L600 60 H900",
    "M20 100 H220 L260 140 H520 L560 100 H860",
    "M120 20 H330 L370 60 L410 100 L450 140 H700",
    "M60 140 H200 L240 100 H400 L440 60 H660 L700 20 H880",
]
nos = [(20, 60), (900, 60), (20, 100), (860, 100), (120, 20), (700, 140), (60, 140), (880, 20)]
salvar("linhas-circuito_laranja.svg", 920, 160,
       f'  <g stroke="{LARANJA}" stroke-width="4" stroke-linejoin="round">' + "".join(f'<path d="{d}"/>' for d in trilhas) + "</g>\n"
       f'  <g fill="{LARANJA}">' + "".join(f'<circle cx="{x}" cy="{y}" r="7"/>' for x, y in nos) + "</g>\n",
       "Linhas de circuito laranja, como sob o título da série Conexões")

# 13 · explosão
def estrela(cx, cy, n=16, r1=300, r2=210):
    pts = []
    for k in range(2 * n):
        r = r1 * (1 - 0.08 * ((k * 7) % 3)) if k % 2 == 0 else r2
        a = math.pi * k / n - math.pi / 2
        pts.append(f"{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}")
    return "M" + " L".join(pts) + "Z"
for nome, cor, sombra in (("laranja", LARANJA, LILAS), ("roxo", ROXO, LARANJA)):
    salvar(f"explosao_{nome}.svg", 700, 700,
           f'  <path d="{estrela(370, 370)}" fill="{sombra}"/>\n  <path d="{estrela(340, 340)}" fill="{cor}"/>\n',
           f"Explosão {nome} com sombra deslocada: selo de atenção para chamadas curtas")

# 14 · módulo Bauhaus (grade 3×3 de células de 200)
c = 200
b = [
    f'<path d="M{c} {c} A{c} {c} 0 0 0 {0} {2*c} L{c} {2*c}Z" fill="{LARANJA}"/>',           # quarto laranja
    f'<rect x="{c}" y="{c}" width="{c}" height="{c}" fill="{PRETO}"/>',
    f'<path d="M{c} {c} A{c} {c} 0 0 1 {2*c} {0} L{2*c} {c}Z" fill="{CINZA}"/>',
    f'<rect x="{2*c}" y="0" width="{c}" height="{c}" fill="{ROXO}"/>',
    f'<circle cx="{c*1.15}" cy="{c*0.3}" r="{c*0.2}" fill="{ROXO}"/>',
    f'<path d="M{2*c} {2*c} A{c} {c} 0 0 1 {3*c} {3*c} L{2*c} {3*c}Z" fill="{LARANJA}"/>',
    f'<path d="M{2*c} {3*c} A{c} {c} 0 0 0 {3*c} {4*c} L{2*c} {4*c}Z" fill="{ROXO}"/>',
    f'<circle cx="{c*2.7}" cy="{c*1.6}" r="{c*0.18}" fill="{CINZA}"/>',
]
salvar("bauhaus-modulo.svg", 3 * c, 4 * c, "  " + "".join(b) + "\n",
       "Módulo de geometria Bauhaus: quartos de círculo, quadrados e pontos nas cores da marca")

# 15 · ondas concêntricas + brilho
def blob(k, cx, cy, base):
    n, raios = 7, [1.0, 1.18, 0.9, 1.1, 0.85, 1.12, 0.95]
    P = [(cx + (base - k) * r * math.cos(2 * math.pi * i / n), cy + (base - k) * r * math.sin(2 * math.pi * i / n)) for i, r in enumerate(raios)]
    d = f"M{P[0][0]:.1f} {P[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = P[i - 1], P[i], P[(i + 1) % n], P[(i + 2) % n]
        d += (f"C{p1[0] + (p2[0] - p0[0]) / 6:.1f} {p1[1] + (p2[1] - p0[1]) / 6:.1f} "
              f"{p2[0] - (p3[0] - p1[0]) / 6:.1f} {p2[1] - (p3[1] - p1[1]) / 6:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    return d + "Z"
ondas = "".join(f'<path d="{blob(k, 0, 600, 560)}"/>' for k in range(0, 540, 40))
salvar("ondas-concentricas.svg", 600, 600,
       f'  <g stroke="{ROXO}" stroke-width="16">{ondas}</g>\n',
       "Ondas concêntricas roxas, saindo do canto inferior esquerdo, para fundo laranja")
salvar("brilho-4-pontas.svg", 100, 100,
       f'  <path d="M50 0 Q54 46 100 50 Q54 54 50 100 Q46 54 0 50 Q46 46 50 0Z" fill="{BRANCO}"/>\n',
       "Brilho de 4 pontas, branco; detalhe pequeno junto das ondas")

# + retícula roxa (variante para fundo roxo)
passo, pts = 22, []
for gy in range(0, 520, passo):
    for gx in range(0, 520, passo):
        x, y = 520 - gx, gy + (passo / 2 if (gx // passo) % 2 else 0)
        r = 8.5 * max(0.0, 1 - math.hypot(gx, gy) / 520) ** 1.4
        if r > 0.9:
            pts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
salvar("reticula-pontos_roxo.svg", 540, 540, f'  <g fill="{LILAS}">' + "".join(pts) + "</g>\n",
       "Retícula de pontos lilás, para fundo roxo, como na série Conexões")

print("ok")
