# Catálogo v2 · desenho

> Desenho aprovado em conversa em 24/11/2026. Ele orienta o plano de implementação e as Issues que saem dele. Nada aqui é construído antes da aprovação deste documento.

## Por que

O protótipo já mostra 9 materiais, mas a professora ainda não consegue responder, só pelo catálogo, à pergunta que ela traz: **"o que serve para a minha matéria, para a minha turma e cabe no meu tempo de aula?"** Os cards não têm imagem, os filtros só separam tipo e ano de lançamento, e parte do que o Lab já fez (oficinas, peças 3D, visitas, kit de divulgação) não aparece.

Esta versão:

1. leva ao catálogo tudo o que o Lab já pode oferecer, com cópias limpas;
2. dá a cada card uma imagem e quatro tags de filtragem;
3. reorganiza a página de manuais como uma coleção;
4. usa o Printables como vitrine das peças 3D, sem abrir mão da cópia local.

## Metas, não metas e antimetas

**Metas**

- 15 cards no catálogo, cada um com imagem, tipo e as quatro tags.
- Filtros combináveis e busca por texto, sem biblioteca.
- 7 páginas novas e a página `/manuais` como coleção.
- Toda página nova no modelo das páginas de material que já existem.

**Não metas**

- Reescrever os manuais em si.
- Migrar para o WordPress do site oficial.
- Páginas para a Morfogênese de Silício e para os slides de impressão 3D (decisão de 24/11).
- Card com QR, pôsteres e apresentações acadêmicas e anais: ficam para uma futura página "Sobre o Lab".

**Antimetas**: é fracasso, mesmo funcionando:

- foto com rosto de pessoa, de estudante ou de professor (regra 7);
- dado de pesquisa acadêmica no site: falas de professores coletadas em visita, quadros de síntese, opiniões sobre a política pública da rede;
- nome de estudante, e-mail ou telefone (só o e-mail oficial do Lab);
- página que pese e demore no celular da professora;
- tag inventada: onde o dado não existe, o valor é `[a confirmar]` e o card não entra naquele filtro.

## Restrições

- Política de colaboração v1: Issue, ramo, pedido de junção, revisão pelo outro dev. Agente não junta nem envia para a `main`.
- Mudar o gerador, nunca o HTML gerado. Teste que falha antes do código. `checar.py` nas páginas tocadas.
- Licença CC BY-NC-SA 4.0 nos materiais. A marca do Lab (logo, selo, cubo) fica fora da CC, com frase própria de uso.
- Site leve: sem framework, sem biblioteca de JavaScript. Imagem de card com no máximo ~80 KB.
- Publicar sempre das cópias limpas e creditadas, nunca dos originais.

## Abordagens consideradas

| | Como | Troca | Escolha |
| :-- | :-- | :-- | :-- |
| **A** | Os dados de todos os cards num `catalogo.json` no repositório, lido pelos geradores que já existem | Segue o que o protótipo já faz; a validação das tags é um arquivo legível; testes continuam offline | **escolhida** |
| B | Planilha do Google como fonte, puxada pelo gerador | Edição fácil para a equipe, mas o gerador passa a depender de rede e credencial e os testes quebram no pedido de junção | descartada |
| C | Páginas escritas à mão | Rápido para uma página, mas 15 cards com 4 tags viram cópia e cola com erro | descartada |

## O que foi decidido

### 1. Os 15 cards e os 6 tipos

O **tipo** é o primeiro filtro e o selo do card.

| Tipo | Cards |
| :-- | :-- |
| Jogos | Investigadoras do conhecimento · Expedição Sonora · Antropolojogo · Através do Espelho (link externo, Ludopédia) |
| Oficinas e formações | Oficina de Gamificação · **Oficina de Costura** · **Oficina Makey Makey + impressão 3D** · Curso Maker de Férias 2025 |
| Para o professor | **Kit do professor** · Manual Maker (leva a `/manuais`) · **Catálogo de Atividades** (página de entrada) |
| Peças 3D | **Brindes impressos em 3D** |
| Divulgação | **Kit de divulgação do Lab** |
| Visitas e parcerias | **Visitas COPPEi** · Memórias da Maré |

Em negrito, as páginas novas. A faixa de números do topo do catálogo é recontada a partir do `catalogo.json`, nunca escrita à mão.

### 2. As quatro tags

| Tag | Valores | Regra |
| :-- | :-- | :-- |
| **Disciplina** | componentes curriculares da BNCC: Matemática, Ciências, Geografia, História, Arte, Língua Portuguesa, Educação Física, Língua Inglesa, Computação, e "Transversal" | Pode ter mais de uma. As **competências gerais** e os **códigos das habilidades** (ex.: EF06MA24) não viram filtro: vão para a seção "Para quem" da página de cada material |
| **Tempo** | Até 50 min (1 tempo) · 50 a 100 min (2 tempos) · Mais de 100 min (projeto ou oficina) | Um valor por card |
| **Complexidade de reproduzir** | Fácil: só imprimir e usar · Médio: pede montagem ou material comprado · Difícil: pede impressora 3D, eletrônica ou formação antes | Um valor por card |
| **Ano** | Educação Infantil · Fundamental I (1º ao 5º) · Fundamental II (6º ao 9º) · Ensino Médio | Pode ter mais de uma etapa. Quando houver, o card mostra o ano exato (ex.: "6º ao 8º ano") |

**Combinação**: dentro de uma tag, vale qualquer valor marcado (OU); entre tags, valem todas (E). A busca por texto procura no título, na frase e nos nomes das tags, e combina com os filtros.

**Preenchimento**: o construtor propõe os valores a partir das fichas, roteiros e do acervo; o que não tiver fonte fica `[a confirmar]`. Ivan valida a tabela (gerada do `catalogo.json`) antes do pedido de junção ir à revisão.

