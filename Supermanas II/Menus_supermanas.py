import pygame as pg
from Compressao_imagens import *


def mostrar_menu_inicial(indice_menu_func, pos_y_func, estado, mult = 1):
    if estado == 0:
        if mult == 1:
            indice_menu_func += 1
            pos_y_func += 80
            if indice_menu_func > qnt_opcoes:
                indice_menu_func = qnt_opcoes
                pos_y_func = pos_y_limite
        elif mult == -1:
            indice_menu_func -= 1
            pos_y_func -= 80
            if indice_menu_func < 0:
                indice_menu_func = 0
                pos_y_func = pos_y_inicial

    elif estado == 5:
        if mult == 1:
            indice_menu_func += 1
            pos_y_func += 200
            if indice_menu_func > qnt_fases:
                indice_menu_func = qnt_fases
                pos_y_func = pos_x_limite
        elif mult == -1:
            indice_menu_func -= 1
            pos_y_func -= 200
            if indice_menu_func < 0:
                indice_menu_func = 0
                pos_y_func = pos_x_inicial

    return pos_y_func, indice_menu_func


chamar_descompressao_imagens()
pg.init()

bg_menu_inicial = pg.image.load('imagens_compressao/inicio.png')
seta = pg.image.load('Imagens/seta.png')
seta_dois = pg.image.load('Imagens/seta_2.png')
pos_x, pos_y = 150, 240
pos_x_seta_2, pos_y_seta_2 = 100, 130
pos_x_inicial, pos_x_limite = 100, 500
pos_y_inicial, pos_y_limite = 240, 400
qnt_fases= (pos_x_limite - pos_x_inicial)/200
qnt_opcoes = (pos_y_limite - pos_y_inicial)/80
indice_fases = 0
indice_menu = 0
estado = 0

# opcções de estado
# 0 - Menu inicial
# 1 - Jogando
# 2 - Como Jogar
# 3 - Créditos
# 4 - Pausado
# 5 - seleção de fases
# 6 - Game Over
# 7 - Tributo Stan Lee


