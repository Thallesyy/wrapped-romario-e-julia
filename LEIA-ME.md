# O nosso wrapped: Julia & Romário

O "Wrapped" do primeiro ano de namoro do Romário e da Julia, igual ao do Spotify: telas em
pé que passam sozinhas, com números grandes e fotos. É o Romário falando com a Julia.

Os números saíram da conversa deles no WhatsApp. As datas foram confirmadas pelo Romário e
pela conversa:

- **17/09/2025, 12h23:** a primeira mensagem, dela: "Qual o nome da loja do pastel??".
- **08/10/2025:** o primeiro beijo.
- **12/10/2025, 22h48:** o "quer ser?" por mensagem. Nessa noite veio o primeiro "te amo"
  (23h31), e é o dia recorde de mensagens.
- **29/11/2025:** o pedido de namoro, uma surpresa no campestre. **Os dias de namoro e os
  mesversários contam daqui.**

## As telas, em ordem

1. **Abertura:** "o nosso wrapped · 1 ano" e o botão começar.
2. **O começo:** 17/09 e quantos dias se passaram (conta sozinho pela data do aparelho).
3. **A primeira mensagem:** os balões do pastel.
4. **O primeiro beijo.**
5. **O pedido (29/11), no campestre:** a foto do buquê, os dias de namoro e quanto falta pro
   próximo mesversário. No dia 29/11/2026 aparece "hoje faz 1 ano!".
6. **WhatsApp:**
   - as mensagens, com um gráfico por mês;
   - quem manda mais;
   - os "te amo" e o primeiro deles;
   - o emoji do ano;
   - a hora em que eles mais conversam;
   - o dia recorde (que é o dia do "quer ser?");
   - as horas de ligação, com a maior delas.
7. **Top momentos:** os 5 que o Romário escolheu. Ele mandou do 5 pro 1, igual às músicas, então o nº 1
   é o 28/09, "o dia em que eu te olhei".
8. **Um vídeo deles,** em tela cheia.
9. **O mosaico de fotos,** com as fotos e vídeos que eles trocaram.
10. **Top músicas,** com fotos deles de capa. A tela da artista só aparece se preencher
    `ARTISTA` (nenhum artista se repete nas 5).
11. **Os 10 motivos dele,** um de cada vez.
12. **A personalidade do casal.**
13. **O resumo,** que dá pra salvar como imagem.
14. **O final.**

Ela toca na direita pra passar, na esquerda pra voltar, e segura pra pausar.

## As músicas

Cada parte toca uma das 5 músicas deles. As músicas foram cortadas no trecho mais forte, pra
não pesar no celular:

- o começo, a primeira mensagem e o beijo: **Foi Assim**;
- o pedido: **Lei da Física**;
- as telas do WhatsApp: **Te Amo Disgraça**;
- os momentos, o vídeo e as fotos: **Legendary Lovers**;
- do top músicas até o final: **Best Part**, que é a nº 1.

A música de cada tela é o `musica:` dela. Pra cortar outra música:

    python ferramentas/cortar-musica.py entrada.mp3 musicas/nome.mp3 <início em s> <fim em s>

No iPhone o som só começa depois do toque em "começar". O botão no canto de cima liga e desliga.

## O que ainda falta

- **Os textos que não são frases dele:** são rascunho.
- **Teste no iPhone.**

## Trocar coisas

Tudo fica no começo do `<script>` do `index.html`:

- `COMECO`, `BEIJO`, `QUER_SER` e `PEDIDO`: as datas.
- `TEXTOS`: todos os textos, incluindo os balões da primeira mensagem.
- `MOMENTOS`: os top momentos. O primeiro da lista é o número 1.
- `MUSICAS`, `ARTISTA` e `COM_MUSICA`: as músicas (as capas são fotos deles, em `preparar-fotos.py`).
- `MOTIVOS`: os 10 motivos dele.

As fotos ficam em `ferramentas/preparar-fotos.py`. Ele lê as 26 fotos da pasta `fotos/`
do site do céu (`o-ceu-amigos`). Depois de trocar, rode:

    python ferramentas/preparar-fotos.py

## Os números do WhatsApp

A conversa exportada fica **fora desta pasta** e nunca vai pro GitHub. Rode:

    python ferramentas/contar-whatsapp.py "caminho/da/conversa.zip" --ele "Romário"

Ele grava o `dados-whatsapp.js`, que tem **só números** (quantidades, horas, datas, emojis)
e nenhuma mensagem. As poucas frases da conversa que aparecem no site estão escritas à mão
no `TEXTOS`, com a autorização deles.

## Como abrir

Pelo link do GitHub Pages, no Safari. No computador, rode `python -m http.server` na pasta e
abra o endereço que ele mostrar.

## Para testar

- `index.html?teste=1&historia=pedido`: abre parado no fim dessa tela (pra print).
- `&t=3`: parado no segundo 3 da tela.
- `&hoje=2026-10-12`: finge que hoje é outro dia.
- `&semwhats=1`: como fica sem as telas do WhatsApp.

No modo `teste=1` nada anda sozinho. Pra ver normal, abra sem ele.
