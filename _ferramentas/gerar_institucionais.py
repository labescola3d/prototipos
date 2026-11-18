"""Gera as telas institucionais: licenca/ e contribuir/ (mesmo visual da página Sobre).

Uso: py -X utf8 _ferramentas/gerar_institucionais.py
Protótipo vindo da Meta AI (18/11/2026), com acabamento do Claude.
"""
import os

EMAIL_LAB = "labescola3d@gmail.com"  # canal de envio (decisão de Ivan, 18/11); [a confirmar se é o oficial]

CSS = """body{margin:0;background:#F2F2F2;color:#150E1F;font:17px/1.55 'Source Sans 3',system-ui,sans-serif}
main{max-width:860px;margin:0 auto;padding:28px 16px 56px}
h1,h2{font-family:'Big Shoulders Display',sans-serif;font-weight:700;color:#3026AD;line-height:1.1}
h1{font-size:44px;margin:8px 0 12px}h2{font-size:28px;margin:32px 0 10px}
a{color:#3026AD}
.crumb{font-size:14px;color:#555}
.selo{display:inline-block;background:#E3630D;color:#fff;font-weight:700;font-size:13px;padding:3px 10px;border-radius:99px}
.lead{font-size:19px}
.tres{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:18px 0}
.tres>div,.cartao{background:#fff;border-radius:10px;padding:16px 18px}
.tres b{display:block;font-family:'Big Shoulders Display',sans-serif;font-size:22px;color:#3026AD}
.passos{background:#3026AD;color:#fff;border-radius:10px;padding:18px 22px}
.passos h2{color:#fff;margin-top:0}
.pergunta{background:#fff;border-radius:10px;padding:14px 18px;margin:10px 0;border-left:5px solid #3026AD}
.pergunta h3{margin:0 0 4px;font-size:19px}
.pergunta p{margin:0}
.tag{display:inline-block;font-size:12px;font-weight:700;border-radius:99px;padding:2px 9px;margin-bottom:6px;background:#E8E6F7;color:#3026AD}
.tag.nao{background:#FBE5D6;color:#8A3A06}
.copiar{display:block;background:#fff;border:2px dashed #3026AD;border-radius:8px;padding:12px;font-size:15px;margin:10px 0}
.botao{display:inline-block;background:#E3630D;color:#fff;font-weight:700;text-decoration:none;padding:12px 22px;border-radius:99px;margin:10px 10px 0 0}
.botao.contorno{background:#fff;color:#3026AD;border:2px solid #3026AD}
.dois{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.check label{display:block;margin:8px 0}
.aviso{background:#fff;border-left:5px solid #E3630D;border-radius:8px;padding:12px 16px;margin:16px 0}
.pequeno{font-size:14px;color:#555}
footer{margin-top:40px;font-size:14px;color:#555}
@media(max-width:700px){.tres,.dois{grid-template-columns:1fr}h1{font-size:36px}}
"""

FAIXA = ('<div class="alfa" style="background:#150E1F;color:#FFFFFF;font:14px/1.4 system-ui,sans-serif;padding:8px 16px;'
         'text-align:center">Protótipo em <b style="color:#E3630D">versão alfa</b> · Lab Escola 3D · '
         '<a href="../sobre/" style="color:#FFFFFF">o que é este protótipo</a></div>')

RODAPE = ('<footer>Lab Escola 3D · projeto de extensão da UFRJ · materiais e código sob CC BY-NC-SA 4.0 · '
          '<a href="../licenca/">licença e como usar</a> · <a href="../contribuir/">como contribuir</a></footer>')


def pagina(titulo, corpo):
    return ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{titulo} · Lab Escola 3D (protótipo)</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700'
            '&family=Source+Sans+3:wght@400;700&display=swap">\n'
            f'<style>\n{CSS}</style>\n</head>\n<body>\n{FAIXA}\n<main>\n{corpo}\n{RODAPE}\n</main>\n</body>\n</html>\n')


def perg(tag, cls, titulo, texto):
    return (f'<div class="pergunta"><span class="tag{cls}">{tag}</span><h3>{titulo}</h3><p>{texto}</p></div>')


