"""Gera os sites modelo (negócios fictícios) a partir dos dados abaixo.

  python3 gerar.py     → escreve index.html e padaria/, barbearia/, oficina/

O botão de WhatsApp de cada modelo leva para o WhatsApp de quem faz os sites,
com uma mensagem pronta ("vi o modelo e quero um site assim").
"""

from html import escape
from pathlib import Path
from urllib.parse import quote

AUTORA = "Lorrane Jose"
WHATS = "5541974002540"
WHATS_TEXTO = "(41) 97400-2540"
EMAIL = "ccbgyn2000@gmail.com"
PASTA = Path(__file__).resolve().parent

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
  <p>Seu negócio pode ter um assim: rápido, seguro e pronto para o celular.</p>
  <a class="botao" href="{e(zap)}" target="_blank" rel="noopener">Quero um site assim</a>
</div></section>
</main>

<footer><div class="envolve">
  <span>{e(s["nome"])} é um negócio fictício. Site modelo por {e(AUTORA)} · WhatsApp {WHATS_TEXTO}</span>
  <span>Este site não usa cookies nem coleta dados.</span>
</div></footer>

<a class="zap" href="{e(zap)}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">{ICONE_ZAP}</a>
</body>
</html>
"""


def galeria() -> str:
    e = escape
    zap = link_zap("Olá! Vi os modelos de site e quero conversar sobre um site para o meu negócio.")
    cartoes = "\n".join(
        f'<a class="cartao" href="{s["pasta"]}/" style="text-decoration:none;color:inherit">'
        f'<div class="icone">{s["icone"]}</div><h3>{e(s["nome"])}</h3><p>Modelo para {e(s["ramo"])}.</p>'
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
    (PASTA / "index.html").write_text(galeria(), encoding="utf-8")
    print("Gerado: index.html, " + ", ".join(f"{s['pasta']}/index.html" for s in SITES))
