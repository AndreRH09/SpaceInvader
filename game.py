# game.py
# Gestor principal del juego Space Invaders

import pygame
import random
from config import *
from entities import Player, Enemy, Bullet, Bomb
from physics import CollisionDetector, DifficultyManager
from audio_manager import AudioManager
from renderer import Renderer


class Game:
    """Clase principal que gestiona la lógica y flujo del juego."""

    def __init__(self):
        """Inicializa el juego."""
        pygame.init()

        # Inicializar sistemas
        self.renderer = Renderer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.renderer.set_icon(IMAGE_ICON)
        self.audio_manager = AudioManager()
        self.audio_manager.load_audio()
        self.audio_manager.play_background_music()

        # Inicializar reloj
        self.clock = pygame.time.Clock()

        # Estado del juego
        self.running = True
        self.game_over = False
        self.score = 0
        self.lives = 3

        # Inicializar entidades
        self.player = Player(IMAGE_PLAYER, PLAYER_START_X, PLAYER_START_Y)
        self.bullet = Bullet(IMAGE_BULLET, self.player.rect.x, PLAYER_START_Y)
        self.enemies = []
        self.bombs = []

        # Inicializar enemigos
        for i in range(INITIAL_ENEMIES):
            enemy = Enemy(
                IMAGE_ENEMY,
                i,
                speed_x=INITIAL_ENEMY_SPEED,
                speed_y=INITIAL_ENEMY_Y_DROP
            )
            self.enemies.append(enemy)

        # Gestor de dificultad
        self.difficulty_manager = DifficultyManager(
            progression_interval=PROGRESSION_SCORE_INTERVAL,
            enemy_speed_increment=ENEMY_SPEED_INCREMENT,
            enemy_drop_increment=ENEMY_DROP_INCREMENT,
            bullet_speed_increment=BULLET_SPEED_INCREMENT,
            new_enemy_threshold=NEW_ENEMY_THRESHOLD,
            max_enemies=MAX_ENEMIES
        )

        # Teclas presionadas
        self.keys_pressed = {'left': False, 'right': False}

    def handle_events(self):
        """Gestiona los eventos del juego."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_over = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.keys_pressed['left'] = True
                elif event.key == pygame.K_RIGHT:
                    self.keys_pressed['right'] = True
                elif event.key == pygame.K_SPACE:
                    if not self.game_over:
                        if not self.bullet.is_active():
                            self.bullet.fire(self.player.rect.x, PLAYER_START_Y)
                            self.audio_manager.play_laser_sound()
                    else:
                        # Reiniciar juego
                        self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.game_over = False
                elif event.key == pygame.K_m:
                    self.audio_manager.toggle_mute()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.keys_pressed['left'] = False
                elif event.key == pygame.K_RIGHT:
                    self.keys_pressed['right'] = False

    def update(self):
        """Actualiza la lógica del juego."""
        if self.game_over:
            return

        # Movimiento del jugador
        if self.keys_pressed['left']:
            self.player.move_left()
        if self.keys_pressed['right']:
            self.player.move_right()

        # Actualizar proyectil
        self.bullet.update()

        # Actualizar enemigos
        for enemy in self.enemies:
            enemy.update()

            # Verificar si el juego termina (enemigo alcanzó el fondo)
            if enemy.is_game_over():
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    # Reiniciar posición de enemigos
                    for e in self.enemies:
                        e.rect.y = random.randint(50, 150)

        # Detección de colisión: proyectil vs enemigo
        collided_enemy_idx = CollisionDetector.check_bullet_enemy_collision(
            self.bullet,
            self.enemies
        )

        if collided_enemy_idx >= 0:
            self.audio_manager.play_explosion_sound()
            self.score += 1
            self.bullet.active = False

            # Reiniciar enemigo colisionado
            enemy = self.enemies[collided_enemy_idx]
            enemy.rect.x = random.randint(0, SCREEN_WIDTH - enemy.rect.width)
            enemy.rect.y = random.randint(50, 150)

        # Enemigos lanzan bombas ocasionalmente
        for enemy in self.enemies:
            if random.random() < BOMB_SPAWN_CHANCE:
                bomb = Bomb(
                    IMAGE_BOMB,
                    enemy.rect.centerx,
                    enemy.rect.y + 50,
                    speed=BOMB_SPEED
                )
                self.bombs.append(bomb)

        # Actualizar bombas
        for bomb in self.bombs[:]:
            bomb.update()

            if not bomb.is_active():
                self.bombs.remove(bomb)
                continue

            # Detección de colisión: bomba vs jugador
            if CollisionDetector.check_bomb_player_collision(bomb, self.player):
                self.audio_manager.play_bomb_sound()
                self.lives -= 1
                bomb.active = False

                if self.lives <= 0:
                    self.game_over = True

        # Actualizar dificultad
        if self.difficulty_manager.update(self.score, self.enemies, self.bullet):
            # Agregar nuevo enemigo si se cumple el umbral
            if self.score % NEW_ENEMY_THRESHOLD == 0 and len(self.enemies) < MAX_ENEMIES:
                enemy = Enemy(
                    IMAGE_ENEMY,
                    len(self.enemies),
                    speed_x=INITIAL_ENEMY_SPEED * (1 + self.score // 20),
                    speed_y=INITIAL_ENEMY_Y_DROP + (self.score // 20 * ENEMY_DROP_INCREMENT)
                )
                self.enemies.append(enemy)

    def render(self):
        """Renderiza todos los elementos visuales."""
        self.renderer.clear_screen()

        # Dibujar entidades
        self.player.draw(self.renderer.screen)
        self.bullet.draw(self.renderer.screen)

        for enemy in self.enemies:
            enemy.draw(self.renderer.screen)

        for bomb in self.bombs:
            bomb.draw(self.renderer.screen)

        # Dibujar UI
        self.renderer.render_score(self.score)
        self.renderer.render_level(self.difficulty_manager.current_level)
        self.renderer.render_lives(self.lives)

        # Dibujar pantalla de fin de juego si es necesario
        if self.game_over:
            self.renderer.render_game_over(
                self.score,
                self.difficulty_manager.current_level
            )

        self.renderer.update_display()

    def restart_game(self):
        """Reinicia el juego."""
        self.__init__()

    def run(self):
        """Loop principal del juego."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        self.audio_manager.stop_background_music()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()