/* Assistente virtual dos sites modelo.

   As informações do negócio vêm do bloco <script id="dados-assistente"> que o
   gerar.py coloca na página. Quando a página tem o endereço da IA (dados.ia), as
   perguntas livres vão para o Worker do Cloudflare (pasta ia/), que responde com o
   Llama. O agendamento passo a passo, os botões e qualquer falha da IA ficam com o
   assistente local abaixo, que funciona sozinho no navegador: entende palavras-chave,
   com tolerância a acento, plural e erro de digitação, e lembra o último serviço citado. */

function criarAssistente(D, agora = () => new Date()) {
  const SEMANA = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];
  const SEMANA_CURTA = ['dom', 'seg', '', '', 'qui', 'sex', 'sab'];
  const SEMANA_NOME = ['domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado'];

  const norm = t => t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  const raiz = p => (p.length > 3 && p.endsWith('s') ? p.slice(0, -1) : p);
  const palavras = t => norm(t).split(' ').filter(Boolean).map(raiz);
  const maiuscula = t => t.charAt(0).toUpperCase() + t.slice(1);
  const dois = n => String(n).padStart(2, '0');

  const INTENCOES = [
    { id: 'agendar', chaves: ['agendar', 'agendamento', 'marcar', 'reservar', 'reserva', 'encaixe', 'disponivel',
      'disponibilidade', 'tem horario', 'tem vaga', 'quero marcar', 'quero agendar', 'horario livre', 'horarios livres'] },
    { id: 'duracao', chaves: ['demora', 'duracao', 'tempo', 'quanto tempo', 'rapido', 'minutos'] },
    { id: 'preco', chaves: ['preco', 'quanto', 'custa', 'custo', 'valor', 'tabela', 'cobra', 'cobram', 'caro', 'barato',
      'promocao', 'desconto'] },
    { id: 'horario', chaves: ['horario', 'hora', 'abre', 'aberto', 'fecha', 'fechado', 'funciona', 'funcionamento',
      'expediente', 'feriado', 'quando', 'que horas', ...SEMANA] },
    { id: 'endereco', chaves: ['endereco', 'onde', 'localizacao', 'localiza', 'chegar', 'rua', 'bairro', 'mapa', 'perto',
      'longe', 'onde fica'] },
    { id: 'pagamento', chaves: ['pix', 'cartao', 'credito', 'debito', 'dinheiro', 'pagamento', 'pagar', 'parcela',
      'parcelar', 'parcelado', 'aceita', 'aceitam'] },
    { id: 'humano', chaves: ['atendente', 'pessoa', 'humano', 'equipe', 'falar com', 'whatsapp', 'zap', 'telefone',
      'ligar', 'contato', 'numero'] },
    { id: 'servicos', chaves: ['servico', 'faz', 'fazem', 'oferece', 'oferecem', 'trabalha', 'trabalham', 'opcoes',
      'lista', 'tipo', 'que tem'] },
    { id: 'obrigado', chaves: ['obrigado', 'obrigada', 'brigado', 'valeu', 'agradeco', 'perfeito', 'otimo', 'show'] },
    { id: 'tchau', chaves: ['tchau', 'ate mais', 'ate logo', 'falou', 'flw'] },
    { id: 'saudacao', chaves: ['oi', 'ola', 'oie', 'opa', 'eai', 'eae', 'bom dia', 'boa tarde', 'boa noite', 'hello', 'salve'] },
  ];
  const CANCELAR = ['cancelar', 'cancela', 'sair', 'parar', 'desisto', 'desisti', 'esquece', 'deixa pra la', 'nao quero'];
  // Palavras comuns que lembram uma palavra-chave mas não são ("precisa" × "preço").
  const NEUTRAS = ['precisa', 'preciso', 'precisar', 'precisam', 'marca', 'quer', 'quero', 'queria', 'gostaria', 'cabelo',
    'salao', 'voce', 'vcs', 'tudo', 'bem'];

  const FAQ = D.faq.map((f, i) => ({ id: 'faq' + i, chaves: f.chaves, resposta: f.resposta }));
  const SERVICOS = D.servicos.map(s => ({ ...s, chaves: [...s.chaves, s.nome] }));
  const porId = id => INTENCOES.find(c => c.id === id);
  // Em caso de empate vence quem vem antes.
  const ORDEM = [...['agendar', 'duracao', 'preco'].map(porId), ...FAQ,
    ...['horario', 'endereco', 'pagamento', 'humano', 'servicos', 'obrigado', 'tchau', 'saudacao'].map(porId)];
  const INICIAIS = ['Ver todos os preços', 'Horário', 'Quero agendar', 'Endereço'];

  const VOCAB = new Set(NEUTRAS);
  for (const c of [...INTENCOES, ...FAQ, ...SERVICOS, { chaves: CANCELAR }])
    for (const k of c.chaves) { const kn = norm(k); if (!kn.includes(' ')) VOCAB.add(raiz(kn)); }

  function distancia(a, b) {
    const d = Array.from({ length: b.length + 1 }, (_, j) => j);
    for (let i = 1; i <= a.length; i++) {
      let diagonal = d[0];
      d[0] = i;
      for (let j = 1; j <= b.length; j++) {
        const acima = d[j];
        d[j] = Math.min(d[j] + 1, d[j - 1] + 1, diagonal + (a[i - 1] === b[j - 1] ? 0 : 1));
        diagonal = acima;
      }
    }
    return d[b.length];
  }

  // Palavra conhecida só vale igual; desconhecida pode ser variação ("cortar" × "corte")
  // ou erro de digitação ("progresiva").
  function parecida(p, k) {
    if (p === k) return true;
    if (VOCAB.has(p) || p.length < 4 || k.length < 4) return false;
    let i = 0;
    while (i < p.length && i < k.length && p[i] === k[i]) i++;
    if (i >= Math.max(4, Math.min(p.length, k.length) - 1)) return true;
    return Math.min(p.length, k.length) >= 5 && distancia(p, k) <= 1;
  }

  // Cada palavra do visitante conta uma vez ("corta" lembra "corte" e "cortar", mas vale 1);
  // expressões inteiras ("tem horario") valem 2.
  function pontos(chaves, ws, frase) {
    let n = 0;
    const soltas = [];
    for (const k of chaves) {
      const kn = norm(k);
      if (kn.includes(' ')) { if (frase.includes(` ${kn} `)) n += 2; }
      else soltas.push(raiz(kn));
    }
    return n + ws.filter(p => soltas.some(k => parecida(p, k))).length;
  }

  function analisar(texto) {
    const ws = palavras(texto), frase = ` ${norm(texto)} `;
    let melhor = null, n = 0;
    for (const c of ORDEM) { const x = pontos(c.chaves, ws, frase); if (x > n) { melhor = c; n = x; } }
    let serv = null, ns = 0;
    for (const s of SERVICOS) { const x = pontos(s.chaves, ws, frase); if (x > ns) { serv = s; ns = x; } }
    return { texto, ws, frase, id: melhor && melhor.id, faq: melhor && melhor.resposta, n, serv, ns };
  }

  // ---------- Datas ----------
  const fechado = h => /fechado/i.test(h);
  const fechaAs = h => { const m = h.match(/(\d{1,2})h\s*$/); return m ? +m[1] : 24; };

  function emDias(k) {
    const d = agora();
    d.setHours(12, 0, 0, 0);
    d.setDate(d.getDate() + k);
    return d;
  }

  function lerDia(texto) {
    const hoje = emDias(0), n = ` ${norm(texto)} `;
    let m = texto.match(/(\d{1,2})\s*[/.-]\s*(\d{1,2})/);
    if (m) {
      const dia = +m[1], mes = +m[2] - 1;
      const d = new Date(hoje.getFullYear(), mes, dia, 12);
      if (mes >= 0 && mes < 12 && d.getDate() === dia) {
        if (d < hoje) d.setFullYear(d.getFullYear() + 1);
        return d;
      }
    }
    if (n.includes(' depois de amanha ')) return emDias(2);
    if (n.includes(' amanha ')) return emDias(1);
    if (n.includes(' hoje ')) return emDias(0);
    const ws = palavras(texto);
    for (let i = 0; i < 7; i++)
      if (ws.some(p => p === SEMANA_CURTA[i] || parecida(p, SEMANA[i]))) return emDias((i - hoje.getDay() + 7) % 7);
    m = n.match(/ dia (\d{1,2}) /);
    if (m) for (let k = 0; k < 62; k++) { const d = emDias(k); if (d.getDate() === +m[1]) return d; }
    return null;
  }

  const dataBonita = d => `${SEMANA_NOME[d.getDay()]}, ${dois(d.getDate())}/${dois(d.getMonth() + 1)}`;

  function rotuloDia(d) {
    const k = Math.round((d - emDias(0)) / 864e5);
    return k === 0 ? 'hoje' : k === 1 ? 'amanhã' : SEMANA_NOME[d.getDay()];
  }

  function proximosDias(quantos) {
    const lista = [];
    for (let k = 0; k < 14 && lista.length < quantos; k++) {
      const d = emDias(k), h = D.dias[d.getDay()];
      if (fechado(h) || (k === 0 && agora().getHours() >= fechaAs(h) - 1)) continue;
      const data = `${dois(d.getDate())}/${dois(d.getMonth() + 1)}`;
      lista.push(k === 0 ? `Hoje, ${data}` : k === 1 ? `Amanhã, ${data}` : `${maiuscula(SEMANA_NOME[d.getDay()].split('-')[0])}, ${data}`);
    }
    return lista;
  }

  // ---------- Respostas ----------
  const zap = msg => `https://wa.me/${D.whats}?text=${encodeURIComponent(msg)}`;
  const falarComEquipe = { rotulo: 'Falar no WhatsApp', href: zap(D.msg_humano) };
  const tabela = campo => SERVICOS.map(s => `• ${s.nome}: ${s[campo]}`).join('\n');

  let ultimo = null, fluxo = null, falhas = 0;

  function responderLivre(a) {
    const s = a.serv;
    if (a.id && a.id.startsWith('faq') && a.ns <= a.n) return { texto: a.faq, chips: ['Quero agendar', 'Ver todos os preços'] };
    switch (a.id) {
      case 'agendar': return iniciarAgendamento(s || ultimo, a.texto);
      case 'preco': {
        const qual = s || (!/ (todo|toda|tabela|lista|servico)/.test(a.frase) && ultimo);
        if (qual) return { texto: `**${qual.nome}**: ${qual.preco}.\n${qual.desc}`, chips: ['Quero agendar', 'Ver todos os preços'] };
        return { texto: `Nossos valores:\n${tabela('preco')}\n\n${D.obs_preco}`, chips: ['Quero agendar', 'Horário'] };
      }
      case 'duracao': {
        const qual = s || ultimo;
        if (qual) return { texto: `**${qual.nome}** leva ${qual.tempo}.`, chips: ['Quero agendar', 'Ver todos os preços'] };
        return { texto: `Tempo médio de cada serviço:\n${tabela('tempo')}`, chips: ['Quero agendar'] };
      }
      case 'horario': {
        const linhas = D.horario.map(([q, h]) => `• ${q}: ${h}`).join('\n');
        const d = lerDia(a.texto);
        let texto = `Nosso horário:\n${linhas}\n\n${D.obs_horario}`;
        if (d) {
          const h = D.dias[d.getDay()], quando = maiuscula(rotuloDia(d));
          texto = (fechado(h) ? `${quando} estamos fechados.` : `${quando} atendemos das ${h}.`) + `\n\n${texto}`;
        }
        return { texto, chips: ['Quero agendar', 'Endereço'] };
      }
      case 'endereco': return { texto: `📍 ${D.endereco}\n${D.como_chegar}`, chips: ['Horário', 'Quero agendar'] };
      case 'pagamento': return { texto: D.pagamento, chips: ['Ver todos os preços', 'Quero agendar'] };
      case 'humano':
        return { texto: 'Claro! Para falar com uma pessoa da equipe, é só tocar no botão.', link: falarComEquipe, nota: D.nota_whats };
      case 'obrigado': return { texto: 'Por nada! 💕 Se precisar de mais alguma coisa, é só chamar.', chips: INICIAIS };
      case 'tchau': return { texto: 'Até logo! Foi um prazer ajudar. 👋' };
    }
    if (s) return { texto: `**${s.nome}**: ${s.preco}.\n${s.desc}\nDuração: ${s.tempo}.`, chips: ['Quero agendar', 'Ver todos os preços'] };
    if (a.id === 'servicos')
      return { texto: `Nossos serviços:\n${tabela('preco')}\n\nQuer saber mais de algum? É só perguntar.`, chips: SERVICOS.slice(0, 4).map(x => x.nome) };
    if (a.id === 'saudacao') return inicio();
    return null;
  }

  function naoEntendi() {
    falhas++;
    const r = { texto: 'Desculpe, não entendi bem. 🤔 Posso ajudar com preços, horários, endereço, formas de pagamento ou já deixar um agendamento encaminhado.', chips: INICIAIS };
    if (falhas >= 2) Object.assign(r, { texto: r.texto + '\n\nSe preferir, fale direto com a equipe:', link: falarComEquipe, nota: D.nota_whats });
    return r;
  }

  // ---------- Agendamento (passo a passo) ----------
  function pedirServico(prefixo = '') {
    fluxo.passo = 'servico';
    return { texto: prefixo + 'Qual serviço você quer fazer?', chips: [...SERVICOS.map(s => s.nome), 'Cancelar'] };
  }
  function pedirDia(prefixo = '') {
    fluxo.passo = 'dia';
    return { texto: prefixo + 'Para qual dia? Pode escrever, por exemplo, "sábado" ou "25/10".', chips: [...proximosDias(4), 'Cancelar'] };
  }
  function pedirPeriodo(prefixo = '') {
    fluxo.passo = 'periodo';
    return { texto: prefixo + 'Prefere de manhã ou à tarde? Se quiser, diga um horário (ex.: 14h).', chips: ['Manhã', 'Tarde', 'Qualquer horário', 'Cancelar'] };
  }
  function pedirNome(prefixo = '') {
    fluxo.passo = 'nome';
    return { texto: prefixo + 'E qual é o seu nome?', chips: ['Cancelar'] };
  }
  const PEDIR = { servico: pedirServico, dia: pedirDia, periodo: pedirPeriodo, nome: pedirNome };

  // Aproveita o dia se ele já veio na frase ("tem horário amanhã?").
  function iniciarAgendamento(serv, texto) {
    fluxo = { servico: serv || null };
    const d = lerDia(texto);
    if (d && !fechado(D.dias[d.getDay()])) fluxo.dia = d;
    if (!serv) return pedirServico('Claro! ');
    return depoisDoServico(`Ótimo, vamos agendar **${serv.nome}** (${serv.preco}). `);
  }

  function depoisDoServico(prefixo) {
    if (!fluxo.dia) return pedirDia(prefixo);
    return pedirPeriodo(`${prefixo}Dia: **${dataBonita(fluxo.dia)}** (atendemos das ${D.dias[fluxo.dia.getDay()]}). `);
  }

  // Pergunta no meio do agendamento: responde e volta para o passo em que estava.
  function desvio(a) {
    if (!a.id || ['agendar', 'saudacao', 'obrigado', 'servicos'].includes(a.id)) return null;
    const r = responderLivre(a);
    if (!r) return null;
    const volta = PEDIR[fluxo.passo]();
    return { ...r, texto: `${r.texto}\n\nVoltando ao agendamento: ${volta.texto}`, chips: volta.chips };
  }

  function passoFluxo(a) {
    if (pontos(CANCELAR, a.ws, a.frase) > 0) {
      fluxo = null;
      return { texto: 'Tudo bem, cancelei o agendamento. Posso ajudar em mais alguma coisa?', chips: INICIAIS };
    }
    const passo = fluxo.passo;
    if (passo === 'servico') {
      if (a.serv) { fluxo.servico = a.serv; return depoisDoServico(`Ótimo: **${a.serv.nome}** (${a.serv.preco}). `); }
      const d = lerDia(a.texto);
      if (d && !fechado(D.dias[d.getDay()])) { fluxo.dia = d; return pedirServico(`Anotei **${dataBonita(d)}**. `); }
      return desvio(a) || pedirServico('Não encontrei esse serviço. ');
    }
    let troca = '';
    if (passo !== 'nome' && a.serv && a.serv !== fluxo.servico) {
      fluxo.servico = a.serv;
      troca = `Troquei para **${a.serv.nome}** (${a.serv.preco}). `;
    }
    if (passo === 'dia') {
      const d = lerDia(a.texto);
      if (!d) return troca ? pedirDia(troca) : desvio(a) || pedirDia('Não entendi a data. ');
      const h = D.dias[d.getDay()];
      if (fechado(h)) return pedirDia(`${troca}Nesse dia (${dataBonita(d)}) estamos fechados. `);
      fluxo.dia = d;
      return pedirPeriodo(`${troca}Anotado: **${dataBonita(d)}** (atendemos das ${h}). `);
    }
    if (passo === 'periodo') {
      const reconhecido = / (manha|tarde|noite|qualquer|cedo|almoco) /.test(a.frase) || /\d{1,2}\s*(h|:|hora)/i.test(a.texto);
      const outroDia = !reconhecido && lerDia(a.texto);
      if (outroDia) {
        const h = D.dias[outroDia.getDay()];
        if (fechado(h)) return pedirPeriodo(`${troca}Nesse dia (${dataBonita(outroDia)}) estamos fechados; mantive ${dataBonita(fluxo.dia)}. `);
        fluxo.dia = outroDia;
        return pedirPeriodo(`${troca}Troquei o dia para **${dataBonita(outroDia)}** (atendemos das ${h}). `);
      }
      if (!reconhecido && !troca) { const r = desvio(a); if (r) return r; }
      if (!reconhecido && troca) return pedirPeriodo(troca);
      fluxo.periodo = a.texto.trim().slice(0, 40).toLowerCase();
      return pedirNome(troca);
    }
    // passo === 'nome'
    if (a.texto.includes('?')) { const r = desvio(a); if (r) return r; }
    const nome = maiuscula(a.texto.trim().replace(/^(meu nome [eé]|me chamo|eu sou|sou [oa]|aqui [eé])\s+/i, '').slice(0, 40));
    if (!nome) return pedirNome();
    const s = fluxo.servico, data = dataBonita(fluxo.dia), periodo = fluxo.periodo;
    const resumo = `Serviço: ${s.nome} (${s.preco})\nDia: ${data}\nHorário: ${periodo}\nNome: ${nome}`;
    fluxo = null;
    return {
      texto: `Prontinho, ${nome}! 🎉 Seu pedido ficou assim:\n**${s.nome}** (${s.preco})\n${maiuscula(data)}, ${periodo}\n\n` +
        'Toque no botão para enviar pelo WhatsApp. A equipe confirma o horário com você.',
      link: { rotulo: 'Enviar pedido pelo WhatsApp', href: zap(D.msg_agendamento.replace('{resumo}', resumo)) },
      nota: D.nota_whats,
      chips: ['Ver todos os preços', 'Endereço'],
    };
  }

  function inicio() {
    return { texto: D.saudacao, chips: INICIAIS };
  }

  // Agendamento e "falar com a equipe" ficam sempre aqui (precisam do passo a passo
  // e do botão de WhatsApp); o resto pode ir para a IA.
  function querLocal(texto) {
    const a = analisar(texto);
    if (a.serv) ultimo = a.serv;
    return Boolean(fluxo) || a.id === 'agendar' || a.id === 'humano';
  }

  function responder(texto) {
    const a = analisar(texto);
    let r;
    if (fluxo) r = passoFluxo(a);
    else r = responderLivre(a) || naoEntendi();
    if (r !== null && !r.texto.startsWith('Desculpe')) falhas = 0;
    if (a.serv) ultimo = a.serv;
    return r;
  }

  return { inicio, responder, querLocal };
}

