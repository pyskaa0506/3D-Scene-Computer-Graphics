import pygame
import numpy as np
import sys
import json


pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kamera 3D")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIME = (0, 255, 0)
STEP = 0.1
ANGLE_STEP = np.radians(1)


with open('scene.json', 'r') as scene_file:
    scene_data = json.load(scene_file)

vertices = np.array(scene_data['vertices'], dtype=np.float32)
faces = scene_data['faces']

original_vertices = vertices.copy()
original_zoom = 500
zoom = original_zoom

def reset_scene():
    global vertices, zoom
    vertices = original_vertices.copy()
    zoom = original_zoom

def draw_scene():
    screen.fill(BLACK)

    polygons_to_draw = []

    for face in faces:
        indices = face['indices']
        color = face['color']
        
        face_vertices = [vertices[i] for i in indices]

        if any(v[2] < 0.1 for v in face_vertices):
            continue

        projected_points = []
        max_z = max(v[2] for v in face_vertices)

        for v in face_vertices:
            z = v[2]
            print(z)
            x_proj = v[0] * zoom / z
            y_proj = v[1] * zoom / z

            x_resized = int(x_proj + WIDTH / 2)
            y_resized = int(-y_proj + HEIGHT / 2)

            projected_points.append((x_resized, y_resized))


        one_face = {
        "points": projected_points,
        "color": color,
        "max_z": max_z,
        "original_vertices": face_vertices
        }
        polygons_to_draw.append(one_face)

    polygons_to_draw.sort(key=lambda p: p['max_z'], reverse=True)

    for polygon in polygons_to_draw:
        pygame.draw.polygon(screen, polygon['color'], polygon['points'])
        pygame.draw.polygon(screen, LIME, polygon['points'], 1)
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


clock = pygame.time.Clock()

running = True
draw_scene()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_scene()
            draw_scene()

    keys = pygame.key.get_pressed()
    needs_redraw = False

            # Moving around
    if keys[pygame.K_LEFT]:
        translate_scene(STEP, 0, 0)
        needs_redraw = True

    if keys[pygame.K_RIGHT]:
        translate_scene(-STEP, 0, 0)
        needs_redraw = True

    if keys[pygame.K_UP]:
        translate_scene(0, 0, -STEP)
        needs_redraw = True

    if keys[pygame.K_DOWN]:
        translate_scene(0, 0, STEP)
        needs_redraw = True

    if keys[pygame.K_RIGHT]:
        translate_scene(-STEP, 0, 0)
        needs_redraw = True

    if keys[pygame.K_UP]:
        translate_scene(0, 0, -STEP)
        needs_redraw = True

    if keys[pygame.K_DOWN]:
        translate_scene(0, 0, STEP)
        needs_redraw = True

    if keys[pygame.K_SPACE]:
        translate_scene(0, -STEP, 0)
        needs_redraw = True

    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        translate_scene(0, STEP, 0)
        needs_redraw = True

            # --------
            # Rotation
    if keys[pygame.K_a]:
        rotate_scene('y', ANGLE_STEP)
        needs_redraw = True

    if keys[pygame.K_d]:
        rotate_scene('y', -ANGLE_STEP)
        needs_redraw = True

    if keys[pygame.K_w]:
        rotate_scene('x', ANGLE_STEP)
        needs_redraw = True

    if keys[pygame.K_s]:
        rotate_scene('x', -ANGLE_STEP)
        needs_redraw = True

    if keys[pygame.K_q]:
        rotate_scene('z', ANGLE_STEP)
        needs_redraw = True

    if keys[pygame.K_e]:
        rotate_scene('z', -ANGLE_STEP)
        needs_redraw = True

            # --------
            # Zoom
    if keys[pygame.K_EQUALS]:
        zoom += 20
        needs_redraw = True

    if keys[pygame.K_MINUS]:
        zoom -= 20
        needs_redraw = True
    
    if needs_redraw: draw_scene()
    clock.tick(60)
        

pygame.quit()
sys.exit()

