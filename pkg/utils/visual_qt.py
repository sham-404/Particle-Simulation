from pkg.core.quad_tree import QuadTree
from pkg.core.quad_tree import *
import pygame

pygame.init()


def draw_cell(screen, cell):
    pygame.draw.rect(
        screen, (0, 0, 225), pygame.Rect(cell.x, cell.y, cell.width, cell.height), 1
    )


def draw_qt(screen, qt):
    """
    pygame.draw.rect(
        screen,
        (200, 200, 200),
        pygame.Rect(qt.cell.x, qt.cell.y, qt.cell.width, qt.cell.height),
        1,
    )

    """

    if qt.divided:
        pygame.draw.line(
            screen,
            (200, 200, 200),
            (qt.cell.x + qt.cell.width / 2, qt.cell.y),
            (qt.cell.x + qt.cell.width / 2, qt.cell.y + qt.cell.height),
        )

        pygame.draw.line(
            screen,
            (200, 200, 200),
            (qt.cell.x, qt.cell.y + qt.cell.height / 2),
            (qt.cell.x + qt.cell.width, qt.cell.y + qt.cell.height / 2),
        )

    for child in (qt.nw, qt.ne, qt.sw, qt.se):
        if child is not None:
            draw_qt(screen, child)


def draw_points(screen, points, size=2, color=(200, 0, 0)):
    for x, y in points:
        pygame.draw.circle(screen, color, (x, y), size)


def visualize(qt):
    FPS = 60
    screen = pygame.display.set_mode((qt.cell.width, qt.cell.height))
    pygame.display.set_caption("Quad Tree Visualization")
    running = True
    clock = pygame.time.Clock()
    cooldown = 100
    last_clicked = 0
    points = qt.get_points()
    check_cell = Cell(40, 200, 80, 80)
    points_in_cell = qt.items_in(check_cell)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = pygame.time.get_ticks()

        pressed_l, _, pressed_r = pygame.mouse.get_pressed()
        if pressed_l and now - last_clicked >= cooldown:
            last_clicked = now
            x, y = pygame.mouse.get_pos()
            qt.insert(Point(x, y))
            points.append((x, y))

        elif pressed_r and now - last_clicked >= cooldown:
            x, y = pygame.mouse.get_pos()
            check_cell.x = x
            check_cell.y = y
            points_in_cell = [(c.x, c.y) for c in qt.items_in(check_cell)]

        screen.fill((10, 10, 10))

        if points:
            draw_points(screen, points)

        if points_in_cell:
            draw_points(screen, points_in_cell, 5, (0, 200, 0))

        draw_cell(screen, check_cell)
        draw_qt(screen, qt)
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    visualize(QuadTree(Cell(0, 0, 512, 512), 4))
