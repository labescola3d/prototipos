import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from checar import checar  # noqa: E402
from gerar_manuais import VOLUMES, gerar_manuais  # noqa: E402
from gerar_produtos import gerar_todos  # noqa: E402

RAIZ = os.path.join(os.path.dirname(__file__), "..")


def ler(*partes):
    with open(os.path.join(RAIZ, *partes), encoding="utf-8") as f:
        return f.read()


class TestManuais(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        gerar_todos(RAIZ)
        cls.arq = gerar_manuais(RAIZ)
        cls.html = ler("manuais", "index.html")
        cls.pc = cls.html.split('<section class="tela tela--cel"')[0]

    def test_manuais_passa_no_validador(self):
        self.assertEqual(checar(self.arq), [])

    def test_manuais_tem_6_cards_de_volume_com_licenca(self):
        self.assertEqual(len(VOLUMES), 6)
        self.assertEqual(len(re.findall(r'<div class="volume"', self.pc)), 6)
        self.assertIn("CC BY-NC-SA 4.0", self.pc)
        self.assertEqual(self.html.count('data-document-role="page"'), 2)

    def test_manuais_sem_o_kit_das_investigadoras(self):
        self.assertNotIn("Investigadoras", self.html)

    def test_manual_maker_antigo_redireciona(self):
        antigo = ler("catalogo", "manual-maker", "index.html")
        self.assertIn('http-equiv="refresh"', antigo)
        self.assertIn('content="0; url=../../manuais/"', antigo)

    def test_card_do_catalogo_aponta_para_manuais(self):
        from gerar_paginas import gerar_catalogo
        self.assertIn('href="../manuais/"', ler(*os.path.relpath(gerar_catalogo(RAIZ), RAIZ).split(os.sep)))


if __name__ == "__main__":
    unittest.main()
