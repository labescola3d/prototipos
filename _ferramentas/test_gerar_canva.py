import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from checar import checar  # noqa: E402
from gerar_canva import TELAS_CANVA, gerar_todos_canva  # noqa: E402

RAIZ = os.path.join(os.path.dirname(__file__), "..")
ESPERADAS = [
    "home",
    "catalogo",
    "investigadoras-do-conhecimento",
    "manuais",
    "licenca",
    "contribuir",
    "em-obras",
]


def ler(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()


class TestGerarCanva(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arquivos = gerar_todos_canva(RAIZ)

    def test_gera_todas_as_telas_e_indice(self):
        self.assertEqual(TELAS_CANVA, ESPERADAS)
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, "canva", "index.html")))
        for slug in ESPERADAS:
            arq = os.path.join(RAIZ, "canva", slug, "index.html")
            self.assertTrue(os.path.isfile(arq), arq)

    def test_todas_passam_no_validador(self):
        for arq in self.arquivos:
            self.assertEqual(checar(arq), [], arq)

    def test_cada_tela_tem_duas_paginas_canva_sem_media_sem_script_sem_alfa(self):
        for slug in ESPERADAS:
            html = ler(os.path.join("canva", slug, "index.html"))
            self.assertEqual(html.count('data-document-role="page"'), 2, slug)
            self.assertIn('class="tela tela--pc"', html, slug)
            self.assertIn('class="tela tela--cel"', html, slug)
            self.assertNotIn("@media", html, slug)
            self.assertNotIn("<script", html, slug)
            self.assertNotIn('class="alfa"', html, slug)
            self.assertIn("width: 1440px", html, slug)
            self.assertIn("width: 375px", html, slug)

    def test_imagens_locais_existem_no_disco(self):
        for slug in ESPERADAS:
            pasta = os.path.join(RAIZ, "canva", slug)
            html = ler(os.path.join("canva", slug, "index.html"))
            for src in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', html):
                if src.startswith("http"):
                    continue
                caminho = os.path.normpath(os.path.join(pasta, src))
                self.assertTrue(os.path.isfile(caminho), (slug, src, caminho))

    def test_catalogo_espelho_tem_15_cards_e_filtros_sem_js(self):
        html = ler(os.path.join("canva", "catalogo", "index.html"))
        pc = html.split('<section class="tela tela--cel"')[0]
        self.assertEqual(len(re.findall(r'<(?:a|div) class="card[ "]', pc)), 15)
        for g in ("tipo", "disciplina", "tempo", "complexidade", "etapa"):
            self.assertIn(f'data-grupo="{g}"', pc, g)
        self.assertNotIn("<script", html)
        self.assertIn('href="../../manuais/"', pc)
        self.assertNotIn("../../catalogo/../", html)

    def test_produto_espelho_links_locais_existem(self):
        html = ler(os.path.join("canva", "investigadoras-do-conhecimento", "index.html"))
        self.assertIn('href="../../catalogo/investigadoras-do-conhecimento/consultor-de-campo.html"', html)
        self.assertIn('href="../../catalogo/investigadoras-do-conhecimento/editor/"', html)

    def test_institucionais_espelho_preservam_conteudo_e_mascotes(self):
        licenca = ler(os.path.join("canva", "licenca", "index.html"))
        self.assertIn("Licença e como usar", licenca)
        self.assertIn('id="canva"', licenca)

        contribuir = ler(os.path.join("canva", "contribuir", "index.html"))
        self.assertIn("labescola3d@gmail.com", contribuir)

        obras = ler(os.path.join("canva", "em-obras", "index.html"))
        self.assertIn('src="../../em-obras/tom.jpg"', obras)
        self.assertIn('src="../../em-obras/vit.jpg"', obras)

    def test_indice_canva_lista_as_7_telas(self):
        indice = ler(os.path.join("canva", "index.html"))
        self.assertNotIn('data-document-role="page"', indice)
        for slug in ESPERADAS:
            self.assertIn(f'href="{slug}/"', indice, slug)


if __name__ == "__main__":
    unittest.main()