LICENCA = f"""<p class="crumb"><a href="../">Início</a> › Licença e como usar</p>
<span class="selo">Gratuito</span>
<h1>Licença e como usar</h1>
<p class="lead">A regra é curta: <b>pode usar, copiar e adaptar para a sua aula, sem vender, citando o Lab Escola 3D.</b></p>
<div class="tres">
<div><b>Pode usar</b>Na sua aula, com suas turmas, sem pagar nada.</div>
<div><b>Pode adaptar</b>Mude o tema, as perguntas e o nível.</div>
<div><b>Precisa citar</b>Mantenha o crédito ao Lab Escola 3D.</div>
</div>
<div class="passos"><h2>Como usar em 3 passos</h2><ol>
<li>Escolha um material no <a href="../catalogo/" style="color:#fff">catálogo</a>.</li>
<li>Baixe e imprima — ou edite no próprio site, quando o material tiver o botão de editar.</li>
<li>Use na aula. Se adaptar, mantenha o crédito ao Lab Escola 3D.</li></ol></div>
<h2>Perguntas e respostas</h2>
{perg("Pode", "", "Posso usar o material na minha aula?", "<b>Sim.</b> É para isso que ele existe. Baixe, imprima e use com suas turmas.")}
{perg("Não pode", " nao", "Posso vender o material?", "<b>Não.</b> O material é gratuito e não pode ser vendido, nem a versão que você adaptar.")}
{perg("Precisa citar", "", "Preciso citar o Lab Escola 3D?", "<b>Sim, sempre</b> — mesmo se você adaptar. Mantenha o nome do Lab e a licença na sua versão.")}
{perg("Pode", "", "Posso mudar o jogo?", "<b>Sim.</b> Troque o tema e as perguntas, simplifique ou dificulte, crie cartas novas para a sua turma.")}
{perg("Pode", "", "Se eu mudar, preciso compartilhar a minha versão?", "<b>Só se você distribuir.</b> Se passar adiante, compartilhe também de graça e com a mesma licença.")}
{perg("A confirmar", " nao", "Posso usar em escola particular ou em curso pago?", "Usar na aula, sim; vender o material, não. Os casos de curso pago ainda estão em análise pela coordenação do projeto: [a confirmar]. Na dúvida, use só na sua aula e cite a fonte.")}
{perg("Pode", "", "Posso postar foto da atividade?", "<b>Sim, se a sua escola permitir.</b> Cite o Lab Escola 3D. <b>Não publique foto, nome ou dado de estudante</b>: mostre só os materiais.")}
<h2>Copie e cole o crédito</h2>
<p>Use esta frase na sua versão adaptada:</p>
<span class="copiar">Adaptado de material do Lab Escola 3D (UFRJ) — CC BY-NC-SA 4.0 — labescola3d.rio.br</span>
<a class="botao" href="../catalogo/">Ver o catálogo</a><a class="botao contorno" href="../contribuir/">Mandar a minha adaptação</a>
<p class="pequeno">Licença completa: <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt-br">Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0</a>. Esta página é um resumo em linguagem simples e não substitui o texto da licença.</p>"""

ASSUNTO_ADAPT = "Adaptacao%20de%20material%20-%20Lab%20Escola%203D"
ASSUNTO_SUGEST = "Sugestao%20de%20material%20-%20Lab%20Escola%203D"

CONTRIBUIR = f"""<p class="crumb"><a href="../">Início</a> › Como contribuir</p>
<span class="selo">Sem cadastro</span>
<h1>Como contribuir</h1>
<p class="lead">Escolha um caminho. Nenhum deles pede cadastro: você manda um e-mail ao Lab, só com o que quiser contar.</p>
<div class="dois">
<div class="cartao"><h2 style="margin-top:0">1 · Mandar uma adaptação</h2>
<p>Você mudou um material do Lab e ficou bom? Mande de volta para outras professoras usarem: o PDF da sua versão e duas linhas sobre o que mudou.</p>
<span class="copiar">Material: [nome] / O que mudei: [ex.: perguntas para o 4º ano] / Serve para: [ano e tempo de aula]</span>
<a class="botao" href="mailto:{EMAIL_LAB}?subject={ASSUNTO_ADAPT}">Enviar adaptação por e-mail</a></div>
<div class="cartao"><h2 style="margin-top:0">2 · Sugerir um material</h2>
<p>Não precisa mandar arquivo. Diga o que falta no catálogo: tema, ano e tempo de aula.</p>
<span class="copiar">Sugestão: [tema] / Para: [ano] / Tempo: [minutos] / Preciso de: [ex.: só impressão P&amp;B]</span>
<a class="botao contorno" href="mailto:{EMAIL_LAB}?subject={ASSUNTO_SUGEST}">Enviar sugestão por e-mail</a></div>
</div>
<p class="pequeno">Se o botão não abrir o seu e-mail, escreva para <b>{EMAIL_LAB}</b>.</p>
<h2>Antes de enviar, confira</h2>
<div class="cartao check">
<label><input type="checkbox"> O arquivo abre no celular e no computador</label>
<label><input type="checkbox"> Versão colorida até 5 MB; preto e branco até 2 MB</label>
<label><input type="checkbox"> <b>Sem nome, foto ou dado de estudante</b></label>
<label><input type="checkbox"> Tem o crédito: Adaptado de material do Lab Escola 3D — CC BY-NC-SA 4.0</label>
<label><input type="checkbox"> Escrevi o que mudei e para qual turma serve</label>
</div>
<h2>O que acontece depois</h2>
<ul>
<li>O Lab revisa o que você mandou.</li>
<li>Se publicar, a sua versão fica gratuita, com o seu crédito pela adaptação e a mesma licença (CC BY-NC-SA 4.0).</li>
<li>Prazo de resposta: [a confirmar].</li>
</ul>
<div class="aviso">O Lab usa o seu e-mail só para responder a este envio. Não vende, não compartilha e não cadastra em lista.</div>
<a class="botao contorno" href="../catalogo/">Voltar ao catálogo</a>"""


def gerar(raiz):
    saidas = []
    for pasta, titulo, corpo in (("licenca", "Licença e como usar", LICENCA), ("contribuir", "Como contribuir", CONTRIBUIR)):
        os.makedirs(os.path.join(raiz, pasta), exist_ok=True)
        arq = os.path.join(raiz, pasta, "index.html")
        with open(arq, "w", encoding="utf-8", newline="\n") as f:
            f.write(pagina(titulo, corpo))
        saidas.append(arq)
    return saidas


if __name__ == "__main__":
    for a in gerar(os.path.join(os.path.dirname(__file__), "..")):
        print(a)
