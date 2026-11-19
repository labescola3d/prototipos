# PARA IA — como prototipar telas do Lab Escola 3D

Este arquivo orienta assistentes de IA (Meta AI, Claude e outros) que ajudam a prototipar o site do **Lab Escola 3D (LE3D)**. Leia tudo antes de propor uma tela. Se você vai **mudar arquivos deste repositório**, siga também o [`AGENTS.md`](AGENTS.md), a política de colaboração.

## 1. Contexto

- O **Lab Escola 3D** é um projeto de extensão da UFRJ que leva cultura maker, design e tecnologias digitais para escolas públicas do Rio de Janeiro.
- O site reúne **materiais educacionais gratuitos**: jogos, oficinas, formações, atividades e manuais, para baixar, imprimir e adaptar.
- **Quem usa:** a professora da rede pública, de 25 a 50 anos, que não programa. A pergunta que decide toda tela: **"ela clica e baixa?"** Menos é mais.
- **Este repositório** é a vitrine alfa, publicada em https://labescola3d.github.io/prototipos/ . O site oficial é https://labescola3d.rio.br/ .

## 2. Telas que já existem (leia antes de propor)

| Tela | Endereço |
| :-- | :-- |
| Home | https://labescola3d.github.io/prototipos/ |
| Catálogo (lista de materiais) | https://labescola3d.github.io/prototipos/catalogo/ |
| Página de um material | https://labescola3d.github.io/prototipos/catalogo/investigadoras-do-conhecimento/ |
| Editor "Crie sua investigadora" | https://labescola3d.github.io/prototipos/catalogo/investigadoras-do-conhecimento/editor/ |
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

Tudo neste repositório — materiais **e código** — está sob **Creative Commons BY-NC-SA 4.0** (atribuição, não comercial, compartilha igual): é material de extensão da UFRJ, pago com dinheiro público, e ninguém pode explorá-lo comercialmente. **Não é GNU**: as licenças GNU não permitem a restrição "não comercial". Ao explicar a licença na tela, use linguagem simples: "pode usar, copiar e adaptar para a sua aula, sem vender, citando o Lab Escola 3D".

## 5. Princípios do site

- **Navegador primeiro.** A professora edita no próprio site e sai o PDF em A4, pronto para imprimir. Sem conta, sem cadastro, sem instalar nada. Exemplo: o editor "Crie sua investigadora".
- **Canva é extra, não caminho.** Quem quiser pode arrastar o PDF baixado para o Canva. Nenhuma tela pode depender de Canva, plano pago ou login.
- **Site leve.** Tem que abrir num computador antigo, num Chromebook e num Android velho, com internet ruim. Sem vídeo carregando sozinho, sem imagem pesada, sem biblioteca. Conteúdo de fora (Ludopédia, Printables, YouTube) entra como miniatura com link; o player só carrega se a pessoa clicar.

## 6. Regras de produção

1. **Um arquivo HTML completo**, com o CSS dentro de `<style>`. O único recurso externo permitido é o Google Fonts. Sem framework nem biblioteca.
2. **Ícones em SVG** embutido no HTML; nunca fonte de ícones (Font Awesome etc.).
3. **Toda imagem com `alt`** descrevendo o que mostra.
4. **Links internos relativos** (`catalogo/`, nunca `/catalogo/`).
5. **Funcionar no celular** (largura de 375 px) e no computador.
6. **Português do Brasil**, frases curtas, sem jargão técnico.
7. **Imagem gerada por IA só para ilustração ou capa** — nunca a tela inteira como imagem, nunca texto dentro da imagem.

## 7. Proibido (o site é público e indexado)

- **Dados pessoais** (LGPD): nada de nome ou foto de estudante, foto de criança, e-mail, telefone, CPF ou endereço ligado a uma pessoa. Use textos de exemplo claramente fictícios.
- **Inventar fatos**: números, depoimentos, parcerias, prêmios ou nomes de pessoas. Onde faltar dado real, escreva `[a confirmar]`.
- Outra paleta, outro logo ou outras fontes.

## 8. Contexto privado

Este arquivo é o **canal público**: só traz o que qualquer pessoa pode ler. Contexto que não deve ficar na internet chega por outro canal: a pessoa que pede a tela **cola no chat** um texto numerado (CTX01, CTX02…). Esse contexto serve para entender o pedido e **nunca** deve aparecer no HTML, no Markdown ou na imagem que você gerar.

## 9. Formato de entrega

Responda com:

1. três linhas antes do código: **nome da tela**, **o que você propôs**, **dúvidas** que ficaram;
2. **um único bloco de código** `html` com a página inteira, pronta para salvar como `.html`.

Quando pedirem variações, entregue cada uma em um bloco separado, numerado.
