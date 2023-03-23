import pygame
import random

# Inicializa o Pygame
pygame.init()

# Define as constantes do jogo
LARGURA_TELA = 800
ALTURA_TELA = 600
TAMANHO_BLOCO = 20
VELOCIDADE = 10

# Define as cores do jogo
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Define a fonte para o texto
fonte = pygame.font.SysFont(None, 25)

# Cria a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo da Cobrinha")

# Cria a classe Cobra
class Cobra:
    def __init__(self):
        self.tamanho = 1
        self.segmentos = [[LARGURA_TELA/2, ALTURA_TELA/2]]
        self.direcao = "direita"
    
    def desenhar(self):
        for segmento in self.segmentos:
            pygame.draw.rect(tela, VERDE, [segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO])
    
    def mover(self):
        if self.direcao == "direita":
            cabeca = [self.segmentos[0][0] + TAMANHO_BLOCO, self.segmentos[0][1]]
        elif self.direcao == "esquerda":
            cabeca = [self.segmentos[0][0] - TAMANHO_BLOCO, self.segmentos[0][1]]
        elif self.direcao == "cima":
            cabeca = [self.segmentos[0][0], self.segmentos[0][1] - TAMANHO_BLOCO]
        elif self.direcao == "baixo":
            cabeca = [self.segmentos[0][0], self.segmentos[0][1] + TAMANHO_BLOCO]
        self.segmentos.insert(0, cabeca)
        if len(self.segmentos) > self.tamanho:
            del self.segmentos[-1]
    
    def colisao(self):
        if self.segmentos[0][0] < 0 or self.segmentos[0][0] >= LARGURA_TELA or self.segmentos[0][1] < 0 or self.segmentos[0][1] >= ALTURA_TELA:
            return True
        for segmento in self.segmentos[1:]:
            if self.segmentos[0] == segmento:
                return True
        return False
    
    def crescer(self):
        self.tamanho += 1

# Cria a classe Comida
class Comida:
    def __init__(self):
        self.x = random.randrange(0, LARGURA_TELA, TAMANHO_BLOCO)
        self.y = random.randrange(0, ALTURA_TELA, TAMANHO_BLOCO)
    
    def desenhar(self):
        pygame.draw.rect(tela, VERMELHO, [self.x, self.y, TAMANHO_BLOCO, TAMANHO_BLOCO])

# Cria o objeto Cobra
cobra = Cobra()

# Cria o objeto Comida
comida = Comida()

# Define o clock para controlar
clock = pygame.time.Clock()

while True:
    # Verifica se o jogador clicou no botão de fechar a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Verifica se o jogador pressionou uma tecla
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and cobra.direcao != "esquerda":
                cobra.direcao = "direita"
            elif event.key == pygame.K_LEFT and cobra.direcao != "direita":
                cobra.direcao = "esquerda"
            elif event.key == pygame.K_UP and cobra.direcao != "baixo":
                cobra.direcao = "cima"
            elif event.key == pygame.K_DOWN and cobra.direcao != "cima":
                cobra.direcao = "baixo"
                
    # Limpa a tela
    tela.fill(BRANCO)

    # Desenha a cobra e a comida
    cobra.desenhar()
    comida.desenhar()

    # Move a cobra
    cobra.mover()

    # Verifica se a cobra colidiu com a parede ou com ela mesma
    if cobra.colisao():
        # Se a cobra colidiu, termina o jogo
        mensagem = fonte.render("Fim de jogo!", True, PRETO)
        tela.blit(mensagem, [LARGURA_TELA/2 - mensagem.get_width()/2, ALTURA_TELA/2 - mensagem.get_height()/2])
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        quit()

    # Verifica se a cobra comeu a comida
    if cobra.segmentos[0][0] == comida.x and cobra.segmentos[0][1] == comida.y:
        # Se a cobra comeu, faz ela crescer e cria uma nova comida
        cobra.crescer()
        comida = Comida()

    # Atualiza a tela
    pygame.display.update()

    # Controla o FPS do jogo
    clock.tick(VELOCIDADE)