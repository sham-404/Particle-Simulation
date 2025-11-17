from random import randint
from quad_tree import *
import pygame 
pygame.init()

W = 600
H = 600
FPS = 60
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Quad Tree Visualization")
running = True
clock = pygame.time.Clock()
qt = QuadTree(Cell(0, 0, W, H), 4)
points = []

def draw_qt(screen, qt):
    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(qt.cell.x, qt.cell.y, qt.cell.width, qt.cell.height), 1)

    for child in (qt.nw, qt.ne, qt.sw, qt.se):
        if child is not None:
            draw_qt(screen, child)

def draw_points(screen, points):
    for x, y in points:
        pygame.draw.circle(screen, (200, 0, 0), (x, y), 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed, _, _ = pygame.mouse.get_pressed()
    if pressed:
        x, y = pygame.mouse.get_pos()
        qt.insert(Circle(x, y))
        points.append((x, y))

    screen.fill((10, 10, 10))

    if points:
        draw_points(screen, points)

    draw_qt(screen, qt)
    clock.tick(FPS)
    pygame.display.flip()


pygame.quit()
