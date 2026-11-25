"""Gera a página oficial de Identidade Visual (/identidade/) e o espelho 16:9 (/canva/manual-da-marca/).

Uso: py -I -X utf8 _ferramentas/gerar_identidade.py
Também expõe render_canva_manual(raiz, embutir_svg=True) para gerar a cópia
autocontida usada na compilação do PDF vetorial e no arquivamento no Drive.
"""
import base64
import html
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gerar_produtos import cabecalho_simples  # noqa: E402

E = html.escape

GOOGLE_FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Bebas+Neue&family=Big+Shoulders+Display:wght@700;900"
    "&family=Roboto:wght@300;400;500;700"
    "&family=Source+Sans+3:wght@400;600;700&display=swap"
)

QUEM_SOMOS_PARAGRAFOS = [
    (
        "O Lab Escola 3D é um laboratório interdisciplinar, colaborativo e experimental, "
        "como foco em processos de inovação na educação pública do Rio de Janeiro."
    ),
    (
        "Nosso objetivo é apoiar o desenvolvimento de produtos e serviços educacionais, "
        "contribuindo para a formação continuada de professores e estudantes da rede pública."
    ),
    (
        "Baseados no movimento maker e nas metodologias ativas, buscamos cooperar para "
        "formação de cidadãos independentes e inovadores capazes de utilizar o conhecimento "
        "adquirido para transformar o meio em que vivem."
    ),
]

SUMARIO_COLUNAS = [
    (
        "A Marca",
        [
            ("Logo", "05"),
            ("Área de proteção do logo", "06"),
            ("Ícone", "07"),
            ("Área de proteção do ícone", "08"),
            ("Estrutura do ícone", "09"),
            ("Logo vertical e horizontal", "10"),
            ("Redução do logo vertical", "14"),
            ("Redução do logo horizontal", "15"),
            ("Logo em suportes coloridos", "16"),
            ("Logo em imagens coloridas", "17"),
            ("Usos indevidos do logo", "18"),
        ],
    ),
    (
        "Identidade",
        [
            ("Tipografia", "20"),
            ("Cores", "21"),
            ("Padrões visuais", "22"),
            ("Sugestões de padrões", "23"),
            ("Aplicações", "27"),
        ],
    ),
]

USOS_INDEVIDOS = [
    ("p18-01-nao-rotacione.svg", "Não rotacione o logo", "Nota: ver pág 22"),
    ("p18-02-nao-altere-fonte.svg", "Não altere a fonte", ""),
    ("p18-03-nao-distorca.svg", "Não distorça o logo", ""),
    ("p18-04-nao-aplique-fotos.svg", "Não aplique fotos", ""),
    ("p18-05-nao-pinte-icone.svg", "Não pinte o ícone", ""),
    ("p18-06-nao-mude-cores.svg", "Não mude as cores", ""),
    ("p18-07-nao-use-contornos.svg", "Não use contornos", ""),
    ("p18-08-nao-reflita.svg", "Não reflita o logo", ""),
    ("p18-09-nao-aplique-efeitos.svg", "Não aplique efeitos nem mude opacidade", ""),
    ("p18-10-nao-altere-icone.svg", "Não altere o ícone", ""),
]

CORES_MANUAL = [
    ("Roxo", "#3026AD", "R 48 · G 38 · B 173", "C 92 · M 91 · Y 00 · K 00", "Principal"),
    ("Laranja", "#E3630D", "R 227 · G 99 · B 13", "C 06 · M 75 · Y 100 · K 00", "Destaque"),
    ("Preto (impresso)", "#000000", "R 0 · G 0 · B 0", "C 75 · M 68 · Y 67 · K 90", "Suporte (preto composto)"),
    ("Branco", "#FFFFFF", "R 255 · G 255 · B 255", "C 00 · M 00 · Y 00 · K 00", "Suporte"),
]

FUNDOS_CANVA_2026 = {
    "brilho-4-pontas.svg": "#3026AD",
    "canto-cubo.svg": "#3026AD",
    "canto-icone.svg": "#3026AD",
    "chevrons_direita.svg": "#3026AD",
    "chevrons_esquerda.svg": "#3026AD",
    "faixas-diagonais_laranja.svg": "#3026AD",
    "linhas-circuito_laranja.svg": "#3026AD",
    "ondas-concentricas.svg": "#E3630D",
    "reticula-pontos_branco.svg": "#3026AD",
    "reticula-pontos_roxo.svg": "#3026AD",
}


def _escrever(arq: str | Path, texto: str) -> str:
    p = Path(arq)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8", newline="\n")
    return str(p)


def _asset_manual(raiz: Path, nome: str, prefixo_rel: str, embutir: bool) -> str:
    arq = raiz / "identidade" / "manual" / nome
    if not embutir:
        return f"{prefixo_rel}identidade/manual/{nome}"
    if nome.endswith(".svg"):
        b64 = base64.b64encode(arq.read_bytes()).decode("ascii")
        return f"data:image/svg+xml;base64,{b64}"
    if nome.endswith(".png"):
        b64 = base64.b64encode(arq.read_bytes()).decode("ascii")
        return f"data:image/png;base64,{b64}"
    return f"{prefixo_rel}identidade/manual/{nome}"


def _img(src: str, alt: str, estilo: str = "") -> str:
    st = f' style="{E(estilo)}"' if estilo else ""
    return f'<img src="{E(src)}" alt="{E(alt)}"{st}>'


# ── Página pública /identidade/ ───────────────────────────────────────────

