# PARA IA — como prototipar telas do Lab Escola 3D

Este arquivo orienta assistentes de IA (Meta AI, Claude e outros) que ajudam a prototipar o site do **Lab Escola 3D (LE3D)**. Leia tudo antes de propor uma tela.

## 1. Contexto

- O **Lab Escola 3D** é um projeto de extensão da UFRJ que leva cultura maker, design e tecnologias digitais para escolas públicas do Rio de Janeiro.
- O site reúne **materiais educacionais gratuitos**: jogos, oficinas, formações, atividades e manuais, para baixar, imprimir e adaptar.
- **Quem usa:** a professora da rede pública, de 25 a 50 anos, que não programa. A pergunta que decide toda tela: **"ela clica e baixa?"** Menos é mais.
- **Este repositório** é a vitrine alfa, publicada em https://labescola3d.github.io/prototipos/ . O site oficial é https://labescola3d.rio.br/ .

## 2. Telas que já existem (leia antes de propor)

| Tela | Endereço |
| :-- | :-- |
| Home | https://labescola3d.github.io/prototipos/ |
| Acervo (lista de materiais) | https://labescola3d.github.io/prototipos/acervo/ |
| Página de um material | https://labescola3d.github.io/prototipos/acervo/investigadoras-do-conhecimento/ |
| Editor "Crie sua investigadora" | https://labescola3d.github.io/prototipos/acervo/investigadoras-do-conhecimento/editor/ |
| Sobre este protótipo | https://labescola3d.github.io/prototipos/sobre/ |
| Identidade visual (elementos e gabaritos) | https://labescola3d.github.io/prototipos/identidade/ |

**Próximas telas a prototipar:** "Licença e como usar" e "Como contribuir".

## 3. Identidade visual (use sempre; não invente outra)

| Papel | Valor |
| :-- | :-- |
| Roxo (principal) | `#3026AD` |
| Laranja (destaque, botões) | `#E3630D` |
| Preto | `#150E1F` |
| Cinza (fundo) | `#F2F2F2` |
| Branco | `#FFFFFF` |
| Títulos | **Big Shoulders Display**, peso 700 (Google Fonts) |
| Texto na tela | **Source Sans 3** (Google Fonts) |
| Logo | https://labescola3d.rio.br/wp-content/uploads/2023/09/cropped-cropped-02_simbolo-300x213.png |

Elementos gráficos prontos, em SVG, na galeria de identidade (seção 2). Para usar um, aponte o endereço do arquivo; não redesenhe o logo.

## 4. Licença

Os materiais do acervo estão sob **Creative Commons BY-NC-SA 4.0** (atribuição, não comercial, compartilha igual). **Não é GNU**: a GNU GPL é licença de software. Ao explicar a licença na tela, use linguagem simples: "pode usar, copiar e adaptar para a sua aula, sem vender, citando o Lab Escola 3D".

## 5. Regras de produção

1. **Um arquivo HTML completo**, com o CSS dentro de `<style>`. O único recurso externo permitido é o Google Fonts. Sem framework nem biblioteca.
2. **Ícones em SVG** embutido no HTML; nunca fonte de ícones (Font Awesome etc.).
3. **Toda imagem com `alt`** descrevendo o que mostra.
4. **Links internos relativos** (`acervo/`, nunca `/acervo/`).
5. **Funcionar no celular** (largura de 375 px) e no computador.
6. **Português do Brasil**, frases curtas, sem jargão técnico.
7. **Imagem gerada por IA só para ilustração ou capa** — nunca a tela inteira como imagem, nunca texto dentro da imagem.

## 6. Proibido (o site é público e indexado)

- **Dados pessoais** (LGPD): nada de nome ou foto de estudante, foto de criança, e-mail, telefone, CPF ou endereço ligado a uma pessoa. Use textos de exemplo claramente fictícios.
- **Inventar fatos**: números, depoimentos, parcerias, prêmios ou nomes de pessoas. Onde faltar dado real, escreva `[a confirmar]`.
- Outra paleta, outro logo ou outras fontes.

## 7. Formato de entrega

Responda com:

1. três linhas antes do código: **nome da tela**, **o que você propôs**, **dúvidas** que ficaram;
2. **um único bloco de código** `html` com a página inteira, pronta para salvar como `.html`.

Quando pedirem variações, entregue cada uma em um bloco separado, numerado.
