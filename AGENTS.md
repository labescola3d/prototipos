# AGENTS.md — prototipos

Diretiva para **qualquer agente de IA** que trabalhe neste repositório. Leia inteiro antes de mudar qualquer arquivo.

## Este repositório

- Vitrine alfa do site do **Lab Escola 3D (LE3D)**, projeto de extensão da UFRJ: materiais educacionais gratuitos para professoras da rede pública.
- **Público e indexado.** Cada junção na `main` publica em https://labescola3d.github.io/prototipos/ em cerca de um minuto.
- HTML e CSS estáticos, sem framework. Python só nas ferramentas de `_ferramentas/`.
- Identidade visual, princípios das telas e regras de produção: [`PARA_IA.md`](PARA_IA.md).
- Licença: CC BY-NC-SA 4.0 para materiais e código ([`LICENSE`](LICENSE)).

## Comandos

```
py -I -X utf8 -m unittest discover -s _ferramentas        # testes
py -I -X utf8 _ferramentas/checar.py <arquivo.html> ...   # validador das telas
py -I -X utf8 _ferramentas/gerar_produtos.py               # páginas de material
py -I -X utf8 _ferramentas/gerar_paginas.py                # Home e Catálogo
py -I -X utf8 _ferramentas/gerar_institucionais.py         # Como usar e Contribuir
```

Sem o `py` (Linux, macOS), use `python3`.

## Regras deste repositório

- **Mude o gerador, nunca o HTML gerado.** As páginas de material, a Home, o Catálogo e as institucionais saem de `_ferramentas/gerar_*.py`; edição à mão some na próxima geração. Gere de novo e rode o validador nas páginas tocadas.
- HTML vindo de outra IA passa por acabamento antes de entrar: identidade do `PARA_IA.md`, menu, faixa alfa, validador e escape do texto digitado.
- O único e-mail que pode aparecer é o oficial do Lab, `labescola3d@gmail.com`.

<!-- politica:inicio v1 -->
## Política de colaboração

> Política de colaboração · v1 · 2026-11-18 — igual no `prototipos` e no `site-le3d`. Mudou aqui, muda lá, no mesmo número de versão.

Dois devs pares trabalham nestes repositórios, cada um com os próprios agentes de IA (Claude Code, Antigravity, Meta AI ou outros). Não há conversa compartilhada: **o Git é o meio de coordenação**. Tarefa vive em Issue, decisão vive em `docs/decisoes/`, passagem de vez vive no pedido de junção. Este arquivo vale para qualquer agente, em qualquer ferramenta.

### Fluxo

1. Toda tarefa tem uma **Issue** com responsável. Leia a Issue antes de começar.
2. Trabalhe num **ramo** `<pessoa>/<issue>-<tema>` (ex.: `dev-2/12-filtro-catalogo`). Nunca na `main`.
3. **Commits** em Conventional Commits, em português (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore:`). Se uma IA ajudou, o commit termina com `Assisted-by: <ferramenta> (<modelo>)`. Mantenha os trailers que a sua ferramenta acrescenta sozinha (ex.: `Co-Authored-By:`); o obrigatório é o `Assisted-by:`.
4. Entregue por **pedido de junção** (*pull request*) com o modelo do repositório e `Fecha #<issue>`.
5. O **outro dev revisa**. Depois da aprovação, qualquer um dos dois junta (*squash*). Detalhes no `CONTRIBUTING.md`.

### Limites do agente

- **Não junte, não envie para a `main`, não reescreva histórico** (`push --force`, `rebase` de ramo publicado). Entregue no ramo e pare.
- **Leia antes de escrever:** este arquivo, a Issue e o código que vai mudar.
- **Teste antes:** ao mudar código, escreva primeiro o teste que falha. Rode a suíte antes de entregar.
- **Não invente fatos:** números, depoimentos, parcerias, nomes. Onde faltar dado real, escreva `[a confirmar]`.
- **Nunca grave** segredo, senha, chave ou token; dado pessoal (nome ou foto de estudante, e-mail, telefone, CPF, endereço); conteúdo de pesquisa acadêmica; assunto interno do Lab. Na dúvida, pergunte ao dev.
- **Contexto privado** colado no chat (textos CTX01, CTX02…) serve para entender o pedido e nunca entra em arquivo, commit ou pedido.
- **Não decida escopo:** o que a Issue não decidiu volta como pergunta ao dev que chamou você.
- **Quem responde pela mudança é o dev**, não a IA. Explique no pedido o que foi feito e como conferir.

### Melhorar esta política

Qualquer dev ou agente pode propor mudança, sempre por pedido de junção nos **dois** repositórios, com a versão nova (v2, v3…) e um registro em `docs/decisoes/`. A política só muda com a aprovação dos dois devs.
<!-- politica:fim -->