CSS_SITE = """
body{margin:0;background:#F2F2F2;color:#150E1F;font:16px/1.55 'Source Sans 3','Roboto',system-ui,sans-serif}
main{max-width:1160px;margin:0 auto;padding:24px 16px 64px}
h1,h2,h3{font-family:'Big Shoulders Display','Bebas Neue',sans-serif;font-weight:700;color:#3026AD;line-height:1.1}
h1{font-size:48px;margin:8px 0 10px}
h2{font-size:32px;margin:36px 0 12px}
h2 small{color:#E3630D;font-size:15px;font-weight:600;font-family:'Source Sans 3',sans-serif}
h3{font-size:24px;margin:0 0 8px}
a{color:#3026AD}
.hero{background:#3026AD;color:#fff;border-radius:16px;padding:36px 32px;margin-bottom:24px}
.hero h1{color:#fff;font-size:54px;margin:6px 0 8px}
.hero .selo{display:inline-block;background:#E3630D;color:#fff;font-size:13px;font-weight:700;padding:4px 12px;border-radius:99px}
.hero p{max-width:740px;font-size:18px;margin:10px 0 18px;color:#F2F2F2}
.acoes{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;background:#E3630D;color:#fff;text-decoration:none;font-weight:700;padding:11px 20px;border-radius:99px;font-size:15px}
.btn.sec{background:#fff;color:#3026AD}
.nav-sec{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 24px}
.nav-sec a{background:#fff;border:1px solid #D9D6F2;border-radius:99px;padding:6px 14px;text-decoration:none;font-size:14px;font-weight:600}
.bloco{background:#fff;border-radius:14px;padding:24px 26px;margin-bottom:20px;border:1px solid #E5E5E5}
.bloco h2{margin-top:0}
.cols{display:grid;grid-template-columns:1.1fr 1fr;gap:24px;align-items:center}
.cols>*,.grade-2>*,.grade-4>*,.grade-5>*{min-width:0}
.grade-2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.grade-4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.grade-5{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.card-svg{background:#FAFAFC;border:1px solid #E0E0E8;border-radius:10px;padding:12px;display:flex;flex-direction:column;justify-content:space-between;gap:8px}
.card-svg .visor{min-height:110px;display:flex;align-items:center;justify-content:center;border-radius:6px;padding:8px}
.card-svg .visor.escuro{background:#150E1F}
.card-svg img{max-width:100%;max-height:140px;display:block}
.card-svg .rod{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:13px}
.card-svg .dl{font-size:12px;font-weight:700;text-decoration:none;padding:3px 9px;border-radius:99px;background:#EAE8F9;color:#3026AD}
.nota{background:#FFF7F2;border-left:4px solid #E3630D;padding:10px 14px;border-radius:6px;font-size:14px;margin:12px 0}
.tabela-wrap{overflow-x:auto}
.tabela{width:100%;border-collapse:collapse;font-size:15px;margin-top:10px}
.tabela th,.tabela td{border:1px solid #E2E2E8;padding:10px 12px;text-align:left}
.tabela th{background:#F5F4FB;color:#3026AD}
.amostra-cor{display:inline-block;width:22px;height:22px;border-radius:5px;vertical-align:middle;margin-right:8px;border:1px solid #ccc}
.amostra-bebas{font-family:'Bebas Neue',sans-serif;font-size:32px;letter-spacing:0.5px;line-height:1.15;overflow-wrap:anywhere}
.amostra-roboto{font-family:'Roboto',sans-serif;font-size:20px;line-height:1.4;overflow-wrap:anywhere}
.amostra-chars{overflow-wrap:anywhere}
.diag{width:100%;height:auto;display:block;border-radius:8px;border:1px solid #EAEAEF;background:#fff}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}
.c{background:#fff;border:1px solid #ddd;border-radius:8px;overflow:hidden;text-decoration:none;color:inherit}
.v{height:140px;display:flex;align-items:center;justify-content:center}.v img{max-width:90%;max-height:90%}
.t{padding:6px 8px;font-size:12px;word-break:break-all}
.aviso{background:#fff;border-left:4px solid #E3630D;padding:10px 14px;border-radius:6px;margin-bottom:14px}
footer{margin-top:42px;font-size:14px;color:#555}
@media(max-width:860px){.cols,.grade-2,.grade-4,.grade-5{grid-template-columns:1fr}.hero{padding:24px 18px}.hero h1{font-size:38px}h2{font-size:28px}}
""".strip()


def _render_galeria_existente(raiz: Path) -> str:
    def _cards(subpasta: str, bg_fn) -> str:
        pasta = raiz / "identidade" / subpasta
        arqs = sorted(p.name for p in pasta.glob("*.svg"))
        itens = []
        for fn in arqs:
            rel = f"{subpasta}/{fn}"
            nome = fn[:-4]
            bg = bg_fn(fn)
            itens.append(
                f'<a class="c" href="{E(rel)}"><div class="v" style="background:{bg}">'
                f'<img src="{E(rel)}" alt="{E(nome)}" loading="lazy"></div>'
                f'<div class="t">{E(nome)}</div></a>'
            )
        return len(arqs), "".join(itens)

    n_marca, h_marca = _cards("marca", lambda _: "#FFFFFF")
    n_site, h_site = _cards("elementos/site-2024", lambda _: "#FFFFFF")
    n_canva, h_canva = _cards("elementos/canva-2026", lambda fn: FUNDOS_CANVA_2026.get(fn, "#FFFFFF"))
    n_gab, h_gab = _cards("gabaritos-professor", lambda _: "#FFFFFF")

    return f"""
<section class="bloco" id="candidatos">
  <h2>Elementos candidatos e kit do professor</h2>
  <p class="aviso"><b>Candidatos complementares, não oficiais.</b> A definição do que entra na próxima revisão da identidade visual é da equipe de design. Os SVGs são gerados por código (<a href="geradores/README.md">geradores</a>); não edite à mão.</p>
  <p><a href="prancha-proposta-lote1.png">Prancha da proposta (lote 1)</a> · <a href="prancha-lote2.png">Prancha do lote 2 e do kit do professor</a></p>
  <h3>Marca reduzida: cubo e selo <small>{n_marca} arquivos</small></h3>
  <div class="g">{h_marca}</div>
  <h3 style="margin-top:24px">Elementos do site (2024) <small>{n_site} arquivos</small></h3>
  <div class="g">{h_site}</div>
  <h3 style="margin-top:24px">Elementos garimpados no Canva (2026) <small>{n_canva} arquivos</small></h3>
  <div class="g">{h_canva}</div>
  <h3 style="margin-top:24px">Kit do professor — gabaritos A4 <small>{n_gab} arquivos</small></h3>
  <div class="g">{h_gab}</div>
</section>""".strip()


def _cards_variantes(prefixo: str, titulo_base: str) -> str:
    itens = []
    for cor, rot, escuro in (
        ("roxo", "Roxo (#3026AD)", False),
        ("laranja", "Laranja (#E3630D)", False),
        ("preto", "Preto", False),
        ("branco", "Branco", True),
    ):
        fn = f"{prefixo}-{cor}.svg"
        cls_v = "visor escuro" if escuro else "visor"
        itens.append(
            f'<div class="card-svg"><div class="{cls_v}">'
            f'<img src="manual/{E(fn)}" alt="{E(titulo_base)} — {E(rot)}"></div>'
            f'<div class="rod"><span>{E(rot)}</span>'
            f'<a class="dl" href="manual/{E(fn)}" download>SVG</a></div></div>'
        )
    return "".join(itens)


