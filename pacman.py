import pygame
from abc import ABCMeta, abstractmethod
import random

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
fonte = pygame.font.SysFont('arial', 24, True, False)
fonte_dois = pygame.font.SysFont('arial', 90, True, False)
pygame.display.set_caption('Pacman')

AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
ROSA = (255, 0, 255)
CIANO = (0, 255, 255)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
LARANJA = (255, 130, 0)
VERDE = (0, 255, 0)
VELOCIDADE = 0.8
ACIMA = 1
ABAIXO = 2
DIREITA = 3
ESQUERDA = 4

class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, tamanho, personagem):
        pass

class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass


class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac):
        self.pacman = pac
        self.moviveis = []
        self.pontos = 0
        # ESTADOS POSÍVEIS: 0-JOGANDO 1-PAUSADO 2-GAMEOVER 3-VITORIA
        self.estado = 'JOGANDO'
        self.tamanho = tamanho
        self.vidas = 5
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 3, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 3, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)

    def pintar_score(self, tela, pontos):
        texto_x = 30 * self.tamanho
        img_pontos = fonte.render(f'SCORE: {self.pontos}', True, BRANCO)
        tela.blit(img_pontos, (texto_x, 50))
        img_vidas = fonte.render(f'VIDAS: {self.vidas}', True, BRANCO)
        tela.blit(img_vidas, (texto_x, 100))



    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = self.tamanho // 2
            cor = PRETO
            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, BRANCO, (x + half, y + half), self.tamanho // 10, 0)
            if coluna == 3:
                pygame.draw.circle(tela, VERMELHO, (x + half, y + half), self.tamanho // 5, 0)

    def pintar(self, tela):
        if self.estado == 'JOGANDO':
            self.pintar_jogando(tela)
        elif self.estado == 'PAUSADO':
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == 'GAME OVER':
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)
        elif self.estado == 'VITORIA':
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)

    def pintar_texto_centro(self, tela, texto, cor):
        img_texto = fonte_dois.render(texto, True, cor)
        texto_x = (tela.get_width() - img_texto.get_width()) // 2
        texto_y = (tela.get_height() - img_texto.get_height()) //2
        tela.blit(img_texto, (texto_x, texto_y))

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, 'Y O U  W I N', AMARELO)

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, 'G A M E  O V E R', VERMELHO)

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, 'P A U S E', AMARELO)

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_score(tela, self.pontos)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(ACIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(ABAIXO)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIREITA)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        return direcoes

    def fantasma_direcao(self, direcoes):
        direcao = direcoes[random.randint(0, len(direcoes) - 1)]
        return direcao

    def calcular_regras(self):
        if self.estado == 'JOGANDO':
            self.calcular_regras_jogando()
        elif self.estado == 'PAUSADO':
            self.calcular_regras_pausado()
        elif self.estado == 'GAME OVER':
            self.calcular_regras_gameover()
        elif self.estado == 'VITORIA':
            self.calcular_regras_vitoria()

    def calcular_regras_vitoria(self):
        pass

    def calcular_regras_gameover(self):
        pass

    def calcular_regras_pausado(self):
        pass

    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha and \
                movivel.coluna == self.pacman.coluna:
                self.vidas -= 1
                if self.vidas <= 0:
                    self.estado = 'GAME OVER'
                else:
                    self.pacman.linha = 1
                    self.pacman.coluna = 1
            if self.pontos == 327:
                self.estado = 'VITORIA'
            else:
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and \
                        self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                        self.matriz[lin][col] = 0
                        self.pontos += 1
                    if isinstance(movivel, Pacman) and self.matriz[lin][col] == 3:
                        self.matriz[lin][col] = 0
                        self.pontos += 3
                else:
                    movivel.recusar_movimento(direcoes)

    def processar_eventos(self, evts):
        for evento in evts:
            if evento.type == pygame.QUIT:
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    if self.estado == 'JOGANDO':
                        self.estado = 'PAUSADO'
                    else:
                        self.estado = 'JOGANDO'


