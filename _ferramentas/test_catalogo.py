import collections
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from catalogo import A_CONFIRMAR, carregar, validar  # noqa: E402


def _card(**tags):
    base = {"disciplinas": ["Matemática"], "tempo": "ate-50", "complexidade": "facil",
            "etapas": ["fund2"], "anos": "6º ano"}
    base.update(tags)
    return {"slug": "x", "titulo": "X", "tipo": "jogo", "selo": "Jogo", "frase": "f",
            "href": "x/", "imagem": None, "autoria_externa": None, "tags": base}


class TestCatalogo(unittest.TestCase):
    def test_tem_15_cards_com_slugs_unicos(self):
        cards = carregar()
        self.assertEqual(len(cards), 15)
        self.assertEqual(len({c["slug"] for c in cards}), 15)

    def test_todo_card_e_valido(self):
        for c in carregar():
            self.assertEqual(validar(c), [], c["slug"])

    def test_valor_fora_da_lista_reprova(self):
        problemas = validar(_card(tempo="45 min"))
        self.assertTrue(any("tempo" in p for p in problemas), problemas)

    def test_disciplina_fora_da_lista_reprova(self):
        self.assertTrue(validar(_card(disciplinas=["Física"])))

    def test_a_confirmar_e_aceito_em_toda_tag(self):
        c = _card(disciplinas=A_CONFIRMAR, tempo=A_CONFIRMAR, complexidade=A_CONFIRMAR,
                  etapas=A_CONFIRMAR, anos=A_CONFIRMAR)
        self.assertEqual(validar(c), [])

    def test_tipos_dos_15(self):
        cont = collections.Counter(c["tipo"] for c in carregar())
        self.assertEqual(dict(cont), {"jogo": 4, "oficina": 4, "professor": 3, "pecas3d": 1,
                                      "divulgacao": 1, "visitas": 2})

    def test_manual_maker_leva_a_manuais(self):
        mm = {c["slug"]: c for c in carregar()}["manual-maker"]
        self.assertEqual(mm["href"], "../manuais/")


if __name__ == "__main__":
    unittest.main()