def render_identidade_site(raiz: str | Path) -> str:
    r = Path(raiz)
    faixa = (
        '<div class="alfa" style="background:#150E1F;color:#FFFFFF;font:14px/1.4 system-ui,sans-serif;'
        'padding:8px 16px;text-align:center">Protótipo em <b style="color:#E3630D">versão alfa</b> · '
        'Lab Escola 3D · <a href="../sobre/" style="color:#FFFFFF">o que é este protótipo</a></div>'
    )
    cab = cabecalho_simples("../", "")

    usos_html = "".join(
        f'<div class="card-svg"><div class="visor"><img src="manual/{E(fn)}" alt="{E(tit)}"></div>'
        f'<div class="rod"><span><b>{E(tit)}</b>'
        + (f'<br><small>{E(nota)}</small>' if nota else "")
        + f'</span><a class="dl" href="manual/{E(fn)}" download>SVG</a></div></div>'
        for fn, tit, nota in USOS_INDEVIDOS
    )

    cores_rows = "".join(
        f'<tr><td><span class="amostra-cor" style="background:{hex_c}"></span><b>{E(nome)}</b></td>'
        f'<td><code>{E(hex_c)}</code></td><td>{E(rgb)}</td><td>{E(cmyk)}</td><td>{E(uso)}</td></tr>'
        for nome, hex_c, rgb, cmyk, uso in CORES_MANUAL
    )

    persona_cards = "".join(
        f'<div class="card-svg"><div class="visor" style="background:#E3630D;min-height:220px">'
        f'<img src="manual/persona-profa-marcia-0{i}.png" alt="Persona Profª. Márcia — pose {i}" style="max-height:200px"></div>'
        f'<div class="rod"><span>Pose 0{i}</span>'
        f'<a class="dl" href="manual/persona-profa-marcia-0{i}.png" download>PNG</a></div></div>'
        for i in range(1, 5)
    )

    galeria = _render_galeria_existente(r)
    quem_html = "".join(f"<p>{E(p)}</p>" for p in QUEM_SOMOS_PARAGRAFOS)

    corpo = f"""
<div class="hero">
  <span class="selo">Manual da Marca · fevereiro, 2024</span>
  <h1>Identidade Visual · Lab Escola 3D</h1>
  <p>Guia oficial de uso da marca, especificações técnicas de logo, ícone, cores, tipografia, padrões visuais e arquivos vetoriais em SVG para download.</p>
  <div class="acoes">
    <a class="btn" href="../canva/manual-da-marca/">Ver apresentação 16:9 (33 slides)</a>
    <a class="btn sec" href="#downloads-logo">Baixar logos em SVG</a>
    <a class="btn sec" href="#candidatos">Ver elementos candidatos</a>
  </div>
</div>

<nav class="nav-sec" aria-label="Seções do Manual">
  <a href="#quem-somos">Quem somos</a>
  <a href="#marca">Logo e Ícone</a>
  <a href="#protecao">Área de proteção e Estrutura</a>
  <a href="#downloads-logo">Versões e Redução</a>
  <a href="#suportes">Suportes e Usos indevidos</a>
  <a href="#identidade">Tipografia e Cores</a>
  <a href="#padroes">Padrões visuais</a>
  <a href="#aplicacoes">Aplicações e Persona</a>
  <a href="#contato">Contato</a>
</nav>

<section class="bloco" id="quem-somos">
  <h2>Quem somos</h2>
  {quem_html}
</section>

<section class="bloco" id="marca">
  <h2>A Marca · Logo e Ícone</h2>
  <div class="cols">
    <div>
      <h3>Logo</h3>
      <p>O logo do Lab Escola 3D busca transmitir força pelo seu nome e leveza pelo seu ícone. Para isso, a tipografia escolhida foi uma sem serifa de espessura alta e linhas limpas, que tem como característica uma robustez natural e ares de modernidade e inovação.</p>
      <p>O ícone do Lab Escola 3D é a junção da letra “L” com o número três, sendo uma alusão direta ao nome do projeto. Sua forma ser percebida apenas pelos seus contornos oferece um teor de simplicidade e se soma com o ar vanguardista da tipografia.</p>
      <p>Dessa forma, o logo condensa os valores de educação, inovação e modernidade do laboratório. Conta também com versões horizontais e verticais, coloridas e monocromáticas.</p>
    </div>
    <div><img class="diag" src="manual/logo-vertical-roxo.svg" alt="Logo vertical roxo do Lab Escola 3D" style="max-height:300px;object-fit:contain;padding:18px;box-sizing:border-box"></div>
  </div>
  <hr style="border:0;border-top:1px solid #EAEAEF;margin:22px 0">
  <div class="cols">
    <div>
      <h3>Ícone</h3>
      <p>A relação entre a letra “L” e o número três é visualizada em uma perspectiva obliqua, oferecendo vista por igual de ambos os lados da peça.</p>
      <p>Por ter a força de transmitir por si só os ideais de tecnologia, ensino e inovação do Lab Escola 3D, é permitido a aplicação isolada do ícone.</p>
    </div>
    <div><img class="diag" src="manual/icone-roxo.svg" alt="Ícone isolado do Lab Escola 3D" style="max-height:220px;object-fit:contain;padding:18px;box-sizing:border-box"></div>
  </div>
</section>

<section class="bloco" id="protecao">
  <h2>Área de proteção e Estrutura</h2>
  <p>Afim de garantir legibilidade ideal do logo em relação a demais elementos em volta, foi estabelecida uma área mínima de respiro a ser respeitada em futuras aplicações. A medida da área de proteção equivale à largura do “3D”.</p>
  <div class="grade-2">
    <div><img class="diag" src="manual/p06-area-protecao-logo-horizontal.svg" alt="Área de proteção do logo horizontal (largura do 3D)"></div>
    <div><img class="diag" src="manual/p06-area-protecao-logo-vertical.svg" alt="Área de proteção do logo vertical (largura do 3D)"></div>
  </div>
  <div class="cols" style="margin-top:20px">
    <div>
      <h3>Área de proteção do ícone</h3>
      <p>Para o uso do ícone desvinculado do logo, recomenda-se casos à vontade do aplicador, exceto quando o ícone for usado como a única forma de apresentação visual do Lab Escola 3D, requerendo o uso completo do logo posteriormente em outra configuração.</p>
      <p>A medida da área de proteção segue a mesma, equivalendo à largura do “3D”.</p>
    </div>
    <div><img class="diag" src="manual/p08-area-protecao-icone.svg" alt="Área de proteção do ícone isolado"></div>
  </div>
  <div class="cols" style="margin-top:20px">
    <div>
      <h3>Estrutura do ícone</h3>
      <p>Sob a perspectiva oblíqua, o ícone foi traçado com linhas diagonais em uma angulação de 24,1 graus, se mantendo simétricas nos lados opostos da figura.</p>
      <div class="nota"><b>Nota técnica da vetorização:</b> o texto original do manual (2024) cita 24,1°, enquanto a medição exata sobre a arte oficial e sobre o próprio desenho construtivo registra <b>22,34°</b> (ver <a href="geradores/icone-le3d.json">geometria do ícone</a>).</div>
    </div>
    <div><img class="diag" src="manual/p09-estrutura-icone.svg" alt="Estrutura geométrica do ícone em perspectiva oblíqua"></div>
  </div>
</section>

<section class="bloco" id="downloads-logo">
  <h2>Versões oficiais e Redução mínima</h2>
  <h3>Logo vertical</h3>
  <div class="grade-4">{_cards_variantes("logo-vertical", "Logo vertical")}</div>
  <h3 style="margin-top:20px">Logo horizontal</h3>
  <div class="grade-4">{_cards_variantes("logo-horizontal", "Logo horizontal")}</div>
  <h3 style="margin-top:20px">Ícone isolado</h3>
  <div class="grade-4">{_cards_variantes("icone", "Ícone")}</div>

  <div class="grade-2" style="margin-top:22px">
    <div>
      <h3>Redução do logo vertical</h3>
      <p>Para manter a legibilidade do logo em ambientes digitais, o logo não pode ser apresentado menor que <b>101 x 176 px</b>. Em impressos, mantenha a altura do logo acima de <b>3 cm</b>.</p>
      <img class="diag" src="manual/p14-reducao-logo-vertical.svg" alt="Escala de redução mínima do logo vertical: 101 x 176 px">
    </div>
    <div>
      <h3>Redução do logo horizontal</h3>
      <p>Para manter a legibilidade do logo em ambientes digitais, o logo não pode ser apresentado menor que <b>200 x 89 px</b>. Em impressos, mantenha a largura do logo acima de <b>4 cm</b>.</p>
      <img class="diag" src="manual/p15-reducao-logo-horizontal.svg" alt="Escala de redução mínima do logo horizontal: 200 x 89 px">
    </div>
  </div>
</section>

<section class="bloco" id="suportes">
  <h2>Suportes coloridos, Imagens coloridas e Usos indevidos</h2>
  <h3>Logo em suportes coloridos</h3>
  <p>Em fundos com cores chapadas, recomenda-se o uso da paleta de cores do Lab Escola 3D. Não use o logo sobre gradientes nem em fundos com a mesma cor do logo.</p>
  <img class="diag" src="manual/p16-suportes-coloridos.svg" alt="Seis combinações oficiais do logo em suportes coloridos">

  <h3 style="margin-top:22px">Logo em imagens coloridas</h3>
  <p>Atenção ao usar o logo em imagens. Não o posicione em cantos onde as cores se pareçam muito com a cor da logo ou demais situações que comprometam sua legibilidade. Tente escolher um espaço o mais limpo possível.</p>
  <img class="diag" src="manual/p17-aplicacao-fundos-coloridos.svg" alt="Exemplos esquemáticos de posicionamento do logo em zonas limpas de fundos coloridos">

  <h3 style="margin-top:22px">Usos indevidos do logo</h3>
  <p>Pedimos para não alterar o logo a fim de manter sua aparência geral intacta. Abaixo, alguns exemplos.</p>
  <div class="grade-5">{usos_html}</div>
</section>

<section class="bloco" id="identidade">
  <h2>Identidade · Tipografia e Cores</h2>
  <div class="cols">
    <div>
      <h3>Tipografia</h3>
      <p>A fonte primária do Lab Escola 3D é a <b>Bebas Neue</b>, sem serifa notória por sua imponência expressa pela sua verticalidade e espessura acentuada. Recomenda-se uso em títulos grandes e informações de destaque. Pode ser usada como uma fonte display.</p>
      <p>A fonte secundária é a <b>Roboto</b>, com seu estilo leve, moderno e versátil sendo uma excelente união com a fonte primária. Recomenda-se uso dos pesos bold ou semibold em títulos menores, com os pesos regular ou light em textos corridos.</p>
      <div class="nota"><b>Em transição no site alfa:</b> este protótipo web utiliza <b>Big Shoulders Display</b> (para permitir minúsculas em títulos) e <b>Source Sans 3</b> em telas digitais, mantendo o logo em Bebas Neue convertida em curvas.</div>
    </div>
    <div style="background:#FAFAFC;border:1px solid #E2E2EC;border-radius:10px;padding:18px">
      <div class="amostra-bebas">OLÁ, SOU A FONTE PRIMÁRIA</div>
      <div class="amostra-chars" style="font-family:'Bebas Neue',sans-serif;font-size:20px;margin-bottom:14px">ABCDEFGHIJKLMNOPQRSTUVWXYZ · 0 1 2 3 4 5 6 7 8 9 .,:;“”!?@#$%^&amp;*[]+=&lt;&gt;|\\/</div>
      <div class="amostra-roboto"><b>Olá, sou a fonte secundária</b></div>
      <div class="amostra-chars" style="font-family:'Roboto',sans-serif;font-size:15px">abcdefghijklmnopqrstuvwxyz · ABCDEFGHIJKLMNOPQRSTUVWXYZ · 0 1 2 3 4 5 6 7 8 9 .,:;'"!?@#$%^&amp;*()+=&lt;&gt;|\\/</div>
    </div>
  </div>

  <h3 style="margin-top:22px">Cores</h3>
  <p>O Lab Escola 3D expressa sua linguagem por meio de sua paleta de cores composta pela sobriedade do roxo e energia do laranja, indo de encontro com a proposta de inovação educacional e cultura maker que o laboratório foca em desenvolver. De suporte, temos o preto e branco. A paleta dispensa qualquer tipo de gradientes.</p>
  <p><b>Nota:</b> para evitar o preto de sair com aspecto lavado em impressos, use a mistura CMYK especificada.</p>
  <div class="cols">
    <div class="tabela-wrap"><table class="tabela"><thead><tr><th>Cor</th><th>HEX</th><th>RGB</th><th>CMYK</th><th>Papel</th></tr></thead><tbody>{cores_rows}</tbody></table></div>
    <div><img class="diag" src="manual/p21-paleta-cores.svg" alt="Cartões de cores do Lab Escola 3D com códigos RGB, CMYK e HEX"></div>
  </div>
</section>

<section class="bloco" id="padroes">
  <h2>Padrões visuais</h2>
  <p>O ícone do Lab Escola 3D é ideal para qualquer tipo de padronagem, incrementos ou repetições visuais. Contanto que a aplicação do ícone se mantenha alinhada com os guias de uso no manual, outros tipos de padrões e estampas são permitidas. <b>Nota:</b> apenas em aplicações de padronagens e afins, a rotação do ícone é permitida.</p>
  <div class="grade-2">
    <div class="card-svg"><div class="visor"><img src="manual/p22-padrao-amostra.svg" alt="Amostra de padrão em traço" style="max-height:220px"></div><div class="rod"><span>Amostra de padronagem</span><a class="dl" href="manual/p22-padrao-amostra.svg" download>SVG</a></div></div>
    <div class="card-svg"><div class="visor"><img src="manual/p24-padrao-dividido-16x9.svg" alt="Padrão dividido roxo e laranja" style="max-height:220px"></div><div class="rod"><span>Padrão dividido 16:9</span><a class="dl" href="manual/p24-padrao-dividido-16x9.svg" download>SVG</a></div></div>
    <div class="card-svg"><div class="visor"><img src="manual/p23-padrao-roxo.svg" alt="Sugestão de padrão roxo" style="max-height:220px"></div><div class="rod"><span>Sugestão em roxo</span><a class="dl" href="manual/p23-padrao-roxo.svg" download>SVG</a></div></div>
    <div class="card-svg"><div class="visor"><img src="manual/p23-padrao-laranja.svg" alt="Sugestão de padrão laranja" style="max-height:220px"></div><div class="rod"><span>Sugestão em laranja</span><a class="dl" href="manual/p23-padrao-laranja.svg" download>SVG</a></div></div>
    <div class="card-svg"><div class="visor"><img src="manual/p25-padrao-grande-roxo-16x9.svg" alt="Padrão ampliado roxo" style="max-height:220px"></div><div class="rod"><span>Composição ampliada roxa</span><a class="dl" href="manual/p25-padrao-grande-roxo-16x9.svg" download>SVG</a></div></div>
    <div class="card-svg"><div class="visor"><img src="manual/p26-padrao-grande-laranja-16x9.svg" alt="Padrão ampliado laranja" style="max-height:220px"></div><div class="rod"><span>Composição ampliada laranja</span><a class="dl" href="manual/p26-padrao-grande-laranja-16x9.svg" download>SVG</a></div></div>
  </div>
</section>

<section class="bloco" id="aplicacoes">
  <h2>Aplicações e Persona</h2>
  <p>O logo do Lab Escola 3D é ideal em uma infinidade de suportes e formatos diferentes, adequados para diversas situações, como pôsteres, papelaria institucional, camisas, mochilas, bolsas, entre muitas outras.</p>
  <div class="grade-2">
    <div class="card-svg"><div class="visor"><img src="manual/p28-aplicacao-camisetas.svg" alt="Aplicação esquemática em camisetas" style="max-height:220px"></div><div class="rod"><span>Camisetas (preta e branca)</span><a class="dl" href="manual/p28-aplicacao-camisetas.svg" download>SVG</a></div></div>
    <div class="card-svg"><div class="visor"><img src="manual/p29-aplicacao-caneca.svg" alt="Aplicação esquemática em caneca" style="max-height:220px"></div><div class="rod"><span>Caneca institucional</span><a class="dl" href="manual/p29-aplicacao-caneca.svg" download>SVG</a></div></div>
    <div class="card-svg"><div class="visor"><img src="manual/p30-banner-institucional.svg" alt="Banner institucional Programa de Voluntariado" style="max-height:220px"></div><div class="rod"><span>Banner institucional</span><a class="dl" href="manual/p30-banner-institucional.svg" download>SVG</a></div></div>
    <div class="card-svg"><div class="visor"><img src="manual/p31-banner-inovacao.svg" alt="Banner Design para a Inovação Social na Educação Pública" style="max-height:220px"></div><div class="rod"><span>Banner inovação social</span><a class="dl" href="manual/p31-banner-inovacao.svg" download>SVG</a></div></div>
  </div>
  <h3 style="margin-top:22px">Persona — Profª. Márcia</h3>
  <div class="grade-4">{persona_cards}</div>
</section>

{galeria}

<section class="bloco" id="contato" style="background:#3026AD;color:#fff;border-color:#3026AD">
  <h2 style="color:#fff">Contato</h2>
  <p>Se houveram dúvidas, sugestões ou comentários sobre o manual ou o Lab Escola 3D, entre em contato com a gente.</p>
  <p><b><a href="mailto:labescola3d@gmail.com" style="color:#fff">labescola3d@gmail.com</a></b></p>
</section>
""".strip()

    return (
        '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>Identidade Visual · Lab Escola 3D</title>\n'
        f'<link rel="stylesheet" href="{GOOGLE_FONTS_URL}">\n'
        f'<style>\n{CSS_SITE}\n</style>\n</head>\n<body>\n'
        f'{faixa}\n{cab}\n<main>\n{corpo}\n'
        '<footer>Lab Escola 3D · projeto de extensão da UFRJ · materiais e código sob CC BY-NC-SA 4.0 · '
        '<a href="../licenca/">licença e como usar</a> · <a href="../contribuir/">como contribuir</a></footer>\n'
        '</main>\n</body>\n</html>\n'
    )


