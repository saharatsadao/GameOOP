import pygame

# Screen
SCREEN_W = 800
SCREEN_H = 600
FPS = 60
TITLE = "Eden of the Continuum"

# Physics
GRAVITY = 850
MAX_FALL = 800
WALK_SPEED = 240
JUMP_FORCE_1 = -560
JUMP_FORCE_2 = -440

# Dimensions
TILE = 48
P_W, P_H = 36, 48
E_W, E_H = 40, 38
C_R = 14
ENEMY_SPEED = 85

# Colors
SKY = (100, 180, 255)
UI_WHITE = (255, 255, 255)
UI_GOLD = (255, 215, 0)
UI_RED = (230, 50, 50)

# Character Colors
M_RED = (200, 30, 30)
M_DRED = (140, 10, 10)
M_SKIN = (255, 200, 150)
M_BROWN = (100, 50, 20)
M_BLUE = (30, 60, 180)
M_BLACK = (10, 10, 10)
M_WHITE = (250, 250, 250)

# Enemy Colors
G_BROWN = (165, 95, 45)
G_DARK = (80, 40, 20)
G_FEET = (50, 30, 15)

# Tile Colors
GROUND_B = (140, 85, 35)
GROUND_T = (80, 170, 60)
BRICK_R = (180, 50, 30)
BRICK_D = (110, 30, 20)
QBLK_Y = (255, 200, 40)
QBLK_D = (180, 130, 20)
PIPE_G = (60, 180, 50)
PIPE_D = (30, 90, 25)
COIN_Y = (255, 230, 50)
COIN_S = (255, 255, 180)
