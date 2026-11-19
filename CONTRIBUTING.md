# Contribuir com o prototipos

Este repositório é a vitrine alfa do site do Lab Escola 3D. **Juntar na `main` publica** em https://labescola3d.github.io/prototipos/ — por isso nada entra sem a aprovação do outro dev e sem os testes automáticos verdes.

Antes de abrir um pedido: rode os testes e o validador (comandos no `AGENTS.md`) e confira a página no computador e no celular (375 px).

<!-- politica:inicio v1 -->
## Como trabalhamos

> Política de colaboração · v1 · 2026-11-18 — igual no `prototipos` e no `site-le3d`.

Somos dois devs pares, cada um com os próprios agentes de IA. O Git e o GitHub são o meio de coordenação: o que não está numa Issue, num commit, num pedido de junção ou em `docs/decisoes/` não foi combinado.

### O ciclo de uma mudança

| Etapa | Como |
| :-- | :-- |
| 1. Tarefa | uma **Issue** com responsável; quem pega se atribui |
| 2. Ramo | `<pessoa>/<issue>-<tema>`, saído da `main` atualizada |
| 3. Commits | pequenos, em Conventional Commits e em português |
| 4. Pedido de junção | modelo do repositório, `Fecha #<issue>`, como conferir |
| 5. Revisão | o **outro dev** revisa e aprova ou pede mudança |
| 6. Junção | **qualquer um dos dois**, depois da aprovação, com *squash*; o ramo é apagado |

### Commits

```
feat: filtro do catalogo por disciplina

Assisted-by: Claude Code (Claude Opus 5.5)
```

Tipos: `feat` (algo novo), `fix` (correção), `docs` (documentação), `test` (testes), `ci` (automação), `chore` (arrumação). A linha `Assisted-by:` é obrigatória quando uma IA escreveu parte da mudança; ela nomeia a ferramenta e o modelo. Quem assina o commit responde por ele. Na junção, mantenha as linhas `Assisted-by:` na mensagem do squash.

### Revisão

- Revise em até **2 dias úteis**; se não der, avise no pedido.
- Peça mudança com o motivo; aprove só o que você conferiu.
- A aprovação cai se entrar commit novo: o outro revisa de novo.

### Decisões

Decisão que muda estrutura, regra ou rumo vira um arquivo em `docs/decisoes/AAAA-MM-DD-tema.md`, com **Contexto**, **Decisão** e **Consequências**, junto do pedido de junção que a aplica.

### Agentes de IA

As regras para qualquer agente estão no `AGENTS.md` (o Claude Code o lê pelo `CLAUDE.md`). IAs sem acesso ao repositório recebem o `AGENTS.md` colado no chat.
<!-- politica:fim -->