def gerar_identidade_site(raiz: str | Path) -> str:
    return _escrever(Path(raiz) / "identidade" / "index.html", render_identidade_site(raiz))


# ── Espelho Canva 16:9 (33 slides) ────────────────────────────────────────

CSS_CANVA_16X9 = """
@page { size: 1920px 1080px; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; padding: 0; background: #1e1e1e; font-family: 'Roboto', 'Source Sans 3', system-ui, sans-serif; color: #150E1F; }
.slide {
  width: 1920px;
  height: 1080px;
  margin: 0 auto 24px;
  position: relative;
  overflow: hidden;
  background: #FFFFFF;
  color: #150E1F;
  page-break-after: always;
}
.slide--roxo { background: #3026AD; color: #FFFFFF; }
.slide--laranja { background: #E3630D; color: #FFFFFF; }
.slide--full { padding: 0; }
.topo-data { position: absolute; left: 128px; top: 128px; font-size: 26px; font-weight: 300; color: #FFFFFF; }
.capa-titulo { position: absolute; left: 128px; bottom: 268px; font-family: 'Bebas Neue', 'Big Shoulders Display', sans-serif; font-size: 112px; font-weight: 700; letter-spacing: 1px; margin: 0; color: #FFFFFF; line-height: 1; }
.capa-sub { position: absolute; left: 128px; bottom: 214px; font-size: 30px; font-weight: 300; margin: 0; color: #FFFFFF; }
.div-titulo { position: absolute; left: 128px; bottom: 268px; font-family: 'Bebas Neue', 'Big Shoulders Display', sans-serif; font-size: 112px; font-weight: 700; margin: 0; color: #FFFFFF; line-height: 1; }
.div-sub { position: absolute; left: 128px; bottom: 214px; font-size: 30px; font-weight: 300; margin: 0; color: #FFFFFF; }
.sec-h { position: absolute; left: 128px; top: 126px; margin: 0; font-family: 'Roboto', sans-serif; font-size: 38px; font-weight: 700; color: #3026AD; }
.sec-h--branco { color: #FFFFFF; }
.col-txt { position: absolute; left: 128px; top: 216px; width: 650px; font-size: 27px; font-weight: 300; line-height: 1.48; color: #222222; }
.col-txt p { margin: 0 0 30px; }
.col-txt--branco { color: #FFFFFF; }
.num-pg { position: absolute; right: 128px; bottom: 88px; font-size: 26px; font-weight: 400; color: #333333; }
.sumario-grid { position: absolute; left: 128px; top: 216px; display: grid; grid-template-columns: 420px 360px 260px; gap: 72px; align-items: start; }
.sum-col h3 { margin: 0 0 28px; font-size: 27px; font-weight: 700; color: #150E1F; }
.sum-row { display: flex; justify-content: space-between; font-size: 26px; font-weight: 300; line-height: 1.95; color: #222222; }
.sum-contato { padding-top: 416px; display: flex; justify-content: space-between; font-size: 27px; color: #150E1F; }
.duas-pecas { position: absolute; left: 128px; right: 128px; top: 240px; height: 700px; display: flex; align-items: center; justify-content: center; gap: 120px; }
.peca-box { display: flex; align-items: center; justify-content: center; }
.peca-box--preto { background: #000000; padding: 64px 72px; }
.nota-b { font-weight: 700; }
.usos-grid { position: absolute; left: 128px; right: 128px; top: 345px; display: grid; grid-template-columns: repeat(5, 1fr); gap: 52px 36px; }
.uso-item img { width: 100%; height: 145px; object-fit: contain; display: block; margin-bottom: 14px; }
.uso-item p { margin: 0; font-size: 22px; font-weight: 300; line-height: 1.35; color: #222222; }
.tipo-col { position: absolute; left: 1050px; top: 216px; width: 740px; color: #150E1F; }
.tipo-pri-t { font-family: 'Bebas Neue', sans-serif; font-size: 68px; line-height: 1.1; margin: 0 0 12px; }
.tipo-pri-a { font-family: 'Bebas Neue', sans-serif; font-size: 32px; line-height: 1.35; margin: 0 0 56px; letter-spacing: 0.6px; }
.tipo-sec-t { font-family: 'Roboto', sans-serif; font-size: 46px; font-weight: 700; line-height: 1.15; margin: 0 0 14px; }
.tipo-sec-a { font-family: 'Roboto', sans-serif; font-size: 28px; font-weight: 300; line-height: 1.45; margin: 0; }
.padroes-duo { position: absolute; left: 180px; right: 180px; top: 245px; display: flex; justify-content: center; gap: 180px; }
.padroes-duo img { width: 620px; height: 560px; object-fit: contain; display: block; }
.persona-wrap { position: absolute; left: 96px; right: 440px; top: 110px; bottom: 110px; display: flex; align-items: flex-end; justify-content: space-between; gap: 28px; }
.persona-wrap img { height: 800px; width: auto; display: block; }
.persona-marca { position: absolute; right: 96px; bottom: 88px; text-align: right; color: #FFFFFF; }
.persona-marca img { width: 290px; height: auto; display: block; margin-left: auto; margin-bottom: 14px; }
.persona-marca p { margin: 0; font-size: 24px; font-weight: 300; }
""".strip()


