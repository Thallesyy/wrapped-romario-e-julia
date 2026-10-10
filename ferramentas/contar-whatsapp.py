"""Conta os números da conversa do WhatsApp pro Wrapped.

Lê a conversa exportada (o .zip ou o .txt) e grava só os números em dados-whatsapp.js.
Nenhuma mensagem vai pro site, e esse script nunca imprime o texto das mensagens.

    python ferramentas/contar-whatsapp.py "C:/Users/thale/Downloads/WhatsApp Chat - Amor Da Minha Vida ❤️_🔥.zip" --ele "Romário"

--ele é o nome dele como aparece na conversa (quem exportou). A outra pessoa é ela.
"""
import collections, datetime, glob, io, json, os, re, sys, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), 'dados-whatsapp.js')

# [10/10/2026, 15:48:12] Nome: texto   (iPhone)
# 10/10/2026 15:48 - Nome: texto       (Android)
CABECALHO = re.compile(
    r'^\u200e?\[?(\d{1,2})/(\d{1,2})/(\d{2,4}),?\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*([AaPp]\.?\s?[Mm]\.?)?\]?\s*(?:-\s*)?'
    r'([^:]+?):\s(.*)$')
INVISIVEIS = re.compile('[\u200e\u200f\u202a-\u202e\u2066-\u2069]')

MIDIA = [
    ('audios', re.compile(r'(áudio|audio)\s+(ocultad|omitid)', re.I)),
    ('fotos', re.compile(r'(imagem|foto)\s+(ocultad|omitid)', re.I)),
    ('videos', re.compile(r'vídeo\s+(ocultad|omitid)', re.I)),
    ('figurinhas', re.compile(r'figurinha\s+(ocultad|omitid)', re.I)),
    ('gifs', re.compile(r'gif\s+(ocultad|omitid)', re.I)),
    ('midia', re.compile(r'<m[ií]dia oculta>|arquivo de m[ií]dia oculto', re.I)),
]
APAGADA = re.compile(r'(mensagem (foi )?apagada|apagou esta mensagem)', re.I)
SISTEMA = re.compile(r'(criptografia de ponta|end-to-end|mudou o código de segurança|'
                     r'chamada de (voz|vídeo) perdida|ligação de (voz|vídeo) perdida|'
                     r'liga[cç][aã]o em grupo|missed (voice|video) call)', re.I)
LIGACAO = re.compile(r'^\s*(liga[cç][aã]o|chamada) de (voz|v[ií]deo)', re.I)
DURACAO = re.compile(r'(\d+)\s*(segundo|minuto|hora)', re.I)
TE_AMO = re.compile(r'\bt[ei]\s*amo+\b|\bte\s+amu+\b|\bamo\s+(vc|voce|você|tu)\b', re.I)
SAUDADE = re.compile(r'saudade|\bsdds?\b', re.I)
BOM_DIA = re.compile(r'^\W*bom\s+dia', re.I)
BOA_NOITE = re.compile(r'^\W*boa\s+noite', re.I)
EMOJI = re.compile(
    '(?:[\U0001F1E6-\U0001F1FF]{2})|'
    '(?:[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B55\u2763\u2764\u23F0-\u23FA]'
    '[\uFE0F\U0001F3FB-\U0001F3FF]*'
    '(?:\u200D[\U0001F300-\U0001FAFF\u2600-\u27BF\u2640\u2642\u2764][\uFE0F\U0001F3FB-\U0001F3FF]*)*)')


def ler_conversa(caminho):
    """Junta o texto de todos os .txt da pasta, ou de dentro dos .zip."""
    if os.path.isdir(caminho):
        arquivos = sorted(glob.glob(os.path.join(caminho, '*.zip')) + glob.glob(os.path.join(caminho, '*.txt')))
    else:
        arquivos = [caminho]
    textos = []
    for arq in arquivos:
        if arq.lower().endswith('.zip'):
            with zipfile.ZipFile(arq) as z:
                for nome in z.namelist():
                    if nome.lower().endswith('.txt'):
                        textos.append((arq + ':' + nome, z.read(nome).decode('utf-8-sig', 'replace')))
        else:
            with io.open(arq, encoding='utf-8-sig', errors='replace') as f:
                textos.append((arq, f.read()))
    if not textos:
        raise SystemExit('não achei nenhum .txt nem .zip em ' + caminho)
    return textos


