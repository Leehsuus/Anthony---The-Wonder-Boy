import os
from threading import Timer

import pygame as pg
import random as r
import time
from Constantes import *
from Menus_supermanas import *
from Compressao_imagens import *
from Compressao_dict import *


class Personagem(pg.sprite.Sprite):
    def __init__(self, color=darkgreen, largura=52, altura=65):
        super(Personagem, self).__init__()
        self.image = pg.Surface((largura, altura))
        self.image.fill(color)
        self.set_propriedades()
        self.hspeed = 0
        self.vspeed = 0
        self.largura_personagem = largura
        self.altura_personagem = altura
        self.personagem_pos_x_variavel = self.largura_personagem / 3
        self.personagem_pos_y = 400
        self.vida = 5
        self.sangue = 15
        self.especial = 0
        self.divisor_fase = 2
        self.sprite_andando = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                            'personagem_andando.png')
        self.anthony = [0, 1, 2, 3, 4]
        self.frame = 0
        self.estado = "parado"

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_position_variavel(self):
        self.personagem_pos_x_variavel += personagem.hspeed
        self.personagem_pos_y += personagem.vspeed

    def set_propriedades(self):
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self, colidiveis=pg.sprite.Group(), event=None):

        self.experience_gravity()
        self.personagem_pos_x_variavel += self.hspeed
        self.rect.x += self.hspeed
        collision_list = pg.sprite.spritecollide(self, colidiveis, False)
        for collided_object in collision_list:
            if self.hspeed > 0:
                # RIGHT DIRECTION
                self.rect.right = collided_object.rect.left
                self.hspeed = 0
                self.vspeed = 0
                self.image = personagem_parado_LD
                self.estado = None
            elif self.hspeed < 0:
                # LEFT DIRECTION
                self.rect.left = collided_object.rect.right
                self.hspeed = 0
                self.vspeed = 0
                self.image = personagem_parado_LE
                self.estado = None

        self.personagem_pos_y += self.vspeed
        self.rect.y += self.vspeed
        collision_list = pg.sprite.spritecollide(self, colidiveis, False)
        for collided_object in collision_list:
            if self.vspeed > 0:
                # DOWN DIRECTION
                self.rect.bottom = collided_object.rect.top
                self.vspeed = 0
            elif self.vspeed < 0:
                # UP DIRECTION
                self.rect.top = collided_object.rect.bottom
                self.vspeed = 0

        if event is not None:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    self.estado = "andando dir"
                    self.hspeed = self.speed
                if event.key == pg.K_LEFT:
                    self.estado = "andando esq"
                    self.hspeed = -self.speed
                if event.key == pg.K_UP:
                    if len(collision_list) >= 1:
                        self.vspeed = (-self.speed) * 1.6
                if event.key == pg.K_e and self.especial == 8:
                    if self.image == personagem_parado_LD or self.estado == "andando dir":
                        som_tiro_especial_anthony.play()
                        self.especial = self.especial - 8
                        tiro = Tiro(largura=51, altura=12)
                        if personagem.rect.x == personagem.personagem_pos_x_variavel:
                            tiro.set_position(personagem.personagem_pos_x_variavel, personagem.rect.centery)
                            lista_tiros_especial.append(tiro)
                        else:
                            tiro.set_position(personagem.rect.x, personagem.rect.centery)
                            lista_tiros_especial.append(tiro)
                        for t in lista_tiros_especial:
                            t.image = tiro_especial_personagem_imagem
                            objetos_ativos.add(t)
                    else:
                        som_tiro_especial_anthony.play()
                        self.especial = self.especial - 8
                        tiro = Tiro(largura=51, altura=12, mult=-1)
                        if personagem.rect.x == personagem.personagem_pos_x_variavel:
                            tiro.set_position(personagem.personagem_pos_x_variavel, personagem.rect.centery)
                            lista_tiros_especial.append(tiro)
                        else:
                            tiro.set_position(personagem.rect.x, personagem.rect.centery)
                            lista_tiros_especial.append(tiro)
                        for t in lista_tiros_especial:
                            t.image = tiro_especial_personagem_imagem
                            objetos_ativos.add(t)

                if self.rect.colliderect(box_aleatoria.rect) and event.key == pg.K_b:
                    sorteio_box_aleatoria = r.randint(1, 3)
                    # som_abrir_caixa.play()

                    if self.divisor_fase != 1:
                        self.divisor_fase = self.divisor_fase - 1
                        box_aleatoria.resultado_pos_x_box = int(fase_largura / self.divisor_fase)
                    else:
                        self.divisor_fase = 1
                        box_aleatoria.resultado_pos_x_box = int(fase_largura / self.divisor_fase)

                    if sorteio_box_aleatoria == 1 and self.vida < 5:
                        box_aleatoria.set_image("vida.png")
                        self.vida = self.vida + 1

                        i = Timer(2.0, box_aleatoria.set_new_box_position)
                        i.start()

                    elif sorteio_box_aleatoria == 2:
                        box_aleatoria.set_image("especial.png")
                        if self.especial <= 5:
                            self.especial = self.especial + 3
                        else:
                            self.especial = 8

                        # Definir nova posição da box
                        i = Timer(2.0, box_aleatoria.set_new_box_position)
                        i.start()

                    else:
                        box_aleatoria.set_image("onus.png")
                        self.especial = int(self.especial / 2)

                        # Definir nova posição da box
                        i = Timer(2.0, box_aleatoria.set_new_box_position)
                        i.start()

            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    if self.hspeed > 0:
                        self.hspeed = 0
                        self.estado = "parado"
                        self.image = personagem_parado_LD
                if event.key == pg.K_LEFT:
                    if self.hspeed < 0:
                        self.hspeed = 0
                        self.estado = "parado"
                        self.image = personagem_parado_LE
                if personagem.rect.y >= 470:
                    personagem.set_position(0, 0)
                    personagem.vspeed = 0
                    personagem.hspeed = 0

    def experience_gravity(self, gravity=.35):
        if self.vspeed == 0:
            self.vspeed = 1
        else:
            self.vspeed += gravity

    def update_frame(self, estado):
        gId = self.anthony[self.frame]
        sprite_andando = get_frame(self.sprite_andando, gId, 5, 53, 64, space_h=0)
        self.frame += 1
        if estado == "andando dir":
            self.image = sprite_andando

        if self.frame > len(self.anthony) - 1:
            self.frame = 0
        if estado == "andando esq":
            return sprite_andando


