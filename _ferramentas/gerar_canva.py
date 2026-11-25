"""Gera o espelho estático /canva/ para importação direta no Canva do LE3D.

Uso: py -I -X utf8 _ferramentas/gerar_canva.py
Cada tela em canva/<slug>/index.html traz as duas resoluções (1440 px e 375 px)
visíveis, sem @media escondendo telas, sem <script> e sem faixa alfa.
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gerar_identidade import gerar_canva_manual  # noqa: E402
from gerar_institucionais import CONTRIBUIR, CSS, CSS_OBRAS, EM_OBRAS, LICENCA, RODAPE  # noqa: E402
from gerar_manuais import render_manuais  # noqa: E402
from gerar_paginas import _escrever, render_catalogo, render_home  # noqa: E402
from gerar_produtos import PRODUTOS, cabecalho_simples, pagina  # noqa: E402

E = html.escape

TELAS_CANVA = [
    "home",
    "catalogo",
    "investigadoras-do-conhecimento",
    "manuais",
    "licenca",
    "contribuir",
    "em-obras",
]

CSS_CANVA_INST = """
body { background: #d9d9d9; }
.tela { background: #F2F2F2; margin: 40px auto; position: relative; overflow: hidden; }
.tela--pc { width: 1440px; }
.tela--cel { width: 375px; }
.tela--cel .tres, .tela--cel .dois { grid-template-columns: 1fr; }
.tela--cel h1 { font-size: 36px; }
.tela--cel .m { width: 155px; }
"""

CSS_INDICE = """
body { margin: 0; background: #F2F2F2; color: #150E1F; font: 16px/1.6 "Roboto", system-ui, sans-serif; }
main { max-width: 920px; margin: 0 auto; padding: 36px 20px 64px; }
h1 { font-family: "Big Shoulders Display", sans-serif; font-weight: 900; font-size: 48px; color: #3026AD; text-transform: uppercase; margin: 0 0 10px; }
p { margin: 0 0 20px; }
.lista { display: grid; gap: 14px; }
.item { background: #fff; border: 1px solid #E3630D; border-radius: 16px; padding: 18px 22px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between; }
.item b { font-family: "Big Shoulders Display", sans-serif; font-size: 26px; color: #3026AD; text-transform: uppercase; display: block; }
.item span { font-size: 14px; color: #6B6B6B; }
.acoes { display: flex; gap: 10px; flex-wrap: wrap; }
.btn { display: inline-block; background: #3026AD; color: #fff; text-decoration: none; font-size: 12px; letter-spacing: 1.5px; text-transform: uppercase; padding: 11px 18px; }
.btn--claro { background: #F2F2F2; color: #3026AD; border: 1px solid #3026AD; }
"""


def _ajustar_caminhos_institucional(trecho: str, pasta: str) -> str:
    """Ajusta caminhos relativos de uma página institucional para o nível canva/<slug>/."""
    trecho = trecho.replace('href="../', 'href="../../')
    if pasta == "em-obras":
        trecho = trecho.replace('src="tom.jpg"', 'src="../../em-obras/tom.jpg"')
        trecho = trecho.replace('src="vit.jpg"', 'src="../../em-obras/vit.jpg"')
    return trecho


def render_institucional(titulo: str, corpo: str, ativo: str, pasta: str) -> str:
    """Envolve uma tela institucional em páginas 1440 px e 375 px sem @media."""
    css_sem_media = re.sub(r"@media\([^)]*\)\{[^}]*(?:\{[^}]*\}[^}]*)*\}\s*", "", CSS)
    corpo_aj = _ajustar_caminhos_institucional(corpo, pasta)
    rodape_aj = _ajustar_caminhos_institucional(RODAPE, pasta)
    telas = []
    for cls, rot in (("pc", "computador (1440)"), ("cel", "celular (375)")):
        telas.append(
            f'<section class="tela tela--{cls}" data-document-role="page" data-label="{E(titulo)} · {rot}">\n'
            f'{cabecalho_simples("../../", ativo)}\n'
            f'<main>\n{corpo_aj}\n{rodape_aj}\n</main>\n</section>'
        )
    return (
        '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex">\n'
        f'<title>{E(titulo)} · Lab Escola 3D (Canva)</title>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700'
        '&family=Source+Sans+3:wght@400;700&display=swap">\n'
        f'<style>\n{css_sem_media}{CSS_OBRAS}{CSS_CANVA_INST}</style>\n</head>\n<body>\n'
        + "\n\n".join(telas)
        + "\n</body>\n</html>\n"
    )


def _render_indice() -> str:
    itens_meta = [
        ("home", "Home", "Tela inicial com destaques e faixa de números", "../"),
        ("catalogo", "Catálogo", "15 materiais com filtros e busca abertos", "../catalogo/"),
        ("investigadoras-do-conhecimento", "Produto (modelo)", "Página de material — Investigadoras do conhecimento", "../catalogo/investigadoras-do-conhecimento/"),
        ("manuais", "Manuais", "Coleção Manual Maker em 6 volumes", "../manuais/"),
        ("licenca", "Licença e como usar", "Resumo da CC BY-NC-SA 4.0 e uso opcional no Canva", "../licenca/"),
        ("contribuir", "Como contribuir", "Envio de adaptações e sugestões", "../contribuir/"),
        ("em-obras", "Em obras", "Tela de construção com Tom e Vit", "../em-obras/"),
    ]
    cartoes = "".join(
        f'<div class="item"><div><b>{E(nome)}</b><span>{E(desc)}</span></div>'
        f'<div class="acoes"><a class="btn" href="{E(slug)}/">Abrir espelho Canva</a>'
        f'<a class="btn btn--claro" href="{E(site)}">Ver no site</a></div></div>'
        for slug, nome, desc, site in itens_meta
    )
    cartoes += (
        '<div class="item"><div><b>Manual da Marca (16:9 · 33 slides)</b>'
        '<span>Espelho 1920 × 1080 do Manual da Marca 2024 (sem fotos de pessoas)</span></div>'
        '<div class="acoes"><a class="btn" href="manual-da-marca/">Abrir espelho Canva</a>'
        '<a class="btn btn--claro" href="../identidade/">Ver no site</a></div></div>'
    )
    return (
        '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex">\n'
        '<title>Espelho para o Canva · Lab Escola 3D</title>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900'
        '&family=Roboto:wght@400;500;700&display=swap">\n'
        f'<style>{CSS_INDICE}</style>\n</head>\n<body>\n<main>\n'
        '<h1>Espelho estático para o Canva</h1>\n'
        '<p>Versão sem JavaScript, sem media queries e sem faixa alfa, com computador (1440 px) e celular (375 px) visíveis para importação no Canva do Lab Escola 3D.</p>\n'
        f'<div class="lista">{cartoes}</div>\n</main>\n</body>\n</html>\n'
    )


def gerar_todos_canva(raiz: str) -> list[str]:
    """Gera o índice canva/index.html e as 7 telas espelho em canva/<slug>/index.html."""
    inv = next(p for p in PRODUTOS if p["slug"] == "investigadoras-do-conhecimento")
    paginas = {
        "home": render_home(raiz_rel="../../", prefixo_catalogo="../../catalogo/", modo_site=False, com_faixa=False),
        "catalogo": render_catalogo(raiz_rel="../../", prefixo_card="../../catalogo/", catalogo_href="../../catalogo/",
                                    modo_site=False, com_faixa=False, com_script=False),
        "investigadoras-do-conhecimento": pagina(inv, modo_site=False, com_faixa=False,
                                                 prefixo_local="../../catalogo/investigadoras-do-conhecimento/", raiz="../../"),
        "manuais": render_manuais(raiz_rel="../../", modo_site=False, com_faixa=False),
        "licenca": render_institucional("Licença e como usar", LICENCA, "Como usar", "licenca"),
        "contribuir": render_institucional("Como contribuir", CONTRIBUIR, "Contribuir", "contribuir"),
        "em-obras": render_institucional("Em obras", EM_OBRAS, "", "em-obras"),
    }
    saidas = [_escrever(os.path.join(raiz, "canva", "index.html"), _render_indice())]
    for slug in TELAS_CANVA:
        saidas.append(_escrever(os.path.join(raiz, "canva", slug, "index.html"), paginas[slug]))
    saidas.append(gerar_canva_manual(raiz))
    return saidas


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..")
    for arq in gerar_todos_canva(base):
        print(arq)
