"""Gera o Catálogo (catalogo/index.html) e a home (index.html) da Fase 1.

Uso: py -I -X utf8 _ferramentas/gerar_paginas.py
Os números da faixa de volume são texto à mão (desenho §6), contados no inventário.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gerar_produtos import LOGO, PRODUTOS, estilo, faixa_alfa

E = html.escape
POR_SLUG = {p["slug"]: p for p in PRODUTOS}

# (slug ou None, título, tipo, ano, resumo, destino, autoria externa)
CARDS = [
    ("investigadoras-do-conhecimento", "jogo", "2026"),
    ("expedicao-sonora", "jogo", "2026"),
    ("oficina-de-gamificacao", "formacao", "2026"),
    ("memorias-da-mare", "jogo", "2025"),
    ("curso-maker-de-ferias-2025", "formacao", "2025"),
    ("manual-maker", "manual", "2025"),
    ("antropolojogo", "jogo", "2022"),
    {"titulo": "Catálogo de Atividades", "tipo": "atividade", "ano": "2025",
     "resumo": "Roteiros de aula maker alinhados à BNCC e à BNCC Computação, com filtros por ano e componente.",
     "href": "https://labescola3d.rio.br/fichas/", "selo": "Atividades"},
    {"titulo": "Através do Espelho", "tipo": "jogo", "ano": "2025", "autoria": "Raiane",
     "resumo": "Jogo de Física da Raiane, com mecânicas de engajamento para a sala de aula.",
     "href": "https://ludopedia.com.br/jogo/atraves-do-espelho", "selo": "Jogo · na Ludopédia"},
]
NOMES_TIPO = {"jogo": "Jogo", "formacao": "Formação", "manual": "Manual", "atividade": "Atividades"}
NUMEROS = [("5 jogos", "para baixar e jogar"), ("2 formações", "para professores"),
           ("9 atividades", "no catálogo"), ("6 manuais", "de cultura maker")]
DESTAQUES = ["investigadoras-do-conhecimento", "expedicao-sonora", "oficina-de-gamificacao", "antropolojogo"]

CSS = """
.faixa { position: relative; }
.numeros { display: grid; }
.numero b { display: block; font-family: var(--titulo); font-weight: 900; color: var(--laranja); text-transform: uppercase; }
.numero span { font-size: 14px; line-height: 20px; }
.filtros { display: flex; flex-wrap: wrap; gap: 10px; }
.filtros button { font-family: var(--corpo); font-size: 13px; letter-spacing: 1px; text-transform: uppercase; padding: 10px 16px;
                  background: var(--fundo); color: var(--roxo); border: 1px solid var(--roxo); cursor: pointer; }
