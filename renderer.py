# renderer.py
# Sistema de renderización y gestión de interfaz gráfica

import pygame
from config import *


class Renderer:
    """Gestiona la renderización de todos los elementos visuales del juego."""

    def __init__(self, screen_width, screen_height):
        """Inicializa el renderer."""
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.display.set_caption("Space Invaders - Versión Mejorada")

        # Cargar fondo
        try:
            self.background = pygame.image.load(IMAGE_BACKGROUND)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar fondo: {e}")
            self.background = None

        # Configurar fuentes
        self.font_main = pygame.font.Font('freesansbold.ttf', FONT_MAIN_SIZE)
        self.font_gameover = pygame.font.Font('freesansbold.ttf', FONT_GAMEOVER_SIZE)
        self.font_small = pygame.font.Font('freesansbold.ttf', 20)

    def clear_screen(self):
        """Limpia la pantalla."""
        self.screen.fill(COLOR_BLACK)

        # Dibujar fondo si está disponible
        if self.background:
            self.screen.blit(self.background, (0, 0))

    def render_score(self, score, x=10, y=10):
        """Renderiza el texto de puntuación."""
        score_text = self.font_main.render(
            f"Score: {score}",
            True,
            COLOR_GREEN
        )
        self.screen.blit(score_text, (x, y))

    def render_level(self, level, x=600, y=10):
        """Renderiza el nivel actual."""
        level_text = self.font_small.render(
            f"Level: {level}",
            True,
            COLOR_GREEN
        )
        self.screen.blit(level_text, (x, y))

    def render_lives(self, lives, x=10, y=50):
        """Renderiza el número de vidas."""
        lives_text = self.font_small.render(
            f"Lives: {lives}",
            True,
            COLOR_RED
        )
        self.screen.blit(lives_text, (x, y))

    def render_game_over(self, score, level):
        """Renderiza la pantalla de fin de juego."""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))

        # Texto de fin de juego
        gameover_text = self.font_gameover.render(
            "GAME OVER",
            True,
            COLOR_RED
        )
        gameover_rect = gameover_text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 60)
        )
        self.screen.blit(gameover_text, gameover_rect)

        # Puntuación final
        final_score_text = self.font_main.render(
            f"Final Score: {score}",
            True,
            COLOR_GREEN
        )
        final_score_rect = final_score_text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 20)
        )
        self.screen.blit(final_score_text, final_score_rect)

        # Nivel alcanzado
        final_level_text = self.font_main.render(
            f"Level Reached: {level}",
            True,
            COLOR_GREEN
        )
        final_level_rect = final_level_text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 70)
        )
        self.screen.blit(final_level_text, final_level_rect)

        # Instrucciones
        restart_text = self.font_small.render(
            "Press SPACE to restart or ESC to exit",
            True,
            COLOR_WHITE
        )
        restart_rect = restart_text.get_rect(
            center=(self.screen_width // 2, self.screen_height - 50)
        )
        self.screen.blit(restart_text, restart_rect)

    def update_display(self):
        """Actualiza la pantalla."""
        pygame.display.update()

    def set_icon(self, icon_path):
        """Establece el icono de la ventana."""
        try:
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar icono: {e}")