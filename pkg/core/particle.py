# I have used pygame-ce, so if you want to use it on normal pygame,
# change the anti aliased circle (pygame.draw.aacircle()) to
# normal circle (pygame.draw.circle()) in the show() of Particle class

import random, math, pygame
from pkg.core.config import GVar


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
        self.prev_position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(1, 0).rotate_rad(
            random.uniform(0, math.tau)
        )

        if velocity is None:
            velocity = random.uniform(100, 200)  # Pixels per second

        self.velocity *= velocity
        self.acceleration = pygame.math.Vector2(0, 0)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.width = width

    def edge_collision(self):
        if self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x *= -1
        elif self.position.x > GVar.WIDTH - self.radius:
            self.position.x = GVar.WIDTH - self.radius
            self.velocity.x *= -1

        if self.position.y < self.radius:
            self.position.y = self.radius
            self.velocity.y *= -1
        elif self.position.y > GVar.HEIGHT - self.radius:
            self.position.y = GVar.HEIGHT - self.radius
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

            return True
        return False

    def update(self):
        self.prev_position = self.position.copy()
        self.position += self.velocity * GVar.DT

    def show(self, screen, alpha=1):

        interpolated_position = self.position * alpha + self.prev_position * (1 - alpha)

        pygame.draw.aacircle(
            surface=screen,
            color=self.color,
            center=interpolated_position,
            radius=self.radius,
            width=self.width,
        )
