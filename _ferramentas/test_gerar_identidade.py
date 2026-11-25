import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from checar import checar  # noqa: E402
from gerar_identidade import gerar_canva_manual, gerar_identidade_site  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SVGS_ESPERADOS = (
    [f"logo-horizontal-{c}.svg" for c in ("roxo", "laranja", "preto", "branco")]
    + [f"logo-vertical-{c}.svg" for c in ("roxo", "laranja", "preto", "branco")]
    + [f"icone-{c}.svg" for c in ("roxo", "laranja", "preto", "branco")]
    + [
        "p06-area-protecao-logo-horizontal.svg",
        "p06-area-protecao-logo-vertical.svg",
        "p08-area-protecao-icone.svg",
        "p09-estrutura-icone.svg",
        "p14-reducao-logo-vertical.svg",
        "p15-reducao-logo-horizontal.svg",
        "p16-suportes-coloridos.svg",
        "p17-aplicacao-fundos-coloridos.svg",
        "p21-paleta-cores.svg",
        "p22-padrao-amostra.svg",
        "p23-padrao-roxo.svg",
        "p23-padrao-laranja.svg",
        "p24-padrao-dividido-16x9.svg",
        "p25-padrao-grande-roxo-16x9.svg",
        "p26-padrao-grande-laranja-16x9.svg",
        "p28-aplicacao-camisetas.svg",
        "p29-aplicacao-caneca.svg",
        "p30-banner-institucional.svg",
        "p31-banner-inovacao.svg",
    ]
    + [
        "p18-01-nao-rotacione.svg",
        "p18-02-nao-altere-fonte.svg",
        "p18-03-nao-distorca.svg",
        "p18-04-nao-aplique-fotos.svg",
        "p18-05-nao-pinte-icone.svg",
        "p18-06-nao-mude-cores.svg",
        "p18-07-nao-use-contornos.svg",
        "p18-08-nao-reflita.svg",
        "p18-09-nao-aplique-efeitos.svg",
        "p18-10-nao-altere-icone.svg",
    ]
)

PERSONA_PNGS = [f"persona-profa-marcia-0{i}.png" for i in range(1, 5)]


def ler(rel: str) -> str:
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()


class TestGerarIdentidade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arq_site = gerar_identidade_site(RAIZ)
        cls.arq_canva = gerar_canva_manual(RAIZ)

    def test_svgs_e_persona_existem(self):
        pasta = os.path.join(RAIZ, "identidade", "manual")
        for nome in SVGS_ESPERADOS + PERSONA_PNGS:
            self.assertTrue(os.path.isfile(os.path.join(pasta, nome)), nome)

    def test_validador_passa_sem_erros(self):
        self.assertEqual(checar(self.arq_site), [])
        self.assertEqual(checar(self.arq_canva), [])
        self.assertEqual(checar(os.path.join(RAIZ, "canva", "index.html")), [])

    def test_pagina_identidade_tem_estrutura_manual_e_galeria_preservada(self):
        html = ler(os.path.join("identidade", "index.html"))
        self.assertIn('class="alfa"', html)
        for href in ("../catalogo/", "../licenca/", "../contribuir/", "../em-obras/", "../canva/manual-da-marca/"):
            self.assertIn(f'href="{href}"', html, href)

        for trecho in (
            "Quem somos",
            "Logo",
            "Área de proteção",
            "Ícone",
            "Estrutura do ícone",
            "Redução",
            "Suportes coloridos",
            "Imagens coloridas",
            "Usos indevidos",
            "Tipografia",
            "#3026AD",
            "#E3630D",
            "Padrões visuais",
            "Aplicações",
            "labescola3d@gmail.com",
            "Bebas Neue",
            "Roboto",
            "22,34",
        ):
            self.assertIn(trecho, html, trecho)

        # Preservação integral da galeria de candidatos e kit do professor
        for pasta in ("marca/", "elementos/site-2024/", "elementos/canva-2026/", "gabaritos-professor/"):
            self.assertIn(pasta, html, pasta)
        for img in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', html):
            if img.startswith("http"):
                continue
            caminho = os.path.normpath(os.path.join(RAIZ, "identidade", img))
            self.assertTrue(os.path.isfile(caminho), (img, caminho))

    def test_canva_manual_33_slides_16x9(self):
        html = ler(os.path.join("canva", "manual-da-marca", "index.html"))
        self.assertEqual(html.count('data-document-role="page"'), 33)
        labels = re.findall(r'data-label="([^"]+)"', html)
        self.assertEqual(len(labels), 33)
        self.assertEqual(len(set(labels)), 33)
        for i, lbl in enumerate(labels, 1):
            self.assertTrue(lbl.startswith(f"P{i:02d}"), (i, lbl))
        self.assertIn("1920px", html)
        self.assertIn("1080px", html)
        self.assertNotIn("@media", html)
        self.assertNotIn("<script", html)
        self.assertNotIn('class="alfa"', html)

        pasta = os.path.join(RAIZ, "canva", "manual-da-marca")
        for img in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', html):
            if img.startswith(("http", "data:")):
                continue
            caminho = os.path.normpath(os.path.join(pasta, img))
            self.assertTrue(os.path.isfile(caminho), (img, caminho))

    def test_indice_canva_lista_manual_da_marca(self):
        indice = ler(os.path.join("canva", "index.html"))
        self.assertIn('href="manual-da-marca/"', indice)


if __name__ == "__main__":
    unittest.main()
