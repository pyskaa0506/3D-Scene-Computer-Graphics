import pygame
import numpy as np
import sys
import json

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kamera 3D")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIME = (0, 255, 0)

zoom = 400

with open('scene.json', 'r') as scene_file:
    scene_data = json.load(scene_file)

vertices = np.array(scene_data['vertices'], dtype=np.float32)
edges = scene_data['edges']


def draw_scene():
    screen.fill(BLACK)

    for edge in edges:
        v1 = vertices[edge[0]]
        v2 = vertices[edge[1]]

        z1 = v1[2] if v1[2] != 0 else 0.0001
        z2 = v2[2] if v2[2] != 0 else 0.0001

        x1_proj = v1[0] * zoom / z1
        y1_proj = v1[1] * zoom / z1

        x2_proj = v2[0] * zoom / z2
        y2_proj = v2[1] * zoom / z2

        x1_resized = int(x1_proj + WIDTH / 2)
        y1_resized = int(-y1_proj + HEIGHT / 2)
        x2_resized = int(x2_proj + WIDTH / 2)
        y2_resized = int(-y2_proj + HEIGHT / 2)

        pygame.draw.line(screen, LIME, (x1_resized, y1_resized), (x2_resized, y2_resized), 2)
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