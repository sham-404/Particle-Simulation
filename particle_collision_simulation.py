import pygame, random, math

WIDTH = 1200
HEIGHT = 600
FPS = 30


class Particle:
    def __init__(
        self, x, y, mass=None, radius=None, velocity=None, color=None, width=2
    ):
        if mass is None:
            mass = random.uniform(1, 10)

        if radius is None:
            radius = int(math.sqrt(mass) * 5)

        if color is None:
            color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255),
            )

        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(1, 0).rotate_rad(
            random.uniform(0, math.tau)
        )

        if velocity is None:
            velocity = random.uniform(2, 6)

        self.velocity *= velocity
        self.acceleration = pygame.math.Vector2(0, 0)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.width = width

    def edge_collision(self, screen):
        width = screen.get_width()
        height = screen.get_height()

        if self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x *= -1
        elif self.position.x > width - self.radius:
            self.position.x = width - self.radius
            self.velocity.x *= -1

        if self.position.y < self.radius:
            self.position.y = self.radius
            self.velocity.y *= -1
        elif self.position.y > height - self.radius:
            self.position.y = height - self.radius
            self.velocity.y *= -1

    def collision(self, other):
        impact = self.position - other.position
        dist = impact.length()

        if impact.length() <= self.radius + other.radius:
            overlap = (self.radius + other.radius) - dist
            correction = impact.normalize() * (overlap / 2)
            self.position += correction
            other.position -= correction

            den = impact.length_squared() * (self.mass + other.mass)
            num = (other.velocity - self.velocity).dot(impact) * impact

            self.velocity += (2 * other.mass) * num / den
            other.velocity += (2 * self.mass) * -num / den

    def update(self):
        self.position += self.velocity

    def show(self, screen):
        pygame.draw.circle(
            surface=screen,
            color=self.color,
            center=self.position,
            radius=self.radius,
            width=self.width,
        )


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    particle = []
    no_of_particle = 99

    for i in range(no_of_particle - 33):
        particle.append(
            Particle(
                random.uniform(0, WIDTH),
                random.uniform(0, HEIGHT),
                mass=random.randint(11, 25),
                width=2,
            )
        )

    for i in range(no_of_particle - 33):
        particle.append(
            Particle(
                random.uniform(0, WIDTH),
                random.uniform(0, HEIGHT),
                mass=random.randint(2, 4),
                width=0,
            )
        )

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for i in range(no_of_particle):
            particle[i].show(screen)
            particle[i].update()
            particle[i].edge_collision(screen)

            for j in range(i + 1, no_of_particle):
                particle[i].collision(particle[j])

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
