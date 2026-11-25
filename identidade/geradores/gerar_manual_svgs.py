"""Gera em SVG todos os vetores do Manual da Marca 2024 do Lab Escola 3D.

Deriva as variantes cromáticas de logo/ícone, diagramas técnicos,
exemplos de usos indevidos, padrões visuais e aplicações vetoriais
a partir do kit vetorial oficial e de icone-le3d.json.

Uso: py -I -X utf8 identidade/geradores/gerar_manual_svgs.py
Determinístico (sem dependências externas).
"""
import json
import math
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
KIT_DIR = RAIZ / "catalogo" / "kit-de-divulgacao"
GER_DIR = Path(__file__).resolve().parent
OUT_DIR = RAIZ / "identidade" / "manual"

CORES = {
    "roxo": "#3026AD",
    "laranja": "#E3630D",
    "preto": "#000000",
    "branco": "#FFFFFF",
}
PRETO_TEXTO = "#150E1F"
CINZA_FUNDO = "#F2F2F2"


def tint(hex_cor: str, p: float) -> str:
    """Regra da rampa da marca: mistura com branco truncando cada canal."""
    r, g, b = (int(hex_cor[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{int(c + (255 - c) * p):02X}" for c in (r, g, b))


def _ler_paths_kit() -> tuple[str, str, str]:
    h_txt = (KIT_DIR / "logo-lab-escola-3d-horizontal.svg").read_text(encoding="utf-8")
    v_txt = (KIT_DIR / "logo-lab-escola-3d-vertical.svg").read_text(encoding="utf-8")
    h_paths = re.findall(r'<path\b[^>]*\bd="([^"]+)"', h_txt)
    v_paths = re.findall(r'<path\b[^>]*\bd="([^"]+)"', v_txt)
    if len(h_paths) < 2 or len(v_paths) < 2:
        raise RuntimeError("SVGs do kit-de-divulgacao não têm os 2 paths esperados.")
    return h_paths[0], h_paths[1], v_paths[1]


def _salvar_svg(nome: str, w: float, h: float, corpo: str, titulo: str,
                viewbox: str | None = None, fundo: str | None = None) -> Path:
    vb = viewbox or f"0 0 {w:g} {h:g}"
    bg = f'  <rect width="100%" height="100%" fill="{fundo}"/>\n' if fundo else ""
    conteudo = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!-- Gerado por identidade/geradores/gerar_manual_svgs.py · não editar à mão -->\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" viewBox="{vb}">\n'
        f'  <title>{titulo}</title>\n'
        + bg
        + corpo
        + "</svg>\n"
    )
    arq = OUT_DIR / nome
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text(conteudo, encoding="utf-8", newline="\n")
    return arq


def _bloco_3d_rotulado(x: float, y: float, w: float, h: float, vertical: bool = False) -> str:
    rot = f' transform="rotate(-90 {x + w / 2:.1f} {y + h / 2:.1f})"' if vertical else ""
    fs = (w if vertical else h) * 0.68
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#E3630D" fill-opacity="0.38"/>'
        f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + fs * 0.35:.1f}" text-anchor="middle" '
        f'font-family="\'Bebas Neue\',\'Big Shoulders Display\',Arial,sans-serif" font-weight="700" '
        f'font-size="{fs:.1f}" fill="#FFFFFF"{rot}>3D</text>'
    )


def _cota_h(x1: float, x2: float, y: float, rotulo: str, fs: float = 28) -> str:
    xm = (x1 + x2) / 2
    return (
        f'<g stroke="#444444" stroke-width="2">'
        f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}"/>'
        f'<line x1="{x1:.1f}" y1="{y - 8:.1f}" x2="{x1:.1f}" y2="{y + 8:.1f}"/>'
        f'<line x1="{x2:.1f}" y1="{y - 8:.1f}" x2="{x2:.1f}" y2="{y + 8:.1f}"/>'
        f'</g>'
        f'<rect x="{xm - fs * 0.85:.1f}" y="{y - fs * 0.65:.1f}" width="{fs * 1.7:.1f}" height="{fs * 1.25:.1f}" fill="#FFFFFF"/>'
        f'<text x="{xm:.1f}" y="{y + fs * 0.36:.1f}" text-anchor="middle" '
        f'font-family="\'Roboto\',\'Source Sans 3\',Arial,sans-serif" font-size="{fs:.1f}" fill="#444444">{rotulo}</text>'
    )