.filtros button.ativo { background: var(--roxo); color: var(--fundo); }
.cards { display: grid; }
.card.externo { border-style: dashed; }
.card .capa { display: block; padding-top: 70px; text-align: center; color: var(--roxo); font-size: 13px; }
.passos-home { display: grid; }
.passo b { display: block; font-family: var(--titulo); font-size: 28px; color: var(--roxo); text-transform: uppercase; }
.tela--pc .faixa { padding: 100px 160px 40px; }
.tela--pc .faixa p { font-size: 20px; line-height: 30px; max-width: 760px; margin: 16px 0 28px; }
.tela--pc .numeros { grid-template-columns: repeat(4, 1fr); gap: 24px; padding: 0 160px; }
.tela--pc .numero b { font-size: 48px; line-height: 48px; }
.tela--pc .bloco { padding: 64px 160px 0; }
.tela--pc .bloco h2 { margin-bottom: 24px; }
.tela--pc .filtros { margin-bottom: 28px; }
.tela--pc .cards { grid-template-columns: repeat(3, 1fr); gap: 28px; }
.tela--pc .cards.quatro { grid-template-columns: repeat(4, 1fr); gap: 24px; }
.tela--pc .passos-home { grid-template-columns: repeat(3, 1fr); gap: 40px; }
.tela--pc .rodape { margin-top: 80px; padding: 32px 160px 48px; display: flex; justify-content: space-between; }
.tela--cel .faixa { padding: 60px 20px 28px; }
.tela--cel .faixa p { font-size: 17px; line-height: 26px; margin: 12px 0 22px; }
.tela--cel .numeros { grid-template-columns: 1fr 1fr; gap: 16px; padding: 0 20px; }
.tela--cel .numero b { font-size: 34px; line-height: 36px; }
.tela--cel .bloco { padding: 44px 20px 0; }
.tela--cel .bloco h2 { margin-bottom: 16px; }
.tela--cel .filtros { margin-bottom: 20px; }
.tela--cel .cards, .tela--cel .cards.quatro { grid-template-columns: 1fr; gap: 16px; }
.tela--cel .passos-home { grid-template-columns: 1fr; gap: 24px; }
.tela--cel .rodape { margin-top: 56px; padding: 28px 20px 40px; }
.tela--cel .rodape .redes { margin-top: 16px; }
"""

FILTRO_JS = """<script>
document.querySelectorAll('.filtros').forEach(function (f) {
  f.addEventListener('click', function (ev) {
    var b = ev.target.closest('button'); if (!b) return;
    f.querySelectorAll('button').forEach(function (x) { x.classList.toggle('ativo', x === b); });
    var tela = f.closest('.tela'), v = b.dataset.filtro;
    tela.querySelectorAll('.card').forEach(function (c) {
      c.style.display = (v === 'todos' || c.dataset.tipo === v || c.dataset.ano === v) ? '' : 'none';
    });
  });
});
</script>"""


def _dados_card(c):
    if isinstance(c, tuple):
        slug, tipo, ano = c
        p = POR_SLUG[slug]
        return {"titulo": p["titulo"], "tipo": tipo, "ano": ano, "resumo": p["frase"],
                "href": f"{slug}/", "selo": p["selo"]}
    return c


def card(c, prefixo=""):
    d = _dados_card(c)
    externo = "autoria" in d
    href = d["href"] if d["href"].startswith("http") else prefixo + d["href"]
    classe = "card externo" if externo else "card"
    autoria = f' data-autoria="{E(d["autoria"])}"' if externo else ""
    credito = f'<p class="creditos">Autoria: {E(d["autoria"])}</p>' if externo else ""
    return (f'<a class="{classe}" href="{E(href)}" data-tipo="{d["tipo"]}" data-ano="{d["ano"]}"{autoria}>'
            f'<span class="capa reservada">Área reservada · imagem do material</span>'
            f'<div class="corpo"><span class="tipo">{E(d["selo"])}</span><h3>{E(d["titulo"])}</h3>'
            f'<p>{E(d["resumo"])}</p>{credito}</div></a>')


def _topo(tela, raiz, ativo):
    if tela == "pc":
        a = lambda nome, href: f'<a class="ativo" href="{href}">{nome}</a>' if nome == ativo else f'<a href="{href}">{nome}</a>'
        nav = (f'<nav class="menu">{a("Catálogo", raiz + "catalogo/")}{a("Sobre o Lab", raiz)}{a("Contato", raiz)}'
               f'<img class="icone" src="{raiz}_base/icones/lupa.svg" alt="Buscar no catálogo"></nav>')
    else:
        nav = f'<img class="icone" src="{raiz}_base/icones/menu.svg" alt="Abrir o menu">'
    return (f'<header class="topo"><a href="{raiz or "./"}"><img class="logo" src="{LOGO}" alt="Lab Escola 3D"></a>{nav}</header>'
            '<div class="onda"></div>')


def _rodape(raiz):
    redes = "".join(f'<img src="{raiz}_base/icones/{r}.svg" alt="{n}">' for r, n in
                    [("instagram", "Instagram"), ("facebook", "Facebook"), ("youtube", "YouTube"), ("linkedin", "LinkedIn")])
    return (f'<footer class="rodape"><span>Lab Escola 3D · projeto de extensão da UFRJ · protótipo de tela</span>'
            f'<div class="redes">{redes}</div></footer>')


def _numeros():
    return '<div class="numeros">' + "".join(
        f'<div class="numero"><b>{E(b)}</b><span>{E(s)}</span></div>' for b, s in NUMEROS) + "</div>"


def _doc(titulo, raiz, telas, script=""):
    return (f'<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex">\n'
            f'<title>{E(titulo)}</title>\n{estilo("site.css", extra=CSS)}\n</head>\n<body>\n' + faixa_alfa(raiz) + "\n" + "\n\n".join(telas) + f"\n{script}\n</body>\n</html>\n")


def _escrever(arq, texto):
    os.makedirs(os.path.dirname(arq), exist_ok=True)
    with open(arq, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    return arq


def gerar_catalogo(raiz: str) -> str:
    telas = []
    for tela, rot in (("pc", "computador (1440)"), ("cel", "celular (375)")):
        filtros = "".join(f'<button type="button" data-filtro="{v}"{" class=\"ativo\"" if v == "todos" else ""}>{n}</button>'
                          for v, n in [("todos", "Tudo"), ("jogo", "Jogos"), ("formacao", "Formações"),
                                       ("atividade", "Atividades"), ("manual", "Manuais"), ("2026", "2026"),
                                       ("2025", "2025"), ("2022", "2022")])
        telas.append(
            f'<section class="tela tela--{tela}" data-document-role="page" data-label="Catálogo · {rot}">'
            + _topo(tela, "../", "Catálogo")
            + '<div class="faixa"><span class="selo">Catálogo aberto</span><h1 style="margin-top:16px">Materiais para usar na sua aula</h1>'
              '<p>Jogos, formações, atividades e manuais criados pelo Lab Escola 3D com escolas públicas do Rio. Tudo gratuito, para baixar e adaptar.</p></div>'
            + _numeros()
            + f'<div class="bloco"><div class="filtros">{filtros}</div><div class="cards">'
            + "".join(card(c) for c in CARDS) + "</div></div>"
            + _rodape("../") + "</section>")
    return _escrever(os.path.join(raiz, "catalogo", "index.html"),
                     _doc("Catálogo · Lab Escola 3D (protótipo)", "../", telas, FILTRO_JS))


def gerar_home(raiz: str) -> str:
    destaques = [c for c in CARDS if isinstance(c, tuple) and c[0] in DESTAQUES]
    destaques.sort(key=lambda c: DESTAQUES.index(c[0]))
    telas = []
    for tela, rot in (("pc", "computador (1440)"), ("cel", "celular (375)")):
        telas.append(
            f'<section class="tela tela--{tela}" data-document-role="page" data-label="Home · {rot}">'
            + _topo(tela, "", "")
            + '<div class="faixa"><span class="selo">Lab Escola 3D · extensão da UFRJ</span>'
              '<h1 style="margin-top:16px">Materiais para usar na sua aula</h1>'
              '<p>Jogos, formações e manuais criados com professoras e professores da rede pública do Rio. Gratuitos, para baixar, imprimir e adaptar à sua turma.</p>'
              '<a class="botao botao--grande" href="catalogo/">Ver o catálogo</a></div>'
            + _numeros()
            + '<div class="bloco"><h2>Em destaque</h2><div class="cards quatro">'
            + "".join(card(c, "catalogo/") for c in destaques) + "</div></div>"
            + '<div class="bloco"><h2>O que é o Lab Escola 3D</h2>'
              '<p>Um projeto de extensão da UFRJ que leva a cultura maker, o design e as tecnologias digitais para a escola pública. '
              'Trabalhamos junto com o professor, a partir das necessidades reais da sala de aula, e devolvemos tudo o que criamos como material aberto.</p></div>'
            + '<div class="bloco"><h2>Como fazemos</h2><div class="passos-home">'
              '<div class="passo"><b>1 · Visita</b><p>Vamos à escola, ouvimos os professores e conhecemos o colaboratório.</p></div>'
              '<div class="passo"><b>2 · Produto</b><p>Criamos juntos jogos, oficinas e roteiros, testados com as turmas.</p></div>'
              '<div class="passo"><b>3 · Material aberto</b><p>Publicamos tudo aqui, para qualquer professora baixar e adaptar.</p></div></div></div>'
            + _rodape("") + "</section>")
    return _escrever(os.path.join(raiz, "index.html"), _doc("Lab Escola 3D (protótipo)", "", telas))


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..")
    print(gerar_catalogo(base))
    print(gerar_home(base))
