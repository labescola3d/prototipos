# Geradores dos elementos e gabaritos

Todo SVG desta pasta `identidade/` é **gerado por código**. Para mudar uma forma, uma cor ou uma medida, mude o gerador e rode de novo; não edite o SVG à mão.

Requer Python 3 (sem bibliotecas extras). Rode a partir da raiz do repositório:

```
python identidade/geradores/gerar_elementos_canva.py identidade/geradores identidade/elementos/canva-2026
python identidade/geradores/gerar_elementos_canva_lote2.py identidade/elementos/canva-2026
python identidade/geradores/gerar_gabaritos_professor.py identidade/geradores identidade/gabaritos-professor
```

| Arquivo | O que faz |
| :-- | :-- |
| `gerar_elementos_canva.py` | lote 1 do Canva: padrão de ícones, retícula, mancha orgânica, ícone e cubo no canto, etiqueta, marca-texto, setas |
| `gerar_elementos_canva_lote2.py` | lote 2: mosaico de triângulos, chevrons, faixas diagonais, máscara diagonal, linhas de circuito, explosão, geometria Bauhaus, ondas, brilho, retícula lilás |
| `gerar_gabaritos_professor.py` | kit do professor em A4 (cabeçalho, ficha de pistas, dado, cartas, fichas, quebra-cabeça, tabuleiros) |
| `extrair_elementos_site.py` | separa fita orgânica, quadrados e moldura a partir dos banners originais do site (`originais-site/`) |
| `icone-le3d.json` · `cubo-le3d.json` | geometria do ícone e do cubo do logo, usada pelos geradores |

## Paleta e tipografia

Roxo `#3026AD` · laranja `#E3630D` · preto `#150E1F` · cinza `#F2F2F2` · branco `#FFFFFF`. Tons claros: mistura com branco, truncando cada canal.

Títulos: Big Shoulders Display 700 (provisório) · digital e legendas: Source Sans 3 · texto impresso: Times New Roman · logo: Bebas Neue, já em curvas.
