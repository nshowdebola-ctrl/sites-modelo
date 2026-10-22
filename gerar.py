"""Gera os sites modelo (negócios fictícios) a partir dos dados abaixo.

  python3 gerar.py     → escreve index.html e padaria/, barbearia/, salao/, restaurante/, oficina/

O botão de WhatsApp de cada modelo leva para o WhatsApp de quem faz os sites,
com uma mensagem pronta ("vi o modelo e quero um site assim").

Um modelo com a chave "assistente" ganha o assistente virtual (assistente.js). Os dados
dele também vão para ia/src/dados/, de onde o Worker do Cloudflare (ia/) monta as
instruções da IA. Sem IA_URL, ou se a IA falhar, o assistente responde sozinho no navegador.
"""

import json
from html import escape
from pathlib import Path
from urllib.parse import quote

AUTORA = "Lorrane Jose"
WHATS = "5541974002540"
WHATS_TEXTO = "(41) 97400-2540"
EMAIL = "ccbgyn2000@gmail.com"
PASTA = Path(__file__).resolve().parent
# Endereço do Worker depois de publicado (ia/LEIA-ME.md), por exemplo
# "https://assistente-sites-modelo.SEU-NOME.workers.dev". Vazio = só o assistente local.
IA_URL = "https://assistente-sites-modelo.assistente-sites-modelo.workers.dev"

ICONE_ZAP = ('<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3C9 3 3.3 8.6 3.3 15.6c0 2.3.6 '
             '4.5 1.8 6.4L3 29l7.2-1.9c1.8 1 3.8 1.5 5.9 1.5 7 0 12.7-5.7 12.7-12.7S23 3 16 3zm0 23.2c-1.9 0-3.8-.5-5.4-1.5l-.4-.2'
             '-4.3 1.1 1.1-4.2-.3-.4a10.4 10.4 0 0 1-1.6-5.5C5.2 9.8 10 5.2 16 5.2s10.6 4.7 10.6 10.5S21.8 26.2 16 26.2zm5.8-7.8c-.3-.2'
             '-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.6 8.6 0 0 1-4.3-3.7c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6'
             '-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.8 5 2.1.9 3 1 4 .8.7-.1 1.9-.8 2.2'
             '-1.5.3-.7.3-1.4.2-1.5-.1-.1-.3-.2-.6-.3z"/></svg>')

