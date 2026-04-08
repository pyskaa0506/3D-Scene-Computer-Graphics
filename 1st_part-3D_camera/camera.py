import pygame
import numpy as np
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kamera 3D")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_scene():
    screen.fill(BLACK)

    pygame.draw.line(screen, WHITE, (400,300), (500, 400), 2)
    pygame.display.flip()

draw_scene()

running = True
while running:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pygame.KEYDOWN:

            # Moving around
            if event.key == pygame.K_LEFT:
                print("Left key pressed")
                draw_scene()

            if event.key == pygame.K_RIGHT:
                
                draw_scene()

            if event.key == pygame.K_UP:

                draw_scene()

            if event.key == pygame.K_DOWN:

                draw_scene()

            if event.key == pygame.K_SPACE:

                draw_scene()

            if event.key == pygame.K_LSHIFT:

                draw_scene()

            # --------
            # Rotation
            if event.key == pygame.K_a:

                draw_scene()

            if event.key == pygame.K_d:
                draw_scene()

            if event.key == pygame.K_w:

                draw_scene()

            if event.key == pygame.K_s:

                draw_scene()

            if event.key == pygame.K_q:
                
                draw_scene()

            if event.key == pygame.K_e:

                draw_scene()

            # --------
            # Zoom
            if event.key == pygame.K_EQUALS:

                draw_scene()

            if event.key == pygame.K_MINUS:

                draw_scene()
        

pygame.quit()
sys.exit()