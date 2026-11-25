import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from catalogo import carregar  # noqa: E402
from checar import checar  # noqa: E402
from gerar_produtos import PRODUTOS, gerar_todos  # noqa: E402

RAIZ = os.path.join(os.path.dirname(__file__), "..")
SLUGS = {"investigadoras-do-conhecimento", "expedicao-sonora", "oficina-de-gamificacao",
         "curso-maker-de-ferias-2025", "memorias-da-mare", "antropolojogo", "manual-maker",
         "oficina-de-costura", "oficina-makey-makey-3d", "kit-do-professor", "catalogo-de-atividades", "brindes-3d", "kit-de-divulgacao", "visitas-coppei"}


class TestGerarProdutos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arquivos = gerar_todos(RAIZ)

    def ler(self, slug):
        with open(os.path.join(RAIZ, "catalogo", slug, "index.html"), encoding="utf-8") as f:
            return f.read()

    def test_gera_as_paginas(self):
        self.assertEqual({p["slug"] for p in PRODUTOS}, SLUGS)
        self.assertEqual(len(self.arquivos), len(SLUGS))

    def test_oficinas_seguem_o_modelo_da_gamificacao(self):
        for slug in ("oficina-de-costura", "oficina-makey-makey-3d"):
            html = self.ler(slug)
            for s in ("O que é", "Para quem", "De onde veio", "baixar-bloco"):
                self.assertIn(s, html, (slug, s))
            self.assertRegex(html, r'class="(botao botao--grande )?baixar" href="[^h"][^"]*\.pdf"')

    def test_oficinas_sem_dado_de_pesquisa(self):
        for slug in ("oficina-de-costura", "oficina-makey-makey-3d"):
            html = self.ler(slug)
            for proibido in ("Certezas", "Suposições", "Que pena", "Paes"):
                self.assertNotIn(proibido, html, (slug, proibido))

    def test_kit_do_professor_baixa_o_pdf_local(self):
        html = self.ler("kit-do-professor")
        self.assertIn('href="kit-do-professor-a4.pdf"', html)
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, "catalogo", "kit-do-professor", "kit-do-professor-a4.pdf")))

    def test_catalogo_de_atividades_aponta_para_as_fichas(self):
        html = self.ler("catalogo-de-atividades")
        self.assertIn('href="https://labescola3d.rio.br/fichas/"', html)
        self.assertIn("Almofadinhas Geométricas", html)

    def test_costura_credita_a_autora(self):
        self.assertIn("Ana da Hora", self.ler("oficina-de-costura"))

    def test_toda_pagina_passa_no_validador(self):
        for arq in self.arquivos:
            self.assertEqual(checar(arq), [], arq)

    def test_toda_pagina_tem_tela_de_computador_e_de_celular(self):
        for slug in SLUGS - {"manual-maker"}:
            html = self.ler(slug)
            self.assertEqual(html.count('data-document-role="page"'), 2, slug)

    def test_kit_de_divulgacao_usa_a_frase_da_marca_e_nao_a_cc(self):
        from gerar_produtos import FRASE_MARCA
        html = self.ler("kit-de-divulgacao")
        self.assertIn(FRASE_MARCA, html)
        self.assertNotIn("CC BY-NC-SA 4.0", html)

    def test_visitas_e_relato_sem_download(self):
        self.assertNotIn('class="baixar"', self.ler("visitas-coppei"))

    def test_visitas_convida_a_pedir_visita(self):
        html = self.ler("visitas-coppei")
        self.assertIn("Diretoria de Extensão da COPPE", html)
        self.assertIn("[a confirmar]", html)

    def test_visitas_liga_aos_jogos_das_mesas(self):
        html = self.ler("visitas-coppei")
        for s in ("antropolojogo/", "investigadoras-do-conhecimento/", "expedicao-sonora/"):
            self.assertIn(f'href="../{s}"', html)

    def test_toda_pagina_tem_licenca(self):
        for slug in SLUGS - {"kit-de-divulgacao", "visitas-coppei", "manual-maker"}:
            self.assertIn("CC BY-NC-SA 4.0", self.ler(slug), slug)

    def test_mare_baixa_o_rola_rola(self):
        html = self.ler("memorias-da-mare")
        self.assertIn('href="rola-rola.stl"', html)
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, "catalogo", "memorias-da-mare", "rola-rola.stl")))

    def test_brindes_tem_copia_local_e_printables(self):
        html = self.ler("brindes-3d")
        pc, cel = html.split('<section class="tela tela--cel"')
        self.assertIn("Baixe aqui ou acesse a nossa página no Printables", pc)
        self.assertIn('class="baixar"', pc)
        self.assertRegex(pc, r'<iframe [^>]*src="https://www.printables.com/embed/\d+"[^>]*width="400"')
        self.assertRegex(cel, r'<iframe [^>]*src="https://www.printables.com/embed/\d+"[^>]*width="300"')

    def test_peca_sem_printables_so_tem_copia_local(self):
        from gerar_produtos import bloco_pecas
        h = bloco_pecas([{"nome": "X", "ensina": "e", "bncc": "b", "arquivos": [("X", "x.3mf", "3MF")], "printables": None}], "pc")
        self.assertIn('href="x.3mf"', h)
        self.assertNotIn("iframe", h)
        h2 = bloco_pecas([{"nome": "X", "ensina": "e", "bncc": "b", "arquivos": [("X", "x.3mf", "3MF")], "printables": 1875729}], "cel")
        self.assertIn('src="https://www.printables.com/embed/1875729" width="300" height="340"', h2)

    def test_parceria_tem_selo_e_creditos(self):
        html = self.ler("memorias-da-mare")
        self.assertIn("Parceria", html)
        self.assertIn("Rio DESIS Lab", html)
        self.assertIn("Redes da Maré", html)

    def test_investigadoras_baixa_o_kit_do_site(self):
        self.assertIn("/wp-content/uploads/2026/11/Investigadoras_do_Conhecimento_PnP_v0.pdf",
                      self.ler("investigadoras-do-conhecimento"))


    def test_investigadoras_oferece_o_consultor_de_campo(self):
        html = self.ler("investigadoras-do-conhecimento")
        self.assertIn('href="consultor-de-campo.html"', html)
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, "catalogo", "investigadoras-do-conhecimento", "consultor-de-campo.html")))

    def test_investigadoras_credita_a_equipe(self):
        html = self.ler("investigadoras-do-conhecimento")
        self.assertIn("Raiane Pacheco (responsável), Eduardo Cóser e Ivan Silveira", html)
        self.assertNotIn("Equipe: [a confirmar]", html)

    def test_pagina_com_varios_arquivos_mantem_o_editor(self):
        self.assertIn('class="editor" href="editor/"', self.ler("investigadoras-do-conhecimento"))
        self.assertIn('class="editor" href="editor/"', self.ler("expedicao-sonora"))

    def test_oficina_oferece_apostila_ficha_roteiro_e_kit(self):
        html = self.ler("oficina-de-gamificacao")
        self.assertNotIn("está em revisão", html)
        for arq in ("apostila-roteiro-para-o-professor.docx", "ficha-de-planejamento.pdf", "roteiro-oficina-modelo.pdf",
                    "roteiro-oficina-modelo.odt", "kit-do-professor-a4.pdf"):
            self.assertIn(f'href="{arq}"', html, arq)
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, "catalogo", "oficina-de-gamificacao", arq)), arq)

    def test_expedicao_oferece_os_peoes_e_credita_a_equipe(self):
        html = self.ler("expedicao-sonora")
        self.assertIn('href="peoes-tom-e-vit-pacote-c.zip"', html)
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, "catalogo", "expedicao-sonora", "peoes-tom-e-vit-pacote-c.zip")))
        self.assertIn("Eduardo Cóser (responsável)", html)

    def test_celular_mostra_baixar_antes_da_midia(self):
        for p in PRODUTOS:
            if p["slug"] == "manual-maker":
                continue
            html = self.ler(p["slug"])
            pos_cel = html.index('class="tela tela--cel"')
            trecho_cel = html[pos_cel:]
            self.assertIn('class="baixar-bloco"', trecho_cel, p["slug"])
            self.assertIn('class="midia-cel"', trecho_cel, p["slug"])
            self.assertLess(
                trecho_cel.index('class="baixar-bloco"'),
                trecho_cel.index('class="midia-cel"'),
                p["slug"],
            )

    def test_nenhuma_pagina_expoe_nota_interna_sem_pessoas(self):
        for p in PRODUTOS:
            self.assertNotIn("sem pessoas", self.ler(p["slug"]), p["slug"])

    def test_produtos_com_capa_no_catalogo_usam_img_real(self):
        capas = {item["slug"]: item["imagem"] for item in carregar() if item.get("imagem")}
        for p in PRODUTOS:
            if p["slug"] == "manual-maker":
                continue
            if p["slug"] in capas:
                html = self.ler(p["slug"])
                self.assertIn(f'src="../../{capas[p["slug"]]["arquivo"]}"', html, p["slug"])
                self.assertNotIn('class="reservada"', html, p["slug"])

    def test_produtos_sem_capa_mostram_imagem_em_preparacao(self):
        capas = {item["slug"]: item["imagem"] for item in carregar() if item.get("imagem")}
        for p in PRODUTOS:
            if p["slug"] not in capas:
                html = self.ler(p["slug"])
                self.assertIn("Imagem em preparação ·", html, p["slug"])

if __name__ == "__main__":
    unittest.main()


class TestInvestigadoras(unittest.TestCase):
    def test_investigadoras_diz_31_fichas(self):
        gerar_todos(RAIZ)
        with open(os.path.join(RAIZ, "catalogo", "investigadoras-do-conhecimento", "index.html"), encoding="utf-8") as f:
            html = f.read()
        self.assertIn("31 fichas", html)
        self.assertNotIn("33 homenageadas", html)
        self.assertIn("uma ficha para a dupla", html)
