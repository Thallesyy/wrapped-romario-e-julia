# O nosso wrapped: Julia & Romário

O "Wrapped" do primeiro ano de namoro do Romário e da Julia, igual ao do Spotify: telas em
pé que passam sozinhas, com números grandes e fotos. É o Romário falando com a Julia.

Os números saíram da conversa deles no WhatsApp. As datas foram confirmadas pelo Romário e
pela conversa:

- **17/09/2025, 12h23:** a primeira mensagem, dela: "Qual o nome da loja do pastel??".
- **08/10/2025:** o primeiro beijo.
- **12/10/2025, 22h48:** o "quer ser?" por mensagem ("Quer ser?" / "Vc é minha namorada?" /
  "Então eu sou"). É daqui que eles contam os mesversários (todo dia 12) e o 1 ano.
- **12/10/2025, 23h31:** o primeiro "te amo", na mesma noite.
- **29/11/2025:** o pedido de namoro oficial (com aliança).

## As telas, em ordem

1. **Abertura:** "o nosso wrapped · 1 ano" e o botão começar.
2. **O começo:** 17/09 e quantos dias se passaram (conta sozinho pela data do aparelho).
3. **A primeira mensagem:** os balões do pastel.
4. **O primeiro beijo.**
5. **"A gente namora" (12/10):** a conversa em balões, os dias de namoro e quanto falta pro
   1 ano. No dia 12/10 aparece "hoje faz 1 ano!".
6. **O pedido (29/11),** com a foto do buquê.
7. **WhatsApp:**
   - as mensagens, com um gráfico por mês;
   - quem manda mais;
   - os "te amo" e o primeiro deles;
   - o emoji do ano;
   - a hora em que eles mais conversam;
   - o dia recorde (que é o dia do "quer ser?");
   - as horas de ligação, com a maior delas.
8. **Top momentos.**
9. **A artista e as top músicas:** só aparecem quando preencher `MUSICAS` e `ARTISTA`.
10. **Um vídeo deles,** em tela cheia.
11. **O mosaico de fotos,** com as fotos e vídeos que eles trocaram.
12. **Os motivos.**
13. **A personalidade do casal.**
14. **O resumo,** que dá pra salvar como imagem.
15. **O final.**

Ela toca na direita pra passar, na esquerda pra voltar, e segura pra pausar.

## O que ainda falta

- **As músicas:** o nome, o artista e os arquivos.
  1. Coloque os .mp3 em `musicas/`.
  2. Preencha `MUSICAS` (e `ARTISTA`, se tiver uma artista que aparece muito).
  3. Ponha `COM_MUSICA = true`.
  4. Troque o `musica:` de cada tela pelo nome do arquivo (sem o .mp3).

  Sem isso o site funciona mudo, e o botão de som não aparece.
- **Os textos:** os motivos e os textos que não são frases dele são rascunho.
- **Teste no iPhone.**

## Trocar coisas

Tudo fica no começo do `<script>` do `index.html`:

- `COMECO`, `BEIJO`, `NAMORO` e `PEDIDO`: as datas.
- `TEXTOS`: todos os textos, incluindo os balões da primeira mensagem e do pedido.
- `MOMENTOS`: os top momentos. O primeiro da lista é o número 1.
- `MUSICAS`, `ARTISTA` e `COM_MUSICA`: as músicas.
- `MOTIVOS`: os motivos.

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