def _cota_v(x: float, y1: float, y2: float, rotulo: str, fs: float = 28) -> str:
    ym = (y1 + y2) / 2
    linhas = rotulo.split("\n")
    txts = "".join(
        f'<text x="{x:.1f}" y="{ym + (idx - (len(linhas) - 1) / 2) * fs * 1.15 + fs * 0.35:.1f}" '
        f'text-anchor="middle" font-family="\'Roboto\',\'Source Sans 3\',Arial,sans-serif" '
        f'font-size="{fs:.1f}" fill="#444444">{ln}</text>'
        for idx, ln in enumerate(linhas)
    )
    box_h = len(linhas) * fs * 1.25 + 8
    return (
        f'<g stroke="#444444" stroke-width="2">'
        f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}"/>'
        f'<line x1="{x - 8:.1f}" y1="{y1:.1f}" x2="{x + 8:.1f}" y2="{y1:.1f}"/>'
        f'<line x1="{x - 8:.1f}" y1="{y2:.1f}" x2="{x + 8:.1f}" y2="{y2:.1f}"/>'
        f'</g>'
        f'<rect x="{x - fs * 0.95:.1f}" y="{ym - box_h / 2:.1f}" width="{fs * 1.9:.1f}" height="{box_h:.1f}" fill="#FFFFFF"/>'
        + txts
    )