SITES = [
    {
        "pasta": "padaria", "nome": "Padaria Forno da Vila", "icone": "🥐",
        "ramo": "padaria",
        "cores": {"fundo": "#fffaf3", "cor": "#b5651d", "cor-escura": "#8a4a12", "cor-clara": "#f7e6d0"},
        "titulo": "Pão quentinho saindo do forno a cada hora",
        "chamada": "Pães artesanais, bolos caseiros e café da manhã completo no coração do bairro. "
                   "Encomende pelo WhatsApp e retire na hora certa.",
        "botao": "Encomendar pelo WhatsApp",
        "selos": ["✔ Fornadas das 6h às 19h", "✔ Encomendas para festas", "✔ Retirada sem fila"],
        "titulo_itens": "Do nosso forno", "sub_itens": "Os mais pedidos da semana.",
        "itens": [
            ("🍞", "Pão francês", "Crocante por fora, macio por dentro. Fornadas a cada hora.", "R$ 18,90/kg"),
            ("🥖", "Pão de fermentação natural", "Massa descansada por 24 horas, casca dourada.", "R$ 22,00"),
            ("🎂", "Bolos caseiros", "Cenoura com chocolate, fubá, laranja e o de milho da casa.", "a partir de R$ 28,00"),
            ("☕", "Café da manhã", "Café coado, pão na chapa, suco e fruta. Servido até 11h.", "R$ 24,90"),
        ],
        "depoimentos": [("O pão de fermentação natural é o melhor que já comi na região.", "Mariana, cliente"),
                        ("Encomendei o bolo de aniversário pelo WhatsApp e chegou perfeito.", "Ricardo, cliente")],
        "horario": [("Segunda a sexta", "6h às 20h"), ("Sábado", "6h às 18h"), ("Domingo e feriados", "7h às 13h")],
        "endereco": "Rua das Araucárias, 100 — Bairro Exemplo, Curitiba",
        "msg": "Olá! Vi o modelo de site da padaria e quero um site assim para o meu negócio.",
    },
    {
        "pasta": "barbearia", "nome": "Barbearia Navalha Fina", "icone": "💈",
        "ramo": "barbearia",
        "cores": {"fundo": "#f6f6f4", "cor": "#1f3a5f", "cor-escura": "#132640", "cor-clara": "#dfe7f1"},
        "titulo": "Corte, barba e aquele café enquanto espera",
        "chamada": "Atendimento com hora marcada, ambiente tranquilo e profissionais experientes. "
                   "Agende em 30 segundos pelo WhatsApp.",
        "botao": "Agendar pelo WhatsApp",
        "selos": ["✔ Hora marcada, sem espera", "✔ Pix e cartão", "✔ Estacionamento ao lado"],
        "titulo_itens": "Serviços", "sub_itens": "Preços claros, sem surpresa.",
        "itens": [
            ("✂️", "Corte masculino", "Tesoura ou máquina, finalizado com lavagem.", "R$ 45,00"),
            ("🧔", "Barba completa", "Toalha quente, navalha e hidratação.", "R$ 35,00"),
            ("💈", "Corte + barba", "O combo mais pedido da casa.", "R$ 70,00"),
            ("👦", "Corte infantil", "Até 12 anos, com toda a paciência.", "R$ 35,00"),
        ],
        "depoimentos": [("Agendei pelo celular, cheguei e fui atendido na hora. Corte impecável.", "Felipe, cliente"),
                        ("Ambiente muito bom e o pessoal entende de barba.", "André, cliente")],
        "horario": [("Terça a sexta", "9h às 20h"), ("Sábado", "8h às 17h"), ("Domingo e segunda", "Fechado")],
        "endereco": "Av. do Pinheiro, 250 — Bairro Exemplo, Curitiba",
        "msg": "Olá! Vi o modelo de site da barbearia e quero um site assim para o meu negócio.",
    },
    {
        "pasta": "salao", "nome": "Salão Fio de Seda", "icone": "💇‍♀️",
        "ramo": "salão de cabeleireiro",
        "cores": {"fundo": "#fdf7f9", "cor": "#9d174d", "cor-escura": "#701a3e", "cor-clara": "#fbe4ee"},
        "titulo": "Cabelo bonito do jeito que você sempre quis",
        "chamada": "Corte, cor, mechas e tratamentos com profissionais que escutam você. "
                   "Tire dúvidas com o nosso assistente virtual a qualquer hora e agende pelo WhatsApp.",
        "botao": "Agendar pelo WhatsApp",
        "selos": ["✔ Assistente virtual 24h", "✔ Especialistas em cachos", "✔ Progressiva sem formol"],
        "titulo_itens": "Serviços", "sub_itens": "Valores para cabelo médio. Química varia com o comprimento.",
        "itens": [
            ("✂️", "Corte feminino", "Lavagem, corte e finalização. Também corte a seco para cachos.", "R$ 80,00"),
            ("💨", "Escova", "Escova modelada, lisa ou com movimento.", "a partir de R$ 50,00"),
            ("🎨", "Coloração", "Retoque de raiz ou cor global, cobrindo os fios brancos.", "a partir de R$ 120,00"),
            ("✨", "Mechas e luzes", "Luzes, balayage e morena iluminada.", "a partir de R$ 250,00"),
            ("🌿", "Progressiva sem formol", "Reduz volume e frizz, sem formol.", "a partir de R$ 220,00"),
            ("💧", "Hidratação", "Hidratação, nutrição ou reconstrução, conforme o fio.", "R$ 70,00"),
        ],
        "depoimentos": [("Tirei as dúvidas com o assistente à noite e no dia seguinte já estava com horário marcado.", "Camila, cliente"),
                        ("Finalmente um salão que entende de cacho. Saí apaixonada pelo corte.", "Bianca, cliente")],
        "horario": [("Terça e quarta", "9h às 19h"), ("Quinta e sexta", "9h às 20h"), ("Sábado", "8h às 17h"),
                    ("Domingo e segunda", "Fechado")],
        "endereco": "Rua das Hortênsias, 320 — Bairro Exemplo, Curitiba",
        "msg": "Olá! Vi o modelo de site do salão e quero um site assim para o meu negócio.",
        "assistente": {
            "saudacao": "Olá! 😊 Sou o assistente virtual do Salão Fio de Seda. Posso tirar dúvidas sobre serviços, "
                        "preços e horários, e já deixar o seu agendamento encaminhado. Como posso ajudar?",
            # Índice 0 = domingo.
            "dias": ["Fechado", "Fechado", "9h às 19h", "9h às 19h", "9h às 20h", "9h às 20h", "8h às 17h"],
            "obs_horario": "Em feriados o horário muda; confirme pelo WhatsApp.",
            "obs_preco": "Os valores de química (cor, mechas e progressiva) variam com o comprimento e o volume do "
                         "cabelo. A profissional confirma o valor antes de começar.",
            "pagamento": "Aceitamos Pix, dinheiro e cartão de débito e crédito. Serviços acima de R$ 200 podem ser "
                         "parcelados em até 3x sem juros no cartão.",
            "como_chegar": "Fica a duas quadras da praça do bairro, com estacionamento gratuito em frente.",
            "servicos": {
                "Corte feminino": {"tempo": "cerca de 1 hora",
                                   "chaves": ["corte", "cortar", "aparar", "franja", "ponta", "repicado", "chanel", "camada"]},
                "Escova": {"tempo": "cerca de 40 minutos",
                           "chaves": ["escova", "escovar", "modelar", "babyliss", "chapinha", "prancha"]},
                "Coloração": {"tempo": "cerca de 2 horas",
                              "chaves": ["coloracao", "colorir", "pintar", "tinta", "tintura", "raiz", "branco",
                                         "tonalizante", "cor"]},
                "Mechas e luzes": {"tempo": "de 3 a 4 horas",
                                   "chaves": ["mecha", "luzes", "luz", "loiro", "loira", "platinado", "balayage",
                                              "ombre", "reflexo", "descolorir", "morena iluminada"]},
                "Progressiva sem formol": {"tempo": "cerca de 3 horas",
                                           "chaves": ["progressiva", "alisar", "alisamento", "liso", "lisa", "botox",
                                                      "selagem", "frizz", "escova progressiva"]},
                "Hidratação": {"tempo": "cerca de 45 minutos",
                               "chaves": ["hidratacao", "hidratar", "tratamento", "nutricao", "reconstrucao",
                                          "cronograma", "ressecado", "quebrado", "quebradico"]},
            },
            "faq": [
                (["hora marcada", "precisa marcar", "sem marcar", "chegar direto", "ordem de chegada", "fila", "espera"],
                 "Trabalhamos com hora marcada, para você não esperar. Se surgir encaixe no dia, a equipe avisa "
                 "pelo WhatsApp. Quer que eu já encaminhe um agendamento?"),
                (["cacheado", "cacho", "crespo", "ondulado", "curly", "finalizacao", "fitagem", "transicao"],
                 "Sim! Temos profissional especializada em cachos e crespos: corte a seco, hidratação, fitagem e "
                 "acompanhamento de transição capilar. O corte para cachos tem o mesmo valor do corte feminino (R$ 80)."),
                (["noiva", "casamento", "penteado", "formatura", "festa", "madrinha", "debutante", "maquiagem", "make"],
                 "Fazemos penteados para festas a partir de R$ 150 e pacotes para noivas com teste antes do grande dia. "
                 "Maquiagem é feita por uma parceira, no próprio salão. Para datas especiais, vale agendar com antecedência."),
                (["homem", "masculino", "menino", "marido", "barba"],
                 "Atendemos homens também! Corte masculino a partir de R$ 45. Barba nós não fazemos."),
                (["crianca", "infantil", "filho", "filha", "menina", "bebe"],
                 "Atendemos crianças, sim. Corte infantil (até 10 anos) por R$ 40, com toda a paciência."),
                (["estacionamento", "estacionar", "carro", "acessibilidade", "cadeira de roda", "escada"],
                 "Temos estacionamento gratuito em frente ao salão, e a entrada é no térreo, sem escadas."),
                (["produto", "shampoo", "vende", "vendem", "venda", "loja", "kit"],
                 "Usamos produtos profissionais e também vendemos kits de manutenção para usar em casa. "
                 "Pergunte à profissional qual combina com o seu cabelo."),
                (["atraso", "atrasar", "atrasada", "atrasado", "desmarcar", "remarcar", "cancelar horario", "imprevisto"],
                 "Sem problema: para remarcar, avise pelo WhatsApp com pelo menos 2 horas de antecedência. "
                 "Atrasos de até 15 minutos a gente segura o horário."),
                (["formol", "formaldeido", "gravida", "gestante", "gravidez", "amamentando", "alergia", "alergico"],
                 "Nossa progressiva é sem formol. Para gestantes, lactantes ou quem tem alergia, recomendamos "
                 "conversar com o médico antes de qualquer química. Corte, escova e hidratação estão liberados."),
            ],
        },
    },
    {
        "pasta": "restaurante", "nome": "Restaurante Tempero da Casa", "icone": "🍽️",
        "ramo": "restaurante",
        "cores": {"fundo": "#fffaf7", "cor": "#a4161a", "cor-escura": "#7a0f12", "cor-clara": "#fbe3e1"},
        "titulo": "Comida caseira de verdade, no salão ou na sua casa",
        "chamada": "Almoço executivo, buffet por quilo e marmitas para entrega. Veja o cardápio do "
                   "dia e peça pelo WhatsApp em poucos toques.",
        "botao": "Pedir pelo WhatsApp",
        "selos": ["✔ Entrega no bairro", "✔ Cardápio novo todo dia", "✔ Opções vegetarianas"],
        "titulo_itens": "Cardápio", "sub_itens": "Os pratos que mais saem. Preços do almoço.",
        "itens": [
            ("🍛", "Prato executivo", "Arroz, feijão, salada, guarnição e a carne do dia.", "R$ 32,90"),
            ("⚖️", "Buffet por quilo", "Mais de 20 opções quentes e frias, todo dia.", "R$ 69,90/kg"),
            ("🥡", "Marmita para entrega", "Tamanho média ou grande, entregue quentinha.", "a partir de R$ 24,00"),
            ("🫘", "Feijoada de sábado", "Completa, com couve, farofa, laranja e torresmo.", "R$ 49,90"),
            ("🍝", "Massa da casa", "Massa fresca com molho de tomate ou à bolonhesa.", "R$ 38,00"),
            ("🍮", "Sobremesa caseira", "Pudim, mousse ou doce de leite da casa.", "R$ 12,00"),
        ],
        "depoimentos": [("Tempero de comida de vó. Peço a marmita toda semana pelo WhatsApp.", "Patrícia, cliente"),
                        ("A feijoada de sábado é imperdível, e o atendimento é ótimo.", "Marcos, cliente")],
        "horario": [("Segunda a sexta", "11h às 15h"), ("Sábado", "11h às 16h"), ("Domingo", "11h às 15h")],
        "endereco": "Rua das Palmeiras, 410 — Bairro Exemplo, Curitiba",
        "msg": "Olá! Vi o modelo de site do restaurante e quero um site assim para o meu negócio.",
    },
    {
        "pasta": "oficina", "nome": "Auto Center Pistão", "icone": "🔧",
        "ramo": "oficina mecânica",
        "cores": {"fundo": "#f7f8f6", "cor": "#c2410c", "cor-escura": "#9a3412", "cor-clara": "#fde3d3"},
        "titulo": "Seu carro em boas mãos, com orçamento antes de mexer",
        "chamada": "Mecânica geral, revisão, freios e suspensão. Mandamos foto e orçamento pelo "
                   "WhatsApp antes de qualquer serviço.",
        "botao": "Pedir orçamento pelo WhatsApp",
        "selos": ["✔ Orçamento sem compromisso", "✔ Garantia de 90 dias", "✔ Peças com nota"],
        "titulo_itens": "O que fazemos", "sub_itens": "Do óleo à suspensão.",
        "itens": [
            ("🛢️", "Troca de óleo e filtros", "Óleo certo para o seu motor, em 30 minutos.", "a partir de R$ 159,00"),
            ("🛑", "Freios", "Pastilhas, discos e fluido, com teste no final.", "orçamento grátis"),
            ("🔩", "Suspensão", "Amortecedores, buchas e alinhamento.", "orçamento grátis"),
            ("🔍", "Revisão completa", "Checklist de 40 itens antes de viajar.", "R$ 199,00"),
        ],
        "depoimentos": [("Mandaram foto da peça gasta antes de trocar. Confiança total.", "Juliana, cliente"),
                        ("Preço justo e entregaram no mesmo dia.", "Carlos, cliente")],
        "horario": [("Segunda a sexta", "8h às 18h"), ("Sábado", "8h às 12h"), ("Domingo", "Fechado")],
        "endereco": "Rua dos Ipês, 780 — Bairro Exemplo, Curitiba",
        "msg": "Olá! Vi o modelo de site da oficina e quero um site assim para o meu negócio.",
    },
]