// ---------- Janela de conversa na página ----------
if (typeof document !== 'undefined') (() => {
  const fonte = document.getElementById('dados-assistente');
  if (!fonte) return;
  const D = JSON.parse(fonte.textContent);
  const bot = criarAssistente(D);
  const esc = t => t.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const formata = t => esc(t).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');

  const abrir = document.createElement('button');
  abrir.type = 'button';
  abrir.className = 'assist-abrir';
  abrir.setAttribute('aria-controls', 'assist');
  abrir.setAttribute('aria-expanded', 'false');
  abrir.innerHTML = '<span aria-hidden="true">💬</span><span class="assist-rotulo">Dúvidas? Pergunte aqui</span>';

  const painel = document.createElement('section');
  painel.className = 'assist';
  painel.id = 'assist';
  painel.hidden = true;
  painel.setAttribute('aria-label', 'Assistente virtual');
  painel.innerHTML = `
    <header><div class="assist-avatar" aria-hidden="true">${esc(D.icone)}</div>
      <div><b>Assistente virtual</b><small>${esc(D.nome)} · ${D.ia ? 'com IA' : 'responde na hora'}</small></div>
      <button type="button" class="assist-fechar" aria-label="Fechar">×</button></header>
    <div class="assist-msgs" aria-live="polite"></div>
    <div class="assist-chips"></div>
    <form class="assist-form"><input type="text" aria-label="Escreva sua pergunta" placeholder="Escreva sua pergunta…" autocomplete="off" maxlength="300">
      <button type="submit" aria-label="Enviar">➤</button></form>
    <p class="assist-aviso">${D.ia
      ? 'Respostas de inteligência artificial (Llama), que podem ter erros: a equipe confirma tudo pelo WhatsApp. Não envie dados pessoais.'
      : 'Respostas automáticas. O que você escreve fica só no seu aparelho.'}</p>`;
  document.body.append(abrir, painel);

  const msgs = painel.querySelector('.assist-msgs');
  const chips = painel.querySelector('.assist-chips');
  const campo = painel.querySelector('input');
  let ocupado = false, iniciou = false, chipsAtuais = [];
  const historico = [];

  function bolha(classe, html) {
    const div = document.createElement('div');
    div.className = 'assist-msg ' + classe;
    div.innerHTML = html;
    msgs.append(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
  }

  function mostrarChips(lista) {
    chipsAtuais = lista;
    chips.replaceChildren(...lista.map(t => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = t;
      b.onclick = () => enviar(t);
      return b;
    }));
  }

  function mostrar(r) {
    const div = bolha('robo', formata(r.texto));
    if (r.link) {
      const a = document.createElement('a');
      Object.assign(a, { className: 'botao', href: r.link.href, target: '_blank', rel: 'noopener', textContent: r.link.rotulo });
      div.append(a);
    }
    if (r.nota) { const s = document.createElement('small'); s.textContent = r.nota; div.append(s); }
    mostrarChips(r.chips || []);
    msgs.scrollTop = msgs.scrollHeight;
  }

  // Devolve null se a IA não responder (sem internet, cota do dia esgotada etc.).
  async function perguntarIA() {
    const parar = new AbortController();
    const prazo = setTimeout(() => parar.abort(), 15000);
    try {
      const r = await fetch(D.ia, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ negocio: D.negocio, mensagens: historico.slice(-10) }),
        signal: parar.signal,
      });
      const { resposta } = r.ok ? await r.json() : {};
      return resposta ? { texto: resposta, chips: ['Quero agendar', 'Falar com a equipe'] } : null;
    } catch {
      return null;
    } finally {
      clearTimeout(prazo);
    }
  }

  async function enviar(texto) {
    texto = texto.trim();
    if (!texto || ocupado) return;
    ocupado = true;
    const local = !D.ia || chipsAtuais.includes(texto) || bot.querLocal(texto);
    bolha('cliente', esc(texto));
    campo.value = '';
    mostrarChips([]);
    historico.push({ role: 'user', content: texto });
    const digitando = bolha('robo assist-digitando', '•••');
    const r = (!local && await perguntarIA()) || bot.responder(texto);
    historico.push({ role: 'assistant', content: r.texto });
    // A resposta local é instantânea: uma pausa curta deixa a conversa mais natural.
    setTimeout(() => { digitando.remove(); mostrar(r); ocupado = false; }, local ? 450 + Math.min(r.texto.length * 3, 700) : 0);
  }

  function alternar(aberto) {
    painel.hidden = !aberto;
    abrir.hidden = aberto;
    abrir.setAttribute('aria-expanded', String(aberto));
    if (!aberto) return abrir.focus();
    if (!iniciou) { iniciou = true; mostrar(bot.inicio()); }
    if (matchMedia('(min-width: 521px)').matches) campo.focus();
  }

  abrir.onclick = () => alternar(true);
  painel.querySelector('.assist-fechar').onclick = () => alternar(false);
  painel.addEventListener('keydown', e => { if (e.key === 'Escape') alternar(false); });
  painel.querySelector('form').onsubmit = e => { e.preventDefault(); enviar(campo.value); };
})();

if (typeof module !== 'undefined') module.exports = { criarAssistente };
