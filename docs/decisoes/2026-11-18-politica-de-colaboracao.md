# 2026-11-18 · Política de colaboração v1

## Contexto

Dois devs pares, Ivan e Gleyci, constroem o site do LE3D, cada um com os próprios agentes de IA. Nenhuma ferramenta permite que duas contas conversem com a mesma IA na mesma sessão, e cada dev usa ferramentas diferentes (Claude Code, Antigravity, Meta AI).

## Decisão

- **O Git é o meio de coordenação.** Tarefa em Issue, decisão em `docs/decisoes/`, passagem de vez no pedido de junção.
- **Cada repositório se basta.** `prototipos` e `site-le3d` têm os mesmos arquivos de política, com a parte comum idêntica e versionada.
- **`AGENTS.md` é a diretiva única para qualquer agente**, por ser o formato aberto lido pela maioria das ferramentas; o `CLAUDE.md` só o importa.
- **Pares de verdade:** qualquer dev junta na `main`, depois da aprovação do outro; a `main` é protegida.
- **Uso de IA declarado** no commit com `Assisted-by:`; quem assina responde pela mudança.

## Consequências

- Mudar a política exige um pedido de junção em cada repositório.
- Uma IA sem acesso ao repositório (ex.: Meta AI) recebe o `AGENTS.md` colado no chat.
- A proteção da `main` só se aplica depois que a Gleyci entrar no `CODEOWNERS`; antes, ela travaria os pedidos do único dono.
