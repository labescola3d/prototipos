"""Confere que a política de colaboração v1 está completa neste repositório."""
import os
import re
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VERSAO = "Política de colaboração · v1 · 2026-11-18"
INICIO = "<!-- politica:inicio v1 -->"
FIM = "<!-- politica:fim -->"
EMAILS_PERMITIDOS = {"labescola3d@gmail.com", "noreply@anthropic.com"}
ARQUIVOS = [
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    "docs/decisoes/2026-11-18-politica-de-colaboracao.md",
]


def ler(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()


class TestPolitica(unittest.TestCase):
    def test_agents_tem_versao(self):
        t = ler("AGENTS.md")
        self.assertIn(VERSAO, t)
        self.assertIn(INICIO, t)
        self.assertIn(FIM, t)

    def test_claude_importa_agents(self):
        self.assertEqual(ler("CLAUDE.md").strip(), "@AGENTS.md")

    def test_contributing_tem_versao(self):
        t = ler("CONTRIBUTING.md")
        for trecho in (VERSAO, INICIO, FIM, "Assisted-by:", "squash"):
            self.assertIn(trecho, t)

    def test_codeowners(self):
        linhas = [l.strip() for l in ler(".github/CODEOWNERS").splitlines()]
        self.assertIn("* @ivansssilveira", linhas)

    def test_modelo_de_pedido(self):
        t = ler(".github/pull_request_template.md")
        for trecho in ("Fecha #", "IA usada", "dado pessoal"):
            self.assertIn(trecho, t)

    def test_decisao_registrada(self):
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, ARQUIVOS[-1])))

    def test_acao_roda_testes(self):
        t = ler(".github/workflows/testes.yml")
        for trecho in ("pull_request", "unittest discover -s _ferramentas", "checar.py"):
            self.assertIn(trecho, t)

    def test_sem_dado_pessoal(self):
        for rel in ARQUIVOS:
            achados = set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", ler(rel))) - EMAILS_PERMITIDOS
            self.assertEqual(achados, set(), rel)


if __name__ == "__main__":
    unittest.main()