class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.avanco = True
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.abertura = 0
        self.velocidade_abertura = 5

    def calcular_regras(self):
        self.coluna_intencao = round(self.coluna + self.vel_x)
        self.linha_intencao = round(self.linha + self.vel_y)
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

        if self.centro_x + self.raio > 800:
            self.vel_x = self.vel_x * -1
            self.avanco = False
        if self.centro_x - self.raio < 0:
            self.vel_x = self.vel_x * -1
            self.avanco = True

        if self.centro_y + self.raio > 600:
            self.vel_y = self.vel_y * -1
        if self.centro_y - self.raio < 0:
            self.vel_y = self.vel_y * -1

    def pintar(self, tela):
        #CORPO DO PACMAN
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        self.abertura += self.velocidade_abertura
        if self.abertura > self.raio - 1:
            self.velocidade_abertura = self.velocidade_abertura * - 1
        if self.abertura < 1:
            self.velocidade_abertura = self.velocidade_abertura * - 1

        #BOCA DO PACMAN
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura)
        labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        #OLHO DO PACMAN
        olho_x = int(self.centro_x + self.raio / 10)
        olho_y = int(self.centro_y - self.raio / 1.5)
        olho_raio = int(self.raio / 7)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def pintar_esquerda(self, tela):
        #CORPO DO PACMAN
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        self.abertura += self.velocidade_abertura
        if self.abertura > self.raio - 1:
            self.velocidade_abertura = self.velocidade_abertura * - 1
        if self.abertura < 1:
            self.velocidade_abertura = self.velocidade_abertura * - 1

        #BOCA DO PACMAN
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x - self.raio, self.centro_y - self.abertura)
        labio_inferior = (self.centro_x - self.raio, self.centro_y + self.abertura)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        #OLHO DO PACMAN
        olho_x = int(self.centro_x - self.raio / 10)
        olho_y = int(self.centro_y - self.raio / 1.5)
        olho_raio = int(self.raio / 7)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    self.vel_x = VELOCIDADE
                    self.vel_y = 0
                    self.avanco = True
                if evento.key == pygame.K_LEFT:
                    self.vel_x = - VELOCIDADE
                    self.vel_y = 0
                    self.avanco = False
                if evento.key == pygame.K_DOWN:
                    self.vel_y = VELOCIDADE
                    self.vel_x = 0
                if evento.key == pygame.K_UP:
                    self.vel_y = - VELOCIDADE
                    self.vel_x = 0
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT:
                    self.vel_x = 0
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_UP:
                    self.vel_y = 0

    def processar_eventos_mouse(self, eventos):
        delay = 50
        for evento in eventos:
            if evento.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = evento.pos
                self.coluna = (mouse_x - self.centro_x) / delay
                self.linha = (mouse_y - self.centro_y) / delay

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao  = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass

class Fantasma(ElementoJogo):
    def __init__(self, cor, tamanho):
        self.coluna = 13.0
        self.linha = 15.0
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.velocidade = 1
        self.direcao = 0
        self.tamanho = tamanho
        self.cor = cor

    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho),
                    (px + fatia, py + fatia * 2),
                    (px + fatia * 2, py + fatia // 2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_externo = fatia
        olho_raio_interno = fatia // 2

        olho_esq_x = int(px + fatia * 2.5)
        olho_esq_y = int(py + fatia * 2)

        olho_dir_x = int(px + fatia * 5.5)
        olho_dir_y = int(py + fatia * 2)

        pygame.draw.circle(tela, BRANCO, (olho_esq_x, olho_esq_y), olho_raio_externo, 0)
        pygame.draw.circle(tela, BRANCO, (olho_dir_x, olho_dir_y), olho_raio_externo, 0)
        pygame.draw.circle(tela, AZUL, (olho_esq_x, olho_esq_y), olho_raio_interno, 0)
        pygame.draw.circle(tela, AZUL, (olho_dir_x, olho_dir_y), olho_raio_interno, 0)

    def calcular_regras(self):
        if self.direcao == ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == ABAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def processar_eventos(self, evts):
        pass


if __name__ == '__main__':
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Fantasma(VERMELHO, size)
    inky = Fantasma(CIANO, size)
    clyde = Fantasma(LARANJA, size)
    pinky = Fantasma(ROSA, size)
    cenario = Cenario(size, pacman)
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)


    while True:
        #CALCULAR AS REGRAS
        pacman.calcular_regras()
        blinky.calcular_regras()
        inky.calcular_regras()
        clyde.calcular_regras()
        pinky.calcular_regras()
        cenario.calcular_regras()

        #PINTAR A TELA
        screen.fill(PRETO)
        cenario.pintar(screen)
        if pacman.avanco == True:
            pacman.pintar(screen)
        if pacman.avanco == False:
            pacman.pintar_esquerda(screen)
        blinky.pintar(screen)
        inky.pintar(screen)
        clyde.pintar(screen)
        pinky.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

        #CAPTURA OS EVENTOS (COMANDOS, CLIQUES, TECLAS...)
        eventos = pygame.event.get()
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)


# (=