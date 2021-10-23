import pygame
from board import Board


class window:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 800))
        screen.fill((0,191,255))
        pygame.display.set_caption("Catan")
        board = Board(screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            pygame.display.update()

if __name__ == '__main__':
    game = window()