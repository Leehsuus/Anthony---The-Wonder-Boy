import zlib
import os


def comprimir_imagem(nome_imagem):
    img_original = open(nome_imagem, 'rb').read()
    compressao = zlib.compress(img_original, zlib.Z_BEST_COMPRESSION)
    porcentagem_arquivo_comprimido = (100 * len(compressao)) / len(img_original)
    tx_compressao = 100 - porcentagem_arquivo_comprimido

    print("A imagem original tem {} bytes, a imagem comprimida tem {} bytes, "
          "a compressão resulta em uma imagem {:.2f}% menor "
          .format(len(img_original), len(compressao), float(tx_compressao)))

    return compressao


def descomprimir_imagem(imagem_comprimida):
    teste_descompressao = open(imagem_comprimida, 'rb').read()
    descompressao = zlib.decompress(teste_descompressao)

    print("A imagem {} foi descomprimida".format(imagem_comprimida))
    return descompressao


def chamar_descompressao_imagens():
    creditos_descomprimido = descomprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/'
                                                 'imagens_compressao/creditos_comprimido.png')
    gameover_descomprimido = descomprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/'
                                                 'imagens_compressao/gameover_comprimido.png')
    inicio_descomprimido = descomprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/'
                                               'imagens_compressao/inicio_comprimido.png')
    selecao_1_descomprimido = descomprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/'
                                                  'imagens_compressao/selecao_1_comprimido.png')
    selecao_2_descomprimido = descomprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/'
                                                  'imagens_compressao/selecao_2_comprimido.png')
    stan_lee_descomprimido = descomprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/'
                                                 'imagens_compressao/stan_lee_comprimido.png')

    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/creditos.png', 'wb'). \
        write(creditos_descomprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/gameover.png', 'wb'). \
        write(gameover_descomprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/inicio.png', 'wb'). \
        write(inicio_descomprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/selecao_1.png', 'wb'). \
        write(selecao_1_descomprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/selecao_2.png', 'wb'). \
        write(selecao_2_descomprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/stan_lee_tributo.png', 'wb'). \
        write(stan_lee_descomprimido)

    pasta = '/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao'
    procura_imagem = os.listdir(pasta)

    for img in procura_imagem:
        if img == 'creditos_comprimido.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'gameover_comprimido.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'inicio_comprimido.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'selecao_1_comprimido.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'selecao_2_comprimido.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'stan_lee_comprimido.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))


def chamar_compressao_imagem():
    creditos_comprimido = \
        comprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/creditos.png')
    gameover_comprimido = \
        comprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/gameover.png')
    inicio_comprimido = \
        comprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/inicio.png')
    selecao_1_comprimido = \
        comprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/selecao_1.png')
    selecao_2_comprimido = \
        comprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/selecao_2.png')
    stan_lee_comprimido = \
        comprimir_imagem('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/stan_lee_tributo.png')

    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/creditos_comprimido.png', 'wb') \
        .write(creditos_comprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/gameover_comprimido.png', 'wb') \
        .write(gameover_comprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/inicio_comprimido.png', 'wb') \
        .write(inicio_comprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/selecao_1_comprimido.png', 'wb') \
        .write(selecao_1_comprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/selecao_2_comprimido.png', 'wb') \
        .write(selecao_2_comprimido)
    open('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/stan_lee_comprimido.png', 'wb') \
        .write(stan_lee_comprimido)

    pasta = '/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao'
    procura_imagem = os.listdir(pasta)

    for img in procura_imagem:
        if img == 'creditos.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'gameover.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'inicio.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'selecao_1.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'selecao_2.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
        elif img == 'stan_lee_tributo.png':
            os.remove('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/{}'.format(img))
