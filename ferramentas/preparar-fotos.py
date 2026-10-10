"""Copia e diminui as fotos do Wrapped pra pasta fotos/.

As fotos originais são as 26 que o Romario mandou, já com nomes simples (foto01 a foto26)
na pasta fotos/ do site do céu (o-ceu-amigos). Pra trocar uma foto, mude o nome nas
listas abaixo e rode de novo:

    python ferramentas/preparar-fotos.py
"""
import os
from PIL import Image, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
ORIGEM = os.path.join(SITE, '..', 'o-ceu-amigos', 'fotos')
DESTINO = os.path.join(SITE, 'fotos')

# fotos grandes: nome no site -> foto original
GRANDES = {
    'pedido': 'foto01',         # os dois de rosto colado, os rostos ficam no alto
    'mensagens': 'foto09',      # espelho com o celular
    'personalidade': 'foto15',  # caretas de mão dada
    'resumo': 'foto06',         # beijo no rosto, de noite
    'final': 'foto21',
}

# o mosaico da tela "fotos" (18)
MOSAICO = [
    'foto02', 'foto03', 'foto04', 'foto05', 'foto07', 'foto11', 'foto12', 'foto13', 'foto14',
    'foto16', 'foto18', 'foto19', 'foto20', 'foto22', 'foto23', 'foto24', 'foto25', 'foto26',
]


def abrir(nome):
    im = Image.open(os.path.join(ORIGEM, nome + '.jpg'))
    return ImageOps.exif_transpose(im).convert('RGB')


def salvar(im, nome, qualidade=82):
    caminho = os.path.join(DESTINO, nome + '.jpg')
    im.save(caminho, 'JPEG', quality=qualidade, optimize=True, progressive=True)
    return os.path.getsize(caminho)


def main():
    os.makedirs(DESTINO, exist_ok=True)
    total = 0
    for nome, original in GRANDES.items():
        im = abrir(original)
        im.thumbnail((1100, 1100), Image.LANCZOS)
        total += salvar(im, nome)
    for i, original in enumerate(MOSAICO):
        im = ImageOps.fit(abrir(original), (420, 560), Image.LANCZOS, centering=(0.5, 0.35))
        total += salvar(im, 'mosaico%d' % (i + 1), 78)
    print('%d fotos, %.1f MB' % (len(GRANDES) + len(MOSAICO), total / 1e6))


if __name__ == '__main__':
    main()
