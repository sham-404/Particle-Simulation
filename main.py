# I have used pygame-ce, so if you want to use it on normal pygame,
# change the anti aliased circle (pygame.draw.aacircle()) to
# normal circle (pygame.draw.circle()) in the show() of Particle class
# which is located in pkg/core/particle.py

import pygame, random, time
from pkg.core.particle import Particle
from pkg.core.config import GVar
from pkg.core.quad_tree import *
from pkg.utils.visual_qt import draw_qt


def main():
    pygame.init()
    screen = pygame.display.set_mode((GVar.WIDTH, GVar.HEIGHT + 40))
    pygame.display.set_caption("Elastic Collision Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    running = True

    particle = []
    no_of_big_particle = 50
    no_of_small_particles = 125

    for i in range(no_of_big_particle):
        particle.append(
            Point(
                obj=Particle(
                    random.randint(0, GVar.WIDTH),
                    random.randint(0, GVar.HEIGHT),
                    mass=random.randint(11, 20),
                    width=2,
                )
            )
        )

    for i in range(no_of_small_particles):
        particle.append(
            Point(
                obj=Particle(
                    random.randint(0, GVar.WIDTH),
                    random.randint(0, GVar.HEIGHT),
                    mass=random.randint(2, 4),
                    width=0,
                    velocity=300,
                )
            )
        )

    qt = QuadTree(Cell(0, 0, GVar.WIDTH, GVar.HEIGHT), 4)
    check_cell = Cell(0, 0, 40, 40)

    no_of_collisions = 0
    time_accumulated = 0
    current_time = time.perf_counter()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        new_time = time.perf_counter()
        frame_time = new_time - current_time
        current_time = new_time

        # Accounting for lag
        if frame_time > 0.1:  # Max lag allowed in 100ms
            frame_time = 0.1

        time_accumulated += frame_time

        # Updating only once in dt (dt = 1 / FPS) regardless of system speed
        # ie, running at a constant FPS regardless of external factors
        # for accurate physics rendering
        while time_accumulated > GVar.DT:
            for p in particle:
                p.data.update()
                p.data.edge_collision()

                print(qt.items_in(check_cell))

                for near_point in qt.items_in(check_cell):
                    if p.data.collision(near_point.data):
                        no_of_collisions += 1

            time_accumulated -= GVar.DT
            for p in particle:
                qt.insert(p)

        alpha = time_accumulated / GVar.DT  # To find interpolated position

        screen.fill((0, 0, 0))

        for p in particle:
            p.data.show(screen, alpha)

        pygame.draw.aaline(
            screen,
            (50, 50, 50),
            (0, GVar.HEIGHT + 1),
            (GVar.WIDTH + 1, GVar.HEIGHT + 1),
            3,
        )

        text = font.render(
            f"Total no of collisions: {no_of_collisions}",
            True,
            (225, 225, 225),
        )
        screen.blit(text, (20, GVar.HEIGHT + 7))

        text = font.render(
            f"FPS: {clock.get_fps(): .3f}",
            True,
            (225, 225, 225),
        )
        screen.blit(text, (GVar.WIDTH - 150, GVar.HEIGHT + 7))

        pygame.display.update()
        clock.tick()

    pygame.quit()


if __name__ == "__main__":
    main()
