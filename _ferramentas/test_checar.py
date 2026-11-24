import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from checar import checar  # noqa: E402

BASE = os.path.join(os.path.dirname(__file__), "..", "_base", "site.css")

BOA = """<!doctype html><html><head>
<style>.x{}</style></head><body>
<section class="tela tela--pc" data-document-role="page" data-label="pc">
  <img src="../_base/icones/lupa.svg" alt="Buscar">
  <a href="../catalogo/">Catálogo</a>
  <a class="botao baixar" href="arquivos/kit.pdf">Baixar</a>
  <a class="card externo" data-autoria="Raiane" href="https://ludopedia.com.br/jogo/x">X</a>
</section>
<section class="tela tela--cel" data-document-role="page" data-label="cel"><h1>Titulo</h1></section>
</body></html>"""


def rodar(html, arquivos=("arquivos/kit.pdf",)):
    pasta = tempfile.mkdtemp()
    for a in arquivos:
        caminho = os.path.join(pasta, a)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        open(caminho, "wb").close()
    f = os.path.join(pasta, "index.html")
    with open(f, "w", encoding="utf-8") as h:
        h.write(html)
    return " | ".join(checar(f)).lower()


class TestChecar(unittest.TestCase):
    def test_css_local_externo_falha(self):
        self.assertIn("css", rodar(BOA.replace(
            "</head>", '<link rel="stylesheet" href="../_base/site.css"></head>')))

    def test_tela_boa_passa(self):
        self.assertEqual(rodar(BOA), "")

    def test_tela_sem_data_label_falha(self):
        self.assertIn("data-label", rodar(BOA.replace(' data-label="pc"', "")))

    def test_tela_aninhada_falha(self):
        html = BOA.replace("<h1>Titulo</h1>",
                           '<div data-document-role="page" data-label="x"></div>')
        self.assertIn("aninhad", rodar(html))

    def test_fonte_de_icones_falha(self):
        self.assertIn("ícone", rodar(BOA.replace("<h1>", '<i class="fas fa-search"></i><h1>')))
        self.assertIn("ícone", rodar(BOA.replace(
            "</head>", '<link rel="stylesheet" href="https://x/font-awesome/all.css"></head>')))

    def test_link_interno_absoluto_falha(self):
        self.assertIn("relativo", rodar(BOA.replace('href="../catalogo/"', 'href="/catalogo/x/"')))

    def test_link_para_drive_ou_instagram_como_download_falha(self):
        html = BOA.replace('href="arquivos/kit.pdf"', 'href="https://drive.google.com/file/d/1"')
        self.assertIn("drive", rodar(html))
        html = BOA.replace('href="arquivos/kit.pdf"', 'href="https://www.instagram.com/x"')
        self.assertIn("drive", rodar(html))

    def test_email_ou_telefone_no_texto_falha(self):
        self.assertIn("dado pessoal", rodar(BOA.replace("Titulo", "fale com a@b.com")))
        self.assertIn("dado pessoal", rodar(BOA.replace("Titulo", "(21) 99999-0000")))

    def test_img_sem_alt_falha(self):
        self.assertIn("alt", rodar(BOA.replace(' alt="Buscar"', "")))

    def test_botao_baixar_aponta_para_arquivo_existente(self):
        self.assertIn("arquivo", rodar(BOA, arquivos=()))

    def test_tela_celular_tem_largura_fixa_e_quebra_titulo(self):
        css = open(BASE, encoding="utf-8").read()
        self.assertIn(".tela--cel", css)
        self.assertIn("width: 375px", css)
        self.assertIn("overflow-wrap: anywhere", css)

    def test_card_externo_tem_credito_e_destino(self):
        self.assertIn("externo", rodar(BOA.replace(' data-autoria="Raiane"', "")))
        self.assertIn("externo", rodar(BOA.replace('href="https://ludopedia.com.br/jogo/x"', 'href="x/"')))

    def test_iframe_sem_title_reprova(self):
        self.assertIn("iframe", rodar(BOA.replace("</section>", '<iframe src="https://www.printables.com/embed/1"></iframe></section>', 1)))

    def test_capa_acima_de_80kb_reprova(self):
        pasta = tempfile.mkdtemp()
        os.makedirs(os.path.join(pasta, "capas"))
        with open(os.path.join(pasta, "capas", "x.jpg"), "wb") as h:
            h.write(b"0" * (81 * 1024))
        f = os.path.join(pasta, "index.html")
        with open(f, "w", encoding="utf-8") as h:
            h.write('<section data-document-role="page" data-label="a"><img class="capa" src="capas/x.jpg" alt="x"></section>')
        self.assertIn("capa pesada", " | ".join(checar(f)))

    def test_capa_leve_passa(self):
        pasta = tempfile.mkdtemp()
        os.makedirs(os.path.join(pasta, "capas"))
        with open(os.path.join(pasta, "capas", "x.jpg"), "wb") as h:
            h.write(b"0" * (40 * 1024))
        f = os.path.join(pasta, "index.html")
        with open(f, "w", encoding="utf-8") as h:
            h.write('<section data-document-role="page" data-label="a"><img class="capa" src="capas/x.jpg" alt="x"></section>')
        self.assertEqual(checar(f), [])


if __name__ == "__main__":
    unittest.main()
