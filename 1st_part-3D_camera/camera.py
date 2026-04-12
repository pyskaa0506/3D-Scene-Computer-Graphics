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
STEP = 0.1
ANGLE_STEP = np.radians(5)

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

        if v1[2] < 0.1 or v2[2] < 0.1:
            continue

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

        try:
            pygame.draw.line(screen, LIME, (x1_resized, y1_resized), (x2_resized, y2_resized), 2)
        except TypeError:
            pass
    pygame.display.flip()
draw_scene()

def translate_scene(dx, dy, dz):
    global vertices
    translation_matrix = np.array([[1, 0, 0, dx],
                                    [0, 1, 0, dy],
                                    [0, 0, 1, dz],
                                    [0, 0, 0, 1]], dtype=np.float32)
    vertices = np.dot(vertices, translation_matrix.T)

def rotate_scene(axis, angle):
    global vertices
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)

    if axis == 'x':
        rotation_matrix = np.array([[1, 0, 0, 0],
                                    [0, cos_angle, -sin_angle, 0],
                                    [0, sin_angle, cos_angle, 0],
                                    [0, 0, 0, 1]], dtype=np.float32)
    elif axis == 'y':
        rotation_matrix = np.array([[cos_angle, 0, sin_angle, 0],
                                    [0, 1, 0, 0],
                                    [-sin_angle, 0, cos_angle, 0],
                                    [0, 0, 0, 1]], dtype=np.float32)
    elif axis == 'z':
        rotation_matrix = np.array([[cos_angle, -sin_angle, 0, 0],
                                    [sin_angle, cos_angle, 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], dtype=np.float32)
    vertices = np.dot(vertices, rotation_matrix.T)

running = True
while running:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pygame.KEYDOWN:

            # Moving around
            if event.key == pygame.K_LEFT:
                translate_scene(STEP, 0, 0)
                draw_scene()

            if event.key == pygame.K_RIGHT:
                translate_scene(-STEP, 0, 0)
                draw_scene()

            if event.key == pygame.K_UP:
                translate_scene(0, 0, -STEP)
                draw_scene()

            if event.key == pygame.K_DOWN:
                translate_scene(0, 0, STEP)
                draw_scene()

            if event.key == pygame.K_SPACE:
                translate_scene(0, -STEP, 0)
                draw_scene()

            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                translate_scene(0, STEP, 0)
                draw_scene()

            # --------
            # Rotation
            if event.key == pygame.K_a:
                rotate_scene('y', ANGLE_STEP)
                draw_scene()

            if event.key == pygame.K_d:
                rotate_scene('y', -ANGLE_STEP)
                draw_scene()

            if event.key == pygame.K_w:
                rotate_scene('x', ANGLE_STEP)
                draw_scene()

            if event.key == pygame.K_s:
                rotate_scene('x', -ANGLE_STEP)
                draw_scene()

            if event.key == pygame.K_q:
                rotate_scene('z', ANGLE_STEP)
                draw_scene()

            if event.key == pygame.K_e:
                rotate_scene('z', -ANGLE_STEP)
                draw_scene()

            # --------
            # Zoom
            if event.key == pygame.K_EQUALS:
                zoom += 20
                draw_scene()

            if event.key == pygame.K_MINUS:
                zoom -= 20
                draw_scene()
        

pygame.quit()
sys.exit()