### 3. Imagens dos cards

- Fonte: **capas dos designs do Canva do Lab**, já organizados por projeto, exportadas pelo conector.
- Cada capa é conferida pela **regra 7**: nenhum rosto de pessoa. Capa que não passa, ou projeto sem design adequado, mantém a área reservada.
- Formato: JPG ou WebP, largura de ~800 px, no máximo ~80 KB, em `_base/capas/<slug>.jpg`, com texto alternativo que descreve o que se vê.

### 4. Páginas de oficina (Costura e Makey Makey + 3D)

Seguem o mais perto possível a página da **Oficina de Gamificação**: o que é a oficina, para quem é, como foi aplicada, e um bloco **"baixe e aplique"**.

- **Costura**: a ficha "Almofadinhas Geométricas: calculando e costurando perímetros" (6º ao 8º ano, Matemática e Arte, 50 min; autoria: Ana da Hora) e o card das partes da máquina de costura, em PDF limpo e creditado.
- **Makey Makey + 3D**: o roteiro com as duas estações ("Ajude o Bibo", caça aos órgãos com peças impressas, e o jogo do dinossauro no Makey Makey) e as fichas de charadas para imprimir.
- As cópias limpas dessas duas oficinas ainda não existem: o construtor as monta no pacote de curadoria antes de publicar.
- **Sai das cópias**: anexos com falas e sínteses de professores, quadros de dinâmica de pesquisa, comentários sobre a política pública da rede e nomes de pessoas fora da equipe.
- "Como foi aplicada" conta a formação feita numa escola da rede, sem foto de pessoa.

### 5. Visitas COPPEi

Página de **relato**, sem nada para baixar: o percurso de cinco passos, as três mesas (apresentação do Lab com peças 3D; jogos de Humanas; jogos de Exatas e Artes) e os jogos de cada mesa, com link para as páginas deles. Termina com a mensagem de que **a escola da professora pode pedir uma visita à Diretoria de Extensão da COPPE**. O contato da Diretoria fica `[a confirmar]` até ser fornecido. Nenhuma foto de visitantes.

### 6. Brindes impressos em 3D

- Uma página com todas as peças (chaveiros, lanterna, spinner, colcheia e mapa da Catarina, régua de engrenagens); cada peça diz **o que contribui no ensino, com base na BNCC**.
- As peças foram impressas e funcionaram: **botão de baixar direto**, só no bico 0,6.
- **Duas saídas para cada peça**, comunicadas como "baixe aqui ou acesse a nossa página no Printables":
  - cópia local do STL ou 3MF;
  - o **embed oficial do Printables** (`https://www.printables.com/embed/<id>`), tamanho **Card (400×445)** no computador e **Small (300×340)** no celular, porque o embed não se ajusta à largura. Na página de uma peça só, tamanho **Wide (640×190)**.
- O embed vem em inglês e pode mostrar o selo "AI": isso é do Printables e não se altera.
- Os IDs do Printables chegam conforme as peças forem publicadas; peça sem ID mostra só a cópia local.

### 7. Kit de divulgação do Lab

Logo, adesivos, bottons e crachás para baixar, **para a professora espalhar a marca**, como adesivo de rádio: usar a logo para dar aula e divulgar o Lab é permitido, desde que sem alterá-la. Arquivos para imprimir exportados do Canva. Frase de uso da marca no lugar da licença CC.

### 8. Kit do professor

Página própria para os 14 gabaritos A4 (PDF de ~150 KB), transversal a qualquer componente, para preparar aula. Ele continua listado também na Oficina de Gamificação.

### 9. Catálogo de Atividades (página de entrada)

Explica o que são as fichas de atividade, para que servem (roteiros de aula maker alinhados à BNCC e à BNCC Computação, com filtros por ano e componente), mostra uma ficha de exemplo e aponta para o catálogo de fichas no site oficial.

### 10. `/manuais` como coleção

`/manuais` vira a página da **coleção Manual Maker**: cada volume é um card com capa, "o que a professora vai aprender", número de páginas, tamanho e licença, mais o manual completo e os créditos. O kit das Investigadoras sai daqui e fica só na página do jogo. O card "Manual Maker" do catálogo aponta para `/manuais`; a página antiga `catalogo/manual-maker/` redireciona para lá.

### 11. Correções

- **Investigadoras**: "33 homenageadas" vira **"31 fichas"** (32 mulheres: uma ficha é de uma dupla). O Consultor de Campo e a página têm a mesma lista; o número 30 do acervo conta retratos.
- **Memórias da Maré**: entra o STL do Rola-rola, modelado do zero, com crédito.

## O que fica com o construtor

- A forma do `catalogo.json` e como os geradores o leem.
- O desenho dos filtros e da busca dentro da identidade do `PARA_IA.md`, no computador e no celular.
- Como alternar o tamanho do embed do Printables por largura de tela sem baixar os dois.
- Os textos das páginas novas, no tom das páginas que já existem, a partir das fontes; o que faltar fica `[a confirmar]`.
- A divisão em pedidos de junção. Sugestão: (1) dados, tags, filtros e busca, e a correção das Investigadoras; (2) imagens dos cards; (3) oficinas, Kit do professor e Catálogo de Atividades; (4) Brindes, Printables e Kit de divulgação; (5) Visitas COPPEi e `/manuais`.

## Pendências de Ivan

- IDs do Printables de cada peça.
- Contato da Diretoria de Extensão da COPPE para as visitas.
- Validar a tabela de tags.
- Confirmar que as ilustrações do Bibo, feitas com IA, podem ir com crédito "ilustração gerada com IA".
