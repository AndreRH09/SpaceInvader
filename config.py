# config.py
# Configuración centralizada del juego Space Invaders

# Pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Jugador
PLAYER_START_X = 370
PLAYER_START_Y = 480
PLAYER_SPEED = 3
PLAYER_SIZE = (64, 64)

# Enemigos
INITIAL_ENEMIES = 3
MAX_ENEMIES = 8
INITIAL_ENEMY_SPEED = 1
INITIAL_ENEMY_Y_DROP = 40
INITIAL_BULLET_SPEED = 10

# Progresión de dificultad
PROGRESSION_SCORE_INTERVAL = 10  # Cada 10 puntos aumenta dificultad
ENEMY_SPEED_INCREMENT = 0.3
ENEMY_DROP_INCREMENT = 5
BULLET_SPEED_INCREMENT = 1
NEW_ENEMY_THRESHOLD = 20  # Cada 20 puntos se agrega un enemigo
MAX_BOMBS = 3

# Bomb (bombas de enemigos)
BOMB_SPEED = 2
BOMB_SPAWN_CHANCE = 0.005  # 2% de probabilidad por frame
BOMB_SIZE = (32, 32)

# Colores (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Fuentes
FONT_MAIN_SIZE = 32
FONT_GAMEOVER_SIZE = 64

# Rutas de assets
AUDIO_BACKGROUND = 'background.wav'
AUDIO_LASER = 'laser.wav'
AUDIO_EXPLOSION = 'explosion.wav'
AUDIO_BOMB_SOUND = 'bomb.mp3'

IMAGE_BACKGROUND = 'background.jpg'
IMAGE_PLAYER = 'player.png'
IMAGE_ENEMY = 'enemy.png'
IMAGE_BULLET = 'bullet.png'
IMAGE_ICON = 'ufo.png'
IMAGE_BOMB = 'bomb.png'