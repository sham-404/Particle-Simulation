# I have used pygame-ce, so if you want to use it on normal pygame,
# change the anti aliased circle (pygame.draw.aacircle()) to
# normal circle (pygame.draw.circle()) in the show() of Particle class

import pygame, random
from particle import Particle, GVar


def main():
    pygame.init()
    screen = pygame.display.set_mode((GVar.WIDTH, GVar.HEIGHT + 40))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    running = True

    particle = []
    no_of_particle = 150

    for i in range(no_of_particle - 75):
        particle.append(
            Particle(
                random.randint(0, GVar.WIDTH),
                random.randint(0, GVar.HEIGHT),
                mass=random.randint(11, 20),
                width=2,
            )
        )

    for i in range(75):
        particle.append(
            Particle(
                random.randint(0, GVar.WIDTH),
                random.randint(0, GVar.HEIGHT),
                mass=random.randint(2, 4),
                width=0,
                velocity=6,
            )
        )

    no_of_collisions = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for i in range(no_of_particle):
            particle[i].show(screen)
            particle[i].update()
            particle[i].edge_collision()

            for j in range(i + 1, no_of_particle):
                if particle[i].collision(particle[j]):
                    no_of_collisions += 1

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

        pygame.display.update()
        clock.tick(GVar.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