def mensagens(texto):
    atual = None
    for linha in texto.splitlines():
        m = CABECALHO.match(linha)
        if m:
            if atual:
                yield atual
            d, mes, a, h, mi, s, ampm, quem, corpo = m.groups()
            a = int(a)
            if a < 100:
                a += 2000
            h = int(h)
            if ampm and ampm.lower().startswith('p') and h < 12:
                h += 12
            if ampm and ampm.lower().startswith('a') and h == 12:
                h = 0
            try:
                quando = datetime.datetime(a, int(mes), int(d), h, int(mi), int(s or 0))
            except ValueError:
                atual = None
                continue
            atual = [quando, INVISIVEIS.sub('', quem).strip(), INVISIVEIS.sub('', corpo)]
        elif atual:
            atual[2] += '\n' + INVISIVEIS.sub('', linha)
    if atual:
        yield atual


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    args = sys.argv[1:]
    ele = None
    if '--ele' in args:
        i = args.index('--ele')
        ele = args[i + 1]
        del args[i:i + 2]
    if not args or not ele:
        raise SystemExit(__doc__)

    # se tiver mais de uma exportação, cada mensagem entra o máximo de vezes que
    # aparece num arquivo só (assim duas figurinhas iguais no mesmo segundo continuam duas)
    juntas = collections.Counter()
    cortada = False
    for origem, texto in ler_conversa(args[0]):
        lidas = [tuple(m) for m in mensagens(texto)]
        print('%s: %d mensagens' % (os.path.basename(origem), len(lidas)))
        # o Android exporta só as últimas 40 mil (ou 10 mil com mídia)
        cortada = cortada or len(lidas) in (10000, 40000)
        juntas |= collections.Counter(lidas)
    unicas = sorted(juntas.elements(), key=lambda x: x[0])
    unicas = [m for m in unicas if not SISTEMA.search(m[2])]

    nomes = collections.Counter(quem for _, quem, _ in unicas)
    print('quem aparece:', ', '.join('%s (%d)' % kv for kv in nomes.most_common()))
    pessoas = [n for n, _ in nomes.most_common(2)]
    if len(pessoas) < 2:
        raise SystemExit('a conversa tem menos de duas pessoas')
    if ele not in pessoas:
        raise SystemExit('"%s" não está entre as duas pessoas da conversa' % ele)
    ela = [n for n in pessoas if n != ele][0]
    quem_e = {ela: 'ela', ele: 'ele'}
    print('ela:', ela, '| ele:', ele)

    unicas = [m for m in unicas if m[1] in quem_e]
    por = collections.Counter()
    te_amo = collections.Counter()
    bom_dia = collections.Counter()
    boa_noite = collections.Counter()
    midia = collections.Counter()
    horas = [0] * 24
    dias = collections.Counter()
    meses = collections.Counter()
    emojis = collections.Counter()
    forma_emoji = {}
    primeiro_do_dia = {}
    saudade = palavras = apagadas = 0
    ligacoes = nao_atendidas = segundos_ligacao = 0
    maior_ligacao = (0, None, None)
    primeiro_te_amo = None
    recorde_te_amo = (0, None, None)
    maior = (0, None)

    for quando, nome, corpo in unicas:
        p = quem_e[nome]
        if LIGACAO.search(corpo):
            tempo = sum(int(n) * {'s': 1, 'm': 60, 'h': 3600}[u[0].lower()] for n, u in DURACAO.findall(corpo))
            if tempo:
                ligacoes += 1
                segundos_ligacao += tempo
                if tempo > maior_ligacao[0]:
                    maior_ligacao = (tempo, quando, 'vídeo' if re.search(r'v[ií]deo', corpo, re.I) else 'voz')
            else:
                nao_atendidas += 1
            continue
        por[p] += 1
        horas[quando.hour] += 1
        dias[quando.date()] += 1
        meses[quando.strftime('%Y-%m')] += 1
        # o "dia" começa às 5h, pra conversa de madrugada contar no dia anterior
        dia_logico = (quando - datetime.timedelta(hours=5)).date()
        if dia_logico not in primeiro_do_dia:
            primeiro_do_dia[dia_logico] = p
        if APAGADA.search(corpo):
            apagadas += 1
            continue
        tipo = next((t for t, r in MIDIA if r.search(corpo)), None)
        if tipo:
            midia[tipo] += 1
            continue
        quantos = len(TE_AMO.findall(corpo))
        if quantos:
            te_amo[p] += 1   # uma vez por mensagem (senão um 'te amo te amo te amo...' gigante ganha tudo)
            if primeiro_te_amo is None:
                primeiro_te_amo = (quando, p)
            if quantos > recorde_te_amo[0]:
                recorde_te_amo = (quantos, p, quando.date().isoformat())
        saudade += len(SAUDADE.findall(corpo))
        if BOM_DIA.search(corpo):
            bom_dia[p] += 1
        if BOA_NOITE.search(corpo):
            boa_noite[p] += 1
        n = len(re.findall(r'\w+', corpo))
        palavras += n
        if n > maior[0]:
            maior = (n, p)
        for e in EMOJI.findall(corpo):
            chave = e.replace('\uFE0F', '')
            emojis[chave] += 1
            forma_emoji.setdefault(chave, collections.Counter())[e] += 1

    if not unicas:
        raise SystemExit('nenhuma mensagem das duas pessoas')
    inicio, fim = unicas[0][0].date(), unicas[-1][0].date()
    total_dias = (fim - inicio).days + 1
    seq = melhor_seq = 0
    anterior = None
    for d in sorted(dias):
        seq = seq + 1 if anterior and (d - anterior).days == 1 else 1
        melhor_seq = max(melhor_seq, seq)
        anterior = d
    recorde = max(dias.items(), key=lambda kv: kv[1])
    puxa = collections.Counter(primeiro_do_dia.values())
    primeira = unicas[0]

    dados = {
        'desde': inicio.isoformat(),
        'ate': fim.isoformat(),
        'completa': not cortada,
        'total': por['ela'] + por['ele'],
        'pessoas': {'ela': por['ela'], 'ele': por['ele']},
        'teAmo': {'ela': te_amo['ela'], 'ele': te_amo['ele']},
        'primeiroTeAmo': {'data': primeiro_te_amo[0].strftime('%Y-%m-%d'), 'hora': primeiro_te_amo[0].strftime('%H:%M'),
                          'quem': primeiro_te_amo[1]} if primeiro_te_amo else None,
        'teAmoRecorde': {'vezes': recorde_te_amo[0], 'quem': recorde_te_amo[1], 'data': recorde_te_amo[2]},
        'ligacoes': ligacoes,
        'ligacoesNaoAtendidas': nao_atendidas,
        'minutosLigacao': round(segundos_ligacao / 60),
        'maiorLigacao': {'minutos': round(maior_ligacao[0] / 60), 'data': maior_ligacao[1].strftime('%Y-%m-%d'),
                         'hora': maior_ligacao[1].strftime('%H:%M'), 'tipo': maior_ligacao[2]} if maior_ligacao[1] else None,
        'saudade': saudade,
        'bomDia': bom_dia['ela'] + bom_dia['ele'],
        'boaNoite': boa_noite['ela'] + boa_noite['ele'],
        'puxaAssunto': {'ela': puxa['ela'], 'ele': puxa['ele']},
        'palavras': palavras,
        'maiorMensagem': {'palavras': maior[0], 'quem': maior[1]},
        'apagadas': apagadas,
        'audios': midia['audios'],
        'fotos': midia['fotos'] + midia['videos'],
        'figurinhas': midia['figurinhas'] + midia['gifs'],
        'midiaSemTipo': midia['midia'],
        'emojis': [[forma_emoji[k].most_common(1)[0][0], c] for k, c in emojis.most_common(5)],
        'horas': horas,
        'meses': [[m, meses[m]] for m in sorted(meses)],
        'diaRecorde': {'data': recorde[0].isoformat(), 'total': recorde[1]},
        'diasFalando': len(dias),
        'diasTotal': total_dias,
        'maiorSequencia': melhor_seq,
        'primeira': {'data': primeira[0].strftime('%Y-%m-%d'), 'hora': primeira[0].strftime('%H:%M'),
                     'quem': quem_e[primeira[1]]},
    }
    with io.open(SAIDA, 'w', encoding='utf-8', newline='\n') as f:
        f.write('/* gerado por ferramentas/contar-whatsapp.py: só números, nenhuma mensagem */\n')
        f.write('window.WHATS = ' + json.dumps(dados, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(json.dumps(dados, ensure_ascii=False))
    print('gravado em', SAIDA)


if __name__ == '__main__':
    main()
