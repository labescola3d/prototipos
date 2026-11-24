"""Gera /manuais: a coleção Manual Maker como página própria.

Uso: py -I -X utf8 _ferramentas/gerar_manuais.py
Cada volume é um card com capa, o que a professora aprende, páginas, tamanho e licença.
Dado que a fonte não traz sai como [a confirmar]; nada é inventado.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gerar_paginas import _doc, _escrever, _rodape, _topo  # noqa: E402
from gerar_produtos import LICENCA, SITE  # noqa: E402

E = html.escape
A_CONFIRMAR = "[a confirmar]"

VOLUMES = [
    {"titulo": "Manual completo", "aprende": "Os cinco volumes num arquivo só: metodologias ativas e tecnologias da cultura maker para inovar o ensino.",
     "paginas": "67 páginas", "tamanho": "PDF · 10 MB", "href": SITE + "2025/06/Manuais-Educacionais-Completo.pdf",
     "capa": "_base/capas/manual-maker.jpg"},
    {"titulo": "Cultura maker", "aprende": "Como o “faça você mesmo” muda a aprendizagem pela criatividade e pela colaboração.",
     "paginas": A_CONFIRMAR, "tamanho": "PDF · 1 MB", "href": SITE + "2025/05/Manuais-Educacionais-Cultura-Maker.pdf", "capa": None},
    {"titulo": "Arduino", "aprende": "Projetos interativos de eletrônica e programação na escola.",
     "paginas": A_CONFIRMAR, "tamanho": "PDF · 2 MB", "href": SITE + "2025/05/Manuais-Educacionais-Arduino.pdf", "capa": None},
    {"titulo": "Micro:bit", "aprende": "Programação, sensores e lógica de forma prática.",
     "paginas": A_CONFIRMAR, "tamanho": "PDF · 2 MB", "href": SITE + "2025/05/Manuais-Educacionais-Microbit.pdf", "capa": None},
    {"titulo": "Impressão 3D", "aprende": "Da ideia ao objeto, com modelagem e impressão.",
     "paginas": A_CONFIRMAR, "tamanho": "PDF · 3 MB", "href": SITE + "2025/05/Manuais-Educacionais-Impressao-3D.pdf", "capa": None},
    {"titulo": "Horta escolar", "aprende": "Sustentabilidade, saúde e aprendizagem prática.",
     "paginas": A_CONFIRMAR, "tamanho": "PDF · 3 MB", "href": SITE + "2025/05/Manuais-Educacionais-Hortas-Escolares.pdf", "capa": None},
]

CSS_EXTRA = """
.volumes { display: grid; }
.volume { background: #fff; border: 1px solid var(--laranja); border-radius: 20px; overflow: hidden; display: flex; flex-direction: column; }
.volume img, .volume .capa-vol { display: block; width: 100%; height: 200px; object-fit: cover; object-position: top; background: var(--roxo-claro); }
.volume .capa-vol { padding-top: 80px; box-sizing: border-box; text-align: center; color: var(--roxo); font-size: 13px; }
.volume .corpo { padding: 20px 24px 24px; display: flex; flex-direction: column; gap: 8px; flex: 1; }
.volume .meta { font-size: 13px; color: var(--cinza); }
.volume .botao { align-self: flex-start; margin-top: auto; }
.tela--pc .volumes { grid-template-columns: repeat(3, 1fr); gap: 28px; }
.tela--cel .volumes { grid-template-columns: 1fr; gap: 16px; }
"""


def _volume(v: dict, raiz: str) -> str:
    capa = (f'<img src="{E(raiz + v["capa"])}" alt="Capa dos Manuais Educacionais do Lab Escola 3D" loading="lazy">'
            if v["capa"] else '<span class="capa-vol reservada">Área reservada · capa do volume</span>')
    return (f'<div class="volume">{capa}<div class="corpo"><h3>{E(v["titulo"])}</h3><p>{E(v["aprende"])}</p>'
            f'<p class="meta">{E(v["paginas"])} · {E(v["tamanho"])}</p>'
            f'<a class="botao" href="{E(v["href"])}">Baixar</a></div></div>')


def render_manuais(raiz_rel: str = "../", modo_site: bool = True, com_faixa: bool = True) -> str:
    r = raiz_rel
    telas = []
    for tela, rot in (("pc", "computador (1440)"), ("cel", "celular (375)")):
        telas.append(
            f'<section class="tela tela--{tela}" data-document-role="page" data-label="Manuais · {rot}">'
            + _topo(tela, r, "Catálogo")
            + '<div class="faixa"><span class="selo">Coleção · 2025</span><h1 style="margin-top:16px">Manual Maker</h1>'
              '<p>Guias gratuitos para levar a cultura maker, o Arduino, o Micro:bit, a impressão 3D e a horta escolar para a sala de aula. '
              'Cada volume pode ser usado sozinho.</p></div>'
            + '<div class="bloco"><div class="volumes">' + "".join(_volume(v, r) for v in VOLUMES) + "</div>"
            + f'<p class="meta" style="margin-top:24px">{E(LICENCA)} <a href="{r}licenca/" style="color:inherit">Como usar →</a></p></div>'
            + '<div class="bloco"><h2>De onde veio</h2><p>Produzido pelo Lab Escola 3D a partir das formações nos GETs. '
              'Créditos: equipe do projeto de extensão Lab Escola 3D (UFRJ/COPPE), 2025.</p></div>'
            + _rodape(r) + "</section>")
    return _doc("Manual Maker · Lab Escola 3D (protótipo)", r, telas, modo_site=modo_site,
                com_faixa=com_faixa).replace("</style>", CSS_EXTRA + "</style>", 1)


def gerar_manuais(raiz: str) -> str:
    return _escrever(os.path.join(raiz, "manuais", "index.html"), render_manuais())


if __name__ == "__main__":
    print(gerar_manuais(os.path.join(os.path.dirname(__file__), "..")))
