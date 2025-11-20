from pkg.core.quad_tree import *
import pygame

pygame.init()


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


def draw_points(screen, points):
    for x, y in points:
        pygame.draw.circle(screen, (200, 0, 0), (x, y), 2)


def visualize(qt):
    FPS = 60
    screen = pygame.display.set_mode((qt.cell.width, qt.cell.height))
    pygame.display.set_caption("Quad Tree Visualization")
    running = True
    clock = pygame.time.Clock()
    cooldown = 100
    last_clicked = 0
    points = qt.get_points()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = pygame.time.get_ticks()

        pressed, _, _ = pygame.mouse.get_pressed()
        if pressed and now - last_clicked >= cooldown:
            last_clicked = now
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


if __name__ == "__main__":
    visualize(QuadTree(Cell(0, 0, 512, 512), 4))