class Blocos(pg.sprite.Sprite):
    def __init__(self, x, y, largura, altura, color=blue):
        super(Blocos, self).__init__()
        self.image = pg.Surface((largura, altura))
        self.image.fill(color)
        self.largura = largura
        self.altura = altura
        self.color = color
        self.resultado_pos_x_box = 0
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename=None):
        if filename is not None:
            self.image = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/{}'
                                       .format(filename)).convert_alpha()

    def set_new_box_position(self):
        box_aleatoria.rect.x = box_aleatoria.rect.x + 400
        if box_aleatoria.rect.x < fase_largura - start_scrolling_pos_x:
            resultado_x, resultado_y = r.randint(box_aleatoria.rect.x, box_aleatoria.resultado_pos_x_box), \
                                       r.randint(70, altura - 80)

            if fase == 1:
                for pos_plat_fase_1 in lista_pos_fase_1:
                    if not pos_plat_fase_1[1] < resultado_y < pos_plat_fase_1[1] + 30:
                        if not pos_plat_fase_1[0] < resultado_x < pos_plat_fase_1[0] + 200:
                            box_aleatoria.rect.y = resultado_y
                            box_aleatoria.rect.x = resultado_x
                            box_aleatoria.set_image("caixa.png")
                        else:
                            box_aleatoria.set_new_box_position()
                    else:
                        box_aleatoria.set_new_box_position()
            elif fase == 2:
                for pos_plat_fase_2 in lista_pos_fase_2:
                    if resultado_y != pos_plat_fase_2[1] + 30:
                        if resultado_x != pos_plat_fase_2[0] + 200:
                            box_aleatoria.rect.y = resultado_y
                            box_aleatoria.rect.x = resultado_x
                            box_aleatoria.set_image("caixa.png")
                        else:
                            box_aleatoria.set_new_box_position()
                    else:
                        box_aleatoria.set_new_box_position()

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Inimigos(pg.sprite.Sprite):
    def __init__(self, color=blue, largura=51, altura=60):
        super(Inimigos, self).__init__()
        self.image = pg.Surface((largura, altura))
        self.image.fill(color)
        self.hspeed = - 0.5
        self.vspeed = 1
        self.set_propriedades()
        self.vida = 3

    def set_image(self, filename=None):
        if filename is not None:
            self.image = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/{}'
                                       .format(filename)).convert_alpha()

        return self.image

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_propriedades(self):
        self.rect = self.image.get_rect()

    def update(self, collidable=pg.sprite.Group()):

        self.rect.x += self.hspeed
        collision_list = pg.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if self.hspeed > 0:
                # RIGHT DIRECTION
                self.rect.right = collided_object.rect.left
                self.hspeed = 0
            elif self.hspeed < 0:
                # LEFT DIRECTION
                self.rect.left = collided_object.rect.right
                self.hspeed = 0

        self.rect.y += self.vspeed
        collision_list = pg.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            if self.vspeed > 0:
                # DOWN DIRECTION
                self.rect.bottom = collided_object.rect.top
                self.hspeed = 0
            elif self.vspeed < 0:
                # UP DIRECTION
                self.rect.top = collided_object.rect.bottom
                self.hspeed = 0


class Tiro(pg.sprite.Sprite):
    def __init__(self, largura=16, altura=9, color=red, mult=1):
        super(Tiro, self).__init__()
        self.image = pg.Surface((largura, altura))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.mult = mult
        self.status = "desativado"

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename=None):
        if filename is not None:
            self.image = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/{}'
                                       .format(filename))

    def criar_tiro(self):
        tiro.set_position(i.rect.centerx - 30, i.rect.centery + 8)
        lista_tiros_inimigo.append(tiro)

    def update(self, mult=1):
        self.rect.x += mult * self.speed

    def testa_colisao(self, rect_inimigo):
        colisao = self.rect.colliderect(rect_inimigo)
        return colisao

    def controle_laser(self):
        if self.status == "desativado":
            objetos_ativos.add(laser)
            objetos_ativos.add(laser_2)
            self.status = "ativado"
        elif self.status == "ativado":
            laser.kill()
            laser_2.kill()
            self.status = "desativado"


def get_frame(sprite_sheet, gId, columns, width, height, margin=0, top=0, space_v=0, space_h=4.33):
    col = gId % columns
    lin = int(gId / columns)
    x = margin + (col * (width + space_h))
    y = top + (lin * (height + space_v))
    frame = sprite_sheet.subsurface(x, y, width, height)
    return frame


def reposicionar_fase(fase_func):
    if fase_func == 1:
        fase_pos_x_func = 0
        personagem.personagem_pos_x_variavel = personagem.largura_personagem / 3
        personagem.set_position(0, 400)
        for inimigo in lista_inimigos:
            inimigo.set_position(r.randint(600, fase_largura - 300), r.randint(10, altura - 100))
        i = 0
        for teste_plat in lista_plataformas_fase_um:
            teste_plat.set_position(lista_pos_fase_1[i][0], lista_pos_fase_1[i][1])
            i += 1
        personagem.vspeed = 0
        personagem.hspeed = 0
        personagem.vida -= 1
        personagem.sangue = 15
        laser.set_position(593, 0)
        laser_2.set_position(3666, 0)

    elif fase_func == 2:
        fase_pos_x_func = 0
        personagem.personagem_pos_x_variavel = personagem.largura_personagem / 3
        personagem.set_position(0, 120)
        for inimigo in lista_inimigos:
            inimigo.set_position(r.randint(600, fase_largura - 300), r.randint(10, altura - 100))
        i = 0
        for teste_plat in lista_plataformas_fase_dois:
            teste_plat.set_position(lista_pos_fase_2[i][0], lista_pos_fase_2[i][1])
            i += 1
        personagem.vspeed = 0
        personagem.hspeed = 0
        personagem.vida -= 1
        personagem.sangue = 15
    return fase_pos_x_func


