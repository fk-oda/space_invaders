import pygame as pg
import os

# Folders
IMG_FOLDER = os.path.join(os.path.dirname(__file__), 'images')
ENEMY_FOLDER = os.path.join(IMG_FOLDER, 'enemies')
FONT_FOLDER = os.path.join(os.path.dirname(__file__), 'font')
SOUNDS_FOLDER = os.path.join(os.path.dirname(__file__), 'sounds')
ENEMY_EXPLOSION_FOLDER = os.path.join(IMG_FOLDER, 'explosions','enemy')
PLAYER_EXPLOSION_FOLDER = os.path.join(IMG_FOLDER, 'explosions','player')
EVOLVE_FOLDER = os.path.join(IMG_FOLDER, 'evolve')

# Misc
FONT_NAME = 'AtariClassic.ttf'
ROTATE_ANGLE = - 90
EXPLOSION_RESCALE_X = 100
EXPLOSION_RESCALE_Y = 100

# PowerUps
POWER_UP_IMAGE = 'star_gold.png'
POWER_UP_LV2_IMAGE = 'star_silver.png'
POWER_UP_LV3_IMAGE = 'star_gold.png'
POWER_UP_RATE = 0.9
POWER_UP_SPEED = 200
EVOLVE_SPRITESHEET = 'nebula_spritesheet.png'
POWER_UP_SOUND = 'powerup.wav'
POWER_UP_LVL2_MIN_SCORE = 100
POWER_UP_LVL3_MIN_SCORE = 500

# Sounds variables
MUSIC_FILE = 'bg_music.ogg'
EXPLOSION_ENEMY_SOUND = 'explosion_enemy.wav'
EXPLOSION_PLAYER_SOUND = 'explosion_player.wav'
SHOOT_SOUND = 'shoot.ogg'

# Screen variables
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BORDER = 10
DARK_GREY = (40, 40, 40)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60
TITLE = 'Space Invaders'
BACKGROUND_IMG = 'background_image.jpg'
SCORE_SIZE = 6

# Player variables
PLAYER_IMG = 'player.png'
PLAYER_LV2_IMG = 'player_evolved.png'
PLAYER_LV3_IMG = 'player_evolved_3.png'
PLAYER_EVOLVED_IMG = 'player_evolved.png'
PLAYER_SPAWN_X = 50
PLAYER_SPEED = 400
PLAYER_LIVES = 3
PLAYER_HIDDEN_TIMER = 1000
PLAYER_ICON_LIVES_WIDTH = 48
PLAYER_ICON_LIVES_HEIGHT = 39
PLAYER_ICON_MARGIN = 10

# Enemy variables
ENEMY_SPEED_MIN = 300
ENEMY_SPEED_MAX = 500
ENEMY_SPEED_Y = 250
ENEMY_DIAGONAL_RATE = 0.5
ENEMY_RANGE = 200
ENEMY_MAX_NUM = 4
ENEMY_SPAWN_X = 1300
ENEMY_POINTS_VALUE = 10
ENEMY_SPAWN_POINTS = [(ENEMY_SPAWN_X, 10),(ENEMY_SPAWN_X, 160),(ENEMY_SPAWN_X, 310),(ENEMY_SPAWN_X, 460), (ENEMY_SPAWN_X, 610)]
ENEMY_IMAGES = os.listdir(ENEMY_FOLDER)

#Laser variables
LASER_IMG = 'laserBlue02.png'
LASER_SPEED = 600
LASER_FIRE_RATE = 500
LASER_LIFETIME = 1500
LASER_Y_OFFSET = 5


running = True