import pygame
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
pygame.init()

n = 6

edges = ((0, 1), (0, 2), (0, 4), (7, 3), (7, 5), (7, 6),
         (2, 6), (2, 3), (5, 4), (5, 1), (4, 6), (1, 3))

surfaces = ((0, 1, 3, 2), (0, 1, 5, 4), (0, 2, 6, 4),
            (7, 3, 1, 5), (7, 3, 2, 6), (7, 6, 4, 5), )

grey = (0.5, 0.5, 0.5)
green = (0.0, 0.5, 0.0)
red = (1, 0, 0)
gold = (1, 0.84, 0)
white = (1.0, 1.0, 1.0)

border_colors = [
    (0, 1, 1),  # Cyjan
    (1, 0.6, 0),  # Orange
    (0.89, 0.13, 0.15),  # Red
    (0.1, 0.1, 1.0),  # Blue
]

data = []
for z in range(1, n+1):
    layer = []
    for x in range(1, n+1):
        row = []
        for y in range(1, n+1):
            row.append(x+y+z)
        layer.append(row)
    data.append(layer)

data = np.array(data)
# print(data)

win = pygame.display.set_mode(
    (1920, 1080), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)


class Cube:
    def __init__(self, x: int, y: int, z: int, r: int, value: int) -> None:
        self.x, self.y, self.z, self.r = x, y, z, r
        self.highlighted = False
        self.verteces = []
        self.value = value

        # Verteces in 3D
        self.verteces.append(np.matrix([x,      y,      z]))
        self.verteces.append(np.matrix([x+r,    y,      z]))
        self.verteces.append(np.matrix([x,      y-r,    z]))
        self.verteces.append(np.matrix([x+r,    y-r,    z]))

        self.verteces.append(np.matrix([x,      y,      z+r]))
        self.verteces.append(np.matrix([x+r,    y,      z+r]))
        self.verteces.append(np.matrix([x,      y-r,    z+r]))
        self.verteces.append(np.matrix([x+r,    y-r,    z+r]))

    def render(self) -> None:
        glBegin(GL_LINES)
        glColor3fv(white)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(self.verteces[vertex])
        glEnd()

    def master_render(self) -> None:
        glLineWidth(7.0)
        glBegin(GL_LINES)

        for ind, edge in enumerate(edges):
            glColor3fv(border_colors[ind % len(border_colors)])
            for vertex in edge:
                glVertex3fv(self.verteces[vertex])
        glEnd()
        glLineWidth(1.0)

    def highlight(self) -> None:
        glBegin(GL_QUADS)
        glColor3fv(green)
        for surface in surfaces:
            for vertex in surface:
                glVertex3fv(self.verteces[vertex])
        glEnd()

        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor3fv(red)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(self.verteces[vertex])
        glEnd()
        glLineWidth(1.0)

    def __repr__(self) -> str:
        return f'{self.value}'


def lines() -> None:
    glLineWidth(3.0)
    glBegin(GL_LINES)

    glColor3fv(gold)
    for vertex in line_verteces:
        glVertex3fv(vertex)

    glEnd()
    glLineWidth(1.0)


line_verteces = []
cubes = []

for z, layer in enumerate(data):
    for y, row in enumerate(layer):
        for x, value in enumerate(row):
            cubes.append(Cube(x-n/2, y+1-n/2, z-n/2, 1, value))
            line_verteces.append(cubes[-1].verteces[0])
            line_verteces.append(cubes[-1].verteces[2])
            line_verteces.append(cubes[-1].verteces[1])
            line_verteces.append(cubes[-1].verteces[3])
            line_verteces.append(cubes[-1].verteces[4])
            line_verteces.append(cubes[-1].verteces[6])
            line_verteces.append(cubes[-1].verteces[5])
            line_verteces.append(cubes[-1].verteces[7])

for x in range(3, 3*n+1):
    print(f'Dla {x=} y={len(list(filter(lambda cube: cube.value==x, cubes)))}')

shell = Cube(0-n/2, n-n/2, 0-n/2, n, -1)

highlighting = 0
clock = pygame.time.Clock()
dt = 0
pipe = False
render_cubes = False
animation = False

# Camera
gluPerspective(85, 720/480, 0.1, 50)
glTranslatef(0, 0, -1.3*n)
glRotatef(180, 1, 0, 0)
glEnable(GL_DEPTH_TEST)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            start_rotate_x, start_rotate_y = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_q:
                highlighting = 0
            elif key == pygame.K_1:
                highlighting = 11
            elif key == pygame.K_2:
                highlighting = 12
            elif key == pygame.K_3:
                highlighting = 3
            elif key == pygame.K_4:
                highlighting = 4
            elif key == pygame.K_5:
                highlighting = 5
            elif key == pygame.K_6:
                highlighting = 6
            elif key == pygame.K_7:
                highlighting = 7
            elif key == pygame.K_8:
                highlighting = 8
            elif key == pygame.K_9:
                highlighting = 9
            elif key == pygame.K_0:
                highlighting = 10
            elif key == pygame.K_SPACE:
                glLoadIdentity()
                gluPerspective(85, 720/480, 0.1, 50)
                glTranslatef(0, 0, -1.3*n)
                glRotatef(180, 1, 0, 0)
            elif key == pygame.K_BACKSLASH:
                glLoadIdentity()
                gluPerspective(85, 720/480, 0.1, 50)
                glTranslatef(0, 0, -1.3*n)
                glRotatef(270, 1, 0, 0)

            elif key == pygame.K_p:
                pipe = not pipe

            elif key == pygame.K_c:
                render_cubes = not render_cubes

            elif key == pygame.K_a:
                animation = not animation

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        glRotatef(-0.1*dt, 0, 1, 0)
    if keys[pygame.K_RIGHT]:
        glRotatef(0.1*dt, 0, 1, 0)
    if keys[pygame.K_UP]:
        glRotatef(0.1*dt, 1, 0, 0)
    if keys[pygame.K_DOWN]:
        glRotatef(-0.1*dt, 1, 0, 0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if highlighting:
        for cube in filter(lambda cube: cube.value == highlighting, cubes):
            cube.highlight()

    if pipe:
        lines()

    if render_cubes:
        for cube in cubes:
            cube.render()

    if animation:
        glRotatef(-0.03*dt, 1, 1, 1)

    shell.master_render()
    pygame.display.flip()
    dt = clock.tick(60)
    # print(clock.get_fps())