def link_zap(msg: str) -> str:
    return f"https://wa.me/{WHATS}?text={quote(msg)}"


def dados_assistente(s: dict) -> dict:
    """Informações que o assistente.js e o Worker da IA usam para responder."""
    a = s["assistente"]
    teste = f"Olá! Testei o assistente virtual do modelo de {s['ramo']} e quero um assim no site do meu negócio."
    dados = {
        "nome": s["nome"], "ramo": s["ramo"], "icone": s["icone"], "saudacao": a["saudacao"],
        "negocio": s["pasta"], "ia": f"{IA_URL}/conversa" if IA_URL else "",
        "servicos": [{"nome": t, "preco": p, "desc": d, **a["servicos"][t]} for _, t, d, p in s["itens"]],
        "faq": [{"chaves": c, "resposta": r} for c, r in a["faq"]],
        "horario": s["horario"], "dias": a["dias"], "obs_horario": a["obs_horario"],
        "endereco": s["endereco"], "como_chegar": a["como_chegar"],
        "pagamento": a["pagamento"], "obs_preco": a["obs_preco"],
        # Os modelos são de negócios fictícios: o WhatsApp é o de quem faz os sites.
        "whats": WHATS, "msg_humano": teste, "msg_agendamento": teste + "\n\nPedido de teste:\n{resumo}",
        "nota_whats": f"Site modelo: este botão abre o WhatsApp de {AUTORA}, que faz os sites, e não de um salão de verdade.",
    }
    return dados


