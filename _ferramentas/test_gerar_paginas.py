import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from checar import checar  # noqa: E402
from gerar_paginas import CARDS, gerar_catalogo, gerar_home  # noqa: E402

RAIZ = os.path.join(os.path.dirname(__file__), "..")


def ler(arq):
    with open(arq, encoding="utf-8") as f:
        return f.read()


class TestCatalogo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arq = gerar_catalogo(RAIZ)
        cls.html = ler(cls.arq)
        cls.pc = cls.html.split('<section class="tela tela--cel"')[0]

    def test_catalogo_passa_no_validador(self):
        self.assertEqual(checar(self.arq), [])

    def test_catalogo_tem_duas_telas(self):
        self.assertEqual(self.html.count('data-document-role="page"'), 2)

    def test_catalogo_tem_9_cards_por_tela(self):
        self.assertEqual(len(CARDS), 9)
        self.assertEqual(self.pc.count('<a class="card'), 9)

    def test_filtro_jogo_mostra_os_5_jogos(self):
        jogos = set(re.findall(r'data-tipo="jogo"[^>]*>.*?<h3>(.*?)</h3>', self.pc, re.S))
        self.assertEqual(jogos, {"Investigadoras do conhecimento", "Expedição Sonora", "Antropolojogo",
                                 "Memórias da Maré / Consolidating Maré", "Através do Espelho"})

    def test_card_externo_leva_a_ludopedia_com_credito(self):
        self.assertIn('data-autoria="Raiane"', self.pc)
        self.assertIn("https://ludopedia.com.br/jogo/atraves-do-espelho", self.pc)

    def test_catalogo_leva_as_fichas_do_site(self):
        self.assertIn("https://labescola3d.rio.br/fichas/", self.pc)

    def test_numeros_a_vista(self):
        for n in ("5 jogos", "2 formações", "9 atividades", "6 manuais"):
            self.assertIn(n, self.pc)


class TestHome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arq = gerar_home(RAIZ)
        cls.html = ler(cls.arq)
        cls.pc = cls.html.split('<section class="tela tela--cel"')[0]

    def test_home_passa_no_validador(self):
        self.assertEqual(checar(self.arq), [])

    def test_home_tem_duas_telas(self):
        self.assertEqual(self.html.count('data-document-role="page"'), 2)

    def test_home_leva_ao_catálogo(self):
        self.assertIn('href="catalogo/"', self.pc)
        self.assertIn("Materiais para usar na sua aula", self.pc)

    def test_home_tem_os_4_destaques(self):
        for t in ("Investigadoras do conhecimento", "Expedição Sonora", "Oficina de Gamificação", "Antropolojogo"):
            self.assertIn(t, self.pc)

    def test_menu_sem_itens_suspensos(self):
        self.assertNotIn("sub-menu", self.html)
        self.assertNotIn("seta-baixo", self.html)


if __name__ == "__main__":
    unittest.main()
