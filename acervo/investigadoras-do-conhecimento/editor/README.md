# Editor do Investigadoras — "Crie sua investigadora"

Protótipo (18/11/2026) da edição online do jogo: a professora parte de uma homenageada ou do zero, troca nome, pistas, fato curioso e imagem, e imprime o card e as cartas-pista em A4.

- **No ar:** https://labescola3d.github.io/prototipos/acervo/investigadoras-do-conhecimento/editor/
- **Por que e como foi pensado:** `labescola3d/site-le3d`, `docs/superpowers/specs/2026-11-18-editor-investigadoras-design.md`

| Arquivo | O que é |
| :-- | :-- |
| `index.html` | a página inteira: formulário, prévia, pop-up de aviso, rodapé de licença, impressão. CSS e JS embutidos, sem biblioteca |
| `perfis.json` | as homenageadas do jogo por eixo (nome, resumo, 3 pistas, fato curioso). Extraído do Consultor de Campo v3 |

**Regras que não podem cair:**

1. Nada sai do navegador: sem `fetch` para fora, sem formulário enviado, sem armazenamento. A imagem é lida com `URL.createObjectURL`.
2. O pop-up de aviso aparece antes da primeira edição e só fecha pelo botão.
3. "Imprimir" só libera com o nome da investigadora e o nome de quem editou.
4. Todo material impresso leva o rodapé: adaptado do original do Lab, link do original, licença CC BY-NC-SA 4.0 e o nome de quem editou como responsável.
5. Texto digitado entra na página como texto (`textContent`), nunca como HTML.

**Para editar os perfis**, mude `perfis.json`; perfis com menos de 3 pistas não aparecem na lista.
