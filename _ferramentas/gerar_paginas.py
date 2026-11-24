"""Gera o Catálogo (catalogo/index.html) e a home (index.html).

Uso: py -I -X utf8 _ferramentas/gerar_paginas.py
Os cards, as tags e os números saem de _dados/catalogo.json (módulo catalogo).
"""
import html
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogo import A_CONFIRMAR, COMPLEXIDADES, DISCIPLINAS, ETAPAS, TEMPOS, TIPOS, carregar  # noqa: E402
from gerar_produtos import LOGO, estilo, faixa_alfa, menu  # noqa: E402

E = html.escape
DESTAQUES = ["investigadoras-do-conhecimento", "expedicao-sonora", "oficina-de-gamificacao", "antropolojogo"]
RAIZ_SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Grupos do filtro: (nome do grupo, atributo data-* do card, rótulo, {valor: rótulo do botão})
GRUPOS = [("tipo", "tipo", "Tipo", TIPOS),
          ("disciplina", "disciplinas", "Disciplina", {d: d for d in DISCIPLINAS}),
          ("tempo", "tempo", "Tempo de aula", TEMPOS),
          ("complexidade", "complexidade", "Complexidade", {k: v.split(":")[0] for k, v in COMPLEXIDADES.items()}),
          ("etapa", "etapas", "Ano", ETAPAS)]

