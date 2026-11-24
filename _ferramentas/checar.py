"""Validador das telas do protótipo: regras do Canva e da publicação.

Uso: py -I -X utf8 _ferramentas/checar.py arquivo.html [...]
Sai com código 1 se houver problema.
"""
import os
import re
import sys
from html.parser import HTMLParser

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
EMAIL_INSTITUCIONAL = {"labescola3d@gmail.com"}  # canal oficial do Lab: não é dado pessoal
TELEFONE = re.compile(r"\(?\b\d{2}\)?\s?9?\d{4}-?\d{4}\b")
PROIBIDO_NO_DOWNLOAD = ("drive.google.com", "docs.google.com", "instagram.com")
CAPA_MAX = 80 * 1024  # capa de card: site leve no celular
VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class _Leitor(HTMLParser):
    def __init__(self, pasta):
        super().__init__(convert_charrefs=True)
        self.pasta = pasta
        self.problemas = []
        self.pilha = []          # True quando a tag aberta é uma tela
        self.fora_de_script = True

    def _p(self, msg):
        self.problemas.append(msg)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if a.get("data-document-role") == "page":
            if any(self.pilha):
                self._p("tela aninhada dentro de outra tela")
            if not a.get("data-label"):
                self._p("tela sem data-label")
        if tag == "i" and any(c.startswith("fa") for c in classes):
            self._p("ícone de fonte (use SVG ou imagem)")
        if tag == "link" and re.search(r"font-?awesome", a.get("href") or "", re.I):
            self._p("ícone de fonte carregado (font-awesome)")
        if (tag == "link" and a.get("rel") == "stylesheet"
                and not (a.get("href") or "").startswith("https://fonts.googleapis.com")):
            self._p(f"css externo não chega ao Canva (embutir na página): {a.get('href')}")
        if tag == "img" and "alt" not in a:
            self._p(f"img sem alt: {a.get('src')}")
        if tag == "iframe" and not a.get("title"):
            self._p(f"iframe sem title: {a.get('src')}")
        if tag == "img" and "capa" in classes:
            src = a.get("src") or ""
            local = os.path.join(self.pasta, src)
            if not src.startswith("http") and not os.path.isfile(local):
                self._p(f"capa sem arquivo: {src}")
            elif not src.startswith("http") and os.path.getsize(local) > CAPA_MAX:
                self._p(f"capa pesada (mais de 80 KB): {src}")
        if tag == "a":
            href = a.get("href") or ""
            if href.startswith("/") and not href.startswith("//"):
                self._p(f"link interno deve ser relativo: {href}")
            if "baixar" in classes:
                if any(d in href for d in PROIBIDO_NO_DOWNLOAD):
                    self._p(f"download aponta para drive/instagram: {href}")
                elif not href.startswith("http") and not os.path.exists(os.path.join(self.pasta, href)):
                    self._p(f"botão baixar sem arquivo: {href}")
            if "externo" in classes and (not a.get("data-autoria") or not href.startswith("https://")):
                self._p("card externo sem data-autoria ou sem destino https://")
        if tag in ("script", "style"):
            self.fora_de_script = False
        if tag not in VAZIOS:
            self.pilha.append(a.get("data-document-role") == "page")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.fora_de_script = True
        if tag not in VAZIOS and self.pilha:
            self.pilha.pop()

    def handle_data(self, data):
        texto = data
        for e in EMAIL_INSTITUCIONAL:
            texto = texto.replace(e, "")
        if self.fora_de_script and (EMAIL.search(texto) or TELEFONE.search(texto)):
            self._p(f"dado pessoal no texto: {data.strip()[:40]}")


def checar(caminho_html: str) -> list[str]:
    leitor = _Leitor(os.path.dirname(os.path.abspath(caminho_html)))
    with open(caminho_html, encoding="utf-8") as f:
        leitor.feed(f.read())
    return leitor.problemas


if __name__ == "__main__":
    ruim = False
    for arq in sys.argv[1:]:
        for p in checar(arq):
            print(f"{arq}: {p}")
            ruim = True
    sys.exit(1 if ruim else 0)