def pagina(s: dict) -> str:
    e = escape
    cores = "".join(f"--{k}: {v}; " for k, v in s["cores"].items())
    zap = link_zap(s["msg"])
    itens = "\n".join(
        f'<div class="cartao"><div class="icone">{i}</div><h3>{e(t)}</h3><p>{e(d)}</p>'
        f'<span class="preco">{e(p)}</span></div>' for i, t, d, p in s["itens"])
    depos = "\n".join(
        f'<div class="cartao depo"><div class="estrelas">★★★★★</div><p>“{e(t)}”</p><strong>{e(a)}</strong></div>'
        for t, a in s["depoimentos"])
    horario = "".join(f"<tr><td>{e(d)}</td><td>{e(h)}</td></tr>" for d, h in s["horario"])
    selos = "".join(f"<span>{e(x)}</span>" for x in s["selos"])
    if s.get("assistente"):
        assistente = (f'<script type="application/json" id="dados-assistente">'
                      f'{json.dumps(dados_assistente(s), ensure_ascii=False).replace("</", "<\\/")}</script>\n'
                      '<script src="../assistente.js" defer></script>\n')
        convite = ("Este modelo vem com um assistente virtual que responde os clientes sozinho, a qualquer hora, "
                   "sem mensalidade de IA. Toque em “Dúvidas? Pergunte aqui” para testar.")
    else:
        assistente = ""
        convite = "Seu negócio pode ter um assim: rápido, seguro e pronto para o celular."
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(s["nome"])} — site modelo</title>
<meta name="description" content="{e(s["chamada"])}">
<meta name="robots" content="noindex">
<link rel="stylesheet" href="../estilo.css">
<style>:root {{ {cores}}}</style>
</head>
<body>
<div class="modelo">Site modelo de um negócio fictício, feito por {e(AUTORA)}. <a href="../">Ver outros modelos</a></div>

