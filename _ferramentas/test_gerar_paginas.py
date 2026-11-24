import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from checar import checar  # noqa: E402
from catalogo import carregar  # noqa: E402
from gerar_paginas import gerar_catalogo, gerar_home, normalizar, numeros  # noqa: E402

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

    def test_catalogo_tem_15_cards_por_tela(self):
        self.assertEqual(len(re.findall(r'<(?:a|div) class="card[ "]', self.pc)), 15)

    def test_filtro_jogo_mostra_os_4_jogos(self):
        jogos = set(re.findall(r'data-tipo="jogo"[^>]*>.*?<h3>(.*?)</h3>', self.pc, re.S))
        self.assertEqual(jogos, {"Investigadoras do conhecimento", "Expedição Sonora", "Antropolojogo",
                                 "Através do Espelho"})

    def test_card_externo_leva_a_ludopedia_com_credito(self):
        self.assertIn('data-autoria="Raiane"', self.pc)
        self.assertIn("https://ludopedia.com.br/jogo/atraves-do-espelho", self.pc)

    def test_filtros_tem_os_cinco_grupos(self):
        for g in ("tipo", "disciplina", "tempo", "complexidade", "etapa"):
            self.assertIn(f'data-grupo="{g}"', self.pc, g)

    def test_campo_de_busca(self):
        self.assertIn('<input type="search"', self.pc)
        self.assertIn('aria-label="Buscar no catálogo"', self.pc)

    def test_busca_normalizada(self):
        self.assertEqual(normalizar("Matemática ÇÃO"), "matematica cao")
        m = re.search(r'data-busca="([^"]*)"[^>]*>(?:(?!</a>|</div></div>).)*?<h3>Oficina de Costura</h3>', self.pc, re.S)
        self.assertIsNotNone(m)
        self.assertIn("matematica", m.group(1))
        self.assertIn("costura", m.group(1))

    def test_a_confirmar_fica_fora_do_filtro(self):
        m = re.search(r'<(?:a|div) class="card[^"]*"[^>]*data-slug="expedicao-sonora"[^>]*>', self.pc)
        self.assertIsNotNone(m)
        self.assertIn('data-tempo=""', m.group(0))
        self.assertIn('data-disciplinas="Geografia|Arte"', m.group(0))

    def test_estado_vazio(self):
        self.assertIn("Nenhum material com esses filtros", self.pc)
        self.assertIn("Limpar filtros", self.pc)
        self.assertRegex(self.pc, r'class="vazio"[^>]*hidden')

    def test_pagina_que_ainda_nao_existe_vira_card_sem_link(self):
        from gerar_paginas import card
        base = {c["slug"]: c for c in carregar()}["antropolojogo"]
        h = card(dict(base, slug="nao-existe", href="nao-existe/"))
        self.assertRegex(h, r'^<div class="card em-breve"')
        self.assertNotIn('href="nao-existe/"', h)

    def test_numeros_contados_do_json(self):
        self.assertEqual(numeros(carregar()), [("4 jogos", "para baixar e jogar"),
                                               ("4 oficinas", "e formações para professores"),
                                               ("3 materiais", "para preparar a aula"),
                                               ("15 materiais", "no catálogo")])
        self.assertIn("15 materiais", self.pc)

    def test_card_com_imagem_usa_img_e_sem_imagem_reserva(self):
        from gerar_paginas import card
        base = {c["slug"]: c for c in carregar()}["antropolojogo"]
        com = dict(base, imagem={"arquivo": "_base/capas/antropolojogo.jpg", "alt": "Tabuleiro", "origem_canva": "X"})
        h = card(com)
        self.assertIn('<img class="capa" src="../_base/capas/antropolojogo.jpg" alt="Tabuleiro"', h)
        self.assertIn('loading="lazy"', h)
        self.assertNotIn("reservada", h)
        self.assertIn("reservada", card(dict(base, imagem=None)))


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
