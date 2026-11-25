"""Gera as páginas de produto do Catálogo (Fase 1) a partir dos dados abaixo.

Uso: py -I -X utf8 _ferramentas/gerar_produtos.py
Cada página tem 2 telas (computador 1440 e celular 375) para o Canva.
Dado que a fonte não traz sai como [a confirmar]; nada é inventado.
Fontes: inventário em site-le3d/docs/acervo/inventario.md.
"""
import html
import os
import posixpath
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogo import carregar  # noqa: E402

LOGO = "https://labescola3d.rio.br/wp-content/uploads/2023/09/cropped-cropped-02_simbolo-300x213.png"
SITE = "https://labescola3d.rio.br/wp-content/uploads/"
LICENCA = "Licença CC BY-NC-SA 4.0: uso não comercial em sala de aula, citando o LE3D e os autores."
FRASE_MARCA = ("A marca do Lab Escola 3D não é licenciada em CC. Use a logo, os adesivos e os bottons à vontade "
               "para dar aula e divulgar o Lab, sem alterá-los.")

PRODUTOS = [
    {
        "slug": "investigadoras-do-conhecimento", "titulo": "Investigadoras do conhecimento", "selo": "Jogo · 2026",
        "frase": "Um jogo de pistas para a turma descobrir as grandes mulheres brasileiras da ciência, da arte, da política e do esporte.",
        "reservada": "foto do kit (cartas e dado)",
        "baixar": {"titulo": "Baixe e jogue com a sua turma", "arquivos": [
            ("Baixar o kit", SITE + "2026/11/Investigadoras_do_Conhecimento_PnP_v0.pdf", "Kit para imprimir (print and play) · PDF · 5 páginas · 1 MB"),
            ("Abrir o Consultor de Campo", "consultor-de-campo.html", "As fichas no celular de quem conduz o jogo · HTML · 1 MB · funciona sem internet")],
            "editor": ("Crie sua investigadora", "editor/", "Troque o perfil e as pistas e imprima o card no navegador")},
        "fatos": [("[a confirmar]", "ano escolar"), ("5 a 10 pessoas", "por grupo"), ("5 a 10 min", "por rodada"), ("6 eixos", "31 fichas")],
        "o_que_e": "Um jogo que transforma o Método Científico em uma investigação. A figura de quem faz ciência não se resume ao “homem branco de jaleco”: com histórias reais, o jogo dá visibilidade às mulheres brasileiras que transformaram a ciência, a cultura e a sociedade, e fortalece a autoestima e a autonomia das estudantes.",
        "como": ("Como se joga", [
            "O grupo rola o dado especial, que revela um eixo e a silhueta de uma homenageada.",
            "A mediadora lê até três pistas, da mais difícil para a mais fácil.",
            "O grupo junta as evidências e dá um palpite.",
            "Todo mundo ganha um incentivo por participar; quem acerta leva um prêmio extra."]),
        "itens": ("As homenageadas, por eixo", [
            ("Científico", "Sônia Guimarães, Ester Sabino, Jaqueline Goes de Jesus, Bertha Lutz, Tatiana Sampaio"),
            ("Artístico", "Tarsila do Amaral, Carolina Maria de Jesus, Clarice Lispector, Anita Malfatti, Fernanda Montenegro"),
            ("Musical", "Elis Regina, Dona Ivone Lara, Chiquinha Gonzaga, Clara Nunes, Elza Soares"),
            ("Político", "Dilma Rousseff, Maria da Penha, Marielle Franco, Zuzu Angel, Erika Hilton, Dona Orosina"),
            ("Histórico", "Tia Ciata, Princesa Isabel, Maria Quitéria, Maria Bonita, Dandara dos Palmares"),
            ("Esportes", "Rebeca Andrade, Marta, Daiane dos Santos, Rayssa Leal, Jacqueline Silva e Sandra Pires (uma ficha para a dupla)")]),
        "origem": ["Criado a partir de uma demanda da SME-Rio para o Dia da Mulher (março de 2026).",
                   "Aplicado em dinâmica no GET Levy Neves, em 19/03/2026.", "Apresentado na SIAC/UFRJ."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Equipe: Raiane Pacheco (responsável), Eduardo Cóser e Ivan Silveira.",
    },
    {
        "slug": "expedicao-sonora", "titulo": "Expedição Sonora", "selo": "Jogo · 2026",
        "frase": "Uma viagem pelo Brasil de ouvido: a turma escuta uma música e descobre de que região ela vem.",
        "reservada": "foto do mapa do Brasil e dos peões impressos em 3D",
        "baixar": {"titulo": "Material para levar à sua turma", "arquivos": [
            ("Peões Tom e Vit (três peças)", "peoes-tom-e-vit-pacote-c.zip", "9 arquivos STL para impressora 3D, bico 0,6 ou 0,4 mm, com créditos · ZIP · 5 MB · a versão usada em sala")],
                   "editor": ("Monte suas cartas", "editor/", "Parta das 41 cartas do jogo ou escreva as suas e imprima 9 por folha A4")},
        "fatos": [("2 a 4 pessoas", "por grupo"), ("cerca de 10 min", "por rodada"), ("30 músicas", "6 por região"), ("5 regiões", "do Brasil")],
        "o_que_e": "Um jogo que transforma um tema abstrato em experiência: a turma vira “Exploradores dos Ritmos” e viaja pelo território brasileiro conectando identidades, instrumentos e artistas regionais. A música afina a escuta crítica e estimula a colaboração entre estudantes e famílias.",
        "como": ("Como se joga", [
            "Um par ou ímpar decide quem escolhe a carta surpresa da rodada.",
            "O monitor toca a música sorteada.",
            "A equipe coloca o seu peão de explorador na região do mapa de onde acha que a música veio.",
            "Quem acerta ganha a carta, com curiosidades sobre o artista. Quem acertar mais vira “Embaixador dos Ritmos”."]),
        "itens": ("O que vem no kit", [
            ("Tabuleiro", "Mapa do Brasil com as 5 regiões em cores."),
            ("Playlist", "30 músicas regionais, de artistas nascidos em cada região."),
            ("Peões", "Exploradores impressos em 3D, um por time."),
            ("Cartas", "Cerca de 6 artistas por região, com nome e curiosidades.")]),
        "origem": ["Aplicado no GET Levy Neves, com as famílias, em 14/05/2026.", "Apresentado na SIAC/UFRJ.",
                   "Inscrito no Banco de Inovação da UFRJ."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Equipe: Eduardo Cóser (responsável), Levi Macedo, Yasmim Teles, Raiane Pacheco e Ivan Silveira. Peões: modelo de Eduardo Cóser, adaptado por Ivan Silveira.",
    },
    {
        "slug": "oficina-de-gamificacao", "titulo": "Oficina de Gamificação", "selo": "Oficina · 2026",
        "frase": "Uma oficina para professores vivenciarem dois jogos do LE3D e adaptarem a mecânica para a própria turma.",
        "reservada": "foto dos materiais da oficina sobre a mesa",
        "baixar": {"titulo": "Apostila e modelos do professor", "arquivos": [
            ("Apostila do professor", "apostila-roteiro-para-o-professor.docx", "Word · 9 páginas · 2 MB · links para os modelos no Canva"),
            ("Roteiro da oficina (modelo)", "roteiro-oficina-modelo.pdf", "PDF · 12 páginas · 60 minutos em rotação de bases"),
            ("Roteiro da oficina para editar", "roteiro-oficina-modelo.odt", "ODT (LibreOffice ou Word) · 3 MB"),
            ("Ficha de planejamento", "ficha-de-planejamento.pdf", "PDF · 1 página para preencher em dupla"),
            ("Kit do professor: 14 gabaritos A4", "kit-do-professor-a4.pdf", "PDF · cartas, dado, quebra-cabeças e tabuleiros para imprimir")]},
        "fatos": [("Professores", "público"), ("2 jogos", "vivenciados"), ("15 e 20 min", "por ciclo de cada jogo"), ("Modelos", "editáveis no Canva")],
        "o_que_e": "Na oficina, os professores jogam o Investigadoras do Conhecimento e a Expedição Sonora e, em seguida, esboçam com um colega a adaptação de um dos jogos para a sua disciplina. A apostila mostra tudo o que o LE3D desenvolveu e sugere, elemento por elemento, como trocar o tema, o estímulo e o material.",
        "como": ("Como acontece", [
            "Os professores vivenciam os dois jogos.",
            "Em dupla, escolhem um conteúdo da sua disciplina e esboçam a adaptação.",
            "Levam a apostila e os modelos para terminar com calma.",
            "Testam com um colega, ajustam e aplicam na turma."]),
        "itens": ("Ideias de adaptação", [
            ("O que se investiga", "Figuras históricas, elementos químicos, biomas, obras de arte, conceitos matemáticos."),
            ("O estímulo", "Imagem, trecho de texto, vídeo curto, objeto, cheiro ou sabor no lugar da música."),
            ("O material", "Papel A4 dobrado, tampinhas ou massinha no lugar de fichas plastificadas e peões em 3D.")]),
        "origem": ["Realizada no GET Levy Neves, em 12/08/2026."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Apostila e gabaritos: Ivan Silveira. Roteiro e ficha: gestão do Lab Escola 3D.",
    },
    {
        "slug": "oficina-de-costura", "titulo": "Oficina de Costura", "selo": "Oficina · 2025",
        "frase": "Geometria com tecido e máquina de costura: a turma calcula perímetro e área e costura almofadinhas geométricas.",
        "reservada": "card das partes da máquina de costura",
        "baixar": {"titulo": "Ficha e card para aplicar", "arquivos": [
            ("Ficha da atividade: Almofadinhas Geométricas", "ficha-almofadinhas-geometricas.pdf", "PDF · 2 páginas · etapas, tabela de medidas e BNCC"),
            ("Card das partes da máquina de costura", "card-maquina-de-costura.pdf", "PDF · 1 página para imprimir")]},
        "fatos": [("6º ao 8º ano", "Fundamental II"), ("50 min", "1 tempo de aula"), ("Matemática e Arte", "perímetro, área e criação"),
                  ("EF06MA24 · EF69AR06", "e mais 4 habilidades")],
        "o_que_e": "Uma oficina que usa a máquina de costura do colaboratório como ferramenta pedagógica. Primeiro os professores conhecem as partes da máquina com o card; depois aplicam a ficha: a turma recebe só o perímetro e a área de uma figura, desenha, risca no tecido, costura e enche uma almofadinha, e confere se a peça final bate com os cálculos.",
        "como": ("Como foi aplicada", [
            "Formação com professores de uma escola da rede municipal do Rio, em 2025.",
            "Os professores reconheceram as partes da máquina com o card.",
            "Em duplas e trios, fizeram a almofadinha da ficha do começo ao fim.",
            "No fim, conversaram sobre como levar a costura para as próprias aulas."]),
        "itens": ("Para adaptar", [
            ("Outras figuras", "Troque quadrado, triângulo e círculo por hexágonos, trapézios ou figuras compostas."),
            ("Sem máquina", "Costura à mão com agulha grossa e feltro funciona para turmas menores."),
            ("Outra matéria", "Em Arte, foque na composição de cores e texturas, como no patchwork.")]),
        "origem": ["Ficha do Catálogo de Atividades do Lab Escola 3D, aplicada em formação de professores em 2025."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Ficha da atividade: Ana da Hora. Card da máquina e formação: equipe do Lab Escola 3D.",
    },
    {
        "slug": "oficina-makey-makey-3d", "titulo": "Oficina Makey Makey + impressão 3D", "selo": "Oficina · 2025",
        "frase": "Duas estações para professores: uma caça aos órgãos com peças impressas em 3D e um jogo controlado por Makey Makey.",
        "reservada": "ilustração do Bibo",
        "baixar": {"titulo": "Roteiro para aplicar", "arquivos": [
            ("Roteiro da oficina com as fichas de charadas", "roteiro-da-oficina.pdf", "PDF · estações, falas e anexo para imprimir")]},
        "fatos": [("Professores", "público"), ("1 hora", "3 estações de 15 min"), ("Ciências e Computação", "impressão 3D e eletrônica"),
                  ("EF01CI02", "partes do corpo e suas funções")],
        "o_que_e": "Uma oficina em estações para os professores experimentarem duas tecnologias do colaboratório no papel de alunos. Na caça aos órgãos, o Bibo desmontou e a turma resolve charadas para achar peças impressas em 3D e remontar o corpo. No jogo do dinossauro, um tapete ligado à Makey Makey controla um jogo feito em Scratch. Na terceira estação, todos pensam juntos em como levar isso para cada disciplina.",
        "como": ("Como foi aplicada", [
            "Formação com professores de uma escola da rede municipal do Rio, em 2025.",
            "Os professores se dividiram em dois grupos e trocaram de estação a cada 15 minutos.",
            "Experimentaram as peças, as charadas, o circuito e o jogo.",
            "Fecharam com uma conversa sobre usos em cada disciplina."]),
        "itens": ("As estações", [
            ("Ajude o Bibo", "Caça aos órgãos com peças impressas em 3D, charadas e um mapa de letras e números."),
            ("O que faz esse botão?", "O jogo do dinossauro controlado por um tapete ligado à Makey Makey."),
            ("E agora, José?", "Conversa para adaptar as duas dinâmicas a cada disciplina.")]),
        "origem": ["Roteiro da equipe do Lab Escola 3D, aplicado em formação de professores em 2025."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Roteiro e dinâmicas: equipe do Lab Escola 3D.",
    },
    {
        "slug": "kit-do-professor", "titulo": "Kit do professor", "selo": "Para o professor",
        "frase": "Catorze gabaritos A4 para imprimir e preparar aula: tabuleiros, cartas, dados e fichas para adaptar a qualquer matéria.",
        "reservada": "gabaritos impressos sobre a mesa",
        "baixar": {"titulo": "Baixe e imprima", "arquivos": [
            ("Kit do professor: 14 gabaritos A4", "kit-do-professor-a4.pdf", "PDF · 14 páginas A4 · cartas, dado, quebra-cabeças e tabuleiros")]},
        "fatos": [("14 gabaritos", "em A4"), ("Qualquer matéria", "você põe o conteúdo"), ("Só imprimir", "e recortar"), ("Gratuito", "para baixar")],
        "o_que_e": "Um conjunto de moldes em branco para a professora transformar o conteúdo da aula em jogo: cartas, dado de montar, quebra-cabeças e tabuleiros. É a mesma base usada na Oficina de Gamificação, pronta para imprimir em A4.",
        "como": ("Como usar", [
            "Escolha o conteúdo que a turma precisa praticar.",
            "Imprima o gabarito que combina com a dinâmica: cartas, dado ou tabuleiro.",
            "Escreva perguntas, imagens ou desafios nos espaços em branco.",
            "Recorte, monte e jogue com a turma."]),
        "itens": None,
        "origem": ["Feito para a Oficina de Gamificação do Lab Escola 3D (2026)."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Gabaritos: Ivan Silveira.",
    },
    {
        "slug": "catalogo-de-atividades", "titulo": "Catálogo de Atividades", "selo": "Atividades",
        "frase": "Roteiros de aula maker alinhados à BNCC e à BNCC Computação, com filtros por ano e componente.",
        "reservada": "uma ficha de atividade aberta",
        "baixar": {"titulo": "As fichas ficam no site do Lab",
                   "aviso": "O Catálogo de Atividades tem filtros por ano e por componente curricular.",
                   "editor": ("Abrir o Catálogo de Atividades", "https://labescola3d.rio.br/fichas/",
                              "Fichas gratuitas para ler, imprimir e adaptar")},
        "fatos": [("Roteiros", "de aula prontos"), ("BNCC", "e BNCC Computação"), ("Por ano", "e por componente"), ("Gratuito", "para usar")],
        "o_que_e": "Cada ficha é um roteiro de aula maker: diz o ano, o componente, as habilidades da BNCC, os pré-requisitos, as etapas da aula, os recursos e como avaliar. Serve para a professora planejar uma aula prática sem partir do zero, e pode ser adaptada à turma.",
        "como": ("Como usar", [
            "Abra o catálogo e filtre pelo ano e pelo componente da sua turma.",
            "Leia a ficha: habilidades, etapas e recursos.",
            "Separe o material e ajuste a complexidade à turma.",
            "Aplique e, se quiser, conte para o Lab como foi."]),
        "itens": ("Uma ficha de exemplo", [
            ("Almofadinhas Geométricas", "6º ao 8º ano, Matemática e Arte, 50 minutos: a turma calcula perímetro e área e costura almofadinhas. É a ficha da Oficina de Costura."),
            ("O que toda ficha traz", "Ano, eixo, habilidades da BNCC, pré-requisitos, etapas, recursos, avaliação e observações para adaptar."),
            ("Para quem", "Professoras e professores do ensino básico que querem levar a cultura maker para a sala de aula.")]),
        "origem": ["Fichas escritas pela equipe do Lab Escola 3D a partir das formações nos GETs."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Cada ficha traz a autoria no rodapé.",
    },
    {
        "slug": "brindes-3d", "titulo": "Brindes impressos em 3D", "selo": "Peças 3D",
        "frase": "Chaveiros, lanterna, spinner, colcheia, mapa e peões para imprimir e usar como apoio de aula.",
        "reservada": "peças impressas sobre a mesa",
        "baixar": {"titulo": "Arquivos prontos para imprimir",
                   "aviso": "Cada peça abaixo tem o arquivo para baixar aqui e, quando houver, a página no Printables. Bico 0,6 mm, testados na impressora do Lab."},
        "pecas": [
            {"nome": "Peões Tom e Vit", "printables": 1875729,
             "ensina": "Os exploradores da Expedição Sonora: viram peões do jogo e mascotes da turma.",
             "bncc": "Geografia e Arte (música) · [a confirmar]",
             "arquivos": [("Peões Tom e Vit em três peças", "../expedicao-sonora/peoes-tom-e-vit-pacote-c.zip", "ZIP · 5 MB · STL e créditos")]},
            {"nome": "Colcheia e mapa da Catarina", "printables": None,
             "ensina": "Uma colcheia para falar de ritmo e duração das notas, e um mapa do Brasil para ligar música e região.",
             "bncc": "Arte (música) e Geografia · [a confirmar]",
             "arquivos": [("Mesa pronta: colcheia e mapa", "mesa-catarina-colcheia-e-mapa.3mf", "3MF · 58 KB")]},
            {"nome": "Medalhas para o mapa", "printables": None,
             "ensina": "Medalhas para marcar as regiões no mapa da Catarina durante o jogo.",
             "bncc": "Geografia · [a confirmar]",
             "arquivos": [("Mesa pronta: medalhas", "mesa-catarina-medalhas.3mf", "3MF · 57 KB")]},
            {"nome": "Lanterna LE3D", "printables": None,
             "ensina": "Uma lanterna vazada que projeta a marca do Lab: luz, sombra e projeção na prática.",
             "bncc": "Ciências (luz e sombra) · [a confirmar]",
             "arquivos": [("Mesa pronta: lanterna", "mesa-lanterna.3mf", "3MF · 763 KB")]},
            {"nome": "Spinner LE3D", "printables": None,
             "ensina": "Um spinner para conversar sobre rotação, equilíbrio e atrito.",
             "bncc": "Ciências · [a confirmar]",
             "arquivos": [("Mesa pronta: spinner", "mesa-spinner.3mf", "3MF · 267 KB")]},
            {"nome": "Chaveiros moeda", "printables": None,
             "ensina": "Seis chaveiros de 40 mm com padrões diferentes, bons para primeiras impressões e para falar de padrões e simetria.",
             "bncc": "Matemática (simetria) e Arte · [a confirmar]",
             "arquivos": [("Mesa pronta: 6 chaveiros", "mesa-chaveiros.3mf", "3MF · 485 KB")]},
        ],
        "fatos": [("6 peças", "prontas para imprimir"), ("Bico 0,6 mm", "testado no Lab"), ("3MF", "mesa pronta para fatiar"), ("Printables", "página do Lab")],
        "o_que_e": "As peças que o Lab Escola 3D imprime como brindes também servem de apoio de aula: cada uma puxa uma conversa de Ciências, Matemática, Geografia ou Arte. Os arquivos já vêm como mesa de impressão (3MF), prontos para abrir no fatiador.",
        "como": ("Como usar", [
            "Baixe a mesa da peça (3MF) e abra no fatiador da sua impressora.",
            "Confira o bico: os arquivos foram feitos para 0,6 mm.",
            "Imprima e use a peça para abrir a conversa da aula.",
            "Peças com página no Printables também podem ser baixadas por lá."]),
        "itens": None,
        "origem": ["Brindes do Lab Escola 3D, impressos e testados na impressora do Lab em 2026."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Modelagem: Ivan Silveira. Peões: ilustração original de Eduardo Cóser, adaptação de Ivan Silveira. Colcheia e mapa: original de Catarina Reis, adaptação de Ivan Silveira. Lanterna: ideia de Gabriel Texeira e Lucas Rizzo.",
    },
    {
        "slug": "kit-de-divulgacao", "titulo": "Kit de divulgação do Lab", "selo": "Divulgação",
        "frase": "Logo, adesivos, bottons e crachás do Lab Escola 3D para imprimir, usar em aula e espalhar por aí.",
        "reservada": "adesivos e bottons do Lab",
        "licenca": FRASE_MARCA,
        "baixar": {"titulo": "Baixe e espalhe", "arquivos": [
            ("Logo horizontal", "logo-lab-escola-3d-horizontal.svg", "SVG · vetor, qualquer tamanho"),
            ("Logo vertical", "logo-lab-escola-3d-vertical.svg", "SVG · vetor, qualquer tamanho"),
            ("Adesivos", "adesivos-lab-escola-3d.pdf", "PDF · A4 · 1,6 MB · para papel adesivo"),
            ("Bottons", "bottons-lab-escola-3d.pdf", "PDF · 2 modelos"),
            ("Crachás", "cracha-lab-escola-3d.pdf", "PDF · 2 modelos de 70 × 100 mm com espaço para o nome")]},
        "fatos": [("Logo em vetor", "horizontal e vertical"), ("Adesivos", "para imprimir"), ("Bottons e crachás", "modelos prontos"), ("Gratuito", "para divulgar")],
        "o_que_e": "Como os adesivos das rádios, a marca do Lab circula de mão em mão. Use a logo nos seus slides e atividades, imprima adesivos para a turma, monte bottons e crachás para a feira de ciências. Cada vez que o Lab aparece, mais professoras descobrem os materiais gratuitos.",
        "como": ("Como usar", [
            "Baixe a logo e use em slides, fichas e cartazes da aula.",
            "Imprima os adesivos em papel adesivo e distribua para a turma.",
            "Monte bottons e crachás para eventos e feiras da escola.",
            "Marque o Lab nas redes quando postar."]),
        "itens": None,
        "origem": ["Identidade visual e peças de divulgação feitas pela equipe do Lab Escola 3D."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Marca: gestões do Lab Escola 3D. Adesivos, bottons e crachás: equipe de comunicação do Lab.",
    },
    {
        "slug": "visitas-coppei", "titulo": "Visitas COPPEi", "selo": "Visita",
        "frase": "Como é a visita ao Lab na COPPE: peças 3D, jogos de Humanas e de Exatas, e como a sua escola pode pedir a dela.",
        "reservada": "a sala i118 montada com as três mesas",
        "contato": ("Quer levar a sua turma?",
                    "A escola pode pedir uma visita à Diretoria de Extensão da COPPE/UFRJ. Contato: [a confirmar].", None),
        "links": [("Antropolojogo", "../antropolojogo/"), ("Investigadoras do Conhecimento", "../investigadoras-do-conhecimento/"),
                  ("Expedição Sonora", "../expedicao-sonora/"), ("Através do Espelho (na Ludopédia)", "https://ludopedia.com.br/jogo/atraves-do-espelho")],
        "fatos": [("Escolas", "público"), ("3 mesas", "de atividades"), ("4 jogos", "para experimentar"), ("Sala i118", "Centro de Tecnologia da UFRJ")],
        "o_que_e": "Nas Visitas COPPEi, turmas e professores conhecem o Lab Escola 3D numa sala montada com três mesas: peças impressas em 3D, jogos de Humanas e jogos de Exatas e Artes. Os visitantes jogam, perguntam e saem sabendo onde encontrar os materiais gratuitos.",
        "como": ("O percurso", [
            "Recepção na mesa do Lab: apresentações e boas-vindas.",
            "Peças em 3D: a Terra é plana? Onde fica o cérebro? Qual o lado de fora da fita de Möbius?",
            "Jogos de Humanas: Antropolojogo e Investigadoras do Conhecimento.",
            "Jogos de Exatas e Artes: Através do Espelho e Expedição Sonora.",
            "Encerramento: os visitantes exploram livremente as mesas."]),
        "itens": ("As três mesas", [
            ("Apresentação do Lab", "Impressora 3D, globos, modelos de cérebro e nariz, spinners e o card da máquina de costura."),
            ("Jogos de Humanas", "História, Filosofia e Sociologia em jogo: Antropolojogo e Investigadoras do Conhecimento."),
            ("Jogos de Exatas e Artes", "Física e música: Através do Espelho e Expedição Sonora.")]),
        "origem": ["Visitas recebidas pelo Lab Escola 3D na sala i118 do Centro de Tecnologia da UFRJ."],
        "creditos": "Lab Escola 3D · extensão da UFRJ, com a Diretoria de Extensão da COPPE.",
    },
    {
        "slug": "curso-maker-de-ferias-2025", "titulo": "Curso Maker de Férias 2025", "selo": "Formação · 2025",
        "frase": "Um curso de férias para professores da rede municipal conhecerem a cultura maker na prática.",
        "reservada": "imagem de uma aula",
        "baixar": {"titulo": "As aulas do curso",
                   "aviso": "As apresentações das aulas estão em revisão antes da publicação."},
        "fatos": [("Fevereiro de 2025", "edição"), ("Professores", "da rede municipal"), ("[a confirmar]", "número de aulas"), ("Certificado", "para quem participou")],
        "o_que_e": "Uma formação de férias voltada à difusão da cultura maker entre professores da rede municipal do Rio, com aulas práticas que incluem jogos de tabuleiro modernos no ensino.",
        "como": ("Algumas aulas", [
            "Jogos de tabuleiro modernos e o ensino.",
            "Jogos de tabuleiro modernos: prática.",
            "[demais aulas a confirmar]"]),
        "itens": None,
        "origem": ["Realizado em fevereiro de 2025, pelo Lab Escola 3D."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Equipe: [a confirmar].",
    },
    {
        "slug": "memorias-da-mare", "titulo": "Memórias da Maré / Consolidating Maré", "selo": "Parceria · 2025",
        "frase": "Uma réplica impressa em 3D do Rola-rola, o barril que os moradores da Maré criaram para levar água, vira objeto de aprendizagem numa aula de campo.",
        "reservada": "foto da réplica do Rola-rola",
        "baixar": {"titulo": "Arquivo 3D do Rola-rola", "arquivos": [
            ("Réplica do Rola-rola para imprimir", "rola-rola.stl", "STL · 2,7 MB · modelagem: Ivan Silveira, a partir do Rola-rola criado pelos moradores da Maré")]},
        "fatos": [("Nova Holanda", "Maré, Rio de Janeiro"), ("Aula de campo", "pelo território"), ("Réplica em 3D", "objeto de aprendizagem"), ("2027", "exposição DESIS Cluster, Zaragoza")],
        "o_que_e": "Na “aula de campo Maré”, estudantes e educadores do pré-vestibular da Redes da Maré percorrem o território para resgatar a memória local. Na Nova Holanda, onde faltava água encanada nos anos 1970, uma réplica do Rola-rola impressa em 3D abre a conversa sobre as tecnologias sociais criadas pelos próprios moradores e liga essa memória à fabricação digital.",
        "como": ("Como acontece", [
            "O grupo percorre a Maré, com paradas em pontos da memória local.",
            "Na Nova Holanda, conversa sobre a falta de água e as soluções dos moradores.",
            "A réplica em 3D do Rola-rola passa de mão em mão.",
            "A turma discute tecnologia social e se vê como criadora de soluções locais."]),
        "itens": None,
        "origem": ["Projeto do Rio DESIS Lab (COPPE/UFRJ) com a Redes da Maré.",
                   "Selecionado para a exposição do DESIS Cluster (Zaragoza, abril a agosto de 2027)."],
        "creditos": "Parceria: Rio DESIS Lab (COPPE/UFRJ), coordenação de Carla Cipolla, com os pesquisadores Carlos Alberto dos Santos Gonçalves e Ivan Silveira, e a Redes da Maré.",
    },
    {
        "slug": "antropolojogo", "titulo": "Antropolojogo", "selo": "Jogo · 2022",
        "frase": "Um jogo de tabuleiro de ciências sociais, criado com o LabES/UFRJ para a Olimpíada de Sociologia do Rio.",
        "reservada": "foto do tabuleiro e das peças",
        "baixar": {"titulo": "Material do jogo", "aviso": "O material para imprimir o jogo está em preparação."},
        "fatos": [("Ciências sociais", "componente"), ("16 escolas", "receberam o jogo"), ("2022", "Olimpíada de Sociologia"), ("Design Thinking", "5 etapas")],
        "o_que_e": "Um jogo de tabuleiro divertido e dinâmico, pensado para ter impacto real no ensino público de ciências sociais. É a versão física do jogo digital Antropolojogo, reimaginada para a 2ª Olimpíada de Sociologia do Estado do Rio de Janeiro.",
        "como": ("Como foi feito", [
            "Empatia: reuniões com a coordenadora do LabES para entender as expectativas.",
            "Definição: estudo de jogos parecidos, público e jogabilidade.",
            "Ideação: formatos, materiais, cores e regras.",
            "Prototipagem e implementação: o jogo foi jogado na Olimpíada e virou prêmio."]),
        "itens": None,
        "origem": ["Criado em 2022 com o Laboratório de Ensino de Sociologia Florestan Fernandes (LabES/UFRJ).",
                   "Distribuído a 16 escolas na 2ª Olimpíada de Sociologia do Estado do Rio de Janeiro."],
        "creditos": "Lab Escola 3D com o LabES/UFRJ, coordenado pela Profª Drª Julia Polessa Maçaira. Equipe: [a confirmar].",
    },
    {
        "slug": "manual-maker", "titulo": "Manual Maker", "selo": "Manual · 2025", "redirect": "../../manuais/",
        "frase": "Guias gratuitos para levar a cultura maker, o Arduino, o Micro:bit, a impressão 3D e a horta escolar para a sala de aula.",
        "reservada": "capa do Manual Maker",
        "baixar": {"titulo": "Baixe os volumes", "arquivos": [
            ("Manual completo", SITE + "2025/06/Manuais-Educacionais-Completo.pdf", "PDF · 10 MB"),
            ("Cultura maker", SITE + "2025/05/Manuais-Educacionais-Cultura-Maker.pdf", "PDF · 1 MB"),
            ("Arduino", SITE + "2025/05/Manuais-Educacionais-Arduino.pdf", "PDF · 2 MB"),
            ("Micro:bit", SITE + "2025/05/Manuais-Educacionais-Microbit.pdf", "PDF · 2 MB"),
            ("Impressão 3D", SITE + "2025/05/Manuais-Educacionais-Impressao-3D.pdf", "PDF · 3 MB"),
            ("Horta escolar", SITE + "2025/05/Manuais-Educacionais-Hortas-Escolares.pdf", "PDF · 3 MB")]},
        "fatos": [("6 volumes", "e um completo"), ("Gratuito", "para baixar"), ("Professores", "público"), ("2025", "publicação")],
        "o_que_e": "Um guia técnico e pedagógico com metodologias ativas e tecnologias para inovar o ensino com a cultura maker, organizado em volumes que podem ser usados separadamente.",
        "como": None,
        "itens": ("Os volumes", [
            ("Cultura maker", "Como o “faça você mesmo” muda a aprendizagem pela criatividade e pela colaboração."),
            ("Arduino", "Projetos interativos de eletrônica e programação na escola."),
            ("Micro:bit", "Programação, sensores e lógica de forma prática."),
            ("Impressão 3D", "Da ideia ao objeto, com modelagem e impressão."),
            ("Horta escolar", "Sustentabilidade, saúde e aprendizagem prática.")]),
        "origem": ["Produzido pelo Lab Escola 3D a partir das formações nos GETs."],
        "creditos": "Lab Escola 3D · extensão da UFRJ. Equipe: [a confirmar].",
    },
]

E = html.escape
BASE = os.path.join(os.path.dirname(__file__), "..", "_base")
FONTES = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900'
          '&family=Roboto:wght@400;500;700&display=swap">')


ITENS_MENU = [("Catálogo", "catalogo/"), ("Como usar", "licenca/"), ("Contribuir", "contribuir/"), ("Sobre o Lab", "em-obras/")]


def menu(raiz, ativo="", cel=False):
    """Menu igual em todo o site. No celular, abre e fecha sem JavaScript (<details>)."""
    links = "".join(f'<a class="ativo" href="{raiz}{h}">{n}</a>' if n == ativo else f'<a href="{raiz}{h}">{n}</a>'
                    for n, h in ITENS_MENU)
    if cel:
        return (f'<details class="menu-cel"><summary><img class="icone" src="{raiz}_base/icones/menu.svg" alt="Abrir o menu">'
                f'</summary><nav>{links}</nav></details>')
    return (f'<nav class="menu">{links}<a href="{raiz}em-obras/"><img class="icone" src="{raiz}_base/icones/lupa.svg" '
            f'alt="Buscar no catálogo (em obras)"></a></nav>')


def cabecalho_simples(raiz, ativo=""):
    """Cabeçalho das páginas que não vêm do gerador de telas (Sobre, Licença, editores...): logo + o mesmo menu."""
    links = "".join(f'<a href="{raiz}{h}" style="color:{"#fff" if n == ativo else "#3026AD"};background:{"#3026AD" if n == ativo else "transparent"};'
                    f'text-decoration:none;font-weight:700;padding:8px 12px;border-radius:6px">{n}</a>' for n, h in ITENS_MENU)
    return ('<header class="cab" style="background:#fff;display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;'
            'padding:10px 16px;font:15px/1.3 system-ui,sans-serif;border-bottom:1px solid #E5E5E5">'
            f'<a href="{raiz}"><img src="{LOGO}" alt="Lab Escola 3D — início" style="height:44px;width:auto;display:block"></a>'
            f'<nav style="display:flex;flex-wrap:wrap;gap:4px">{links}</nav></header>')


CSS_MODO_SITE = """
/* modo site: uma tela por aparelho (as duas seguem no código para o Canva) */
@media (min-width: 1200px) { body { background: var(--fundo); } .tela--cel { display: none; }
  .tela--pc { width: auto; max-width: 1440px; margin: 0 auto; } }
@media (max-width: 1199px) { body { background: var(--fundo); } .tela--pc { display: none; }
  .tela--cel { width: auto; margin: 0; } }
"""

CSS_MENU_CEL = """.menu-cel { position: relative; } .menu-cel summary { list-style: none; cursor: pointer; } .menu-cel summary::-webkit-details-marker { display: none; }
.menu-cel nav { position: absolute; right: 0; top: 44px; background: #fff; box-shadow: 0 4px 16px rgba(0,0,0,.15); border-radius: 10px;
  display: flex; flex-direction: column; min-width: 190px; z-index: 10; }
.menu-cel nav a { padding: 14px 18px; color: var(--roxo); text-decoration: none; font-weight: 700; border-bottom: 1px solid #eee; }
.menu-cel nav a.ativo { background: var(--roxo); color: #fff; }
"""

CSS_SITE = CSS_MODO_SITE + CSS_MENU_CEL


def _resolver_href(url: str, prefixo_local: str = "") -> str:
    """Resolve link relativo para outro diretório (ex.: espelho /canva/), preservando barra final."""
    if not prefixo_local or url.startswith(("http://", "https://", "mailto:", "#")):
        return url
    barra = "/" if url.endswith("/") else ""
    return posixpath.normpath(posixpath.join(prefixo_local, url)) + barra


def faixa_alfa(raiz):
    """Faixa de versão alfa no topo de toda página, com link para a página Sobre."""
    return ('<div class="alfa" style="background:#150E1F;color:#FFFFFF;font:14px/1.4 system-ui,sans-serif;'
            'padding:8px 16px;text-align:center">Protótipo em <b style="color:#E3630D">versão alfa</b> · '
            f'Lab Escola 3D · <a href="{raiz}sobre/" style="color:#FFFFFF">o que é este protótipo</a></div>')


def estilo(*nomes, extra="", modo_site=True):
    """CSS embutido na página: o Canva ignora folha de estilo externa."""
    css = "".join(open(os.path.join(BASE, n), encoding="utf-8").read() for n in nomes)
    css_modo = CSS_SITE if modo_site else ("\n" + CSS_MENU_CEL)
    return f"{FONTES}\n<style>\n{css}{css_modo}{extra}</style>"


def _baixar(p, tela, prefixo_local="", raiz="../../"):
    b = p["baixar"]
    meta = f'<p class="meta">{E(p.get("licenca", LICENCA))} <a href="{raiz}licenca/" style="color:inherit">Como usar →</a></p>'
    if "arquivos" in b and len(b["arquivos"]) == 1:
        rot, url, info = b["arquivos"][0]
        botao = (f'<a class="botao botao--grande baixar" href="{E(_resolver_href(url, prefixo_local))}">'
                 f'<img src="{raiz}_base/icones/baixar.svg" alt="">{E(rot)}</a>')
        texto = f'<h2>{E(b["titulo"])}</h2><p class="meta">{E(info)}</p>{meta}'
        if "editor" in b:  # edição online do perfil (patamar A): link secundário sob o botão
            er, eu, ei = b["editor"]
            botao += (f'<p class="meta" style="margin-top:12px"><a class="editor" href="{E(_resolver_href(eu, prefixo_local))}" '
                      f'style="color:inherit;font-weight:700">{E(er)} →</a><br>{E(ei)}</p>')
        return f'<div class="baixar-bloco"><div>{texto}</div><div>{botao}</div></div>'
    if "arquivos" in b:
        links = "".join(f'<a class="baixar" href="{E(_resolver_href(u, prefixo_local))}">{E(r)} <span>· {E(i)}</span></a>'
                        for r, u, i in b["arquivos"])
        if "editor" in b:  # o editor no navegador continua visível quando há vários arquivos
            er, eu, ei = b["editor"]
            links += (f'<p class="meta" style="margin-top:12px"><a class="editor" href="{E(_resolver_href(eu, prefixo_local))}" '
                      f'style="color:inherit;font-weight:700">{E(er)} →</a><br>{E(ei)}</p>')
        return (f'<div class="baixar-bloco"><div><h2>{E(b["titulo"])}</h2>{meta}</div>'
                f'<div class="lista">{links}</div></div>')
    editor = ""
    if "editor" in b:  # editor no navegador, mesmo sem arquivo para baixar
        er, eu, ei = b["editor"]
        editor = (f'<p class="meta" style="margin-top:12px"><a class="editor" href="{E(_resolver_href(eu, prefixo_local))}" '
                  f'style="color:inherit;font-weight:700">{E(er)} →</a><br>{E(ei)}</p>')
    return (f'<div class="baixar-bloco"><div><h2>{E(b["titulo"])}</h2>{meta}</div>'
            f'<div><p class="aviso">{E(b["aviso"])}</p>{editor}</div></div>')


def _contato(p, prefixo_local="") -> str:
    """Página de relato: no lugar do bloco de baixar, um convite (ex.: pedir uma visita) e os links do percurso."""
    titulo, texto, link = p["contato"]
    acao = f'<a class="botao botao--grande" href="{E(_resolver_href(link, prefixo_local))}">Entrar em contato</a>' if link else ""
    links = "".join(f'<a class="baixar-link" href="{E(_resolver_href(h, prefixo_local))}">{E(r)} →</a>' for r, h in p.get("links", []))
    lista = f'<div class="lista">{links}</div>' if links else ""
    return (f'<div class="baixar-bloco"><div><h2>{E(titulo)}</h2><p class="meta">{E(texto)}</p>{acao}</div>'
            f'{lista}</div>')


PRINTABLES = "https://www.printables.com/embed/"
# O embed do Printables não se ajusta à largura: Card no computador, Small no celular.
TAMANHO_EMBED = {"pc": (400, 445), "cel": (300, 340)}


def bloco_pecas(pecas: list[dict], tela: str, prefixo_local: str = "") -> str:
    """Uma peça 3D por cartão: o que ensina, cópia local para baixar e, se houver, o embed do Printables."""
    if not pecas:
        return ""
    w, h = TAMANHO_EMBED[tela]
    cartoes = []
    for pc in pecas:
        links = "".join(f'<a class="baixar" href="{E(_resolver_href(u, prefixo_local))}">{E(r)} <span>· {E(i)}</span></a>'
                        for r, u, i in pc["arquivos"])
        embed = ""
        if pc.get("printables"):
            embed = (f'<iframe src="{PRINTABLES}{int(pc["printables"])}" width="{w}" height="{h}" scrolling="no" '
                     f'frameborder="0" loading="lazy" title="{E(pc["nome"])} no Printables"></iframe>')
        cartoes.append(f'<div class="peca"><h3>{E(pc["nome"])}</h3><p>{E(pc["ensina"])}</p>'
                       f'<p class="meta">BNCC: {E(pc["bncc"])}</p><div class="lista">{links}</div>{embed}</div>')
    return ('<div class="secao"><h2>As peças</h2><p>Baixe aqui ou acesse a nossa página no Printables.</p>'
            f'<div class="pecas">{"".join(cartoes)}</div></div>')


def _midia(p, raiz="../../") -> str:
    """Devolve a capa real do catálogo ou o espaço reservado sem notas internas."""
    capas = {item["slug"]: item["imagem"] for item in carregar() if item.get("imagem")}
    img = capas.get(p["slug"])
    if img:
        return (f'<img class="capa" src="{E(raiz + img["arquivo"])}" '
                f'alt="{E(img["alt"])}" width="800" height="450">')
    return f'<div class="reservada">Imagem em preparação · {E(p["reservada"])}</div>'


def _tela(p, tela, prefixo_local="", raiz="../../"):
    pc = tela == "pc"
    rotulo = "computador (1440)" if pc else "celular (375)"
    nav = menu(raiz, "Catálogo", cel=not pc)
    fatos = "".join(f'<div class="fato"><b>{E(b)}</b><span>{E(s)}</span></div>' for b, s in p["fatos"])
    cabecalho_heroi = (
        f'<div><span class="selo">{E(p["selo"])}</span>'
        f'<h1 style="margin-top:16px">{E(p["titulo"])}</h1><p class="frase">{E(p["frase"])}</p></div>'
    )
    midia = _midia(p, raiz=raiz)
    acao = (_contato(p, prefixo_local=prefixo_local) if "contato" in p
            else _baixar(p, tela, prefixo_local=prefixo_local, raiz=raiz))
    partes = [
        f'<section class="tela tela--{tela}" data-document-role="page" data-label="Produto · {E(p["titulo"])} · {rotulo}">',
        f'<header class="topo"><a href="{raiz}"><img class="logo" src="{LOGO}" alt="Lab Escola 3D"></a>{nav}</header>',
        '<div class="onda"></div>',
        *(
            [f'<div class="heroi">{cabecalho_heroi}{midia}</div>', acao]
            if pc
            else [f'<div class="heroi">{cabecalho_heroi}</div>', acao, f'<div class="midia-cel">{midia}</div>']
        ),
        bloco_pecas(p.get("pecas") or [], tela, prefixo_local=prefixo_local),
        f'<div class="secao"><h2>Para quem</h2><div class="fatos">{fatos}</div></div>',
    ]
    o_que = f'<div><h2>O que é</h2><p>{E(p["o_que_e"])}</p></div>'
    if p["como"]:
        titulo, passos = p["como"]
        lis = "".join(f"<li>{E(x)}</li>" for x in passos)
        partes.append(f'<div class="secao duas">{o_que}<div><h2>{E(titulo)}</h2><ol class="passos">{lis}</ol></div></div>')
    else:
        partes.append(f'<div class="secao">{o_que}</div>')
    if p["itens"]:
        titulo, itens = p["itens"]
        cards = "".join(f'<div class="item"><b>{E(b)}</b><p>{E(t)}</p></div>' for b, t in itens)
        partes.append(f'<div class="secao"><h2>{E(titulo)}</h2><div class="itens">{cards}</div></div>')
    origem = "".join(f"<li>{E(x)}</li>" for x in p["origem"])
    partes.append(f'<div class="secao duas"><div><h2>De onde veio</h2><ul class="origem">{origem}</ul></div>'
                  f'<div><h2>Créditos</h2><p class="creditos">{E(p["creditos"])}</p></div></div>')
    redes = "".join(f'<img src="{raiz}_base/icones/{r}.svg" alt="{n}">' for r, n in
                    [("instagram", "Instagram"), ("facebook", "Facebook"), ("youtube", "YouTube"), ("linkedin", "LinkedIn")])
    partes.append(f'<footer class="rodape"><span>Lab Escola 3D · projeto de extensão da UFRJ · <a href="{raiz}sobre/" style="color:inherit">sobre este protótipo</a> · <a href="{raiz}contribuir/" style="color:inherit">contato</a></span>'
                  f'<div class="redes">{redes}</div></footer></section>')
    return "\n".join(partes)


def pagina(p, modo_site=True, com_faixa=True, prefixo_local="", raiz="../../") -> str:
    faixa = (faixa_alfa(raiz) + "\n") if com_faixa else ""
    return (f'<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex">\n'
            f'<title>{E(p["titulo"])} · Catálogo LE3D (protótipo)</title>\n'
            f'{estilo("site.css", "produto.css", modo_site=modo_site)}\n'
            f'</head>\n<body>\n{faixa}{_tela(p, "pc", prefixo_local=prefixo_local, raiz=raiz)}\n\n'
            f'{_tela(p, "cel", prefixo_local=prefixo_local, raiz=raiz)}\n</body>\n</html>\n')


def redirecionar(destino: str) -> str:
    """Página antiga que passou a morar noutro endereço (ex.: o Manual Maker foi para /manuais)."""
    return ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="robots" content="noindex">\n'
            f'<meta http-equiv="refresh" content="0; url={E(destino)}">\n<title>Manual Maker · Lab Escola 3D (protótipo)</title>\n'
            f'</head>\n<body>\n<p>Esta página mudou para <a href="{E(destino)}">a coleção Manual Maker</a>.</p>\n</body>\n</html>\n')


def gerar_todos(raiz: str) -> list[str]:
    saidas = []
    for p in PRODUTOS:
        pasta = os.path.join(raiz, "catalogo", p["slug"])
        os.makedirs(pasta, exist_ok=True)
        arq = os.path.join(pasta, "index.html")
        with open(arq, "w", encoding="utf-8", newline="\n") as f:
            f.write(redirecionar(p["redirect"]) if p.get("redirect") else pagina(p))
        saidas.append(arq)
    return saidas


if __name__ == "__main__":
    for a in gerar_todos(os.path.join(os.path.dirname(__file__), "..")):
        print(a)
