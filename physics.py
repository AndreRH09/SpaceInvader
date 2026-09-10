# physics.py
# Sistema de detección de colisiones y física del juego

import math


class CollisionDetector:
    """Gestiona la detección de colisiones entre entidades."""

    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        """Calcula la distancia euclidiana entre dos puntos."""
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def check_bullet_enemy_collision(bullet, enemies, collision_radius=27):
        """
        Verifica colisión entre un proyectil y enemigos.
        Retorna el índice del enemigo colisionado o -1 si no hay colisión.
        """
        if not bullet.is_active():
            return -1

        bullet_center_x = bullet.rect.centerx
        bullet_center_y = bullet.rect.centery

        for idx, enemy in enumerate(enemies):
            enemy_center_x = enemy.rect.centerx
            enemy_center_y = enemy.rect.centery

            distance = CollisionDetector.calculate_distance(
                bullet_center_x,
                bullet_center_y,
                enemy_center_x,
                enemy_center_y
            )

            if distance < collision_radius:
                return idx

        return -1

    @staticmethod
    def check_bomb_player_collision(bomb, player, collision_radius=30):
        """
        Verifica colisión entre una bomba y el jugador.
        Retorna True si hay colisión.
        """
        if not bomb.is_active():
            return False

        bomb_center_x = bomb.rect.centerx
        bomb_center_y = bomb.rect.centery
        player_center_x = player.rect.centerx
        player_center_y = player.rect.centery

        distance = CollisionDetector.calculate_distance(
            bomb_center_x,
            bomb_center_y,
            player_center_x,
            player_center_y
        )

        return distance < collision_radius

    @staticmethod
    def check_rect_collision(rect1, rect2):
        """Verifica colisión de rectángulos (AABB - Axis-Aligned Bounding Box)."""
        return rect1.colliderect(rect2)


class DifficultyManager:
    """Gestiona la progresión y dificultad del juego."""

    def __init__(self, progression_interval, enemy_speed_increment,
                 enemy_drop_increment, bullet_speed_increment,
                 new_enemy_threshold, max_enemies):
        self.progression_interval = progression_interval
        self.enemy_speed_increment = enemy_speed_increment
        self.enemy_drop_increment = enemy_drop_increment
        self.bullet_speed_increment = bullet_speed_increment
        self.new_enemy_threshold = new_enemy_threshold
        self.max_enemies = max_enemies

        self.current_level = 0
        self.last_progression_score = 0
        self.last_enemy_add_score = 0

    def update(self, current_score, enemies, bullet):
        """
        Actualiza la dificultad basado en la puntuación.
        Retorna True si hubo cambios.
        """
        changed = False

        # Incrementar velocidad de enemigos y proyectil
        if current_score - self.last_progression_score >= self.progression_interval:
            self._increase_difficulty(enemies, bullet)
            self.last_progression_score = current_score
            self.current_level += 1
            changed = True

        # Agregar nuevo enemigo
        if (current_score - self.last_enemy_add_score >= self.new_enemy_threshold
                and len(enemies) < self.max_enemies):
            self.last_enemy_add_score = current_score
            changed = True

        return changed

    def _increase_difficulty(self, enemies, bullet):
        """Incrementa la dificultad del juego."""
        for enemy in enemies:
            # Aumentar velocidad de movimiento horizontal
            if enemy.speed_x > 0:
                enemy.speed_x += self.enemy_speed_increment
            else:
                enemy.speed_x -= self.enemy_speed_increment

            # Aumentar velocidad de descenso
            enemy.speed_y += self.enemy_drop_increment

        # Aumentar velocidad del proyectil
        bullet.speed += self.bullet_speed_increment

    def get_level_info(self):
        """Retorna información del nivel actual."""
        return {
            'level': self.current_level,
            'speed_multiplier': 1 + (self.current_level * 0.2)
        }