def _slide(num: int, label: str, corpo: str, classe: str = "") -> str:
    cls = f"slide {classe}".strip()
    return f'<section class="{cls}" data-document-role="page" data-label="P{num:02d} · {E(label)}">\n{corpo}\n</section>'


def _num_pg(num: int) -> str:
    return f'<span class="num-pg">{num:02d}</span>'


def render_canva_manual(raiz: str | Path, embutir_svg: bool = False) -> str:
    r = Path(raiz)
    pref = "../../"

    def a(nome: str) -> str:
        return _asset_manual(r, nome, pref, embutir_svg)

    slides: list[str] = []

    # P01 · Capa
    slides.append(_slide(1, "Capa", (
        '<span class="topo-data">fevereiro, 2024</span>'
        '<h1 class="capa-titulo">LAB ESCOLA 3D</h1>'
        '<p class="capa-sub">Guia de identidade visual</p>'
    ), "slide--roxo"))

    # P02 · Quem somos
    slides.append(_slide(2, "Quem somos", (
        '<h2 class="sec-h">Quem somos</h2>'
        '<div class="col-txt">'
        + "".join(f"<p>{E(p)}</p>" for p in QUEM_SOMOS_PARAGRAFOS)
        + "</div>"
    )))

    # P03 · Conteúdo
    cols_sum = "".join(
        f'<div class="sum-col"><h3>{E(tit)}</h3>'
        + "".join(f'<div class="sum-row"><span>{E(item)}</span><span>{pg}</span></div>' for item, pg in itens)
        + "</div>"
        for tit, itens in SUMARIO_COLUNAS
    )
    slides.append(_slide(3, "Conteúdo", (
        '<h2 class="sec-h">Conteúdo</h2>'
        f'<div class="sumario-grid">{cols_sum}'
        '<div class="sum-contato"><b>Contato</b><span>33</span></div></div>'
    )))

    # P04 · Divisória A MARCA
    slides.append(_slide(4, "Divisória A Marca", (
        '<h2 class="div-titulo">A MARCA</h2>'
        '<p class="div-sub">Logo, uso e especificidades</p>'
    ), "slide--laranja"))

    # P05 · Logo
    slides.append(_slide(5, "Logo", (
        '<h2 class="sec-h">Logo</h2>'
        '<div class="col-txt">'
        '<p>O logo do Lab Escola 3D busca transmitir força pelo seu nome e leveza pelo seu ícone. Para isso, a tipografia escolhida foi uma sem serifa de espessura alta e linhas limpas, que tem como característica uma robustez natural e ares de modernidade e inovação.</p>'
        '<p>O ícone do Lab Escola 3D é a junção da letra “L” com o número três, sendo uma alusão direta ao nome do projeto. Sua forma ser percebida apenas pelos seus contornos oferece um teor de simplicidade e se soma com o ar vanguardista da tipografia.</p>'
        '<p>Dessa forma, o logo condensa os valores de educação, inovação e modernidade do laboratório. Conta também com versões horizontais e verticais, coloridas e monocromáticas.</p>'
        '</div>'
        f'<div style="position:absolute;right:330px;top:245px">{_img(a("logo-vertical-roxo.svg"), "Logo vertical roxo", "height:590px;width:auto")}</div>'
        + _num_pg(5)
    )))

    # P06 · Área de proteção do logo
    slides.append(_slide(6, "Área de proteção do logo", (
        '<h2 class="sec-h">Área de proteção do logo</h2>'
        '<div class="col-txt" style="width:760px">'
        '<p>Afim de garantir legibilidade ideal do logo em relação a demais elementos em volta, foi estabelecida uma área mínima de respiro a ser respeitada em futuras aplicações. A medida da área de proteção equivale à largura do “3D”.</p>'
        '</div>'
        f'<div style="position:absolute;left:128px;top:465px">{_img(a("p06-area-protecao-logo-horizontal.svg"), "Área de proteção do logo horizontal", "width:690px;height:auto")}</div>'
        f'<div style="position:absolute;right:240px;top:220px">{_img(a("p06-area-protecao-logo-vertical.svg"), "Área de proteção do logo vertical", "height:660px;width:auto")}</div>'
        + _num_pg(6)
    )))

    # P07 · Ícone
    slides.append(_slide(7, "Ícone", (
        '<h2 class="sec-h">Ícone</h2>'
        '<div class="col-txt">'
        '<p>A relação entre a letra “L” e o número três é visualizada em uma perspectiva obliqua, oferecendo vista por igual de ambos os lados da peça.</p>'
        '<p>Por ter a força de transmitir por si só os ideais de tecnologia, ensino e inovação do Lab Escola 3D, é permitido a aplicação isolada do ícone.</p>'
        '</div>'
        f'<div style="position:absolute;right:290px;top:370px">{_img(a("icone-roxo.svg"), "Ícone roxo", "width:420px;height:auto")}</div>'
        + _num_pg(7)
    )))

    # P08 · Área de proteção do ícone
    slides.append(_slide(8, "Área de proteção do ícone", (
        '<h2 class="sec-h">Área de proteção do ícone</h2>'
        '<div class="col-txt">'
        '<p>Para o uso do ícone desvinculado do logo, recomenda-se casos à vontade do aplicador, exceto quando o ícone for usado como a única forma de apresentação visual do Lab Escola 3D, requerendo o uso completo do logo posteriormente em outra configuração.</p>'
        '<p>A medida da área de proteção segue a mesma, equivalendo à largura do “3D”.</p>'
        '</div>'
        f'<div style="position:absolute;right:260px;top:310px">{_img(a("p08-area-protecao-icone.svg"), "Área de proteção do ícone", "width:540px;height:auto")}</div>'
        + _num_pg(8)
    )))

    # P09 · Estrutura do ícone
    slides.append(_slide(9, "Estrutura do ícone", (
        '<h2 class="sec-h">Estrutura do ícone</h2>'
        '<div class="col-txt">'
        '<p>Sob a perspectiva oblíqua, o ícone foi traçado com linhas diagonais em uma angulação de 24,1 graus, se mantendo simétricas nos lados opostos da figura.</p>'
        '</div>'
        f'<div style="position:absolute;right:180px;top:210px">{_img(a("p09-estrutura-icone.svg"), "Estrutura oblíqua do ícone", "width:700px;height:auto")}</div>'
        + _num_pg(9)
    )))

    # P10 · Logo vertical colorido
    slides.append(_slide(10, "Logo vertical colorido", (
        '<h2 class="sec-h">Logo vertical e horizontal</h2>'
        '<div class="duas-pecas">'
        f'<div class="peca-box">{_img(a("logo-vertical-roxo.svg"), "Logo vertical roxo", "height:590px;width:auto")}</div>'
        f'<div class="peca-box">{_img(a("logo-vertical-laranja.svg"), "Logo vertical laranja", "height:590px;width:auto")}</div>'
        '</div>' + _num_pg(10)
    )))

    # P11 · Logo vertical monocromático
    slides.append(_slide(11, "Logo vertical monocromático", (
        '<div class="duas-pecas" style="top:185px">'
        f'<div class="peca-box">{_img(a("logo-vertical-preto.svg"), "Logo vertical preto", "height:590px;width:auto")}</div>'
        f'<div class="peca-box peca-box--preto">{_img(a("logo-vertical-branco.svg"), "Logo vertical branco", "height:590px;width:auto")}</div>'
        '</div>' + _num_pg(11)
    )))

    # P12 · Logo horizontal colorido
    slides.append(_slide(12, "Logo horizontal colorido", (
        '<div class="duas-pecas" style="top:200px;gap:140px">'
        f'<div class="peca-box">{_img(a("logo-horizontal-roxo.svg"), "Logo horizontal roxo", "width:660px;height:auto")}</div>'
        f'<div class="peca-box">{_img(a("logo-horizontal-laranja.svg"), "Logo horizontal laranja", "width:660px;height:auto")}</div>'
        '</div>' + _num_pg(12)
    )))

    # P13 · Logo horizontal monocromático
    slides.append(_slide(13, "Logo horizontal monocromático", (
        '<div class="duas-pecas" style="top:190px;gap:90px">'
        f'<div class="peca-box">{_img(a("logo-horizontal-preto.svg"), "Logo horizontal preto", "width:660px;height:auto")}</div>'
        f'<div class="peca-box peca-box--preto">{_img(a("logo-horizontal-branco.svg"), "Logo horizontal branco", "width:660px;height:auto")}</div>'
        '</div>' + _num_pg(13)
    )))

    # P14 · Redução do logo vertical
    slides.append(_slide(14, "Redução do logo vertical", (
        '<h2 class="sec-h">Redução do logo vertical</h2>'
        '<div class="col-txt" style="width:820px">'
        '<p>Para manter a legibilidade do logo em ambientes digitais, o logo não pode ser apresentado menor que 101 x 176 px.</p>'
        '<p>Em impressos, mantenha a altura do logo acima de 3 cm.</p>'
        '</div>'
        f'<div style="position:absolute;left:160px;top:415px">{_img(a("p14-reducao-logo-vertical.svg"), "Redução do logo vertical", "width:1560px;height:auto")}</div>'
        + _num_pg(14)
    )))

    # P15 · Redução do logo horizontal
    slides.append(_slide(15, "Redução do logo horizontal", (
        '<h2 class="sec-h">Redução do logo horizontal</h2>'
        '<div class="col-txt" style="width:820px">'
        '<p>Para manter a legibilidade do logo em ambientes digitais, o logo não pode ser apresentado menor que 200 x 89 px.</p>'
        '<p>Em impressos, mantenha a largura do logo acima de 4 cm.</p>'
        '</div>'
        f'<div style="position:absolute;left:160px;top:460px">{_img(a("p15-reducao-logo-horizontal.svg"), "Redução do logo horizontal", "width:1580px;height:auto")}</div>'
        + _num_pg(15)
    )))

    # P16 · Logo em suportes coloridos
    slides.append(_slide(16, "Logo em suportes coloridos", (
        '<h2 class="sec-h">Logo em suportes coloridos</h2>'
        '<div class="col-txt" style="width:820px">'
        '<p>Em fundos com cores chapadas, recomenda-se o uso da paleta de cores do Lab Escola 3D (ver página 21).</p>'
        '<p>Não use o logo sobre gradientes nem em fundos com a mesma cor do logo.</p>'
        '</div>'
        f'<div style="position:absolute;left:128px;top:495px">{_img(a("p16-suportes-coloridos.svg"), "Logo em suportes coloridos", "width:1660px;height:auto")}</div>'
        + _num_pg(16)
    )))

    # P17 · Logo em imagens coloridas
    slides.append(_slide(17, "Logo em imagens coloridas", (
        '<h2 class="sec-h">Logo em imagens coloridas</h2>'
        '<div class="col-txt" style="width:840px">'
        '<p>Atenção ao usar o logo em imagens. Não o posicione em cantos onde as cores se pareçam muito com a cor da logo ou demais situações que comprometam sua legibilidade. Tente escolher um espaço o mais limpo possível.</p>'
        '</div>'
        f'<div style="position:absolute;left:128px;top:470px">{_img(a("p17-aplicacao-fundos-coloridos.svg"), "Posicionamento em zonas limpas de fundos coloridos", "width:1664px;height:auto")}</div>'
        + _num_pg(17)
    )))

    # P18 · Usos indevidos do logo
    usos_cards = "".join(
        f'<div class="uso-item">{_img(a(fn), tit)}'
        f'<p>{E(tit)}' + (f'<br><span class="nota-b">Nota:</span> ver pág 22' if nota else '') + '</p></div>'
        for fn, tit, nota in USOS_INDEVIDOS
    )
    slides.append(_slide(18, "Usos indevidos do logo", (
        '<h2 class="sec-h">Usos indevidos do logo</h2>'
        '<div class="col-txt" style="width:820px"><p>Pedimos para não alterar o logo a fim de manter sua aparência geral intacta. Abaixo, alguns exemplos.</p></div>'
        f'<div class="usos-grid">{usos_cards}</div>'
        + _num_pg(18)
    )))

    # P19 · Divisória IDENTIDADE
    slides.append(_slide(19, "Divisória Identidade", (
        '<h2 class="div-titulo">IDENTIDADE</h2>'
        '<p class="div-sub">Tipos, cores e padrões</p>'
    ), "slide--laranja"))

    # P20 · Tipografia
    slides.append(_slide(20, "Tipografia", (
        '<h2 class="sec-h">Tipografia</h2>'
        '<div class="col-txt" style="width:760px">'
        '<p>A fonte primária do Lab Escola 3D é a Bebas Neue, sem serifa notória por sua imponência expressa pela sua verticalidade e espessura acentuada.</p>'
        '<p>Recomenda-se uso em títulos grandes e informações de destaque. Pode ser usada como uma fonte display.</p>'
        '<p>A fonte secundária é a Roboto, com seu estilo leve, moderno e versátil sendo uma excelente união com a fonte primária.</p>'
        '<p>Recomenda-se uso dos pesos bold ou semibold em títulos menores, com os pesos regular ou light em textos corridos.</p>'
        '</div>'
        '<div class="tipo-col">'
        '<p class="tipo-pri-t">OLÁ, SOU A FONTE PRIMÁRIA</p>'
        '<p class="tipo-pri-a">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>0 1 2 3 4 5 6 7 8 9 .,:;“”!?@#$%^&amp;*[]+=&lt;&gt;|\\/</p>'
        '<p class="tipo-sec-t">Olá, sou a fonte secundária</p>'
        '<p class="tipo-sec-a">abcdefghijklmnopqrstuvwxyz<br>ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>0 1 2 3 4 5 6 7 8 9 .,:;\'"!?@#$%^&amp;*()+=&lt;&gt;|\\/</p>'
        '</div>' + _num_pg(20)
    )))

    # P21 · Cores
    slides.append(_slide(21, "Cores", (
        '<h2 class="sec-h">Cores</h2>'
        '<div class="col-txt" style="width:740px">'
        '<p>O Lab Escola 3D expressa sua linguagem por meio de sua paleta de cores composta pela sobriedade do roxo e energia do laranja, indo de encontro com a proposta de inovação educacional e cultura maker que o laboratório foca em desenvolver. De suporte, temos o preto e branco.</p>'
        '<p>A paleta dispensa qualquer tipo de gradientes.</p>'
        '<p><span class="nota-b">Nota:</span> para evitar o preto de sair com aspecto lavado em impressos, use a mistura CMYK especificada.</p>'
        '</div>'
        f'<div style="position:absolute;right:150px;top:216px">{_img(a("p21-paleta-cores.svg"), "Paleta de cores oficial", "width:700px;height:auto")}</div>'
        + _num_pg(21)
    )))

    # P22 · Padrões visuais
    slides.append(_slide(22, "Padrões visuais", (
        '<h2 class="sec-h">Padrões visuais</h2>'
        '<div class="col-txt" style="width:740px">'
        '<p>O ícone do Lab Escola 3D é ideal para qualquer tipo de padronagem, incrementos ou repetições visuais. Contanto que a aplicação do ícone se mantenha alinhada com os guias de uso no manual, outros tipos de padrões e estampas são permitidas.</p>'
        '<p><span class="nota-b">Nota:</span> apenas em aplicações de padronagens e afins, a rotação do ícone é permitida.</p>'
        '<p>A seguir, exemplos de padrões visuais com o ícone.</p>'
        '</div>'
        f'<div style="position:absolute;right:160px;top:220px">{_img(a("p22-padrao-amostra.svg"), "Amostra de padrão visual", "width:740px;height:auto")}</div>'
        + _num_pg(22)
    )))

    # P23 · Sugestões de padrões
    slides.append(_slide(23, "Sugestões de padrões", (
        '<h2 class="sec-h">Sugestões de padrões</h2>'
        '<div class="padroes-duo">'
        f'{_img(a("p23-padrao-roxo.svg"), "Sugestão de padrão roxo")}'
        f'{_img(a("p23-padrao-laranja.svg"), "Sugestão de padrão laranja")}'
        '</div>' + _num_pg(23)
    )))

    # P24–P26 · Padrões full-bleed
    slides.append(_slide(24, "Padrão dividido roxo e laranja",
                         _img(a("p24-padrao-dividido-16x9.svg"), "Padrão dividido roxo e laranja", "width:1920px;height:1080px;display:block"), "slide--full"))
    slides.append(_slide(25, "Padrão ampliado roxo",
                         _img(a("p25-padrao-grande-roxo-16x9.svg"), "Padrão ampliado roxo", "width:1920px;height:1080px;display:block"), "slide--full"))
    slides.append(_slide(26, "Padrão ampliado laranja",
                         _img(a("p26-padrao-grande-laranja-16x9.svg"), "Padrão ampliado laranja", "width:1920px;height:1080px;display:block"), "slide--full"))

    # P27 · Aplicações
    slides.append(_slide(27, "Aplicações", (
        '<h2 class="sec-h">Aplicações</h2>'
        '<div class="col-txt" style="width:740px">'
        '<p>O logo do Lab Escola 3D é ideal em uma infinidade de suportes e formatos diferentes, adequados para diversas situações, como pôsteres, papelaria institucional, camisas, mochilas, bolsas, entre muitas outras.</p>'
        '<p>A seguir, exemplos de aplicações com o logo.</p>'
        '</div>' + _num_pg(27)
    )))

    # P28 · Camisetas (vetorial LGPD-safe)
    slides.append(_slide(28, "Aplicação em camisetas", (
        '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#F2F2F2">'
        f'{_img(a("p28-aplicacao-camisetas.svg"), "Aplicação esquemática em camisetas", "width:1920px;height:1080px;object-fit:contain")}'
        '</div>'
    ), "slide--full"))

    # P29 · Caneca (vetorial)
    slides.append(_slide(29, "Aplicação em caneca",
                         _img(a("p29-aplicacao-caneca.svg"), "Aplicação esquemática em caneca", "width:1920px;height:1080px;object-fit:cover;display:block"), "slide--full"))

    # P30 · Banner institucional (vetorial LGPD-safe)
    slides.append(_slide(30, "Banner institucional", (
        '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#FFFFFF">'
        f'{_img(a("p30-banner-institucional.svg"), "Banner institucional", "width:1920px;height:600px;display:block")}'
        '</div>'
    ), "slide--full"))

    # P31 · Banner inovação social (vetorial LGPD-safe)
    slides.append(_slide(31, "Banner inovação social", (
        '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#FFFFFF">'
        f'{_img(a("p31-banner-inovacao.svg"), "Banner inovação social", "width:1920px;height:740px;display:block")}'
        '</div>'
    ), "slide--full"))

    # P32 · Persona Profª. Márcia
    poses = "".join(
        _img(a(f"persona-profa-marcia-0{i}.png"), f"Persona Profª. Márcia — pose {i}")
        for i in range(1, 5)
    )
    slides.append(_slide(32, "Persona — Profª. Márcia", (
        f'<div class="persona-wrap">{poses}</div>'
        f'<div class="persona-marca">{_img(a("logo-horizontal-branco.svg"), "Lab Escola 3D")}'
        '<p>Persona - Profª. Márcia</p></div>'
    ), "slide--laranja"))

    # P33 · Contato
    slides.append(_slide(33, "Contato", (
        '<h2 class="sec-h sec-h--branco">Contato</h2>'
        '<div class="col-txt col-txt--branco" style="width:760px">'
        '<p>Se houveram dúvidas, sugestões ou comentários sobre o manual ou o Lab Escola 3D, entre em contato com a gente.</p>'
        '<p><b>labescola3d@gmail.com</b></p>'
        '</div>'
    ), "slide--roxo"))

    return (
        '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="robots" content="noindex">\n'
        '<title>Manual da Marca 2024 (16:9) · Lab Escola 3D</title>\n'
        f'<link rel="stylesheet" href="{GOOGLE_FONTS_URL}">\n'
        f'<style>\n{CSS_CANVA_16X9}\n</style>\n</head>\n<body>\n'
        + "\n\n".join(slides)
        + "\n</body>\n</html>\n"
    )


def gerar_canva_manual(raiz: str | Path) -> str:
    return _escrever(
        Path(raiz) / "canva" / "manual-da-marca" / "index.html",
        render_canva_manual(raiz, embutir_svg=False),
    )


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    print(gerar_identidade_site(base))
    print(gerar_canva_manual(base))