CSS = """
.faixa { position: relative; }
.numeros { display: grid; }
.numero b { display: block; font-family: var(--titulo); font-weight: 900; color: var(--laranja); text-transform: uppercase; }
.numero span { font-size: 14px; line-height: 20px; }
.busca { font: inherit; font-size: 16px; padding: 12px 18px; border: 1px solid var(--roxo); border-radius: 24px;
         width: 100%; max-width: 520px; box-sizing: border-box; margin-bottom: 18px; background: #fff; color: var(--texto); }
.filtros { display: flex; flex-direction: column; gap: 14px; }
.grupo { display: flex; flex-wrap: wrap; gap: 8px; border: 0; padding: 0; margin: 0; min-width: 0; }
.grupo legend { font-size: 12px; letter-spacing: 2px; text-transform: uppercase; color: var(--cinza); padding: 0; margin-bottom: 6px; }
.filtros button { font-family: var(--corpo); font-size: 13px; padding: 8px 14px; border-radius: 18px;
                  background: var(--fundo); color: var(--roxo); border: 1px solid var(--roxo); cursor: pointer; }
.filtros button[aria-pressed="true"] { background: var(--roxo); color: var(--fundo); }
.filtrar summary { cursor: pointer; font-weight: 700; color: var(--roxo); padding: 6px 0 12px; }
.vazio p { margin-bottom: 14px; }
.cards { display: grid; }
.card[hidden] { display: none; }
.card.externo { border-style: dashed; }
.card.em-breve .tipo::after { content: " · em preparação"; }
.card .capa { display: block; padding-top: 70px; text-align: center; color: var(--roxo); font-size: 13px; }
.card .tags-card { font-size: 12px; line-height: 18px; color: var(--cinza); margin-top: 8px; }
.passos-home { display: grid; }
.passo b { display: block; font-family: var(--titulo); font-size: 28px; color: var(--roxo); text-transform: uppercase; }
.tela--pc .faixa { padding: 100px 160px 40px; }
.tela--pc .faixa p { font-size: 20px; line-height: 30px; max-width: 760px; margin: 16px 0 28px; }
.tela--pc .numeros { grid-template-columns: repeat(4, 1fr); gap: 24px; padding: 0 160px; }
.tela--pc .numero b { font-size: 48px; line-height: 48px; }
.tela--pc .bloco { padding: 64px 160px 0; }
.tela--pc .bloco h2 { margin-bottom: 24px; }
.tela--pc .filtros { margin-bottom: 32px; }
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

# Dentro de um grupo vale qualquer valor marcado (OU); entre grupos, valem todos (E); a busca soma (E).
FILTRO_JS = r"""<script>
(function () {
  function norm(s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
  document.querySelectorAll('.tela').forEach(function (tela) {
    var caixa = tela.querySelector('.filtros'); if (!caixa) return;
    var busca = tela.querySelector('.busca'), vazio = tela.querySelector('.vazio');
    function aplicar() {
      var ativos = {};
      caixa.querySelectorAll('button[aria-pressed="true"]').forEach(function (b) {
        (ativos[b.dataset.campo] = ativos[b.dataset.campo] || []).push(b.dataset.valor);
      });
      var termos = busca ? norm(busca.value.trim()).split(/\s+/).filter(Boolean) : [], vistos = 0;
      tela.querySelectorAll('.cards .card').forEach(function (c) {
        var ok = Object.keys(ativos).every(function (campo) {
          var tem = (c.dataset[campo] || '').split('|');
          return ativos[campo].some(function (v) { return tem.indexOf(v) >= 0; });
        }) && termos.every(function (p) { return c.dataset.busca.indexOf(p) >= 0; });
        c.hidden = !ok; if (ok) vistos++;
      });
      if (vazio) vazio.hidden = vistos > 0;
    }
    caixa.addEventListener('click', function (ev) {
      var b = ev.target.closest('button[data-campo]'); if (!b) return;
      b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      aplicar();
    });
    if (busca) busca.addEventListener('input', aplicar);
    var limpar = tela.querySelector('.limpar');
    if (limpar) limpar.addEventListener('click', function () {
      caixa.querySelectorAll('button[data-campo]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      if (busca) busca.value = '';
      aplicar();
    });
  });
})();
</script>"""


def normalizar(texto: str) -> str:
    """Minúsculas e sem acento: a busca acha "matematica" em "Matemática"."""
    return "".join(ch for ch in unicodedata.normalize("NFD", texto) if not unicodedata.combining(ch)).lower()


def _valores(v) -> list:
    if v is None or v == A_CONFIRMAR:
        return []
    return v if isinstance(v, list) else [v]


def numeros(cards: list[dict]) -> list[tuple[str, str]]:
    def n(tipo):
        return sum(1 for c in cards if c["tipo"] == tipo)
    return [(f"{n('jogo')} jogos", "para baixar e jogar"),
            (f"{n('oficina')} oficinas", "e formações para professores"),
            (f"{n('professor')} materiais", "para preparar a aula"),
            (f"{len(cards)} materiais", "no catálogo")]


def _pagina_existe(c: dict) -> bool:
    """Card de página que ainda não foi gerada vira card sem link (em preparação)."""
    h = c["href"]
    if h.startswith("http"):
        return True
    return os.path.isfile(os.path.normpath(os.path.join(RAIZ_SITE, "catalogo", h, "index.html")))


def card(c: dict, prefixo: str = "") -> str:
    t = c["tags"]
    attrs = {"slug": c["slug"], "tipo": c["tipo"]}
    for _g, campo, _rot, _vals in GRUPOS[1:]:
        attrs[campo] = "|".join(_valores(t[campo]))
    rotulos = ([TIPOS[c["tipo"]]] + _valores(t["disciplinas"]) + [TEMPOS[x] for x in _valores(t["tempo"])]
               + [COMPLEXIDADES[x] for x in _valores(t["complexidade"])] + [ETAPAS[x] for x in _valores(t["etapas"])]
               + _valores(t["anos"]))
    attrs["busca"] = normalizar(" ".join([c["titulo"], c["frase"]] + rotulos))
    dados = "".join(f' data-{k}="{E(v)}"' for k, v in attrs.items())
    autoria = c.get("autoria_externa")
    if autoria:
        dados += f' data-autoria="{E(autoria)}"'
    resumo = " · ".join(x for x in [", ".join(_valores(t["disciplinas"])), ", ".join(_valores(t["anos"]))] if x)
    miolo = ('<span class="capa reservada">Área reservada · imagem do material</span>'
             f'<div class="corpo"><span class="tipo">{E(c["selo"])}</span><h3>{E(c["titulo"])}</h3>'
             f'<p>{E(c["frase"])}</p>'
             + (f'<p class="tags-card">{E(resumo)}</p>' if resumo else "")
             + (f'<p class="creditos">Autoria: {E(autoria)}</p>' if autoria else "")
             + "</div>")
    if not _pagina_existe(c):
        return f'<div class="card em-breve"{dados}>{miolo}</div>'
    href = c["href"] if c["href"].startswith("http") else prefixo + c["href"]
    classe = "card externo" if autoria else "card"
    return f'<a class="{classe}" href="{E(href)}"{dados}>{miolo}</a>'


def _filtros(tela: str) -> str:
    grupos = "".join(
        f'<fieldset class="grupo" data-grupo="{g}"><legend>{E(rot)}</legend>'
        + "".join(f'<button type="button" data-campo="{campo}" data-valor="{E(v)}" aria-pressed="false">{E(n)}</button>'
                  for v, n in valores.items())
        + "</fieldset>"
        for g, campo, rot, valores in GRUPOS)
    caixa = f'<div class="filtros">{grupos}</div>'
    busca = '<input type="search" class="busca" aria-label="Buscar no catálogo" placeholder="Buscar: costura, matemática, 6º ano…">'
    if tela == "cel":
        return busca + f'<details class="filtrar"><summary>Filtrar</summary>{caixa}</details>'
    return busca + caixa


def _topo(tela, raiz, ativo):
    nav = menu(raiz, ativo, cel=(tela != "pc"))
    return (f'<header class="topo"><a href="{raiz or "./"}"><img class="logo" src="{LOGO}" alt="Lab Escola 3D"></a>{nav}</header>'
            '<div class="onda"></div>')


def _rodape(raiz):
    redes = "".join(f'<img src="{raiz}_base/icones/{r}.svg" alt="{n}">' for r, n in
                    [("instagram", "Instagram"), ("facebook", "Facebook"), ("youtube", "YouTube"), ("linkedin", "LinkedIn")])
    return (f'<footer class="rodape"><span>Lab Escola 3D · projeto de extensão da UFRJ · <a href="{raiz}sobre/" style="color:inherit">sobre este protótipo</a> · <a href="{raiz}contribuir/" style="color:inherit">contato</a></span>'
            f'<div class="redes">{redes}</div></footer>')


def _numeros(cards):
    return '<div class="numeros">' + "".join(
        f'<div class="numero"><b>{E(b)}</b><span>{E(s)}</span></div>' for b, s in numeros(cards)) + "</div>"


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
    cards = carregar()
    telas = []
    for tela, rot in (("pc", "computador (1440)"), ("cel", "celular (375)")):
        telas.append(
            f'<section class="tela tela--{tela}" data-document-role="page" data-label="Catálogo · {rot}">'
            + _topo(tela, "../", "Catálogo")
            + '<div class="faixa"><span class="selo">Catálogo aberto</span><h1 style="margin-top:16px">Materiais para usar na sua aula</h1>'
              '<p>Jogos, oficinas, peças 3D e manuais criados pelo Lab Escola 3D com escolas públicas do Rio. Tudo gratuito, para baixar e adaptar.</p></div>'
            + _numeros(cards)
            + '<div class="bloco">' + _filtros(tela)
            + '<div class="vazio" hidden><p>Nenhum material com esses filtros.</p>'
              '<button type="button" class="botao botao--claro limpar">Limpar filtros</button></div>'
            + '<div class="cards">' + "".join(card(c) for c in cards) + "</div></div>"
            + _rodape("../") + "</section>")
    return _escrever(os.path.join(raiz, "catalogo", "index.html"),
                     _doc("Catálogo · Lab Escola 3D (protótipo)", "../", telas, FILTRO_JS))


def gerar_home(raiz: str) -> str:
    cards = carregar()
    por_slug = {c["slug"]: c for c in cards}
    destaques = [por_slug[s] for s in DESTAQUES]
    telas = []
    for tela, rot in (("pc", "computador (1440)"), ("cel", "celular (375)")):
        telas.append(
            f'<section class="tela tela--{tela}" data-document-role="page" data-label="Home · {rot}">'
            + _topo(tela, "", "")
            + '<div class="faixa"><span class="selo">Lab Escola 3D · extensão da UFRJ</span>'
              '<h1 style="margin-top:16px">Materiais para usar na sua aula</h1>'
              '<p>Jogos, formações e manuais criados com professoras e professores da rede pública do Rio. Gratuitos, para baixar, imprimir e adaptar à sua turma.</p>'
              '<a class="botao botao--grande" href="catalogo/">Ver o catálogo</a></div>'
            + _numeros(cards)
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