if __name__ == "__main__":

    # Centralizar tela
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Inicializações
    pg.init()
    pg.font.init()

    # Display
    tamanho_tela = largura, altura = 640, 480
    pg.display.set_caption("Anthony - The wonder boy")
    tela = pg.display.set_mode(tamanho_tela)

    # Background
    bg = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/base_fundo_posicoes.png') \
        .convert_alpha()
    bg_dois = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/fundo_2.png').convert_alpha()
    bg_largura, bg_altura = bg.get_rect().size
    fase_largura = bg_largura
    fase_pos_x = 0
    start_scrolling_pos_x = largura / 2
    selecao_tela = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/'
                                 'selecao_1.png').convert_alpha()
    selecao_tela_dois = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/'
                                      'selecao_2.png').convert_alpha()
    tela_creditos = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/'
                                  'creditos.png').convert_alpha()
    tela_como_jogar = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/como_jogar.png') \
        .convert_alpha()
    tela_game_over = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/'
                                   'gameover.png').convert_alpha()
    tela_tributo_stan_lee = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/imagens_compressao/'
                                          'stan_lee_tributo.png').convert_alpha()
    sprite_sheet_barra_hp = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/barra_hp.png')

    # Textos
    fonte = pg.font.SysFont("Comic Sans MS", 20, True)
    fonte_grande = pg.font.SysFont("Comic Sans MS", 40, True)

    # Tempo
    tempo = 0

    # Personagem
    personagem = Personagem()
    anthony = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    frame = 0
    estado_anthony = "transforma"
    sprite_sheet_anthony = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/personagem.png')
    personagem.set_position(personagem.rect.x, personagem.personagem_pos_y)
    personagem_parado_LD = None
    personagem_parado_LE = None
    tiro_personagem_imagem = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                           'tiro_tony.png').convert_alpha()
    tiro_especial_personagem_imagem = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                                    'tiro_especial.png').convert_alpha()

    # Inimigos
    inimigo_teste = Inimigos()
    inimigo_LE = pg.transform.scale(inimigo_teste.set_image('soldado.png'), (51, 60))
    inimigo_LD = pg.transform.flip(inimigo_LE, True, False)
    tiro_inimigo_imagem = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/tiro_soldado.png')
    laser = Tiro(25, 310)
    laser.set_image("laser.png")
    laser.set_position(593, 0)
    laser_2 = Tiro(25, 310)
    laser_2.set_image("laser.png")
    laser_2.set_position(3666, 0)

    # Sons
    som_tiro_anthony = pg.mixer.Sound('/home/leticia/PycharmProjects/projetos/Supermanas II/Sons/tiro_anthony.wav')
    som_tiro_inimigos = pg.mixer.Sound('/home/leticia/PycharmProjects/projetos/Supermanas II/Sons/tiro_inimigos.wav')
    som_selecao_menus = pg.mixer.Sound('/home/leticia/PycharmProjects/projetos/Supermanas II/Sons/selecao_menus.wav')
    som_transformacao_anthony = pg.mixer.Sound('/home/leticia/PycharmProjects/projetos/Supermanas II/Sons/'
                                               'Transformação Anthony.wav')
    som_tributo_stan_lee = pg.mixer.Sound('/home/leticia/PycharmProjects/projetos/Supermanas II/Sons/'
                                          'Tributo_stan_lee.wav')
    som_anthony_trans = False
    som_confirmar_opcao_menu = pg.mixer.Sound('/home/leticia/PycharmProjects/projetos/Supermanas II/Sons/'
                                              'confirmar_opcao_menu.wav')
    som_tiro_especial_anthony = pg.mixer.Sound('/home/leticia/PycharmProjects/projetos/Supermanas II/Sons/'
                                               'tiro_especial_anthony.wav')

    # Pontuações
    pontos = 0
    fase = 1
    comecou_fase = False

    # Criação das plataformas
    # fase 1
    #              x, y , largura, altura, color
    plataforma_um = Blocos(4030, 181, 200, 20, white)
    plataforma_um.set_image("plat_4.png")
    plataforma_dois = Blocos(3282, 242, 200, 20, black)
    plataforma_dois.set_image("plat_3.png")
    plataforma_tres = Blocos(325, 333, 200, 20, gray)
    plataforma_tres.set_image("plat_2.png")
    plataforma_quatro = Blocos(1390, 249, 200, 20, silver)
    plataforma_quatro.set_image("plat_3.png")
    plataforma_cinco = Blocos(2430, 349, 200, 20, red)
    plataforma_cinco.set_image("plat_3.png")
    plataforma_seis = Blocos(909, 399, 200, 20, green)
    plataforma_seis.set_image("plat_3.png")
    plataforma_nove = Blocos(104, 393, 200, 20, magenta)
    plataforma_nove.set_image("plat_1.png")
    plataforma_doze = Blocos(828, 221, 200, 20, pink)
    plataforma_doze.set_image("plat_3.png")
    plataforma_treze = Blocos(1126, 172, 200, 20, teal)
    plataforma_treze.set_image("plat_3.png")
    plataforma_quatorze = Blocos(1171, 329, 200, 20, purple)
    plataforma_quatorze.set_image("plat_3.png")
    plataforma_quinze = Blocos(1629, 355, 200, 20, yellow)
    plataforma_quinze.set_image("plat_3.png")
    plataforma_dezesseis = Blocos(2100, 251, 200, 20, indigo)
    plataforma_dezesseis.set_image("plat_3.png")
    plataforma_dezessete = Blocos(2799, 350, 200, 20, crimson)
    plataforma_dezessete.set_image("plat_3.png")
    plataforma_dezoito = Blocos(3042, 300, 200, 20, deepskyblue)
    plataforma_dezoito.set_image("plat_3.png")
    plataforma_dezenove = Blocos(4272, 256, 200, 20, darkgreen)
    plataforma_dezenove.set_image("plat_4.png")
    plataforma_vinte = Blocos(4471, 331, 200, 20, chocolate)
    plataforma_vinte.set_image("plat_4.png")
    plataforma_vinte_um = Blocos(4309, 127, 200, 20, olive)
    plataforma_vinte_um.set_image("plat_4.png")
    plataforma_vinte_dois = Blocos(4546, 90, 200, 20, salmon)
    plataforma_vinte_dois.set_image("plat_4.png")
    plataforma_vinte_tres = Blocos(4747, 378, 200, 20, lime)
    plataforma_vinte_tres.set_image("plat_4.png")
    plataforma_vinte_quatro = Blocos(4770, 150, 200, 20, midnightblue)
    plataforma_vinte_quatro.set_image("plat_4.png")
    plataforma_vinte_cinco = Blocos(4989, 207, 200, 20, rosybrown)
    plataforma_vinte_cinco.set_image("plat_4.png")
    plataforma_vinte_seis = Blocos(5203, 306, 200, 20, lightgrey)
    plataforma_vinte_seis.set_image("plat_2.png")
    plataforma_vinte_sete = Blocos(5499, 380, 200, 20, lightcoral)
    plataforma_vinte_sete.set_image("plat_2.png")
    plataforma_sete = Blocos(5756, 303, 200, 20, blue)
    plataforma_sete.set_image("plat_2.png")
    plataforma_oito = Blocos(5992, 211, 200, 20, orchid)
    plataforma_oito.set_image("plat_4.png")
    plataforma_onze = Blocos(6200, 122, 200, 20, cyan)
    plataforma_onze.set_image("plat_4.png")

    muro_um = Blocos(578, 305, 60, 150, orange)
    muro_um.set_image("portao_lab.png")
    muro_dois = Blocos(2682, 305, 60, 150, orange)
    muro_dois.set_image("estante.png")
    muro_tres = Blocos(3648, 305, 60, 150, orange)
    muro_tres.set_image("portao_lab.png")

    chao_um = Blocos(0, 445, 638, 10, yellow)
    chao_um.set_image("chao_1.png")
    chao_dois = Blocos(909, 445, 2534, 10, yellow)
    chao_dois.set_image("chao_2.png")
    chao_tres = Blocos(3648, 445, 1280, 10, yellow)
    chao_tres.set_image("chao_3.png")
    chao_quatro = Blocos(6152, 445, 255, 10, yellow)
    chao_quatro.set_image("chao_4.png")

    # fase 2
    plataforma_vinte_oito = Blocos(2, 121, 200, 20, lightcoral)
    plataforma_vinte_oito.set_image("plat_4.png")
    plataforma_vinte_nove = Blocos(208, 209, 200, 20, white)
    plataforma_vinte_nove.set_image("plat_4.png")
    plataforma_trinta = Blocos(643, 330, 170, 20, red)
    plataforma_trinta.set_image("plat_7.png")
    plataforma_trinta_um = Blocos(880, 330, 170, 20, green)
    plataforma_trinta_um.set_image("plat_7.png")
    plataforma_trinta_dois = Blocos(1148, 374, 150, 20, blue)
    plataforma_trinta_dois.set_image("plat_8.png")
    plataforma_trinta_quatro = Blocos(1503, 374, 150, 20, magenta)
    plataforma_trinta_quatro.set_image("plat_8.png")
    plataforma_trinta_cinco = Blocos(1148, 143, 150, 20, brown)
    plataforma_trinta_cinco.set_image("plat_8.png")
    plataforma_trinta_sete = Blocos(1503, 143, 150, 20, purple)
    plataforma_trinta_sete.set_image("plat_8.png")
    plataforma_trinta_oito = Blocos(1723, 345, 170, 20, pink)
    plataforma_trinta_oito.set_image("plat_7.png")
    plataforma_trinta_nove = Blocos(2022, 345, 170, 20, teal)
    plataforma_trinta_nove.set_image("plat_7.png")
    plataforma_quarenta = Blocos(1723, 158, 170, 20, indigo)
    plataforma_quarenta.set_image("plat_7.png")
    plataforma_quarenta_um = Blocos(2022, 158, 170, 20, crimson)
    plataforma_quarenta_um.set_image("plat_7.png")
    plataforma_quarenta_dois = Blocos(1900, 250, 130, 20, deepskyblue)
    plataforma_quarenta_dois.set_image("plat_10.png")
    plataforma_quarenta_tres = Blocos(2275, 114, 203, 38, darkgreen)
    plataforma_quarenta_tres.set_image("plat_5.png")
    plataforma_trinta_seis = Blocos(2617, 224, 200, 20, cyan)
    plataforma_trinta_seis.set_image("plat_2.png")
    plataforma_quarenta_quatro = Blocos(2900, 280, 400, 230, darkgreen)
    plataforma_quarenta_quatro.set_image("navio.png")
    plataforma_sessenta_tres = Blocos(2970, 247, 264, 81)
    plataforma_sessenta_tres.set_image("navio_cima.png")
    plataforma_trinta_tres = Blocos(3375, 247, 200, 20, orange)
    plataforma_trinta_tres.set_image("plat_2.png")
    plataforma_quarenta_cinco = Blocos(3657, 280, 400, 230, darkgreen)
    plataforma_quarenta_cinco.set_image("navio.png")
    plataforma_sessenta_dois = Blocos(3727, 199, 264, 81, white)
    plataforma_sessenta_dois.set_image("navio_cima.png")
    plataforma_quarenta_seis = Blocos(4137, 190, 200, 20, yellow)
    plataforma_quarenta_seis.set_image("plat_2.png")
    plataforma_quarenta_sete = Blocos(4425, 114, 203, 38, darkgreen)
    plataforma_quarenta_sete.set_image("plat_6.png")
    plataforma_quarenta_oito = Blocos(4772, 349, 170, 20, chocolate)
    plataforma_quarenta_oito.set_image("plat_7.png")
    plataforma_quarenta_nove = Blocos(5009, 349, 170, 20, olive)
    plataforma_quarenta_nove.set_image("plat_7.png")
    plataforma_cinquenta = Blocos(5316, 347, 120, 20, rosybrown)
    plataforma_cinquenta.set_image("plat_9.png")
    plataforma_cinquenta_um = Blocos(5556, 347, 120, 20, salmon)
    plataforma_cinquenta_um.set_image("plat_9.png")
    plataforma_cinquenta_dois = Blocos(5436, 249, 120, 20, lime)
    plataforma_cinquenta_dois.set_image("plat_9.png")
    plataforma_cinquenta_tres = Blocos(5316, 152, 120, 20, midnightblue)
    plataforma_cinquenta_tres.set_image("plat_9.png")
    plataforma_cinquenta_quatro = Blocos(5556, 152, 120, 20, lightcoral)
    plataforma_cinquenta_quatro.set_image("plat_9.png")
    plataforma_cinquenta_cinco = Blocos(5809, 375, 120, 20, lightgrey)
    plataforma_cinquenta_cinco.set_image("plat_9.png")
    plataforma_cinquenta_seis = Blocos(6049, 375, 120, 20, orchid)
    plataforma_cinquenta_seis.set_image("plat_9.png")
    plataforma_cinquenta_sete = Blocos(5928, 281, 120, 20, lime)
    plataforma_cinquenta_sete.set_image("plat_9.png")
    plataforma_cinquenta_oito = Blocos(5808, 184, 120, 20, midnightblue)
    plataforma_cinquenta_oito.set_image("plat_9.png")
    plataforma_cinquenta_nove = Blocos(6048, 184, 120, 20, lightcoral)
    plataforma_cinquenta_nove.set_image("plat_9.png")
    plataforma_sessenta = Blocos(6239, 436, 150, 20, white)
    plataforma_sessenta.set_image("plat_8.png")
    plataforma_sessenta_um = Blocos(6240, 205, 150, 20, white)
    plataforma_sessenta_um.set_image("plat_8.png")

    lista_plataformas_fase_um = [
        plataforma_um,
        plataforma_dois,
        plataforma_tres,
        plataforma_quatro,
        plataforma_cinco,
        plataforma_seis,
        plataforma_nove,
        plataforma_doze,
        plataforma_treze,
        plataforma_quatorze,
        plataforma_quinze,
        plataforma_dezesseis,
        plataforma_dezessete,
        plataforma_dezoito,
        plataforma_dezenove,
        plataforma_vinte,
        plataforma_vinte_um,
        plataforma_vinte_dois,
        plataforma_vinte_tres,
        plataforma_vinte_quatro,
        plataforma_vinte_cinco,
        plataforma_vinte_seis,
        plataforma_vinte_sete,
        plataforma_sete,
        plataforma_oito,
        plataforma_onze,
        muro_um,
        muro_dois,
        muro_tres,
        chao_um,
        chao_dois,
        chao_tres,
        chao_quatro
    ]

    lista_plataformas_fase_dois = [
        plataforma_vinte_oito,
        plataforma_vinte_nove,
        plataforma_trinta,
        plataforma_trinta_um,
        plataforma_trinta_dois,
        plataforma_trinta_quatro,
        plataforma_trinta_cinco,
        plataforma_trinta_sete,
        plataforma_trinta_oito,
        plataforma_trinta_nove,
        plataforma_quarenta,
        plataforma_quarenta_um,
        plataforma_quarenta_dois,
        plataforma_quarenta_tres,
        plataforma_trinta_seis,
        plataforma_quarenta_quatro,
        plataforma_sessenta_tres,
        plataforma_trinta_tres,
        plataforma_quarenta_cinco,
        plataforma_sessenta_dois,
        plataforma_quarenta_seis,
        plataforma_quarenta_sete,
        plataforma_quarenta_oito,
        plataforma_quarenta_nove,
        plataforma_cinquenta,
        plataforma_cinquenta_um,
        plataforma_cinquenta_dois,
        plataforma_cinquenta_tres,
        plataforma_cinquenta_quatro,
        plataforma_cinquenta_cinco,
        plataforma_cinquenta_seis,
        plataforma_cinquenta_sete,
        plataforma_cinquenta_oito,
        plataforma_cinquenta_nove,
        plataforma_sessenta,
        plataforma_sessenta_um

    ]

    lista_pos_fase_1 = [
        [4030, 181],
        [3282, 242],
        [325, 333],
        [1390, 249],
        [2430, 349],
        [909, 399],
        [104, 393],
        [828, 221],
        [1126, 172],
        [1171, 329],
        [1629, 355],
        [2100, 251],
        [2799, 350],
        [3042, 300],
        [4272, 256],
        [4471, 331],
        [4309, 127],
        [4546, 90],
        [4747, 378],
        [4770, 150],
        [4989, 207],
        [5203, 306],
        [5499, 380],
        [5756, 303],
        [5992, 211],
        [6200, 122],
        [578, 305],
        [2682, 305],
        [3648, 305],
        [0, 445],
        [909, 445],
        [3648, 445],
        [6152, 445]
    ]

    lista_pos_fase_2 = [
        [2, 121],
        [208, 209],
        [643, 330],
        [880, 330],
        [1148, 374],
        [1503, 374],
        [1148, 143],
        [1503, 143],
        [1723, 345],
        [2022, 345],
        [1723, 158],
        [2022, 158],
        [1900, 250],
        [2275, 114],
        [2617, 224],
        [2900, 280],
        [2970, 199],
        [3375, 247],
        [3657, 280],
        [3727, 199],
        [4137, 190],
        [4425, 114],
        [4772, 349],
        [5009, 349],
        [5316, 347],
        [5556, 347],
        [5436, 249],
        [5316, 152],
        [5556, 152],
        [5809, 375],
        [6049, 375],
        [5928, 281],
        [5808, 184],
        [6048, 184],
        [6239, 436],
        [6240, 205]
    ]

    # Criação de mystery box
    box_pos_x = 835
    box_aleatoria = Blocos(r.randint(box_pos_x, int(fase_largura / 3)), r.randint(70, altura - 80), 40, 40)
    box_aleatoria.set_image("caixa.png")

    # Criação de tiros
    lista_tiros = []
    lista_tiros_inimigo = []
    lista_tiros_especial = []

    # adição das plataformas para desenhar
    plataformas_desenhar = pg.sprite.Group()
    objetos_ativos = pg.sprite.Group()
    objetos_ativos.add(box_aleatoria)
    objetos_ativos.add(personagem)

    # Definição de barra de vida e barra de especial
    barra_especial = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                   'barra_especial.png').convert_alpha()
    barra_especial_1 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                     'barra_especial_1.png').convert_alpha()
    barra_especial_2 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                     'barra_especial_2.png').convert_alpha()
    barra_especial_3 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                     'barra_especial_3.png').convert_alpha()
    barra_especial_4 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                     'barra_especial_4.png').convert_alpha()
    barra_especial_5 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                     'barra_especial_5.png').convert_alpha()
    barra_especial_6 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                     'barra_especial_6.png').convert_alpha()
    barra_especial_7 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                     'barra_especial_7.png').convert_alpha()
    barra_especial_8 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/'
                                     'barra_especial_8.png').convert_alpha()
    vida_1 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/vida_1.png').convert_alpha()
    vida_2 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/vida_2.png').convert_alpha()
    vida_3 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/vida_3.png').convert_alpha()
    vida_4 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/vida_4.png').convert_alpha()
    vida_5 = pg.image.load('/home/leticia/PycharmProjects/projetos/Supermanas II/Imagens/vida_5.png').convert_alpha()

    barra_especial_padrao = None
    vidas_padrao = None
    barra_hp_padrao = None
    barra_hp_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    frame_barra_hp = 13

    # Criação inimigos
    lista_inimigos = []

    for i in range(0, 31):
        inimigo_criacao = Inimigos()
        lista_inimigos.append(inimigo_criacao)

    for plataforma in lista_plataformas_fase_um:
        plataformas_desenhar.add(plataforma)
        objetos_ativos.add(plataforma)

    for inimigo in lista_inimigos:
        inimigo.set_position(r.randint(600, fase_largura - 300), r.randint(10, altura - 100))
        inimigo.image = inimigo_LE
        objetos_ativos.add(inimigo)

    clock = pg.time.Clock()
    fps = 60
    delay_tiro_inimigo = 0
    delay_laser = 0
    tempo_pause, tempo_total_pause = 0, 0
    comprimiu = False

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and
                                         (estado == 0 or estado == 7)):
                running = False
                if comprimiu is not True:
                    chamar_compressao_imagem()
                    comprimiu = True
                    print("comprimiu")

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE and (estado == 5 or estado == 2 or estado == 3):
                    estado = 0

                elif event.key == pg.K_ESCAPE and estado == 1:
                    comecou_fase = False
                    estado = 5
                    estado_anthony = "transforma"
                    frame = 0
                    som_anthony_trans = False
                    '''if fase == 2:
                        fase_pos_x = reposicionar_fase(1)'''

                if event.key == pg.K_SPACE and estado == 1:
                    if personagem.image == personagem_parado_LD or personagem.estado == "andando dir":
                        tiro = Tiro()
                        if personagem.rect.x == personagem.personagem_pos_x_variavel:
                            tiro.set_position(personagem.personagem_pos_x_variavel + 30, personagem.rect.centery - 10)
                            lista_tiros.append(tiro)
                            som_tiro_anthony.play()
                        else:
                            tiro.set_position(personagem.rect.x + 30, personagem.rect.centery - 10)
                            lista_tiros.append(tiro)
                            som_tiro_anthony.play()
                        for t in lista_tiros:
                            t.image = tiro_personagem_imagem
                            objetos_ativos.add(t)
                    else:
                        tiro = Tiro(mult=-1)
                        if personagem.rect.x == personagem.personagem_pos_x_variavel:
                            tiro.set_position(personagem.personagem_pos_x_variavel + 30, personagem.rect.centery - 10)
                            lista_tiros.append(tiro)
                            som_tiro_anthony.play()
                        else:
                            tiro.set_position(personagem.rect.x + 30, personagem.rect.centery - 10)
                            lista_tiros.append(tiro)
                            som_tiro_anthony.play()
                        for t in lista_tiros:
                            t.image = tiro_personagem_imagem
                            objetos_ativos.add(t)

                if event.key == pg.K_p and estado == 1:
                    estado = 4
                    tempo_inicial_pause = (int(round(time.time())) % 10000)

                elif event.key == pg.K_p and estado == 4:
                    tempo_pause = (int(round(time.time())) % 10000) - tempo_inicial_pause
                    tempo_total_pause += tempo_pause
                    estado = 1

                if estado == 0:
                    if event.key == pg.K_DOWN:
                        som_selecao_menus.play()
                        pos_y, indice_menu = mostrar_menu_inicial(indice_menu, pos_y, 0)

                    elif event.key == pg.K_UP:
                        som_selecao_menus.play()
                        pos_y, indice_menu = mostrar_menu_inicial(indice_menu, pos_y, 0, -1)

                    if event.key == pg.K_RETURN:
                        if pos_y == pos_y_inicial:
                            som_confirmar_opcao_menu.play()
                            estado = 5
                        elif pos_y == pos_y_limite:
                            som_confirmar_opcao_menu.play()
                            estado = 3
                        elif pos_y_inicial < pos_y < pos_y_limite:
                            som_confirmar_opcao_menu.play()
                            estado = 2

                elif estado == 5:
                    if event.key == pg.K_RIGHT:
                        som_selecao_menus.play()
                        pos_x_seta_2, indice_fases = mostrar_menu_inicial(indice_fases, pos_x_seta_2, 5)

                    elif event.key == pg.K_LEFT:
                        som_selecao_menus.play()
                        pos_x_seta_2, indice_fases = mostrar_menu_inicial(indice_fases, pos_x_seta_2, 5, -1)

                    if event.key == pg.K_RETURN:
                        if pos_x_seta_2 == pos_x_inicial:
                            som_confirmar_opcao_menu.play()
                            fase = 1
                            estado = 1
                            tempo_inicial = (int(round(time.time())) % 10000)
                            laser.status = "desativado"
                            laser_2.status = "desativado"
                        elif pos_x_seta_2 == pos_x_limite:
                            pass
                        elif pos_x_inicial < pos_x_seta_2 < pos_x_limite and fase == 2:
                            laser.status = "desativado"
                            laser_2.status = "desativado"
                            som_confirmar_opcao_menu.play()
                            estado = 1
                            tempo_inicial = (int(round(time.time())) % 10000)
                            personagem.vspeed = 0
                            personagem.hspeed = 0
                            fase_pos_x = 0
                            personagem.personagem_pos_x_variavel = personagem.largura_personagem / 3
                            personagem.set_position(0, 4)
                            i = 0
                            for teste_plat in lista_plataformas_fase_dois:
                                teste_plat.set_position(lista_pos_fase_2[i][0], lista_pos_fase_2[i][1])
                                i += 1
                                objetos_ativos.add(teste_plat)
                                plataformas_desenhar.add(teste_plat)
                            objetos_ativos.add(box_aleatoria)
                            objetos_ativos.add(personagem)
                            for i in range(0, 31):
                                inimigo_criacao = Inimigos()
                                lista_inimigos.append(inimigo_criacao)
                            for inimigo in lista_inimigos:
                                inimigo.set_position(r.randint(600, fase_largura - 300),
                                                     r.randint(10, altura - 100))
                                inimigo.image = inimigo_LE
                                objetos_ativos.add(inimigo)

                elif estado == 6:
                    if event.key == pg.K_RETURN:
                        estado = 0

        if estado == 1:
            if estado_anthony == "transforma":
                if som_anthony_trans is False:
                    som_transformacao_anthony.play(maxtime=2600)
                    som_anthony_trans = True
                fps = 5
                gId = anthony[frame]
                sprite_anthony = get_frame(sprite_sheet_anthony, gId
                                           , 11, 53.25, 65)

                personagem.image = sprite_anthony

                if frame < len(anthony) - 1:
                    frame += 1
                else:
                    estado_anthony = "jogando"
            else:
                fps = 60
                personagem_parado_LD = sprite_anthony
                personagem_parado_LE = pg.transform.flip(sprite_anthony, True, False)

            if fase == 1:
                if delay_laser < 20:
                    laser.controle_laser()
                    laser_2.controle_laser()
                    delay_laser = 150

                if laser.status == "ativado":
                    if laser.testa_colisao(personagem.rect):
                        fase_pos_x = reposicionar_fase(1)

                if laser_2.status == "ativado":
                    if laser_2.testa_colisao(personagem.rect):
                        fase_pos_x = reposicionar_fase(1)

            comecou_fase = True
            tempo = ((180 + tempo_total_pause) - ((int(round(time.time())) % 10000) - tempo_inicial))
            personagem.update(plataformas_desenhar, event)
            event = None
            if personagem.estado == "andando dir":
                personagem.update_frame("andando dir")
            elif personagem.estado == "andando esq":
                andando_esq = personagem.update_frame("andando esq")
                personagem.image = pg.transform.flip(andando_esq, True, False)

            if start_scrolling_pos_x <= personagem.personagem_pos_x_variavel <= 6400 - start_scrolling_pos_x:
                if fase == 1:
                    laser.rect.x -= personagem.hspeed
                    laser_2.rect.x -= personagem.hspeed
                    for plataformas_pos in lista_plataformas_fase_um:
                        plataformas_pos.rect.x -= personagem.hspeed
                elif fase == 2:
                    for plataformas_pos in lista_plataformas_fase_dois:
                        plataformas_pos.rect.x -= personagem.hspeed

                for inimigos_pos in lista_inimigos:
                    inimigos_pos.rect.x -= personagem.hspeed

                box_aleatoria.rect.x -= personagem.hspeed

            for i in lista_inimigos:
                if 300 >= i.rect.x - personagem.rect.x >= 15:
                    i.image = inimigo_LE
                    if delay_tiro_inimigo < 50:
                        tiro = Tiro(largura=7, altura=4, mult=-1)
                        tiro.criar_tiro()
                        delay_tiro_inimigo = 120
                        som_tiro_inimigos.play()
                if -300 <= i.rect.x - personagem.rect.x <= -15:
                    i.image = inimigo_LD
                    if delay_tiro_inimigo < 50:
                        tiro = Tiro(largura=7, altura=4)
                        tiro.criar_tiro()
                        delay_tiro_inimigo = 100
                        som_tiro_inimigos.play()
                if i.rect.y >= 490:
                    lista_inimigos.remove(i)
                    i.kill()

            for t_inimigo in lista_tiros_inimigo:
                t_inimigo.image = tiro_inimigo_imagem
                objetos_ativos.add(t_inimigo)

            for tiro_inimigo in lista_tiros_inimigo:
                if tiro_inimigo.testa_colisao(personagem.rect):
                    personagem.sangue -= 1
                    frame_barra_hp -= 1
                    lista_tiros_inimigo.remove(tiro_inimigo)
                    tiro_inimigo.kill()
                    if personagem.sangue <= 1:
                        personagem.vida -= 1
                        personagem.sangue = 15
                elif tiro_inimigo.rect.x >= 640 or tiro_inimigo.rect.x <= 0 or comecou_fase is False:
                    lista_tiros_inimigo.remove(tiro_inimigo)
                    tiro_inimigo.kill()
                for plat_colisao in plataformas_desenhar:
                    if tiro_inimigo in lista_tiros_inimigo:
                        if tiro_inimigo.testa_colisao(plat_colisao.rect):
                            lista_tiros_inimigo.remove(tiro_inimigo)
                            tiro_inimigo.kill()
                if personagem.vida <= 0:
                    estado = 6
                    fase = 1
                    fase_pos_x = reposicionar_fase(1)
                    comecou_fase = False
                    personagem.vida = 5
                    personagem.sangue = 15
                    personagem.especial = 0
                    pontos = 0
                    estado_anthony = "transforma"
                    tempo_total_pause = 0

                    for i in range(0, 31):
                        inimigo_criacao = Inimigos()
                        lista_inimigos.append(inimigo_criacao)
                    for inimigo in lista_inimigos:
                        inimigo.set_position(r.randint(600, fase_largura - 300),
                                             r.randint(10, altura - 100))
                        inimigo.image = inimigo_LE
                        objetos_ativos.add(inimigo)

            for inimigo_colisao in lista_inimigos:
                for tiro in lista_tiros:
                    if tiro.testa_colisao(inimigo_colisao.rect):
                        inimigo_colisao.vida = inimigo_colisao.vida - 1
                        lista_tiros.remove(tiro)
                        tiro.kill()
                        if inimigo_colisao.vida <= 0:
                            inimigo_colisao.kill()
                            lista_inimigos.remove(inimigo_colisao)
                            pontos += 10
                            if personagem.especial < 8:
                                personagem.especial += 1
                    elif tiro.rect.x >= 640 or tiro.rect.x <= 0:
                        lista_tiros.remove(tiro)
                        tiro.kill()
                    for plat_colisao in plataformas_desenhar:
                        if tiro in lista_tiros:
                            if tiro.testa_colisao(plat_colisao.rect):
                                lista_tiros.remove(tiro)
                                tiro.kill()

            for inimigo_colisao in lista_inimigos:
                for tiro_especial in lista_tiros_especial:
                    if tiro_especial.testa_colisao(inimigo_colisao.rect):
                        inimigo_colisao.vida = inimigo_colisao.vida - 3
                        lista_tiros_especial.remove(tiro_especial)
                        tiro_especial.kill()
                        if inimigo_colisao.vida <= 0:
                            inimigo_colisao.kill()
                            lista_inimigos.remove(inimigo_colisao)
                            pontos += 10
                    for plat_colisao in plataformas_desenhar:
                        if tiro_especial.testa_colisao(plat_colisao.rect):
                            lista_tiros_especial.remove(tiro_especial)
                            tiro_especial.kill()

            for inimigos_pos in lista_inimigos:
                inimigos_pos.update(plataformas_desenhar)

            for tiro in lista_tiros:
                tiro.update(tiro.mult)

            for tiro_enemy in lista_tiros_inimigo:
                tiro_enemy.update(tiro_enemy.mult)

            for tiro in lista_tiros_especial:
                tiro.update(tiro.mult)

            if personagem.especial == 0:
                barra_especial_padrao = barra_especial
            elif personagem.especial == 1:
                barra_especial_padrao = barra_especial_1
            elif personagem.especial == 2:
                barra_especial_padrao = barra_especial_2
            elif personagem.especial == 3:
                barra_especial_padrao = barra_especial_3
            elif personagem.especial == 4:
                barra_especial_padrao = barra_especial_4
            elif personagem.especial == 5:
                barra_especial_padrao = barra_especial_5
            elif personagem.especial == 6:
                barra_especial_padrao = barra_especial_6
            elif personagem.especial == 7:
                barra_especial_padrao = barra_especial_7
            else:
                barra_especial_padrao = barra_especial_8

            gId_barra = barra_hp_indices[frame_barra_hp]
            barra_hp_sprite = get_frame(sprite_sheet_barra_hp, gId_barra, 1, 100, 16, space_h=0)
            barra_hp_padrao = barra_hp_sprite

            if frame_barra_hp < 0:
                frame_barra_hp = 13

            if personagem.vida == 1:
                vidas_padrao = vida_1
            elif personagem.vida == 2:
                vidas_padrao = vida_2
            elif personagem.vida == 3:
                vidas_padrao = vida_3
            elif personagem.vida == 4:
                vidas_padrao = vida_4
            elif personagem.vida == 5:
                vidas_padrao = vida_5
            else:
                estado = 6
                fase = 1
                fase_pos_x = reposicionar_fase(1)
                comecou_fase = False
                personagem.vida = 5
                personagem.sangue = 15
                personagem.especial = 0
                pontos = 0

            # limites da tela
            # lado direito
            if personagem.personagem_pos_x_variavel > fase_largura - personagem.largura_personagem:
                personagem.personagem_pos_x_variavel = fase_largura - personagem.largura_personagem

            # lado esquerdo
            if personagem.personagem_pos_x_variavel < personagem.largura_personagem / 2:
                personagem.personagem_pos_x_variavel = personagem.largura_personagem / 2

            # posicionar personagem na tela
            if personagem.personagem_pos_x_variavel < start_scrolling_pos_x:
                personagem.rect.x = personagem.personagem_pos_x_variavel
            elif personagem.personagem_pos_x_variavel > fase_largura - start_scrolling_pos_x:
                personagem.rect.x = personagem.personagem_pos_x_variavel - fase_largura + largura
            else:
                personagem.rect.x = start_scrolling_pos_x
                fase_pos_x += -personagem.hspeed

            pos_relativa_bg = fase_pos_x % bg_largura

            if fase == 1:
                tela.blit(bg, (pos_relativa_bg - bg_largura, 0))
                if pos_relativa_bg < largura:
                    tela.blit(bg, (pos_relativa_bg, 0))
            elif fase == 2:
                bg = bg_dois
                tela.blit(bg, (pos_relativa_bg - bg_largura, 0))
                if pos_relativa_bg < largura:
                    tela.blit(bg, (pos_relativa_bg, 0))

            if personagem.rect.y >= 470:
                if personagem.vida <= 0:
                    estado = 6
                    fase = 1
                    fase_pos_x = reposicionar_fase(1)
                    comecou_fase = False
                    personagem.vida = 5
                    personagem.sangue = 15
                    personagem.especial = 0
                    pontos = 0
                    objetos_ativos.empty()
                    plataformas_desenhar.empty()
                    fase += 1
                    estado_anthony = "transforma"
                    frame = 0
                    som_anthony_trans = False
                    personagem.estado = None
                elif fase == 1:
                    fase_pos_x = reposicionar_fase(1)

                elif fase == 2:
                    fase_pos_x = reposicionar_fase(2)

            if estado == 1 or estado == 4:
                imagem_pontos = fonte.render("Pontos:" + str(pontos), True, red)
                imagem_tempo = fonte.render(str(tempo), True, red)
                tela.blit(imagem_tempo, (320, 0))
                tela.blit(imagem_pontos, (400, 0))
                tela.blit(barra_especial_padrao, (0, 17))
                tela.blit(barra_hp_padrao, (0, 0))
                tela.blit(vidas_padrao, (102, 0))
                objetos_ativos.draw(tela)

            delay_tiro_inimigo -= 1
            if delay_tiro_inimigo < 0:
                delay_tiro_inimigo = 0

            delay_laser -= 1
            if delay_laser < 0:
                delay_laser = 0

            if personagem.rect.x >= 587:
                if fase == 1:
                    objetos_ativos.empty()
                    plataformas_desenhar.empty()
                    fase += 1
                    comecou_fase = False
                    estado = 5
                    estado_anthony = "transforma"
                    frame = 0
                    som_anthony_trans = False
                    personagem.estado = None
                    tempo_total_pause = 0
                else:
                    estado = 7

            if tempo <= 0:
                if personagem.vida > 1:
                    if fase == 1:
                        if len(lista_inimigos) > 20:
                            tempo_inicial = (int(round(time.time())) % 10000)
                            personagem.sangue = 15
                            comecou_fase = False
                            tempo_total_pause = 0
                            fase_pos_x = reposicionar_fase(1)
                        else:
                            tempo_inicial = (int(round(time.time())) % 10000)
                            personagem.sangue = 15
                            comecou_fase = False
                            fase_pos_x = reposicionar_fase(1)
                            tempo_total_pause = 0
                            for i in range(0, 15):
                                inimigo_criacao = Inimigos()
                                lista_inimigos.append(inimigo_criacao)

                            for inimigo in lista_inimigos:
                                inimigo.set_position(r.randint(600, fase_largura - 300), r.randint(10, altura - 100))
                                inimigo.image = inimigo_LE
                                objetos_ativos.add(inimigo)

                    elif fase == 2:
                        if len(lista_inimigos) > 20:
                            tempo_inicial = (int(round(time.time())) % 10000)
                            personagem.sangue = 15
                            comecou_fase = False
                            tempo_total_pause = 0
                            fase_pos_x = reposicionar_fase(2)
                        else:
                            tempo_inicial = (int(round(time.time())) % 10000)
                            personagem.sangue = 15
                            comecou_fase = False
                            tempo_total_pause = 0
                            fase_pos_x = reposicionar_fase(2)
                            for i in range(0, 15):
                                inimigo_criacao = Inimigos()
                                lista_inimigos.append(inimigo_criacao)
                            for inimigo in lista_inimigos:
                                inimigo.set_position(r.randint(600, fase_largura - 300), r.randint(10, altura - 100))
                                inimigo.image = inimigo_LE
                                objetos_ativos.add(inimigo)
                else:
                    estado = 6
                    fase = 1
                    fase_pos_x = reposicionar_fase(1)
                    comecou_fase = False
                    personagem.vida = 5
                    personagem.sangue = 15
                    personagem.especial = 0
                    pontos = 0

        elif estado == 0:
            tela.blit(bg_menu_inicial, (0, 0))
            tela.blit(seta, (pos_x, pos_y))

        elif estado == 2:
            tela.blit(tela_como_jogar, (0, 0))

        elif estado == 3:
            tela.blit(tela_creditos, (0, 0))

        elif estado == 4:
            imagem_pausado = fonte_grande.render("PAUSE", True, black)
            tela.blit(imagem_pausado, (320, 240))

        elif estado == 5 and comecou_fase is False:
            if fase == 1:
                tela.blit(selecao_tela, (0, 0))
                tela.blit(seta_dois, (pos_x_seta_2, pos_y_seta_2))
            elif fase == 2:
                tela.blit(selecao_tela_dois, (0, 0))
                tela.blit(seta_dois, (pos_x_seta_2, pos_y_seta_2))

        elif estado == 6:
            tela.blit(tela_game_over, (0, 0))

        elif estado == 7:
            som_tributo_stan_lee.play()
            tela.blit(tela_tributo_stan_lee, (0, 0))

        clock.tick(fps)
        pg.display.update()

    pg.quit()
