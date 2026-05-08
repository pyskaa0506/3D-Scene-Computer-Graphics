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
STEP = 0.08
ANGLE_STEP = np.radians(1)


with open('scene.json', 'r') as scene_file:
    scene_data = json.load(scene_file)

vertices_list = scene_data['vertices']
faces = scene_data['faces']

class BSPNode:
    def __init__(self, face):
        self.face = face
        self.front = None
        self.back = None


def get_plane_equation(face, vertices):
    v0 = np.array(vertices[face['indices'][0]][:3])
    v1 = np.array(vertices[face['indices'][1]][:3])
    v2 = np.array(vertices[face['indices'][2]][:3])

    vec1 = v1 - v0
    vec2 = v2 - v0
    normal = np.cross(vec1, vec2)
    length = np.linalg.norm(normal)
    if length > 0:
        normal = normal / length
    return normal, v0

def split_face(face, normal, p0, vertices):
    front_indices = []
    back_indices = []
    indices = face['indices']

    for i in range(len(indices)):
        v1_idx = indices[i]
        v2_idx = indices[(i + 1) % len(indices)]

        v1 = np.array(vertices[v1_idx][:3])
        v2 = np.array(vertices[v2_idx][:3])

        d1 = np.dot(normal, v1 - p0)
        d2 = np.dot(normal, v2 - p0)

        if d1 >= 1e-5:
            front_indices.append(v1_idx)
        elif d1 <= -1e-5:
            back_indices.append(v1_idx)
        else:
            front_indices.append(v1_idx)
            back_indices.append(v1_idx)

    if (d1 > 1e-5 and d2 < -1e-5) or (d1 < -1e-5 and d2 > 1e-5):
        t = d1 / (d1 - d2)
        inter_p = v1 + t * (v2 - v1)
        inter_v = [inter_p[0], inter_p[1], inter_p[2], 0.1]

        vertices.append(inter_v)
        inter_idx = len(vertices) - 1

        front_indices.append(inter_idx)
        back_indices.append(inter_idx)

    front_face = {'indices': front_indices, 'color': face['color']} if len(front_indices) >= 3 else None
    back_face = {'indices': back_indices, 'color': face['color']} if len(back_indices) >= 3 else None

    return front_face, back_face

def build_bsp_tree(faces, vertices):
    if not faces:   return None

    root_face = faces[len(faces) // 2]
    node = BSPNode(root_face)

    normal, p0 = get_plane_equation(root_face, vertices)

    front_faces = []
    back_faces = []

    for face in faces:
        if face == root_face: continue

        front_count = 0
        back_count = 0

        for idx in face['indices']:
            v = np.array(vertices[idx])
            distance = np.dot(normal, v - p0)
            if distance > 1e-5: front_count += 1
            elif distance < -1e-5: back_count += 1

        if front_count > 0 and back_count == 0:
            front_faces.append(face)
        elif back_count > 0 and front_count == 0:
            back_faces.append(face)
        elif front_count == 0 and back_count == 0:
            front_faces.append(face)
        else:
            front_face, back_face = split_face(face, normal, p0, vertices)
            if front_face: front_faces.append(front_face)
            if back_face: back_faces.append(back_face)
    
    node.front = build_bsp_tree(front_faces, vertices)
    node.back = build_bsp_tree(back_faces, vertices)
    return node

bsp_root = build_bsp_tree(faces, vertices_list)
original_vertices = np.array(vertices_list, dtype=np.float32)
vertices = original_vertices.copy()

original_zoom = 500
zoom = original_zoom

def reset_scene():
    global vertices, zoom
    vertices = original_vertices.copy()
    zoom = original_zoom

def traverse_bsp(node, current_vertices, render_list):
    if node is None: return

    normal, p0 = get_plane_equation(node.face, current_vertices)

    distance = np.dot(normal, -p0)

    if distance > 0:
        traverse_bsp(node.back, current_vertices, render_list)
        render_list.append(node.face)
        traverse_bsp(node.front, current_vertices, render_list)
    else:
        traverse_bsp(node.front, current_vertices, render_list)
        render_list.append(node.face)
        traverse_bsp(node.back, current_vertices, render_list)

def draw_scene():
    screen.fill(BLACK)

    polygons_to_draw = []
    traverse_bsp(bsp_root, vertices, polygons_to_draw)

    for face in polygons_to_draw:
        indices = face['indices']
        color = face['color']
        
        face_vertices = [vertices[i] for i in indices]

        if any(v[2] < 0.1 for v in face_vertices):
            continue

        projected_points = []

        for v in face_vertices:
            z = v[2]
            x_proj = v[0] * zoom / z
            y_proj = v[1] * zoom / z

            x_resized = int(x_proj + WIDTH / 2)
            y_resized = int(-y_proj + HEIGHT / 2)

            projected_points.append((x_resized, y_resized))

        
        if len(projected_points) >= 3:
            pygame.draw.polygon(screen, color, projected_points)
            pygame.draw.polygon(screen, LIME, projected_points, 1)
    pygame.display.flip()
    

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

