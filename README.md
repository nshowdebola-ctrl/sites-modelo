# Sites modelo

Modelos de site para pequenas empresas do Paraná (negócios fictícios), feitos
por Lorrane Jose. Publicados em https://nshowdebola-ctrl.github.io/sites-modelo/

- `gerar.py` — gera as páginas a partir dos dados (rode `python3 gerar.py`).
- `estilo.css` — estilo comum; cada modelo define as próprias cores.
- `assistente.js` — chat do assistente virtual. Liga em qualquer modelo que tenha a chave
  `"assistente"` no `gerar.py` (hoje só no `salao/`). Com `IA_URL` preenchido, as perguntas
  livres vão para a IA; sem ele, ou se a IA falhar, responde sozinho por palavras-chave.
- `ia/` — Worker do Cloudflare que conversa com o Llama (cota grátis). Ver `ia/LEIA-ME.md`.