<header class="topo"><div class="envolve">
  <a class="marca" href="#"><span class="icone">{s["icone"]}</span>{e(s["nome"])}</a>
  <nav class="menu"><a href="#servicos">{e(s["titulo_itens"])}</a><a href="#depoimentos">Clientes</a><a href="#horario">Horário</a></nav>
  <a class="botao" href="{e(zap)}" target="_blank" rel="noopener">WhatsApp</a>
</div></header>

<main>
<section class="capa"><div class="envolve">
  <div>
    <h1>{e(s["titulo"])}</h1>
    <p class="chamada">{e(s["chamada"])}</p>
    <div class="acoes">
      <a class="botao" href="{e(zap)}" target="_blank" rel="noopener">{e(s["botao"])}</a>
      <a class="botao contorno" href="#horario">Horário e endereço</a>
    </div>
    <div class="selos">{selos}</div>
  </div>
  <div class="arte" aria-hidden="true">{s["icone"]}</div>
</div></section>

<section class="bloco alt" id="servicos"><div class="envolve">
  <h2>{e(s["titulo_itens"])}</h2><p class="sub">{e(s["sub_itens"])}</p>
  <div class="grade">{itens}</div>
</div></section>

<section class="bloco" id="depoimentos"><div class="envolve">
  <h2>Quem já veio, recomenda</h2><p class="sub">Depoimentos ilustrativos do modelo.</p>
  <div class="grade">{depos}</div>
