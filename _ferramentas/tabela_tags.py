"""Tabela das tags dos cards, para Ivan validar antes da revisão.

Uso: py -I -X utf8 _ferramentas/tabela_tags.py
Escreve docs/decisoes/2026-11-24-tabela-de-tags.md a partir de _dados/catalogo.json.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogo import A_CONFIRMAR, COMPLEXIDADES, ETAPAS, TEMPOS, TIPOS, carregar  # noqa: E402

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "decisoes", "2026-11-24-tabela-de-tags.md")


def _txt(valor, rotulos=None):
    if valor == A_CONFIRMAR:
        return A_CONFIRMAR
    itens = valor if isinstance(valor, list) else [valor]
    return ", ".join(rotulos[i] if rotulos else i for i in itens)


def tabela(cards: list[dict]) -> str:
    linhas = ["| Card | Tipo | Disciplinas | Tempo | Complexidade | Ano | Anos |",
              "|:--|:--|:--|:--|:--|:--|:--|"]
    for c in cards:
        t = c["tags"]
        linhas.append(f'| {c["titulo"]} | {TIPOS[c["tipo"]]} | {_txt(t["disciplinas"])} | {_txt(t["tempo"], TEMPOS)} | '
                      f'{_txt(t["complexidade"], COMPLEXIDADES)} | {_txt(t["etapas"], ETAPAS)} | {t["anos"]} |')
    return "\n".join(linhas) + "\n"


def escrever() -> str:
    texto = ("# Tabela de tags do catálogo · para validar\n\n"
             "> Gerada de `_dados/catalogo.json` por `_ferramentas/tabela_tags.py`. Corrija no JSON e gere de novo.\n"
             f"> `{A_CONFIRMAR}` = sem fonte: o card fica fora daquele filtro até alguém confirmar.\n\n" + tabela(carregar()))
    with open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    return SAIDA


if __name__ == "__main__":
    print(escrever())
