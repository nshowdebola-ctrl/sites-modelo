# IA do assistente (Llama no Cloudflare)

Este Worker faz o chat dos sites modelo responder com uma IA de verdade (Llama 3.3, da Meta),
usando a cota **grátis** do Cloudflare Workers AI (10 mil "neurons" por dia, cerca de 100
respostas). Quando a cota do dia acaba, o Cloudflare só recusa novos pedidos (não cobra nada
no plano grátis) e o site passa a responder com o assistente local até a meia-noite (UTC).

Não guarda conversas. A chave da IA fica no próprio Cloudflare, nunca no site.

## Publicar (uma vez só)

1. Crie uma conta grátis em https://dash.cloudflare.com/sign-up (e-mail e senha).
   Não precisa colocar cartão e **não** mude para o plano pago.
2. Abra o terminal e cole, uma linha por vez:

   ```bash
   export NVM_DIR="$HOME/.config/nvm" && . "$NVM_DIR/nvm.sh"
   cd ~/projetos/sites-modelo/ia
   npx wrangler login
   ```

   O navegador abre: entre na conta do Cloudflare e clique em **Allow** (permitir).
3. Ainda no terminal:

   ```bash
   npx wrangler deploy
   ```

   Se ele pedir um nome de subdomínio "workers.dev", escreva um nome simples (por exemplo,
   `lorrane-sites`). No fim aparece um endereço parecido com
   `https://assistente-sites-modelo.lorrane-sites.workers.dev`.
4. Coloque esse endereço em `IA_URL` no `gerar.py` e rode `python3 gerar.py`.

## Mudar alguma coisa

- **Informações do salão:** edite o `gerar.py`, rode `python3 gerar.py` e depois `npx wrangler deploy`
  de novo (a IA lê os dados de `src/dados/`).
- **Modelo da IA:** `MODELO` em `src/index.js`. O `llama-3.2-3b-instruct` responde umas 700
  vezes por dia na cota grátis, mas escreve pior em português.
- **Ver erros ao vivo:** `npx wrangler tail`.
