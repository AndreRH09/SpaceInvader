# entities.py
# Definición de clases para entidades del juego

import pygame
import random
from config import *


class Player(pygame.sprite.Sprite):
    """Representa la nave del jugador."""

    def __init__(self, image_path, start_x, start_y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed = PLAYER_SPEED

    def move_left(self):
        """Desplaza la nave hacia la izquierda."""
        if self.rect.x > 0:
            self.rect.x -= self.speed

    def move_right(self):
        """Desplaza la nave hacia la derecha."""
        if self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += self.speed

    def draw(self, surface):
        """Dibuja el jugador en la superficie."""
        surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    """Representa un enemigo."""

    def __init__(self, image_path, enemy_id, speed_x=1, speed_y=40):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(50, 150)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.id = enemy_id

    def update(self):
        """Actualiza la posición del enemigo."""
        self.rect.x += self.speed_x

        # Cambio de dirección en los bordes
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - self.rect.width:
            self.speed_x *= -1
            self.rect.y += self.speed_y

    def is_game_over(self):
        """Verifica si el enemigo ha bajado demasiado."""
        return self.rect.y > SCREEN_HEIGHT - 100

    def draw(self, surface):
        """Dibuja el enemigo en la superficie."""
        surface.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    """Representa un proyectil del jugador."""

    def __init__(self, image_path, start_x, start_y, speed=10):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = start_x + 16
        self.rect.y = start_y + 10
        self.speed = speed
        self.active = False

    def fire(self, x, y):
        """Activa el proyectil en la posición especificada."""
        self.rect.x = x + 16
        self.rect.y = y + 10
        self.active = True

    def update(self):
        """Actualiza la posición del proyectil."""
        if self.active:
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.active = False

    def is_active(self):
        """Verifica si el proyectil está activo."""
        return self.active

    def draw(self, surface):
        """Dibuja el proyectil en la superficie."""
        if self.active:
            surface.blit(self.image, self.rect)


class Bomb(pygame.sprite.Sprite):
    """Representa una bomba lanzada por enemigos."""

    def __init__(self, image_path, enemy_x, enemy_y, speed=5):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = enemy_x
        self.rect.y = enemy_y
        self.speed = speed
        self.active = True

    def update(self):
        """Actualiza la posición de la bomba."""
        if self.active:
            self.rect.y += self.speed
            if self.rect.y > SCREEN_HEIGHT:
                self.active = False

    def is_active(self):
        """Verifica si la bomba está activa."""
        return self.active

    def draw(self, surface):
        """Dibuja la bomba en la superficie."""
        if self.active:
            surface.blit(self.image, self.rect)