</div></section>

<section class="bloco alt" id="horario"><div class="envolve duas">
  <div><h2>Horário</h2><p class="sub">{e(s["endereco"])}</p><table class="horario">{horario}</table></div>
  <div class="mapa" aria-label="Mapa ilustrativo">📍</div>
</div></section>

<section class="final"><div class="envolve">
  <h2>Gostou deste site?</h2>
  <p>{e(convite)}</p>
  <a class="botao" href="{e(zap)}" target="_blank" rel="noopener">Quero um site assim</a>
</div></section>
</main>

<footer><div class="envolve">
  <span>{e(s["nome"])} é um negócio fictício. Site modelo por {e(AUTORA)} · WhatsApp {WHATS_TEXTO}</span>
  <span>Este site não usa cookies nem coleta dados.</span>
</div></footer>

<a class="zap" href="{e(zap)}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">{ICONE_ZAP}</a>
{assistente}</body>
</html>
"""


def galeria() -> str:
    e = escape
    zap = link_zap("Olá! Vi os modelos de site e quero conversar sobre um site para o meu negócio.")
    cartoes = "\n".join(
        f'<a class="cartao" href="{s["pasta"]}/" style="text-decoration:none;color:inherit">'
        f'<div class="icone">{s["icone"]}</div><h3>{e(s["nome"])}</h3><p>Modelo para {e(s["ramo"])}.'
        f'{" Com assistente virtual que responde sozinho." if s.get("assistente") else ""}</p>'
        f'<span class="preco">Ver modelo →</span></a>' for s in SITES)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sites para pequenas empresas do Paraná — {e(AUTORA)}</title>
<meta name="description" content="Modelos de site para padaria, barbearia, oficina e outros pequenos negócios do Paraná. Rápidos, seguros e prontos para o celular.">
<link rel="stylesheet" href="estilo.css">
<style>:root {{ --cor: #2563eb; --cor-escura: #1d4ed8; --cor-clara: #dbeafe; --fundo: #f8fafc; }}</style>
</head>
<body>
<main>
<section class="capa"><div class="envolve" style="grid-template-columns:1fr">
  <div>
    <h1>Sites para pequenas empresas do Paraná</h1>
    <p class="chamada">Uma página bem feita, segura (com o cadeado do HTTPS), rápida e pronta para o celular,
    com botão de WhatsApp, horário e endereço. Veja abaixo alguns modelos — os negócios são fictícios,
    o seu site é feito sob medida.</p>
    <div class="acoes"><a class="botao" href="{e(zap)}" target="_blank" rel="noopener">Conversar pelo WhatsApp</a>
    <a class="botao contorno" href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
</div></section>

<section class="bloco alt"><div class="envolve">
  <h2>Modelos</h2><p class="sub">Clique para ver como fica no computador e no celular.</p>
  <div class="grade">{cartoes}</div>
</div></section>

<section class="bloco"><div class="envolve">
  <h2>O que vem em todo site</h2><p class="sub">Sem mensalidade escondida, sem enrolação.</p>
  <div class="grade">
    <div class="cartao"><div class="icone">📱</div><h3>Pronto para o celular</h3><p>A maioria dos clientes vai abrir pelo telefone.</p></div>
    <div class="cartao"><div class="icone">🔒</div><h3>Seguro</h3><p>HTTPS configurado, sem aviso de "site não seguro".</p></div>
    <div class="cartao"><div class="icone">💬</div><h3>Botão de WhatsApp</h3><p>O cliente fala com você em um toque.</p></div>
    <div class="cartao"><div class="icone">🔎</div><h3>Aparece no Google</h3><p>Título, descrição e endereço certos para a busca.</p></div>
  </div>
</div></section>
</main>
<footer><div class="envolve">
  <span>{e(AUTORA)} · WhatsApp {WHATS_TEXTO} · {EMAIL}</span>
  <span>Este site não usa cookies nem coleta dados.</span>
</div></footer>
<a class="zap" href="{e(zap)}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">{ICONE_ZAP}</a>
</body>
</html>
"""


if __name__ == "__main__":
    for s in SITES:
        (PASTA / s["pasta"]).mkdir(exist_ok=True)
        (PASTA / s["pasta"] / "index.html").write_text(pagina(s), encoding="utf-8")
        if s.get("assistente"):
            (PASTA / "ia" / "src" / "dados" / f'{s["pasta"]}.json').write_text(
                json.dumps(dados_assistente(s), ensure_ascii=False, indent=1), encoding="utf-8")
    (PASTA / "index.html").write_text(galeria(), encoding="utf-8")
    print("Gerado: index.html, " + ", ".join(f"{s['pasta']}/index.html" for s in SITES))
