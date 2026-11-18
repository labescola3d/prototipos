import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from checar import checar  # noqa: E402
from gerar_produtos import PRODUTOS, gerar_todos  # noqa: E402

RAIZ = os.path.join(os.path.dirname(__file__), "..")
SLUGS = {"investigadoras-do-conhecimento", "expedicao-sonora", "oficina-de-gamificacao",
         "curso-maker-de-ferias-2025", "memorias-da-mare", "antropolojogo", "manual-maker"}


class TestGerarProdutos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arquivos = gerar_todos(RAIZ)

    def ler(self, slug):
        with open(os.path.join(RAIZ, "catalogo", slug, "index.html"), encoding="utf-8") as f:
            return f.read()

    def test_gera_as_7_paginas_da_fase_1(self):
        self.assertEqual({p["slug"] for p in PRODUTOS}, SLUGS)
        self.assertEqual(len(self.arquivos), 7)

    def test_toda_pagina_passa_no_validador(self):
        for arq in self.arquivos:
            self.assertEqual(checar(arq), [], arq)

    def test_toda_pagina_tem_tela_de_computador_e_de_celular(self):
        for slug in SLUGS:
            html = self.ler(slug)
            self.assertEqual(html.count('data-document-role="page"'), 2, slug)

    def test_toda_pagina_tem_licenca(self):
        for slug in SLUGS:
            self.assertIn("CC BY-NC-SA 4.0", self.ler(slug), slug)

    def test_sem_arquivo_aprovado_mostra_aviso_e_nao_botao(self):
        html = self.ler("memorias-da-mare")
        self.assertIn('class="aviso"', html)
        self.assertNotIn(' baixar"', html)
        self.assertNotIn('class="baixar"', html)

    def test_parceria_tem_selo_e_creditos(self):
        html = self.ler("memorias-da-mare")
        self.assertIn("Parceria", html)
        self.assertIn("Rio DESIS Lab", html)
        self.assertIn("Redes da Maré", html)

    def test_investigadoras_baixa_o_kit_do_site(self):
        self.assertIn("/wp-content/uploads/2026/11/Investigadoras_do_Conhecimento_PnP_v0.pdf",
                      self.ler("investigadoras-do-conhecimento"))


if __name__ == "__main__":
    unittest.main()
