"""Corta um trecho de um MP3 sem recodificar (quadro a quadro), pro site não ficar pesado.

    python ferramentas/cortar-musica.py <entrada.mp3> <saida.mp3> <início em s> <fim em s>

Os trechos usados no site (escolhidos pela parte mais forte de cada música):
    foi-assim         24 -> 86
    lei-da-fisica     41 -> 96
    te-amo-disgraca   19 -> 99
    legendary-lovers  34.4 -> 126 (começa no refrão)
"""
import sys

BITRATES = {
    1: [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],   # MPEG-1 layer III
    2: [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],       # MPEG-2/2.5 layer III
}
TAXAS = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000]}


def quadro(d, i):
    """devolve (tamanho, duração) do quadro que começa em i, ou None se não for um quadro"""
    if i + 4 > len(d) or d[i] != 0xFF or (d[i + 1] & 0xE0) != 0xE0:
        return None
    versao = (d[i + 1] >> 3) & 3
    camada = (d[i + 1] >> 1) & 3
    br_i = d[i + 2] >> 4
    sr_i = (d[i + 2] >> 2) & 3
    if versao == 1 or camada != 1 or br_i in (0, 15) or sr_i == 3:
        return None
    br = BITRATES[1 if versao == 3 else 2][br_i] * 1000
    sr = TAXAS[versao][sr_i]
    pad = (d[i + 2] >> 1) & 1
    if versao == 3:
        return 144 * br // sr + pad, 1152 / sr
    return 72 * br // sr + pad, 576 / sr


def main():
    entrada, saida, ini, fim = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    d = open(entrada, 'rb').read()
    i = 0
    if d[:3] == b'ID3':
        i = 10 + ((d[6] << 21) | (d[7] << 14) | (d[8] << 7) | d[9])
    # acha o primeiro quadro de verdade (dois quadros seguidos)
    while i < len(d):
        q = quadro(d, i)
        if q and quadro(d, i + q[0]):
            break
        i += 1
    t = 0.0
    partes = []
    while i < len(d):
        q = quadro(d, i)
        if not q:
            break
        if ini <= t < fim:
            partes.append(d[i:i + q[0]])
        t += q[1]
        i += q[0]
        if t >= fim:
            break
    open(saida, 'wb').write(b''.join(partes))
    print('%s: %.0fs -> %.0fs, %.1f MB' % (saida, ini, min(t, fim), sum(map(len, partes)) / 1e6))


if __name__ == '__main__':
    main()
