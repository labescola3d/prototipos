"""Camada de cards do Catálogo: tipo, tags, imagem e destino de cada material.

Os dados moram em _dados/catalogo.json. Este módulo lê e confere os valores
contra as listas fixas do desenho (docs/decisoes/2026-11-24-catalogo-v2-desenho.md).
Onde falta fonte, a tag vale "[a confirmar]" e o card fica fora daquele filtro.
"""
import json
import os

TIPOS = {"jogo": "Jogos", "oficina": "Oficinas e formações", "professor": "Para o professor",
         "pecas3d": "Peças 3D", "divulgacao": "Divulgação", "visitas": "Visitas e parcerias"}
DISCIPLINAS = ["Matemática", "Ciências", "Geografia", "História", "Arte", "Língua Portuguesa",
               "Educação Física", "Língua Inglesa", "Computação", "Transversal"]
TEMPOS = {"ate-50": "Até 50 min (1 tempo)", "50-100": "50 a 100 min (2 tempos)",
          "mais-100": "Mais de 100 min (projeto ou oficina)"}
COMPLEXIDADES = {"facil": "Fácil: só imprimir e usar", "medio": "Médio: pede montagem ou material comprado",
                 "dificil": "Difícil: pede impressora 3D, eletrônica ou formação antes"}
ETAPAS = {"infantil": "Educação Infantil", "fund1": "Fundamental I (1º ao 5º)",
          "fund2": "Fundamental II (6º ao 9º)", "medio": "Ensino Médio"}
A_CONFIRMAR = "[a confirmar]"

ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_dados", "catalogo.json")
CAMPOS = ("slug", "titulo", "tipo", "selo", "frase", "href", "imagem", "autoria_externa", "tags")


def carregar(caminho: str | None = None) -> list[dict]:
    with open(caminho or ARQUIVO, encoding="utf-8") as f:
        return json.load(f)


def _lista(valor, permitidos, nome):
    if valor == A_CONFIRMAR:
        return []
    if not isinstance(valor, list) or not valor:
        return [f"{nome}: precisa ser lista não vazia ou {A_CONFIRMAR}"]
    return [f"{nome}: valor fora da lista: {v}" for v in valor if v not in permitidos]


def _um(valor, permitidos, nome):
    if valor == A_CONFIRMAR or valor in permitidos:
        return []
    return [f"{nome}: valor fora da lista: {valor}"]


def validar(card: dict) -> list[str]:
    problemas = [f"campo ausente: {c}" for c in CAMPOS if c not in card]
    if problemas:
        return problemas
    problemas += _um(card["tipo"], TIPOS, "tipo")
    t = card["tags"]
    problemas += _lista(t.get("disciplinas"), DISCIPLINAS, "disciplinas")
    problemas += _um(t.get("tempo"), TEMPOS, "tempo")
    problemas += _um(t.get("complexidade"), COMPLEXIDADES, "complexidade")
    problemas += _lista(t.get("etapas"), ETAPAS, "etapas")
    if not isinstance(t.get("anos"), str):
        problemas.append("anos: precisa ser texto")
    return problemas
