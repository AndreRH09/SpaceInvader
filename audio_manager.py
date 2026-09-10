# audio_manager.py
# Gestor centralizado de audio y efectos de sonido

from pygame import mixer
from config import *


class AudioManager:
    """Gestiona la reproducción de audio y efectos de sonido."""

    def __init__(self):
        """Inicializa el gestor de audio."""
        mixer.init()
        self.background_music = None
        self.sfx_laser = None
        self.sfx_explosion = None
        self.sfx_bomb = None
        self.is_muted = False

    def load_audio(self):
        """Carga todos los archivos de audio."""
        try:
            self.background_music = mixer.Sound(AUDIO_BACKGROUND)
            self.sfx_laser = mixer.Sound(AUDIO_LASER)
            self.sfx_explosion = mixer.Sound(AUDIO_EXPLOSION)
            self.sfx_bomb = mixer.Sound(AUDIO_BOMB_SOUND)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar audio: {e}")

    def play_background_music(self):
        """Reproduce la música de fondo en bucle."""
        if not self.is_muted and self.background_music:
            self.background_music.play(-1)  # -1 indica bucle infinito

    def play_laser_sound(self):
        """Reproduce el sonido del láser."""
        if not self.is_muted and self.sfx_laser:
            self.sfx_laser.play()

    def play_explosion_sound(self):
        """Reproduce el sonido de explosión."""
        if not self.is_muted and self.sfx_explosion:
            self.sfx_explosion.play()

    def play_bomb_sound(self):
        """Reproduce el sonido de bomba."""
        if not self.is_muted and self.sfx_bomb:
            self.sfx_bomb.play()

    def stop_background_music(self):
        """Detiene la música de fondo."""
        if self.background_music:
            self.background_music.stop()

    def toggle_mute(self):
        """Alterna entre silenciar y no silenciar."""
        self.is_muted = not self.is_muted
        return self.is_muted

    def set_volume(self, volume):
        """
        Establece el volumen general (0.0 a 1.0).

        Args:
            volume: Valor entre 0.0 (silencio) y 1.0 (máximo)
        """
        volume = max(0.0, min(1.0, volume))
        mixer.music.set_volume(volume)