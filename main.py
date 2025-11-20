# I have used pygame-ce, so if you want to use it on normal pygame,
# change the anti aliased circle (pygame.draw.aacircle()) to
# normal circle (pygame.draw.circle()) in the show() of Particle class

import pygame, random, time
from pkg.core.particle import Particle
from pkg.core.config import GVar


def main():
    pygame.init()
    screen = pygame.display.set_mode((GVar.WIDTH, GVar.HEIGHT + 40))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    running = True

    particle = []
    no_of_particle = 150
    no_of_small_particles = 100

    for i in range(no_of_particle - no_of_small_particles):
        particle.append(
            Particle(
                random.randint(0, GVar.WIDTH),
                random.randint(0, GVar.HEIGHT),
                mass=random.randint(11, 20),
                width=2,
            )
        )

    for i in range(no_of_small_particles):
        particle.append(
            Particle(
                random.randint(0, GVar.WIDTH),
                random.randint(0, GVar.HEIGHT),
                mass=random.randint(2, 4),
                width=0,
                velocity=300,
            )
        )

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

        while time_accumulated > GVar.DT:
            for i in range(no_of_particle):
                particle[i].update()
                particle[i].edge_collision()

                for j in range(i + 1, no_of_particle):
                    if particle[i].collision(particle[j]):
                        no_of_collisions += 1

            time_accumulated -= GVar.DT

        alpha = time_accumulated / GVar.DT

        screen.fill((0, 0, 0))

        for p in particle:
            p.show(screen, alpha)

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