def gerar_todos() -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    d_icone, d_word_h, d_word_v = _ler_paths_kit()
    ic_json = json.loads((GER_DIR / "icone-le3d.json").read_text(encoding="utf-8"))
    iv, isegs, ih = ic_json["vertices"], ic_json["segmentos"], ic_json["sistema"]["altura_linhas_centrais"]

    gerados: list[Path] = []

    # 1. Logos horizontais, logos verticais e ícones (12 SVGs)
    for nome, cor in CORES.items():
        gerados.append(_salvar_svg(
            f"logo-horizontal-{nome}.svg", 2013.423, 921.780,
            f'  <path d="{d_icone}" fill="{cor}" fill-rule="evenodd"/>\n'
            f'  <path d="{d_word_h}" fill="{cor}"/>\n',
            f"Lab Escola 3D — logo horizontal ({nome})",
        ))
        gerados.append(_salvar_svg(
            f"logo-vertical-{nome}.svg", 1052.798, 1805.083,
            f'  <path d="{d_icone}" fill="{cor}" fill-rule="evenodd"/>\n'
            f'  <path d="{d_word_v}" fill="{cor}"/>\n',
            f"Lab Escola 3D — logo vertical ({nome})",
        ))
        gerados.append(_salvar_svg(
            f"icone-{nome}.svg", 1052.798, 875.220,
            f'  <path d="{d_icone}" fill="{cor}" fill-rule="evenodd"/>\n',
            f"Lab Escola 3D — ícone ({nome})",
        ))

    # 2. P06 — Áreas de proteção do logo (horizontal e vertical)
    # Largura do "3D" no sistema 2013x921 / 1052x1805 = 246.8 u
    pad_3d = 247.0
    # Horizontal: logo em x=[20, 1993.4], y=[20, 901.8]
    lx0, ly0, lx1, ly1 = 20.0, 20.0, 1993.4, 901.8
    ow_h, oh_h = (lx1 - lx0) + 2 * pad_3d + 40, (ly1 - ly0) + 2 * pad_3d + 40
    ox_h, oy_h = pad_3d + 20 - lx0, pad_3d + 20 - ly0
    bx0, by0, bx1, by1 = ox_h + lx0, oy_h + ly0, ox_h + lx1, oy_h + ly1
    corpo_p06_h = (
        f'  <rect x="{bx0 - pad_3d:.1f}" y="{by0 - pad_3d:.1f}" width="{bx1 - bx0 + 2 * pad_3d:.1f}" '
        f'height="{by1 - by0 + 2 * pad_3d:.1f}" fill="#FFFFFF" stroke="#444444" stroke-width="4"/>\n'
        f'  <rect x="{bx0:.1f}" y="{by0:.1f}" width="{bx1 - bx0:.1f}" height="{by1 - by0:.1f}" '
        f'fill="none" stroke="#444444" stroke-width="3"/>\n'
        f'  {_bloco_3d_rotulado(bx0 - pad_3d, by0 + 300, pad_3d, 160)}\n'
        f'  {_bloco_3d_rotulado(bx1, by0 + 300, pad_3d, 160)}\n'
        f'  {_bloco_3d_rotulado(bx0 + 820, by0 - pad_3d, 160, pad_3d, vertical=True)}\n'
        f'  {_bloco_3d_rotulado(bx0 + 820, by1, 160, pad_3d, vertical=True)}\n'
        f'  <g transform="translate({ox_h:.1f},{oy_h:.1f})">\n'
        f'    <path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/>\n'
        f'    <path d="{d_word_h}" fill="#3026AD"/>\n'
        f'  </g>\n'
        f'  {_cota_h(bx0 + 1726, bx1, by1 + 65, "x", fs=34)}\n'
    )
    gerados.append(_salvar_svg(
        "p06-area-protecao-logo-horizontal.svg", ow_h, oh_h, corpo_p06_h,
        "Área de proteção do logo horizontal (largura do 3D)",
    ))

    # Vertical: logo em x=[20, 1032.8], y=[20, 1785.1]
    vx0, vy0, vx1, vy1 = 20.0, 20.0, 1032.8, 1785.1
    ow_v, oh_v = (vx1 - vx0) + 2 * pad_3d + 40, (vy1 - vy0) + 2 * pad_3d + 40
    ox_v, oy_v = pad_3d + 20 - vx0, pad_3d + 20 - vy0
    vbx0, vby0, vbx1, vby1 = ox_v + vx0, oy_v + vy0, ox_v + vx1, oy_v + vy1
    corpo_p06_v = (
        f'  <rect x="{vbx0 - pad_3d:.1f}" y="{vby0 - pad_3d:.1f}" width="{vbx1 - vbx0 + 2 * pad_3d:.1f}" '
        f'height="{vby1 - vby0 + 2 * pad_3d:.1f}" fill="#FFFFFF" stroke="#444444" stroke-width="4"/>\n'
        f'  <rect x="{vbx0:.1f}" y="{vby0:.1f}" width="{vbx1 - vbx0:.1f}" height="{vby1 - vby0:.1f}" '
        f'fill="none" stroke="#444444" stroke-width="3"/>\n'
        f'  {_bloco_3d_rotulado(vbx0 - pad_3d, vby0 + 820, pad_3d, 160)}\n'
        f'  {_bloco_3d_rotulado(vbx1, vby0 + 820, pad_3d, 160)}\n'
        f'  {_bloco_3d_rotulado(vbx0 + 360, vby0 - pad_3d, 160, pad_3d, vertical=True)}\n'
        f'  {_bloco_3d_rotulado(vbx0 + 360, vby1, 160, pad_3d, vertical=True)}\n'
        f'  <g transform="translate({ox_v:.1f},{oy_v:.1f})">\n'
        f'    <path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/>\n'
        f'    <path d="{d_word_v}" fill="#3026AD"/>\n'
        f'  </g>\n'
        f'  {_cota_h(vbx0 + 678, vbx0 + 925, vby1 + 65, "x", fs=34)}\n'
    )
    gerados.append(_salvar_svg(
        "p06-area-protecao-logo-vertical.svg", ow_v, oh_v, corpo_p06_v,
        "Área de proteção do logo vertical (largura do 3D)",
    ))

    # 3. P08 — Área de proteção do ícone
    ix0, iy0, ix1, iy1 = 20.0, 20.0, 1032.8, 855.2
    ow_i, oh_i = (ix1 - ix0) + 2 * pad_3d + 40, (iy1 - iy0) + 2 * pad_3d + 40
    ox_i, oy_i = pad_3d + 20 - ix0, pad_3d + 20 - iy0
    ibx0, iby0, ibx1, iby1 = ox_i + ix0, oy_i + iy0, ox_i + ix1, oy_i + iy1
    corpo_p08 = (
        f'  <rect x="{ibx0 - pad_3d:.1f}" y="{iby0 - pad_3d:.1f}" width="{ibx1 - ibx0 + 2 * pad_3d:.1f}" '
        f'height="{iby1 - iby0 + 2 * pad_3d:.1f}" fill="#FFFFFF" stroke="#444444" stroke-width="4"/>\n'
        f'  <rect x="{ibx0:.1f}" y="{iby0:.1f}" width="{ibx1 - ibx0:.1f}" height="{iby1 - iby0:.1f}" '
        f'fill="none" stroke="#444444" stroke-width="3"/>\n'
        f'  {_bloco_3d_rotulado(ibx0 - pad_3d, iby0 + 340, pad_3d, 160)}\n'
        f'  {_bloco_3d_rotulado(ibx1, iby0 + 340, pad_3d, 160)}\n'
        f'  {_bloco_3d_rotulado(ibx0 + 420, iby0 - pad_3d, 160, pad_3d, vertical=True)}\n'
        f'  {_bloco_3d_rotulado(ibx0 + 420, iby1, 160, pad_3d, vertical=True)}\n'
        f'  <g transform="translate({ox_i:.1f},{oy_i:.1f})">\n'
        f'    <path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/>\n'
        f'  </g>\n'
    )
    gerados.append(_salvar_svg(
        "p08-area-protecao-icone.svg", ow_i, oh_i, corpo_p08,
        "Área de proteção do ícone isolado",
    ))

    # 4. P09 — Estrutura do ícone (linhas oblíquas estendidas a partir de icone-le3d.json)
    pad_g = 340.0
    gw, gh = 1000.0 + 2 * pad_g, ih + 2 * pad_g
    linhas_diag = []
    vistas = set()
    for a, b in isegs:
        x1, y1 = iv[a][0] + pad_g, (ih - iv[a][1]) + pad_g
        x2, y2 = iv[b][0] + pad_g, (ih - iv[b][1]) + pad_g
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) < 5.0:
            continue  # p.09 destaca apenas as linhas diagonais oblíquas
        m = dy / dx
        c = y1 - m * x1
        chave = (round(m, 2), round(c / 4.0))
        if chave in vistas:
            continue
        vistas.add(chave)
        # Intersecta x = 20 e x = gw - 20
        xa, xb = 20.0, gw - 20.0
        ya, yb = m * xa + c, m * xb + c
        linhas_diag.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}"/>')
    icone_linhas = " ".join(
        f"M{iv[a][0] + pad_g:.2f} {(ih - iv[a][1]) + pad_g:.2f}"
        f"L{iv[b][0] + pad_g:.2f} {(ih - iv[b][1]) + pad_g:.2f}"
        for a, b in isegs
    )
    corpo_p09 = (
        f'  <defs><clipPath id="clipG"><rect x="20" y="20" width="{gw - 40:.1f}" height="{gh - 40:.1f}"/></clipPath></defs>\n'
        f'  <g clip-path="url(#clipG)" stroke="#888888" stroke-width="2.2">{"".join(linhas_diag)}</g>\n'
        f'  <path d="{icone_linhas}" fill="none" stroke="#150E1F" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>\n'
    )
    gerados.append(_salvar_svg(
        "p09-estrutura-icone.svg", gw, gh, corpo_p09,
        "Estrutura do ícone em perspectiva oblíqua",
    ))

    # 5. P14 — Redução do logo vertical (5 escalas + cotas 176 px x 101 px)
    alturas_v = [210.0, 260.0, 315.0, 380.0, 455.0]
    w_p14, h_p14 = 1520.0, 580.0
    xs_v = [170.0, 405.0, 665.0, 960.0, 1295.0]
    elementos_p14 = []
    for idx, (cx, hh) in enumerate(zip(xs_v, alturas_v)):
        esc = hh / 1805.083
        ww = 1052.798 * esc
        x0 = cx - ww / 2
        y0 = 460.0 - hh
        elementos_p14.append(
            f'<g transform="translate({x0:.1f},{y0:.1f}) scale({esc:.5f})">'
            f'<path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/>'
            f'<path d="{d_word_v}" fill="#3026AD"/></g>'
        )
        if idx == 0:
            elementos_p14.append(_cota_v(x0 - 42, y0, y0 + hh, "176\npx", fs=22))
            elementos_p14.append(_cota_h(x0, x0 + ww, y0 + hh + 38, "101 px", fs=22))
    gerados.append(_salvar_svg(
        "p14-reducao-logo-vertical.svg", w_p14, h_p14, "  " + "\n  ".join(elementos_p14) + "\n",
        "Redução mínima do logo vertical: 101 × 176 px",
    ))

    # 6. P15 — Redução do logo horizontal (4 escalas + cotas 200 px x 89 px)
    larguras_h = [200.0, 270.0, 345.0, 425.0]
    w_p15, h_p15 = 1620.0, 400.0
    xs_h = [110.0, 375.0, 715.0, 1135.0]
    elementos_p15 = []
    for idx, (x0, ww) in enumerate(zip(xs_h, larguras_h)):
        esc = ww / 2013.423
        hh = 921.780 * esc
        y0 = 260.0 - hh
        elementos_p15.append(
            f'<g transform="translate({x0:.1f},{y0:.1f}) scale({esc:.5f})">'
            f'<path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/>'
            f'<path d="{d_word_h}" fill="#3026AD"/></g>'
        )
        if idx == 0:
            elementos_p15.append(_cota_v(x0 - 42, y0, y0 + hh, "89\npx", fs=20))
            elementos_p15.append(_cota_h(x0, x0 + ww, y0 + hh + 38, "200 px", fs=20))
    gerados.append(_salvar_svg(
        "p15-reducao-logo-horizontal.svg", w_p15, h_p15, "  " + "\n  ".join(elementos_p15) + "\n",
        "Redução mínima do logo horizontal: 200 × 89 px",
    ))

    # 7. P16 — Logo em suportes coloridos (6 quadros)
    pares_p16 = [
        ("#FFFFFF", "#3026AD", True),
        ("#3026AD", "#FFFFFF", False),
        ("#FFFFFF", "#E3630D", True),
        ("#E3630D", "#FFFFFF", False),
        ("#FFFFFF", "#000000", True),
        ("#000000", "#FFFFFF", False),
    ]
    cw16, ch16, gap16 = 240.0, 380.0, 28.0
    w_p16 = len(pares_p16) * cw16 + (len(pares_p16) - 1) * gap16 + 16
    esc16 = 0.165
    lw16, lh16 = 1052.798 * esc16, 1805.083 * esc16
    cards_p16 = []
    for idx, (bg, fg, borda) in enumerate(pares_p16):
        x = 8.0 + idx * (cw16 + gap16)
        stroke_attr = ' stroke="#222222" stroke-width="2"' if borda else ""
        lx = x + (cw16 - lw16) / 2
        ly = 8.0 + (ch16 - lh16) / 2
        cards_p16.append(
            f'<rect x="{x:.1f}" y="8" width="{cw16:.1f}" height="{ch16:.1f}" fill="{bg}"{stroke_attr}/>'
            f'<g transform="translate({lx:.1f},{ly:.1f}) scale({esc16:.5f})">'
            f'<path d="{d_icone}" fill="{fg}" fill-rule="evenodd"/>'
            f'<path d="{d_word_v}" fill="{fg}"/></g>'
        )
    gerados.append(_salvar_svg(
        "p16-suportes-coloridos.svg", w_p16, ch16 + 16, "  " + "\n  ".join(cards_p16) + "\n",
        "Logo em suportes coloridos da paleta oficial",
    ))

    # 8. P17 — Logo em imagens coloridas (composição vetorial LGPD-safe)
    cenas_p17 = [
        ("Aplicação sobre cena clara", "#EAEAF4", "#C8C6E6", "#D97B34", "#E3630D", 32, 26),
        ("Aplicação sobre cena escura", "#1D1938", "#352F5C", "#494078", "#FFFFFF", 180, 26),
        ("Aplicação em canto limpo", "#F2F4F8", "#D0D7E8", "#8B95B5", "#3026AD", 315, 26),
    ]
    cw17, ch17, gap17 = 480.0, 290.0, 24.0
    esc17 = 0.068
    c_p17 = []
    for idx, (alt, c1, c2, c3, logo_c, lx_rel, ly_rel) in enumerate(cenas_p17):
        x = idx * (cw17 + gap17)
        c_p17.append(
            f'<g clip-path="url(#cp17_{idx})">'
            f'<rect x="{x:.1f}" y="0" width="{cw17:.1f}" height="{ch17:.1f}" fill="{c1}"/>'
            f'<path d="M{x:.1f} {ch17:.1f} L{x + 210:.1f} 115 L{x + 420:.1f} {ch17:.1f}Z" fill="{c2}"/>'
            f'<circle cx="{x + 115:.1f}" cy="195" r="58" fill="{c3}" fill-opacity="0.65"/>'
            f'<rect x="{x + 250:.1f}" y="155" width="175" height="95" rx="10" fill="{c3}" fill-opacity="0.45"/>'
            f'<g transform="translate({x + lx_rel:.1f},{ly_rel:.1f}) scale({esc17:.5f})">'
            f'<path d="{d_icone}" fill="{logo_c}" fill-rule="evenodd"/>'
            f'<path d="{d_word_h}" fill="{logo_c}"/></g>'
            f'</g>'
        )
    clips_p17 = "".join(
        f'<clipPath id="cp17_{i}"><rect x="{i * (cw17 + gap17):.1f}" y="0" width="{cw17:.1f}" height="{ch17:.1f}"/></clipPath>'
        for i in range(3)
    )
    gerados.append(_salvar_svg(
        "p17-aplicacao-fundos-coloridos.svg", 3 * cw17 + 2 * gap17, ch17,
        f"  <defs>{clips_p17}</defs>\n  " + "\n  ".join(c_p17) + "\n",
        "Logo em fundos e imagens coloridas com zona limpa de contraste",
    ))

    # 9. P18 — 10 exemplos de usos indevidos do logo
    esc18 = 0.22
    w18, h18 = 520.0, 280.0
    cx18, cy18 = 40.0, 38.0
    base_h = f'<path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/><path d="{d_word_h}" fill="#3026AD"/>'

    usos_indevidos = [
        ("p18-01-nao-rotacione.svg", "Não rotacione o logo",
         f'<g transform="translate(260,140) rotate(-14) translate(-220,-101) scale({esc18})">{base_h}</g>'),
        ("p18-02-nao-altere-fonte.svg", "Não altere a fonte",
         f'<g transform="translate({cx18},{cy18}) scale({esc18})"><path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/></g>'
         '<g fill="#3026AD" font-family="Georgia,Times New Roman,serif" font-size="38">'
         '<text x="275" y="102">LAB</text><text x="275" y="150">ESCOLA</text><text x="385" y="198">3D</text></g>'),
        ("p18-03-nao-distorca.svg", "Não distorça o logo",
         f'<g transform="translate({cx18},20) scale({esc18 * 0.72},{esc18 * 1.28})">{base_h}</g>'),
        ("p18-04-nao-aplique-fotos.svg", "Não aplique fotos",
         '<defs><pattern id="fotoPat" width="60" height="40" patternUnits="userSpaceOnUse">'
         '<rect width="60" height="40" fill="#2E6B9E"/><circle cx="16" cy="12" r="7" fill="#F4C152"/>'
         '<path d="M0 40 L25 14 L45 30 L60 18 L60 40Z" fill="#2D7D46"/></pattern></defs>'
         f'<g transform="translate({cx18},{cy18}) scale({esc18})">'
         f'<path d="{d_icone}" fill="url(#fotoPat)" fill-rule="evenodd"/>'
         f'<path d="{d_word_h}" fill="url(#fotoPat)"/></g>'),
        ("p18-05-nao-pinte-icone.svg", "Não pinte o ícone",
         f'<g transform="translate({cx18},{cy18}) scale({esc18})">'
         '<path d="M27 80 L157 27 L278 76 L278 494 L522 595 L646 540 L718 410 L896 277 L1026 76 L1026 641 L522 848 L27 645Z" fill="#E3630D"/>'
         f'<path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/><path d="{d_word_h}" fill="#3026AD"/></g>'),
        ("p18-06-nao-mude-cores.svg", "Não mude as cores",
         f'<g transform="translate({cx18},{cy18}) scale({esc18})">'
         f'<path d="{d_icone}" fill="#B8252A" fill-rule="evenodd"/><path d="{d_word_h}" fill="#B8252A"/></g>'),
        ("p18-07-nao-use-contornos.svg", "Não use contornos",
         f'<g transform="translate({cx18},{cy18}) scale({esc18})">'
         f'<path d="{d_icone}" fill="none" stroke="#222222" stroke-width="18" fill-rule="evenodd"/>'
         f'<path d="{d_word_h}" fill="none" stroke="#222222" stroke-width="14"/></g>'),
        ("p18-08-nao-reflita.svg", "Não reflita o logo",
         f'<g transform="translate(480,{cy18}) scale(-{esc18},{esc18})">{base_h}</g>'),
        ("p18-09-nao-aplique-efeitos.svg", "Não aplique efeitos nem mude opacidade",
         '<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="140%">'
         '<feDropShadow dx="12" dy="12" stdDeviation="8" flood-color="#000000" flood-opacity="0.65"/></filter></defs>'
         f'<g filter="url(#sh)" opacity="0.72" transform="translate({cx18},{cy18}) scale({esc18})">{base_h}</g>'),
        ("p18-10-nao-altere-icone.svg", "Não altere o ícone",
         f'<g transform="translate({cx18},{cy18}) scale({esc18})">'
         f'<path d="{d_icone}" fill="#3026AD" fill-rule="evenodd" transform="skewX(12)"/>'
         f'<path d="{d_word_h}" fill="#3026AD"/></g>'),
    ]
    for fn, tit, corpo in usos_indevidos:
        gerados.append(_salvar_svg(fn, w18, h18, f"  {corpo}\n", tit))

    # 10. P21 — Paleta de cores oficial
    corpo_p21 = (
        '  <rect x="0" y="0" width="320" height="440" fill="#3026AD"/>\n'
        '  <g fill="#FFFFFF" font-family="\'Roboto\',\'Source Sans 3\',Arial,sans-serif" font-size="22">\n'
        '    <text x="28" y="64">R 48</text><text x="28" y="96">G 38</text><text x="28" y="128">B 173</text>\n'
        '    <text x="292" y="64" text-anchor="end">Roxo</text>\n'
        '    <text x="28" y="294">C 92</text><text x="28" y="326">M 91</text><text x="28" y="358">Y 00</text><text x="28" y="390">K 00</text>\n'
        '    <text x="292" y="390" text-anchor="end">#3026AD</text>\n'
        '  </g>\n'
        '  <rect x="344" y="0" width="320" height="440" fill="#E3630D"/>\n'
        '  <g fill="#FFFFFF" font-family="\'Roboto\',\'Source Sans 3\',Arial,sans-serif" font-size="22">\n'
        '    <text x="372" y="64">R 227</text><text x="372" y="96">G 99</text><text x="372" y="128">B 13</text>\n'
        '    <text x="636" y="64" text-anchor="end">Laranja</text>\n'
        '    <text x="372" y="294">C 06</text><text x="372" y="326">M 75</text><text x="372" y="358">Y 100</text><text x="372" y="390">K 00</text>\n'
        '    <text x="636" y="390" text-anchor="end">#E3630D</text>\n'
        '  </g>\n'
        '  <rect x="0" y="464" width="320" height="72" fill="#000000"/>\n'
        '  <text x="160" y="508" text-anchor="middle" fill="#FFFFFF" font-family="\'Roboto\',\'Source Sans 3\',Arial,sans-serif" font-size="22">C 75 M 68 Y 67 K 90</text>\n'
        '  <rect x="344" y="464" width="320" height="72" fill="#FFFFFF" stroke="#222222" stroke-width="2"/>\n'
        '  <text x="636" y="508" text-anchor="end" fill="#150E1F" font-family="\'Roboto\',\'Source Sans 3\',Arial,sans-serif" font-size="22">Branco</text>\n'
    )
    gerados.append(_salvar_svg(
        "p21-paleta-cores.svg", 664, 536, corpo_p21,
        "Paleta de cores oficial Lab Escola 3D (Roxo #3026AD, Laranja #E3630D, Preto CMYK, Branco)",
    ))

    # 11. P22–P26 — Padrões visuais com o ícone oficial (reusa <defs><path id="ic"> para manter SVG leve)
    def _grade_icones(w: int, h: int, cols: int, rows: int, cor: str, bg: str | None = None,
                      x_off: float = 0.0, def_id: str = "ic") -> str:
        dx = w / cols
        dy = h / rows
        esc = min(dx * 0.88 / 1052.798, dy * 0.88 / 875.220)
        itens = []
        for r in range(rows):
            for c in range(-1, cols + 1):
                x = c * dx + (dx - 1052.798 * esc) / 2 + x_off
                y = r * dy + (dy - 875.220 * esc) / 2
                itens.append(f'<use href="#{def_id}" transform="translate({x:.1f},{y:.1f}) scale({esc:.5f})"/>')
        prefixo = f'  <rect width="{w}" height="{h}" fill="{bg}"/>\n' if bg else ""
        defs = f'  <defs><path id="{def_id}" d="{d_icone}" fill="{cor}" fill-rule="evenodd"/></defs>\n'
        return prefixo + defs + "  " + "\n  ".join(itens) + "\n"

    gerados.append(_salvar_svg(
        "p22-padrao-amostra.svg", 800, 640,
        _grade_icones(800, 640, 8, 8, "#444444"),
        "Amostra de padrão visual com repetição do ícone",
    ))
    gerados.append(_salvar_svg(
        "p23-padrao-roxo.svg", 800, 720,
        _grade_icones(800, 720, 8, 8, "#FFFFFF", bg="#3026AD"),
        "Sugestão de padrão visual roxo",
    ))
    gerados.append(_salvar_svg(
        "p23-padrao-laranja.svg", 800, 720,
        _grade_icones(800, 720, 8, 8, "#FFFFFF", bg="#E3630D"),
        "Sugestão de padrão visual laranja",
    ))
    # P24 — Dividido 16:9 (1920x1080)
    dx24, dy24 = 1920 / 14, 1080 / 8
    esc24 = min(dx24 * 0.88 / 1052.798, dy24 * 0.88 / 875.220)
    uses24 = "".join(
        f'<use href="#ic24" transform="translate({c * dx24 + (dx24 - 1052.798 * esc24) / 2 + 18:.1f},{r * dy24 + (dy24 - 875.220 * esc24) / 2:.1f}) scale({esc24:.5f})"/>'
        for r in range(8) for c in range(-1, 15)
    )
    corpo_p24 = (
        f'  <defs><path id="ic24" d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></defs>\n'
        '  <rect x="0" y="0" width="960" height="1080" fill="#3026AD"/>\n'
        '  <rect x="960" y="0" width="960" height="1080" fill="#E3630D"/>\n'
        f'  {uses24}\n'
    )
    gerados.append(_salvar_svg("p24-padrao-dividido-16x9.svg", 1920, 1080, corpo_p24, "Padrão visual dividido roxo e laranja (16:9)"))

    # P25 — Grande roxo 16:9
    corpo_p25 = (
        f'  <g transform="translate(-80,790) scale(0.42)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
        f'  <g transform="translate(1610,-280) scale(0.80)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
        f'  <g transform="translate(1600,820) rotate(-18) scale(0.32)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
        f'  <g transform="translate(1820,690) scale(0.32)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
    )
    gerados.append(_salvar_svg("p25-padrao-grande-roxo-16x9.svg", 1920, 1080, corpo_p25, "Padrão com ícone ampliado sobre roxo (16:9)", fundo="#3026AD"))

    # P26 — Grande laranja 16:9
    corpo_p26 = (
        f'  <g transform="translate(-160,-100) rotate(22) scale(0.34)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
        f'  <g transform="translate(-140,720) scale(0.60)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
        f'  <g transform="translate(1540,-120) rotate(-25) scale(0.75)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
    )
    gerados.append(_salvar_svg("p26-padrao-grande-laranja-16x9.svg", 1920, 1080, corpo_p26, "Padrão com ícone ampliado sobre laranja (16:9)", fundo="#E3630D"))

    # 12. P28–P31 — Aplicações vetoriais LGPD-safe
    camisa_path = (
        "M150 40 L215 40 Q260 95 305 40 L370 40 L480 115 L440 215 L395 190 "
        "L395 520 L125 520 L125 190 L80 215 L40 115 Z"
    )
    corpo_p28 = (
        '  <rect x="0" y="0" width="660" height="600" fill="#F2F2F2"/>\n'
        f'  <g transform="translate(70,35)"><path d="{camisa_path}" fill="#150E1F"/>'
        f'<g transform="translate(278,165) scale(0.068)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/><path d="{d_word_v}" fill="#FFFFFF"/></g></g>\n'
        '  <rect x="700" y="0" width="660" height="600" fill="#F7A74B"/>\n'
        f'  <g transform="translate(770,35)"><path d="{camisa_path}" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="3"/>'
        f'<g transform="translate(278,165) scale(0.068)"><path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/><path d="{d_word_v}" fill="#3026AD"/></g></g>\n'
    )
    gerados.append(_salvar_svg("p28-aplicacao-camisetas.svg", 1360, 600, corpo_p28, "Aplicação do logo vertical em camisetas preta e branca"))

    corpo_p29 = (
        '  <rect width="1200" height="640" fill="#2A2C34"/>\n'
        '  <rect x="0" y="450" width="1200" height="190" fill="#474A54"/>\n'
        '  <path d="M760 220 Q880 220 880 325 Q880 430 760 430" fill="none" stroke="#F4F4F6" stroke-width="34" stroke-linecap="round"/>\n'
        '  <rect x="430" y="135" width="340" height="370" rx="22" fill="#FFFFFF"/>\n'
        '  <ellipse cx="600" cy="135" rx="170" ry="26" fill="#E8E8EE"/>\n'
        '  <ellipse cx="600" cy="135" rx="150" ry="18" fill="#C9CBD4"/>\n'
        f'  <g transform="translate(534,195) scale(0.125)"><path d="{d_icone}" fill="#3026AD" fill-rule="evenodd"/><path d="{d_word_v}" fill="#3026AD"/></g>\n'
    )
    gerados.append(_salvar_svg("p29-aplicacao-caneca.svg", 1200, 640, corpo_p29, "Aplicação do logo vertical em caneca institucional"))

    corpo_p30 = (
        f'  <g transform="translate(90,90) scale(0.24)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/><path d="{d_word_h}" fill="#FFFFFF"/></g>\n'
        f'  <g opacity="0.14" transform="translate(1320,30) scale(0.58)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
        '  <text x="90" y="425" fill="#FFFFFF" font-family="\'Roboto\',\'Source Sans 3\',Arial,sans-serif" font-weight="700" font-size="38">PROGRAMA DE</text>\n'
        '  <text x="90" y="510" fill="#FFFFFF" font-family="\'Roboto\',\'Source Sans 3\',Arial,sans-serif" font-weight="700" font-size="84">VOLUNTARIADO2024</text>\n'
    )
    gerados.append(_salvar_svg("p30-banner-institucional.svg", 1920, 600, corpo_p30, "Aplicação do logo em banner institucional", fundo="#3026AD"))

    corpo_p31 = (
        f'  <g opacity="0.12" transform="translate(-80,-60) scale(1.1)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
        f'  <g opacity="0.12" transform="translate(1100,20) scale(0.95)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/></g>\n'
        f'  <g transform="translate(768,265) scale(0.19)"><path d="{d_icone}" fill="#FFFFFF" fill-rule="evenodd"/><path d="{d_word_h}" fill="#FFFFFF"/></g>\n'
        '  <text x="960" y="560" text-anchor="middle" fill="#FFFFFF" font-family="\'Roboto\',\'Source Sans 3\',Arial,sans-serif" '
        'font-weight="700" font-size="36">DESIGN PARA A INOVAÇÃO SOCIAL NA EDUCAÇÃO PÚBLICA</text>\n'
    )
    gerados.append(_salvar_svg("p31-banner-inovacao.svg", 1920, 740, corpo_p31, "Aplicação do logo em banner de inovação social", fundo="#3026AD"))

    return gerados


if __name__ == "__main__":
    arqs = gerar_todos()
    print(f"Gerados {len(arqs)} SVGs em {OUT_DIR}")
