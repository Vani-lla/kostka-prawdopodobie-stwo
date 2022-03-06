from cgi import print_arguments
import pygame
import numpy as np

n = 3
projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 1],
])

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

win = pygame.display.set_mode((720, 480), pygame.FULLSCREEN)


class Cube:
    def __init__(self, x: int, y: int, z: int, r: int, color: tuple) -> None:
        self.x, self.y, self.z, self.r = x, y, z, r
        self.color = color
        self.points = []

        # Points in 3D
        self.points.append(np.matrix([x, y, z]))
        self.points.append(np.matrix([x+r, y, z]))
        self.points.append(np.matrix([x+r, y-r, z]))
        self.points.append(np.matrix([x, y-r, z]))

        self.points.append(np.matrix([x, y, z+r]))
        self.points.append(np.matrix([x+r, y, z+r]))
        self.points.append(np.matrix([x+r, y-r, z+r]))
        self.points.append(np.matrix([x, y-r, z+r]))

        self.points.reverse()

        for point in self.points:
            print(point)

    def render(self) -> list:
        for point in self.points:
            projected = np.dot(projection_matrix, point.reshape(3, 1))
            x = int(projected[0][0])
            y = int(projected[1][0])
            # print(x)
            # print(y)
            # print()

            pygame.draw.circle(win, (255, 255, 255), (x, y), 1)


cube = Cube(100, 100, 100, 50, (255, 255, 255))
win.fill((0, 0, 0))
cube.render()
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
