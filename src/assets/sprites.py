import pygame, math, random
from ..constants import *

# Dimensions (Sync with GameOOP)
SN_W, SN_H = 44, 36
SH_W, SH_H = 52, 36

class SpriteFactory:
    _CACHE = {}

    @classmethod
    def _get_cached(cls, key, draw_fn, *args):
        if key not in cls._CACHE:
            cls._CACHE[key] = draw_fn(*args)
        return cls._CACHE[key]

    # --- Mario ---
    @classmethod
    def _draw_player_base(cls, surf, state='idle', frame=0):
        # Premium Sasuke Color Palette
        C_OUTLINE = (5, 5, 10)
        C_BLACK = (20, 20, 25)
        C_HAIR_HIGHLIGHT = (45, 45, 80)
        C_GREY_BASE = (145, 145, 160)
        C_GREY_SHADE = (110, 110, 130)
        C_PURPLE_ROPE = (115, 90, 170)
        C_PURPLE_SHADE = (80, 60, 130)
        C_WAIST_CLOTH = (25, 25, 55)
        C_SKIN = (255, 235, 215)
        C_EYE_RED = (255, 10, 10)
        C_METAL = (200, 200, 210)
        C_WHITE = (255, 255, 255)

        # 1. HAIR (Layered & Rendered)
        # Back layers
        pygame.draw.polygon(surf, C_OUTLINE, [(8, 12), (0, 4), (10, 18)])
        pygame.draw.polygon(surf, C_BLACK, [(8, 12), (2, 6), (10, 18)])
        pygame.draw.polygon(surf, C_OUTLINE, [(6, 20), (0, 25), (10, 28)])
        pygame.draw.polygon(surf, C_BLACK, [(6, 20), (2, 23), (10, 28)])

        # Hair Main Shape
        pygame.draw.ellipse(surf, C_OUTLINE, (8, 2, 28, 30))
        pygame.draw.ellipse(surf, C_BLACK, (10, 4, 24, 26))
        
        # Hair Highlights (Top)
        pygame.draw.arc(surf, C_HAIR_HIGHLIGHT, (14, 6, 16, 12), 0.5, 2.5, 3)

        # Face Detail (Side Profile)
        face_rect = (18, 10, 18, 22)
        pygame.draw.ellipse(surf, C_SKIN, face_rect)
        # Chin/Jawline refine
        pygame.draw.polygon(surf, C_SKIN, [(24, 30), (32, 28), (34, 24)])
        # Eye-Shape (Mangekyo)
        pygame.draw.circle(surf, C_OUTLINE, (30, 20), 4)
        pygame.draw.circle(surf, C_EYE_RED, (30, 20), 3)
        pygame.draw.circle(surf, C_BLACK, (30, 20), 1)
        # Eye glint
        pygame.draw.circle(surf, C_WHITE, (31, 19), 1)

        # 2. CLOTHING (Hebi/Taka Standard)
        # High Collar Shirt
        # Collar Back
        pygame.draw.polygon(surf, C_GREY_SHADE, [(18, 28), (14, 12), (24, 28)])
        # Collar Front
        pygame.draw.polygon(surf, C_GREY_BASE, [(22, 28), (28, 14), (34, 28)])
        
        # Body Material
        pygame.draw.rect(surf, C_OUTLINE, (10, 28, 22, 16), border_radius=3)
        pygame.draw.rect(surf, C_GREY_BASE, (11, 29, 20, 14), border_radius=2)
        # Clothing folds/Shading
        pygame.draw.line(surf, C_GREY_SHADE, (14, 32), (28, 38), 2)
        pygame.draw.line(surf, C_GREY_SHADE, (16, 29), (24, 34), 1)

        # Blue Waist Cloth
        pygame.draw.rect(surf, C_OUTLINE, (8, 40, 26, 8), border_radius=2)
        pygame.draw.rect(surf, C_WAIST_CLOTH, (9, 41, 24, 6))

        # 3. SHIMENAWA ROPE (Twisted Texture)
        def draw_rope_knot(x, y):
             pygame.draw.ellipse(surf, C_OUTLINE, (x, y, 9, 6))
             pygame.draw.ellipse(surf, C_PURPLE_ROPE, (x+1, y+1, 7, 4))
             # Twist detail
             pygame.draw.line(surf, C_PURPLE_SHADE, (x+2, y+1), (x+6, y+4), 1)

        for i in range(3):
            draw_rope_knot(9 + i*7, 42)

        # 4. KUSANAGI SWORD (Polish)
        sword_angle = 0
        if state == 'walk':
             sword_angle = math.sin(frame * math.pi / 2) * 12
        elif state == 'jump':
             sword_angle = -15
             
        # Hand & Sleeve
        arm_x, arm_y = 28, 30
        pygame.draw.ellipse(surf, C_GREY_BASE, (arm_x, arm_y, 12, 12)) 
        pygame.draw.ellipse(surf, C_SKIN, (arm_x+6, arm_y+4, 8, 8))
        
        # Sword Hilt
        hilt_x, hilt_y = arm_x + 10, arm_y + 6
        pygame.draw.rect(surf, C_OUTLINE, (hilt_x, hilt_y, 8, 4), border_radius=1)
        
        # Blade (Gradient effect)
        blade_len = 38
        rad = math.radians(sword_angle - 25)
        ex = hilt_x + 6 + math.cos(rad) * blade_len
        ey = hilt_y + 2 + math.sin(rad) * blade_len
        pygame.draw.line(surf, C_OUTLINE, (hilt_x + 6, hilt_y + 2), (ex, ey), 4)
        pygame.draw.line(surf, C_METAL, (hilt_x + 6, hilt_y + 2), (ex, ey), 2)
        # Blade glint
        pygame.draw.line(surf, C_WHITE, (hilt_x + 8, hilt_y + 1), (hilt_x + 14, hilt_y + (ey-hilt_y)*0.2), 1)

    @classmethod
    def get_mario(cls, state='idle', direction=1, frame=0):
        key = ('sasuke_standard', state, direction, frame % 4)
        if key not in cls._CACHE:
            surf = pygame.Surface((P_W, P_H), pygame.SRCALPHA)
            cls._draw_player_base(surf, state, frame)
            
            C_BLACK = (0, 0, 0)
            C_METAL = (150, 150, 160)
            
            # Legs (Under cloak)
            leg_y = 42
            if state == 'jump':
                pygame.draw.rect(surf, C_BLACK, (8, leg_y-2, 6, 8))
                pygame.draw.rect(surf, C_BLACK, (22, leg_y-2, 6, 8))
                pygame.draw.rect(surf, C_METAL, (6, leg_y+4, 10, 4), border_radius=1)
                pygame.draw.rect(surf, C_METAL, (20, leg_y+4, 10, 4), border_radius=1)
            elif state == 'walk':
                off = int(6 * math.sin(frame * math.pi / 2))
                pygame.draw.rect(surf, C_BLACK, (10 + off, leg_y, 6, 8))
                pygame.draw.rect(surf, C_BLACK, (20 - off, leg_y, 6, 8))
                pygame.draw.rect(surf, C_METAL, (8 + off, leg_y+4, 10, 4), border_radius=1)
                pygame.draw.rect(surf, C_METAL, (18 - off, leg_y+4, 10, 4), border_radius=1)
            else:
                pygame.draw.rect(surf, C_BLACK, (10, leg_y, 6, 8))
                pygame.draw.rect(surf, C_BLACK, (20, leg_y, 6, 8))
                pygame.draw.rect(surf, C_METAL, (8, leg_y+4, 10, 4), border_radius=1)
                pygame.draw.rect(surf, C_METAL, (18, leg_y+4, 10, 4), border_radius=1)

            if direction == -1:
                surf = pygame.transform.flip(surf, True, False)
            cls._CACHE[key] = surf
        return cls._CACHE[key]

    # --- Halloween Enemies ---
    @classmethod
    def get_halloween_ghost(cls, frame=0, squished=False):
        key = ('halloween_ghost_v2', frame % 4, squished)
        if key not in cls._CACHE:
            s = pygame.Surface((32, 40), pygame.SRCALPHA)
            col = (230, 230, 255, 220) # Whiter and more opaque
            C_OUT = (0, 0, 0, 255)
            if squished:
                pygame.draw.ellipse(s, C_OUT, (0, 23, 32, 18))
                pygame.draw.ellipse(s, col, (2, 25, 28, 15))
            else:
                float_y = int(4 * math.sin(frame * math.pi * 0.5))
                # Body Outline & Fill
                pygame.draw.ellipse(s, C_OUT, (2, 2 + float_y, 28, 34))
                pygame.draw.ellipse(s, col, (4, 4 + float_y, 24, 30))
                # Tail/Bottom frills
                for i in range(3):
                    tx = 6 + i * 8
                    pygame.draw.circle(s, C_OUT, (tx, 34 + float_y), 8)
                    pygame.draw.circle(s, col, (tx, 34 + float_y), 6)
                # Eyes
                pygame.draw.circle(s, (0, 0, 0), (10, 14 + float_y), 4)
                pygame.draw.circle(s, (0, 0, 0), (22, 14 + float_y), 4)
                pygame.draw.circle(s, (255, 0, 0), (10, 14 + float_y), 2) # Glowing red pupil
                pygame.draw.circle(s, (255, 0, 0), (22, 14 + float_y), 2)
                # Mouth (ooh!)
                pygame.draw.ellipse(s, (0, 0, 0), (13, 20 + float_y, 6, 8))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_halloween_pumpkin(cls, frame=0, squished=False):
        key = ('halloween_pumpkin_v2', frame % 2, squished)
        if key not in cls._CACHE:
            s = pygame.Surface((40, 40), pygame.SRCALPHA)
            col = (255, 120, 20)
            C_OUT = (0, 0, 0)
            if squished:
                pygame.draw.ellipse(s, C_OUT, (0, 23, 40, 18))
                pygame.draw.ellipse(s, col, (2, 25, 36, 15))
            else:
                # Stem Outline & Fill
                pygame.draw.rect(s, C_OUT, (16, 0, 8, 14), border_radius=2)
                pygame.draw.rect(s, (50, 150, 20), (18, 2, 4, 10), border_radius=2)
                # Pumpkin Shape Outline & Fill
                pygame.draw.ellipse(s, C_OUT, (2, 8, 36, 32))
                pygame.draw.ellipse(s, col, (4, 10, 32, 28))
                # Orange Ribs
                pygame.draw.ellipse(s, (200, 80, 0), (8, 10, 24, 28), 2)
                pygame.draw.ellipse(s, (200, 80, 0), (14, 10, 12, 28), 2)
                # Glowing Face
                glow = (255, 255, 0)
                # Eyes (Triangles)
                pygame.draw.polygon(s, C_OUT, [(11, 19), (19, 19), (15, 13)])
                pygame.draw.polygon(s, glow, [(13, 18), (17, 18), (15, 15)])
                pygame.draw.polygon(s, C_OUT, [(21, 19), (29, 19), (25, 13)])
                pygame.draw.polygon(s, glow, [(23, 18), (27, 18), (25, 15)])
                # Mouth
                pygame.draw.polygon(s, C_OUT, [(10, 24), (30, 24), (25, 32), (15, 32)])
                pygame.draw.polygon(s, glow, [(12, 25), (28, 25), (24, 30), (16, 30)])
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_halloween_spider(cls, frame=0, squished=False):
        key = ('halloween_spider_v2', frame % 4, squished)
        if key not in cls._CACHE:
            s = pygame.Surface((36, 30), pygame.SRCALPHA)
            col = (30, 20, 40)
            C_OUT = (0, 0, 0)
            if squished:
                pygame.draw.ellipse(s, C_OUT, (2, 13, 32, 19))
                pygame.draw.ellipse(s, col, (4, 15, 28, 15))
            else:
                # Legs (Animated)
                leg_off = int(4 * math.sin(frame * math.pi * 0.5))
                for side in [-1, 1]:
                    for i in range(3):
                        ay = 10 + i * 5
                        pygame.draw.line(s, C_OUT, (18 + side * 6, ay), (18 + side * 18, ay + leg_off), 4)
                        pygame.draw.line(s, (100, 50, 150), (18 + side * 6, ay), (18 + side * 18, ay + leg_off), 2)
                # Body Outline & Fill
                pygame.draw.circle(s, C_OUT, (18, 15), 12)
                pygame.draw.circle(s, col, (18, 15), 10)
                # Head Outline & Fill
                pygame.draw.circle(s, C_OUT, (18, 24), 8)
                pygame.draw.circle(s, col, (18, 24), 6)
                # Eyes (Glowing red)
                for ex, ey in [(14, 23), (18, 22), (22, 23), (16, 26), (20, 26)]:
                    pygame.draw.circle(s, (255, 0, 0), (ex, ey), 2)
                    pygame.draw.circle(s, (255, 255, 255), (ex, ey), 1)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    # --- Candy Land Enemies ---
    @classmethod
    def get_gingerbread_man(cls, frame=0, squished=False):
        key = ('gingerbread_v2', frame % 2, squished)
        if key not in cls._CACHE:
            s = pygame.Surface((34, 40), pygame.SRCALPHA)
            col = (210, 130, 60)
            C_OUT = (0, 0, 0)
            if squished:
                pygame.draw.ellipse(s, C_OUT, (0, 23, 34, 18))
                pygame.draw.ellipse(s, col, (2, 25, 30, 15))
            else:
                walk = 4 if frame % 2 == 0 else -4
                # Legs Outline & Fill
                pygame.draw.rect(s, C_OUT, (8, 28, 10, 12), border_radius=4)
                pygame.draw.rect(s, C_OUT, (16, 28, 10, 12), border_radius=4)
                pygame.draw.rect(s, col, (10, 30, 6, 10), border_radius=3)
                pygame.draw.rect(s, col, (18, 30, 6, 10), border_radius=3)
                # Torso Outline & Fill
                pygame.draw.rect(s, C_OUT, (8, 13, 18, 19), border_radius=6)
                pygame.draw.rect(s, col, (10, 15, 14, 15), border_top_left_radius=4, border_top_right_radius=4) 
                # Head Outline & Fill
                pygame.draw.circle(s, C_OUT, (17, 10), 10)
                pygame.draw.circle(s, col, (17, 10), 8) 
                # Icing Details (White lines)
                pygame.draw.line(s, (255, 255, 255), (10, 20), (14, 20), 2)
                pygame.draw.line(s, (255, 255, 255), (20, 20), (24, 20), 2)
                pygame.draw.line(s, (255, 255, 255), (11, 35), (15, 35), 2)
                pygame.draw.line(s, (255, 255, 255), (19, 35), (23, 35), 2)
                # Face
                pygame.draw.circle(s, (255, 255, 255), (14, 8), 3) # Eyes
                pygame.draw.circle(s, (255, 255, 255), (20, 8), 3)
                pygame.draw.circle(s, (0, 0, 0), (14, 8), 1)
                pygame.draw.circle(s, (0, 0, 0), (20, 8), 1)
                # Buttons
                pygame.draw.circle(s, C_OUT, (17, 18), 4)
                pygame.draw.circle(s, (255, 50, 50), (17, 18), 3)
                pygame.draw.circle(s, C_OUT, (17, 25), 4)
                pygame.draw.circle(s, (50, 255, 50), (17, 25), 3)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_candy_monster(cls, frame=0, squished=False):
        key = ('candy_monster_v2', frame % 4, squished)
        if key not in cls._CACHE:
            s = pygame.Surface((44, 44), pygame.SRCALPHA)
            col = (130, 60, 180) # Purple chocolate
            C_OUT = (0, 0, 0)
            if squished:
                pygame.draw.ellipse(s, C_OUT, (0, 22, 44, 24))
                pygame.draw.ellipse(s, col, (2, 24, 40, 20))
            else:
                # Chonky Body Outline & Fill
                pygame.draw.rect(s, C_OUT, (2, 8, 40, 34), border_radius=12)
                pygame.draw.rect(s, col, (4, 10, 36, 30), border_radius=10)
                # Glowing Cream Eyes Outline & Fill
                pygame.draw.circle(s, C_OUT, (14, 20), 7)
                pygame.draw.circle(s, C_OUT, (30, 20), 7)
                pygame.draw.circle(s, (255, 255, 200), (14, 20), 6)
                pygame.draw.circle(s, (255, 255, 200), (30, 20), 6)
                pygame.draw.circle(s, (0, 0, 0), (14, 20), 2)
                pygame.draw.circle(s, (0, 0, 0), (30, 20), 2)
                # Teeth (White sprinkles)
                for i in range(3):
                    pygame.draw.rect(s, C_OUT, (13 + i*6, 29, 5, 7))
                    pygame.draw.rect(s, (255, 255, 255), (14 + i*6, 30, 3, 5))
                # Wrapper bits / horns
                pygame.draw.polygon(s, C_OUT, [(4, 12), (0, 4), (10, 8)])
                pygame.draw.polygon(s, (255, 100, 150), [(4, 12), (2, 6), (8, 10)])
                pygame.draw.polygon(s, C_OUT, [(40, 12), (44, 4), (34, 8)])
                pygame.draw.polygon(s, (255, 100, 150), [(40, 12), (42, 6), (36, 10)])
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_flying_sweet(cls, frame=0):
        key = ('flying_sweet_v2', frame % 4)
        if key not in cls._CACHE:
            s = pygame.Surface((36, 24), pygame.SRCALPHA)
            C_OUT = (0, 0, 0)
            # Wrappers Outline
            pygame.draw.polygon(s, C_OUT, [(0, 0), (8, 12), (0, 24)])
            pygame.draw.polygon(s, C_OUT, [(36, 0), (28, 12), (36, 24)])
            # Wrappers
            pygame.draw.polygon(s, (255, 200, 220), [(2, 2), (7, 12), (2, 22)])
            pygame.draw.polygon(s, (255, 200, 220), [(34, 2), (29, 12), (34, 22)])
            # Wrapped Candy shape Outline
            pygame.draw.ellipse(s, C_OUT, (4, 0, 28, 24))
            pygame.draw.ellipse(s, (255, 100, 150), (6, 2, 24, 20))
            # Spinning stripe
            off = (frame % 4) * 4
            pygame.draw.line(s, (255, 255, 255), (8 + off, 4), (8 + off, 20), 4)
            # Eyes (Small floating candy needs eyes?)
            # Add small cute eyes to make it an enemy
            pygame.draw.circle(s, C_OUT, (14, 12), 2)
            pygame.draw.circle(s, C_OUT, (22, 12), 2)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    # --- Enemies ---
    @classmethod
    def get_goomba(cls, frame=0, squished=False, style=0):
        key = ('goomba_v2', frame % 2, squished, style)
        if key not in cls._CACHE:
            surf = pygame.Surface((E_W, E_H), pygame.SRCALPHA)
            C_OUTLINE = (0, 0, 0)
            if style == 4: # Urban Thug
                col = (60, 60, 70) if not squished else (40, 40, 50)
                if squished:
                    pygame.draw.ellipse(surf, C_OUTLINE, (2, E_H-14, E_W-4, 16))
                    pygame.draw.ellipse(surf, col, (4, E_H-12, E_W-8, 12))
                else:
                    pygame.draw.rect(surf, C_OUTLINE, (6, 2, 32, 36), border_radius=4)
                    pygame.draw.rect(surf, col, (8, 4, 28, 32), border_radius=2) # Body/Hood
                    pygame.draw.rect(surf, (20, 20, 25), (14, 10, 16, 12)) # Face shadow
                    pygame.draw.rect(surf, (255, 50, 50), (16, 14, 4, 3)) # Glowing eyes
                    pygame.draw.rect(surf, (255, 50, 50), (24, 14, 4, 3))
                    walk = 4 if frame % 2 == 0 else -4
                    pygame.draw.rect(surf, C_OUTLINE, (6+walk, 32, 16, 10), border_radius=2)
                    pygame.draw.rect(surf, C_OUTLINE, (22-walk, 32, 16, 10), border_radius=2)
                    pygame.draw.rect(surf, (20, 20, 20), (8+walk, 34, 12, 6), border_radius=1)
                    pygame.draw.rect(surf, (20, 20, 20), (24-walk, 34, 12, 6), border_radius=1)
            elif style == 1: # Ocean Slug
                col = (220, 120, 255) if not squished else (150, 80, 200)
                if squished:
                    pygame.draw.ellipse(surf, C_OUTLINE, (2, E_H-12, E_W-4, 14))
                    pygame.draw.ellipse(surf, col, (4, E_H-10, E_W-8, 10))
                else:
                    pygame.draw.ellipse(surf, C_OUTLINE, (2, 14, E_W-4, 24))
                    pygame.draw.ellipse(surf, col, (4, 16, E_W-8, 20)) # Body
                    # Antennas
                    pygame.draw.line(surf, C_OUTLINE, (14, 14), (10, 4), 6)
                    pygame.draw.line(surf, C_OUTLINE, (26, 14), (30, 4), 6)
                    pygame.draw.line(surf, col, (14, 14), (10, 4), 2)
                    pygame.draw.line(surf, col, (26, 14), (30, 4), 2)
                    # Head
                    pygame.draw.ellipse(surf, C_OUTLINE, (8, 10, 24, 16))
                    pygame.draw.ellipse(surf, (255, 180, 255), (10, 12, 20, 12)) 
                    pygame.draw.circle(surf, C_OUTLINE, (16, 16), 4)
                    pygame.draw.circle(surf, (255, 255, 255), (16, 16), 3) # Eye
                    pygame.draw.circle(surf, C_OUTLINE, (24, 16), 4)
                    pygame.draw.circle(surf, (255, 255, 255), (24, 16), 3) # Eye
            else: # Standard Goomba
                if squished:
                    pygame.draw.ellipse(surf, C_OUTLINE, (0, E_H-16, E_W, 18))
                    pygame.draw.ellipse(surf, G_BROWN, (2, E_H-14, E_W-4, 14))
                    pygame.draw.circle(surf, C_OUTLINE, (12, E_H-8), 6)
                    pygame.draw.circle(surf, (255,255,255), (12, E_H-8), 5)
                    pygame.draw.circle(surf, C_OUTLINE, (28, E_H-8), 6)
                    pygame.draw.circle(surf, (255,255,255), (28, E_H-8), 5)
                else:
                    walk = 2 if frame % 2 == 0 else -2
                    # Body
                    pygame.draw.ellipse(surf, C_OUTLINE, (2, 24, 36, 14))
                    pygame.draw.ellipse(surf, (240, 200, 140), (4, 26, 32, 10))
                    # Feet
                    pygame.draw.ellipse(surf, C_OUTLINE, (-2+walk, 30, 22, 12))
                    pygame.draw.ellipse(surf, C_OUTLINE, (20-walk, 30, 22, 12))
                    pygame.draw.ellipse(surf, (0, 0, 0), (0+walk, 32, 18, 8))
                    pygame.draw.ellipse(surf, (0, 0, 0), (22-walk, 32, 18, 8))
                    # Head
                    pygame.draw.ellipse(surf, C_OUTLINE, (0, 0, 40, 30))
                    pygame.draw.ellipse(surf, (220, 100, 20), (2, 2, 36, 26))
                    # Eyebrows
                    pygame.draw.polygon(surf, C_OUTLINE, [(2,8),(21,17),(21,8)])
                    pygame.draw.polygon(surf, C_OUTLINE, [(38,8),(19,17),(19,8)])
                    pygame.draw.polygon(surf, (0, 0, 0), [(4,10),(19,15),(19,10)])
                    pygame.draw.polygon(surf, (0, 0, 0), [(36,10),(21,15),(21,10)])
                    # Eyes
                    pygame.draw.circle(surf, C_OUTLINE, (12, 17), 7)
                    pygame.draw.circle(surf, C_OUTLINE, (28, 17), 7)
                    pygame.draw.circle(surf, (255,255,255), (12, 17), 6)
                    pygame.draw.circle(surf, (255,255,255), (28, 17), 6)
                    pygame.draw.circle(surf, (0,0,0), (13, 17), 3)
                    pygame.draw.circle(surf, (0,0,0), (27, 17), 3)
            cls._CACHE[key] = surf
        return cls._CACHE[key]

    @classmethod
    def get_snail(cls, frame=0, squished=False, flip=False, style=0):
        key = ('snail_v2', frame % 2, squished, flip, style)
        if key not in cls._CACHE:
            s = pygame.Surface((SN_W, SN_H), pygame.SRCALPHA)
            C_OUT = (0, 0, 0)
            if style == 4: # Urban Drone
                col = (130, 130, 140)
                if squished: 
                    pygame.draw.rect(s, C_OUT, (2, 24, 40, 14), border_radius=2)
                    pygame.draw.rect(s, col, (4, 26, 36, 10))
                else:
                    pygame.draw.rect(s, C_OUT, (2, 8, 40, 24), border_radius=4)
                    pygame.draw.rect(s, col, (4, 10, 36, 20), border_radius=2) # Chassis
                    pygame.draw.rect(s, C_OUT, (8, 13, 28, 14))
                    pygame.draw.rect(s, (200, 240, 255), (10, 15, 24, 10)) # Sensor/Screen
                    pygame.draw.rect(s, (255, 50, 50), (12, 18, 6, 4)) # Scanning light
                if flip: s = pygame.transform.flip(s, True, False)
            elif style == 1: # Ocean Crab (Variant)
                col = (255, 100, 80)
                if squished: 
                    pygame.draw.ellipse(s, C_OUT, (2, 18, 40, 20))
                    pygame.draw.ellipse(s, col, (4, 20, 36, 16))
                else:
                    pygame.draw.ellipse(s, C_OUT, (2, 12, 40, 26))
                    pygame.draw.ellipse(s, col, (4, 14, 36, 22)) # Body
                    # Pincers
                    p_off = 4 if frame%2 else 0
                    pygame.draw.circle(s, C_OUT, (8-p_off, 20), 8)
                    pygame.draw.circle(s, (220, 60, 40), (8-p_off, 20), 6)
                    pygame.draw.circle(s, C_OUT, (36+p_off, 20), 8)
                    pygame.draw.circle(s, (220, 60, 40), (36+p_off, 20), 6)
                    # Eyes
                    pygame.draw.circle(s, C_OUT, (14, 18), 5)
                    pygame.draw.circle(s, (255,255,255), (14, 18), 4)
                    pygame.draw.circle(s, C_OUT, (30, 18), 5)
                    pygame.draw.circle(s, (255,255,255), (30, 18), 4)
                    pygame.draw.circle(s, (0,0,0), (14, 18), 2)
                    pygame.draw.circle(s, (0,0,0), (30, 18), 2)
                if flip: s = pygame.transform.flip(s, True, False)
            else: # Standard Snail/Koopa
                BC, SC, DC = (100, 200, 80), (255, 150, 50), (180, 80, 30)
                if squished: # Just the shell
                    pygame.draw.ellipse(s, C_OUT, (2, 18, 40, 20))
                    pygame.draw.ellipse(s, SC, (4, 20, 36, 16))
                    pygame.draw.ellipse(s, C_OUT, (6, 22, 32, 12))
                    pygame.draw.ellipse(s, DC, (8, 24, 28, 8))
                else:
                    walk = 2 if frame % 2 == 0 else -2
                    # Body
                    pygame.draw.ellipse(s, C_OUT, (-2+walk, 18, 32, 20))
                    pygame.draw.ellipse(s, BC, (0+walk, 20, 28, 16))
                    # Eye
                    pygame.draw.circle(s, C_OUT, (4+walk, 15), 5)
                    pygame.draw.circle(s, (255,255,255), (4+walk, 15), 4)
                    pygame.draw.circle(s, (0,0,0), (3+walk, 15), 2)
                    # Shell
                    pygame.draw.ellipse(s, C_OUT, (10, 4, 36, 28))
                    pygame.draw.ellipse(s, SC, (12, 6, 32, 24))
                    pygame.draw.ellipse(s, C_OUT, (18, 8, 20, 20))
                    pygame.draw.ellipse(s, DC, (20, 10, 16, 16))
                    # Shell highlights
                    pygame.draw.arc(s, (255, 200, 100), (14, 8, 28, 20), math.pi/2, math.pi, 2)
                if flip: s = pygame.transform.flip(s, True, False)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_coral(cls, variant=0):
        key = ('coral_premium', variant)
        if key not in cls._CACHE:
            w, h = TILE*3, TILE*3
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Vibrant Palette from reference
            colors = [
                (255, 105, 180), # Neon Pink
                (255, 127, 80),  # Coral Orange
                (0, 255, 255),   # Cyan
                (173, 255, 47),  # Green Yellow
                (255, 255, 100)  # Pale Yellow
            ]
            col = colors[variant % len(colors)]
            dark_col = (int(col[0]*0.5), int(col[1]*0.5), int(col[2]*0.5))
            
            if variant % 3 == 0: # Fan Coral (Premium)
                center_x, bottom_y = w//2, h-10
                for angle in range(-60, 61, 15):
                    rad = math.radians(angle - 90)
                    length = random.randint(60, 90)
                    end_x = center_x + math.cos(rad) * length
                    end_y = bottom_y + math.sin(rad) * length
                    pygame.draw.line(s, col, (center_x, bottom_y), (end_x, end_y), 6)
                    # Frilly edge
                    for i in range(5):
                        p_rad = rad + math.radians(random.randint(-10, 10))
                        pygame.draw.circle(s, col, (int(end_x + math.cos(p_rad)*10), int(end_y + math.sin(p_rad)*10)), 6)
                pygame.draw.circle(s, dark_col, (center_x, bottom_y), 8)
                
            elif variant % 3 == 1: # Staghorn Coral (Branching)
                def draw_branch(surf, x, y, angle, length, depth, color):
                    if depth == 0: return
                    rad = math.radians(angle - 90)
                    nx = x + math.cos(rad) * length
                    ny = y + math.sin(rad) * length
                    pygame.draw.line(surf, color, (x, y), (nx, ny), depth*3)
                    pygame.draw.circle(surf, color, (int(nx), int(ny)), depth+1)
                    draw_branch(surf, nx, ny, angle - 20, length * 0.7, depth - 1, color)
                    draw_branch(surf, nx, ny, angle + 20, length * 0.7, depth - 1, color)
                draw_branch(s, w//2, h-10, 0, 40, 4, col)
                
            else: # Anemone / Brain Type
                cx, cy = w//2, h-w//4
                for i in range(12):
                    angle = i * 30
                    rad = math.radians(angle)
                    pygame.draw.ellipse(s, col, (cx + math.cos(rad)*20 - 10, cy + math.sin(rad)*20 - 30, 20, 40))
                pygame.draw.circle(s, dark_col, (cx, cy-10), 10)
                
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_seaweed(cls, frame=0):
        key = ('seaweed_premium', frame % 8)
        if key not in cls._CACHE:
            s = pygame.Surface((60, 120), pygame.SRCALPHA)
            col = (50, 200, 100, 200)
            offset = math.sin(frame * math.pi * 0.25) * 15
            points = [
                (30, 120),
                (30 + offset*0.3, 90),
                (30 - offset*0.6, 60),
                (30 + offset, 30),
                (30 + offset*0.5, 5)
            ]
            pygame.draw.lines(s, col, False, points, 10)
            # Add small leaves
            for i, p in enumerate(points[1:]):
                lx, ly = p
                pygame.draw.ellipse(s, (40, 180, 80, 180), (lx-10, ly-5, 20, 10))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_fish_silhouette(cls, frame=0):
        key = ('fish_sil', frame % 4)
        if key not in cls._CACHE:
            s = pygame.Surface((40, 20), pygame.SRCALPHA)
            col = (0, 50, 100, 100) # Semi-transparent blue
            pygame.draw.ellipse(s, col, (5, 5, 25, 10)) # Body
            pygame.draw.polygon(s, col, [(30, 10), (38, 5), (38, 15)]) # Tail
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_god_ray(cls, w=200, h=600):
        key = ('god_ray', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Tapered beams
            for x in range(0, w, 100):
                for i in range(60):
                    alpha = int(30 * (1 - i/60))
                    pygame.draw.polygon(s, (255, 255, 255, alpha), [(x+30, 0), (x+70, 0), (x+i, h), (x-i, h)])
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_sea_shell(cls, variant=0):
        key = ('shell', variant)
        if key not in cls._CACHE:
            s = pygame.Surface((30, 20), pygame.SRCALPHA)
            col = (255, 230, 200)
            pygame.draw.ellipse(s, col, (5, 5, 20, 12))
            # Ribs
            for i in range(5):
                pygame.draw.line(s, (230, 200, 160), (10+i*2, 5), (10+i*2, 17), 1)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_underwater_bubble(cls, size=10):
        key = ('bubble', size)
        if key not in cls._CACHE:
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, 100), (size//2, size//2), size//2)
            pygame.draw.circle(s, (255, 255, 255, 200), (size//3, size//3), size//6)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_heart(cls, size=24):
        key = ('heart_vibrant', size)
        if key not in cls._CACHE:
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            col = (255, 0, 50) # Super vibrant red
            # Heart shape using two circles and a polygon
            r = size // 4
            pygame.draw.circle(s, col, (size//2 - r, size//2 - r//2), r)
            pygame.draw.circle(s, col, (size//2 + r, size//2 - r//2), r)
            pygame.draw.polygon(s, col, [
                (size//2 - r*2, size//2 - r//2),
                (size//2 + r*2, size//2 - r//2),
                (size//2, size - 4)
            ])
            # Glossy Highlight
            pygame.draw.circle(s, (255, 255, 255, 200), (size//2 - r, size//2 - r), r//2)
            pygame.draw.ellipse(s, (255, 255, 255, 120), (size//2 - r*1.5, size//2 - r*1.2, r*1.2, r*0.8))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_shark(cls, frame=0, direction=1):
        key = ('shark_v2', frame % 4, direction)
        if key not in cls._CACHE:
            s = pygame.Surface((SH_W, SH_H), pygame.SRCALPHA)
            C_OUT = (0, 0, 0)
            body, belly = (50, 60, 140), (220, 230, 240)
            tail = int(4 * math.sin(frame * math.pi * 0.5))
            # Tail Fin Back
            pygame.draw.polygon(s, C_OUT, [(3, 17), (-3, 9+tail), (-3, 25+tail), (4, 19)])
            pygame.draw.polygon(s, body, [(5, 17), (0, 11+tail), (0, 23+tail), (6, 19)])
            # Top Fin
            pygame.draw.polygon(s, C_OUT, [(22, 10), (26, 0), (34, 12)])
            pygame.draw.polygon(s, body, [(24, 10), (27, 3), (32, 12)])
            # Main Body
            pygame.draw.ellipse(s, C_OUT, (2, 8, 44, 22))
            pygame.draw.ellipse(s, body, (4, 10, 40, 18))
            pygame.draw.ellipse(s, belly, (6, 18, 36, 9))
            # Front Fin (snout)
            pygame.draw.polygon(s, C_OUT, [(40,12), (54,10), (54,20), (42,21)])
            pygame.draw.polygon(s, body, [(42,14), (52,12), (52,18), (44,19)])
            # Secondary Fin
            pygame.draw.polygon(s, C_OUT, [(26, 22), (20, 32), (34, 26)])
            pygame.draw.polygon(s, belly, [(28, 24), (23, 30), (32, 26)])
            # Eyes
            pygame.draw.circle(s, C_OUT, (38, 14), 5)
            pygame.draw.circle(s, (255, 255, 255), (38, 14), 4)
            pygame.draw.circle(s, (255, 50, 50), (39, 14), 2)
            # Gills
            pygame.draw.line(s, (30, 40, 80), (20, 14), (18, 20), 2)
            pygame.draw.line(s, (30, 40, 80), (24, 14), (22, 20), 2)
            if direction < 0: s = pygame.transform.flip(s, True, False)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    # --- Tiles ---
    @classmethod
    def get_tile(cls, kind, frame=0, used=False):
        key = (kind, frame, used)
        if key not in cls._CACHE:
            s = pygame.Surface((TILE, TILE))
            if kind == 'ground':
                s.fill(GROUND_B)
                pygame.draw.rect(s, GROUND_T, (0, 0, TILE, 10))
                pygame.draw.rect(s, (56, 136, 40), (0, 8, TILE, 3))
            elif kind == 'ground_med':
                # Deep dark dirt
                s.fill((40, 30, 25))
                # Add dirt specks
                for _ in range(12):
                    rx, ry = random.randint(0, TILE-2), random.randint(4, TILE-2)
                    pygame.draw.rect(s, (60, 45, 35), (rx, ry, 2, 2))
                # Lush Grass top
                pygame.draw.rect(s, (45, 90, 30), (0, 0, TILE, 14))
                pygame.draw.rect(s, (70, 140, 50), (0, 0, TILE, 8))
                # Grass "blades" hanging down
                for x in range(0, TILE, 6):
                    h = random.randint(10, 18)
                    pygame.draw.line(s, (45, 90, 30), (x, 14), (x + random.randint(-2, 2), h), 2)
            elif kind == 'ground_ocean':
                # Sandy Seabed with gradients and texture
                s.fill((240, 200, 100)) # Sand base
                for y in range(TILE):
                    shade = int(20 * math.sin(y * 0.1))
                    col = (
                        max(0, min(255, 240 + shade)),
                        max(0, min(255, 200 + shade)),
                        max(0, min(255, 100 + shade))
                    )
                    pygame.draw.line(s, col, (0, y), (TILE, y))
                # Particles and details
                for _ in range(40):
                    rx, ry = random.randint(0, TILE-1), random.randint(0, TILE-1)
                    pygame.draw.rect(s, (200, 160, 60), (rx, ry, 1, 1))
                # Highlights on top ripples
                for x in range(0, TILE, 8):
                    pygame.draw.arc(s, (255, 230, 150), (x-4, -2, 10, 6), 0, math.pi, 1)
            elif kind == 'ground_urban':
                s.fill((40, 40, 45)) # Dark Asphalt
                pygame.draw.rect(s, (60, 60, 65), (0, 0, TILE, 10)) # Concrete Sidewalk edge
                # Road grain
                for _ in range(15):
                    rx, ry = random.randint(0, TILE-2), random.randint(10, TILE-2)
                    pygame.draw.rect(s, (50, 50, 55), (rx, ry, 2, 2))
            elif kind == 'brick':
                s.fill(BRICK_R)
                for row in range(4):
                    y = row * 12
                    off = 24 if row % 2 else 0
                    pygame.draw.line(s, BRICK_D, (0, y), (TILE, y), 2)
                    pygame.draw.line(s, BRICK_D, (off, y), (off, y+12), 2)
                    pygame.draw.line(s, BRICK_D, (off+24, y), (off+24, y+12), 2)
            elif kind == 'qblock':
                if used:
                    s.fill((130, 100, 50))
                    pygame.draw.rect(s, (100, 75, 30), s.get_rect(), 3)
                else:
                    cols = [QBLK_Y, (255, 225, 80), QBLK_Y, (220, 175, 40)]
                    s.fill(cols[frame % 4])
                    pygame.draw.rect(s, QBLK_D, s.get_rect(), 3)
                    try:
                        f = pygame.font.SysFont('Arial', 28, bold=True)
                        t = f.render('?', True, (255, 255, 255))
                        s.blit(t, (TILE//2 - t.get_width()//2, TILE//2 - t.get_height()//2))
                    except: pass
            elif kind == 'brick_candy':
                # Chocolate Bar Brick
                s.fill((70, 40, 30))
                # Bar indent/outline
                pygame.draw.rect(s, (50, 25, 15), (2, 2, TILE-4, TILE-4), 2)
                # Cross lines
                pygame.draw.line(s, (50, 25, 15), (TILE//2, 2), (TILE//2, TILE-2), 1)
                pygame.draw.line(s, (50, 25, 15), (2, TILE//2), (TILE-2, TILE//2), 1)
                # Highlight
                pygame.draw.line(s, (90, 60, 50), (4, 4), (TILE-4, 4), 1)
                pygame.draw.line(s, (90, 60, 50), (4, 4), (4, TILE-4), 1)
            elif kind == 'qblock_candy':
                if used:
                    s.fill((80, 50, 40))
                    pygame.draw.rect(s, (50, 30, 20), s.get_rect(), 3)
                else:
                    # Pink frosting qblock
                    cols = [(255, 180, 220), (255, 200, 240), (255, 180, 220), (255, 160, 200)]
                    s.fill(cols[frame % 4])
                    pygame.draw.rect(s, (255, 140, 200), s.get_rect(), 3)
                    try:
                        f = pygame.font.SysFont('Arial', 28, bold=True)
                        t = f.render('?', True, (255, 255, 255))
                        s.blit(t, (TILE//2 - t.get_width()//2, TILE//2 - t.get_height()//2))
                    except: pass
            elif kind == 'brick_ocean':
                # Sandstone block
                s.fill((200, 160, 90))
                pygame.draw.rect(s, (160, 120, 60), s.get_rect(), 2)
                for y in range(4, TILE, 8):
                    pygame.draw.line(s, (180, 140, 70), (0, y), (TILE, y))
            elif kind == 'qblock_ocean':
                if used:
                    s.fill((100, 80, 60))
                    pygame.draw.rect(s, (70, 50, 40), s.get_rect(), 3)
                else:
                    # Coral/Bubble qblock
                    cols = [(100, 200, 255), (120, 220, 255), (100, 200, 255), (80, 180, 255)]
                    s.fill(cols[frame % 4])
                    pygame.draw.rect(s, (50, 150, 200), s.get_rect(), 3)
                    # Bubble details
                    pygame.draw.circle(s, (255, 255, 255, 100), (8, 8), 4)
                    pygame.draw.circle(s, (255, 255, 255, 100), (TILE-8, TILE-8), 6)
                    try:
                        f = pygame.font.SysFont('Arial', 28, bold=True)
                        t = f.render('?', True, (255, 255, 255))
                        s.blit(t, (TILE//2 - t.get_width()//2, TILE//2 - t.get_height()//2))
                    except: pass
            elif kind == 'brick_spooky':
                # Dark Tombstone / Cobblestone
                s.fill((50, 55, 60))
                pygame.draw.rect(s, (30, 35, 40), s.get_rect(), 2)
                # Cracks
                pygame.draw.line(s, (20, 25, 30), (0, 10), (15, 20), 2)
                pygame.draw.line(s, (20, 25, 30), (15, 20), (20, TILE), 2)
                pygame.draw.line(s, (20, 25, 30), (TILE, 15), (20, 30), 2)
            elif kind == 'qblock_spooky':
                if used:
                    s.fill((40, 40, 45))
                    pygame.draw.rect(s, (20, 20, 25), s.get_rect(), 3)
                else:
                    # Cursed Pumpkin block
                    cols = [(180, 80, 20), (200, 100, 30), (180, 80, 20), (150, 60, 10)]
                    s.fill(cols[frame % 4])
                    pygame.draw.rect(s, (100, 30, 0), s.get_rect(), 3)
                    try:
                        f = pygame.font.SysFont('Arial', 28, bold=True)
                        t = f.render('?', True, (255, 255, 100))
                        st = f.render('?', True, (255, 100, 0))
                        s.blit(st, (TILE//2 - t.get_width()//2 + 2, TILE//2 - t.get_height()//2 + 2))
                        s.blit(t, (TILE//2 - t.get_width()//2, TILE//2 - t.get_height()//2))
                    except: pass
            elif kind == 'brick_urban':
                # Metal Crate
                s.fill((80, 85, 90))
                pygame.draw.rect(s, (50, 55, 60), s.get_rect(), 4)
                pygame.draw.line(s, (50, 55, 60), (0, 0), (TILE, TILE), 4)
                pygame.draw.line(s, (50, 55, 60), (0, TILE), (TILE, 0), 4)
                for pos in [(4,4), (TILE-6, 4), (4, TILE-6), (TILE-6, TILE-6)]:
                    pygame.draw.rect(s, (120, 125, 130), (*pos, 3, 3))
            elif kind == 'qblock_urban':
                if used:
                    s.fill((60, 60, 65))
                    pygame.draw.rect(s, (40, 40, 45), s.get_rect(), 3)
                else:
                    # Neon block
                    cols = [(50, 255, 200), (80, 255, 220), (50, 255, 200), (30, 220, 180)]
                    s.fill((20, 30, 40)) 
                    pygame.draw.rect(s, cols[frame % 4], s.get_rect(), 3)
                    pygame.draw.rect(s, (10, 15, 20), s.get_rect().inflate(-10, -10))
                    try:
                        f = pygame.font.SysFont('Arial', 28, bold=True)
                        t = f.render('?', True, cols[frame % 4])
                        s.blit(t, (TILE//2 - t.get_width()//2, TILE//2 - t.get_height()//2))
                    except: pass
            elif kind == 'ground_spooky':
                # Spooky Graveyard/Mansion Ground
                s.fill((20, 25, 20)) # Very dark green-grey
                # Glowing cracks/veins
                for _ in range(8):
                    rx, ry = random.randint(0, TILE-4), random.randint(4, TILE-4)
                    pygame.draw.rect(s, (0, 60, 0), (rx, ry, 4, 2))
                # Top edge (Grassy/Mossy but dark)
                pygame.draw.rect(s, (15, 30, 15), (0, 0, TILE, 12))
                pygame.draw.rect(s, (30, 80, 30), (0, 0, TILE, 4))
                # Grass tufts
                for x in range(0, TILE, 10):
                    h = random.randint(10, 16)
                    pygame.draw.line(s, (30, 80, 30), (x, 12), (x + random.randint(-1, 1), h), 1)
            elif kind == 'ground_candy':
                # Chocolate & Cream Ground
                s.fill((60, 30, 20)) # Chocolate brown
                # Grid pattern
                for i in range(0, TILE, 8):
                    pygame.draw.line(s, (50, 25, 15), (i, 0), (i, TILE))
                    pygame.draw.line(s, (50, 25, 15), (0, i), (TILE, i))
                # Cream Drips top (THICKER)
                top_col = (255, 250, 255) # White cream
                pygame.draw.rect(s, top_col, (0, 0, TILE, 16), border_bottom_left_radius=10, border_bottom_right_radius=10)
                # Organic Drips
                for x in range(0, TILE, 10):
                    h = 18 + int(6 * math.sin(x * 0.5))
                    pygame.draw.circle(s, top_col, (x + 5, h), 7)
            elif kind.startswith('pipe_candy'):
                W, H = TILE + 8, TILE
                s = pygame.Surface((W, H), pygame.SRCALPHA)
                # Red/White Striped Candy Straw
                s.fill((255, 255, 255))
                for y in range(-20, H + 20, 20):
                    pygame.draw.line(s, (255, 50, 50), (0, y), (W, y + 20), 10)
                # Outline
                pygame.draw.rect(s, (200, 0, 0), (0, 0, W, H), 2)
                if kind == 'pipe_candy_t':
                    # Flat rim top
                    pygame.draw.rect(s, (255, 255, 255), (0, 0, W, 10))
                    pygame.draw.rect(s, (255, 50, 50), (0, 0, 10, 10))
                    pygame.draw.rect(s, (255, 50, 50), (20, 0, 10, 10))
                    pygame.draw.rect(s, (200, 0, 0), (0, 0, W, 10), 2)
            elif kind.startswith('pipe'):
                W, H = TILE + 8, TILE
                s = pygame.Surface((W, H), pygame.SRCALPHA)
                if kind == 'pipe_t':
                    pygame.draw.rect(s, PIPE_G, (0, 6, W, H-6))
                    pygame.draw.rect(s, PIPE_D, (0, 6, W, H-6), 2)
                    pygame.draw.rect(s, PIPE_G, (0, 0, W, 10))
                    pygame.draw.rect(s, PIPE_D, (0, 0, W, 10), 2)
                else:
                    pygame.draw.rect(s, PIPE_G, (4, 0, W-8, H))
                    pygame.draw.rect(s, PIPE_D, (4, 0, W-8, H), 2)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_coin(cls, frame=0):
        key = ('coin', frame % 4)
        if key not in cls._CACHE:
            s = pygame.Surface((C_R*2, C_R*2), pygame.SRCALPHA)
            widths = [C_R*2-2, int(C_R*1.4), 4, int(C_R*1.4)]
            w = widths[frame % 4]
            # Outer Rim - Gold/Bronze
            pygame.draw.ellipse(s, (40, 40, 0), (C_R-w//2, 1, w, C_R*2-2)) # Border/Shadow
            pygame.draw.ellipse(s, COIN_Y, (C_R-w//2 + 1, 2, max(0, w-2), C_R*2-4)) # Main Body
            
            # Inner circle/rim
            if w > 10:
                pygame.draw.ellipse(s, COIN_S, (C_R-w//2 + 4, 5, max(0, w-8), C_R*2-10), 2)
                
                # The 'P' Symbol
                # Drawn proportionally to the width 'w' to Narrow with animation
                if w > 8:
                    p_w = max(2, w // 3)
                    p_h = C_R # Height in middle
                    p_col = (180, 140, 0) # Darker gold/brown for 'P'
                    # Vert line
                    pygame.draw.rect(s, p_col, (C_R - p_w//2 - p_w//2, C_R - p_h//2, p_w//2, p_h))
                    # Top loop of P
                    p_loop_rect = (C_R - p_w//2, C_R - p_h//2, p_w, p_h//2)
                    pygame.draw.ellipse(s, p_col, p_loop_rect, 2)
            
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_cloud(cls, w=140, h=70):
        key = ('cloud', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Main body with subtle shadow
            pygame.draw.ellipse(s, (240, 240, 240), (w//14, h//2, w*6//7, h//2))
            pygame.draw.ellipse(s, (255, 255, 255), (w//14, h//2-2, w*6//7, h//2))
            
            # Fluffs with depth
            pygame.draw.ellipse(s, (230, 230, 230), (w//28, h//3, w//3, h*2//3))
            pygame.draw.ellipse(s, (255, 255, 255), (w//28, h//3-2, w//3, h*2//3))
            
            pygame.draw.ellipse(s, (220, 220, 220), (w//4, h//6, w//2, h*2//3))
            pygame.draw.ellipse(s, (255, 255, 255), (w//4, h//6-2, w//2, h*2//3))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_mountain(cls, w=280, h=190):
        key = ('mountain', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            cx = w // 2
            # Dark side
            pygame.draw.ellipse(s, (45, 65, 35), (cx - w//2, h // 2, w, h))
            # Light side / Tops
            pygame.draw.ellipse(s, (58, 100, 42), (cx - w//2+10, h * 2 // 5 + 2, w * 3 // 4, h * 3 // 5))
            pygame.draw.ellipse(s, (80, 125, 58), (cx - w * 2 // 5 + 5, h // 5 + 4, w * 4 // 5, h * 3 // 5))
            # High highlights
            pygame.draw.ellipse(s, (100, 150, 70), (cx - w // 5, h // 4, w // 3, h // 3))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_bush(cls, w=110, h=55):
        key = ('bush', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (90, 180, 50), (0, h//3, w, h*2//3))
            pygame.draw.ellipse(s, (90, 180, 50), (w//4, 0, w//2, h))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_palm(cls, h=160):
        key = ('palm', h)
        if key not in cls._CACHE:
            w = h // 2
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            for i in range(h - 30):
                sway = int(4 * math.sin(i / h * math.pi))
                pygame.draw.rect(s, (160, 110, 50), (w//2-6+sway, i, 12, 1))
            leaf = (30, 160, 50)
            cx, cy = w//2, 10
            for lx, ly, lw, lh in [(-35,-20,38,14), (5,-20,38,14), (-18,-32,38,14)]:
                pygame.draw.ellipse(s, leaf, (cx+lx, cy+ly, lw, lh))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_medieval_tree(cls, h=240):
        key = ('med_tree', h)
        if key not in cls._CACHE:
            w = h
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            trunk_c = (50, 35, 25)
            # Twisted Trunk
            pygame.draw.rect(s, trunk_c, (w//2-12, h-80, 24, 80))
            pygame.draw.line(s, (70, 50, 35), (w//2-12, h-80), (w//2-12, h), 2)
            # Clumped Foliage
            leaf_d, leaf_m, leaf_l = (25, 55, 25), (45, 95, 35), (80, 160, 50)
            for i in range(12):
                rx, ry = w//2 + random.randint(-w//3, w//3), h-80 - random.randint(0, h-100)
                rw, rh = random.randint(60, 100), random.randint(40, 70)
                pygame.draw.ellipse(s, leaf_d, (rx-rw//2, ry-rh//2, rw, rh))
                pygame.draw.ellipse(s, leaf_m, (rx-rw//2+4, ry-rh//2+2, rw-8, rh-10))
                pygame.draw.ellipse(s, leaf_l, (rx-rw//2+10, ry-rh//2+4, rw-20, rh-25))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_house_small(cls):
        key = ('house_s')
        if key not in cls._CACHE:
            s = pygame.Surface((220, 200), pygame.SRCALPHA)
            stone, wall, roof, wood = (90, 90, 90), (165, 155, 140), (130, 45, 35), (65, 45, 30)
            # masonry and walls
            pygame.draw.rect(s, stone, (20, 120, 180, 60)) # Stone base
            for _ in range(20):
                pygame.draw.rect(s, (110, 110, 110), (random.randint(20, 180), random.randint(120, 170), 12, 6))
            pygame.draw.rect(s, wall, (20, 60, 180, 60)) # Plaster wall
            # Timber frames
            for x in range(20, 201, 44):
                pygame.draw.rect(s, wood, (x, 60, 6, 120))
            pygame.draw.rect(s, wood, (20, 90, 180, 6))
            pygame.draw.rect(s, wood, (20, 120, 180, 8))
            # Door & Windows
            pygame.draw.rect(s, (45, 30, 20), (50, 110, 32, 70)) # Door
            pygame.draw.rect(s, (90, 130, 160), (130, 80, 36, 36)) # Window
            pygame.draw.rect(s, wood, (130, 80, 36, 36), 3)
            # Roof tiles
            pygame.draw.polygon(s, roof, [(10, 70), (110, 10), (210, 70)])
            for i in range(10, 70, 10):
                pygame.draw.line(s, (90, 30, 20), (10+i, 70-i*0.6), (210-i, 70-i*0.6), 2)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_village_well(cls):
        key = ('village_well')
        if key not in cls._CACHE:
            s = pygame.Surface((80, 110), pygame.SRCALPHA)
            st, wd = (100, 100, 105), (75, 45, 30)
            pygame.draw.rect(s, st, (15, 70, 50, 35)) # Base
            for _ in range(8): pygame.draw.rect(s, (80, 80, 85), (random.randint(15, 55), random.randint(70, 100), 8, 4))
            pygame.draw.rect(s, wd, (20, 30, 6, 45))
            pygame.draw.rect(s, wd, (54, 30, 6, 45))
            pygame.draw.polygon(s, (120, 50, 40), [(10, 35), (40, 10), (70, 35)])
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_barrel(cls):
        key = ('barrel')
        if key not in cls._CACHE:
            s = pygame.Surface((40, 50), pygame.SRCALPHA)
            c = (100, 60, 30)
            pygame.draw.ellipse(s, c, (2, 2, 36, 46))
            pygame.draw.rect(s, (50, 50, 50), (2, 10, 36, 4)) # Iron band 1
            pygame.draw.rect(s, (50, 50, 50), (2, 35, 36, 4)) # Iron band 2
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_house_large(cls):
        key = ('house_l')
        if key not in cls._CACHE:
            s = pygame.Surface((280, 220), pygame.SRCALPHA)
            wall, roof, wood = (130, 120, 100), (100, 35, 25), (60, 45, 25)
            # Main Building
            pygame.draw.rect(s, wall, (40, 80, 200, 140))
            # Timber Frame (Medieval Style)
            for x in range(40, 241, 40):
                pygame.draw.line(s, wood, (x, 80), (x, 220), 4)
            pygame.draw.line(s, wood, (40, 150), (240, 150), 4)
            # Roof
            pygame.draw.polygon(s, roof, [(20, 90), (140, 10), (260, 90)])
            # Dormers
            pygame.draw.rect(s, roof, (80, 40, 40, 40))
            pygame.draw.rect(s, roof, (160, 40, 40, 40))
            # Windows
            for wx in [70, 170]:
                pygame.draw.rect(s, (100, 140, 180), (wx, 100, 40, 40))
                pygame.draw.rect(s, wood, (wx, 100, 40, 40), 2)
            # Door
            pygame.draw.rect(s, wood, (120, 160, 40, 60))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_city_skyline(cls, w=400, h=300):
        key = ('skyline', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            col = (20, 20, 30)
            # Faint background silhouettes
            for _ in range(8):
                bw = random.randint(40, 80)
                bh = random.randint(100, 250)
                bx = random.randint(0, w - bw)
                pygame.draw.rect(s, (15, 15, 25), (bx, h-bh, bw, bh))
                # Tiny dots for distant lights
                for _ in range(10):
                    lx, ly = random.randint(bx+5, bx+bw-5), random.randint(h-bh+5, h-5)
                    pygame.draw.rect(s, (40, 40, 60), (lx, ly, 2, 2))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_urban_building(cls, w=200, h=350, style=0):
        key = ('urban_build', w, h, style)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            wall_col = [(45, 45, 50), (60, 55, 50), (35, 40, 45)][style % 3]
            # Main Building
            pygame.draw.rect(s, wall_col, (0, 0, w, h))
            # Brick pattern
            for y in range(0, h, 15):
                for x in range(0, w, 30):
                    off = 15 if (y//15)%2 else 0
                    pygame.draw.rect(s, (int(wall_col[0]*0.8), int(wall_col[1]*0.8), int(wall_col[2]*0.8)), (x+off, y, 28, 13), 1)
            # Windows with glow
            for wy in range(40, h-40, 60):
                for wx in range(30, w-30, 50):
                    glow = random.choice([(255, 200, 100), (255, 255, 200), (40, 40, 60)])
                    pygame.draw.rect(s, glow, (wx, wy, 30, 40))
                    pygame.draw.rect(s, (20, 20, 20), (wx, wy, 30, 40), 2)
                    # Curtains (random)
                    if random.random() > 0.6:
                        pygame.draw.rect(s, (80, 40, 30), (wx, wy, 10, 40))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_street_lamp(cls):
        key = ('street_lamp')
        if key not in cls._CACHE:
            s = pygame.Surface((120, 240), pygame.SRCALPHA)
            col = (40, 40, 45)
            # Post
            pygame.draw.rect(s, col, (55, 40, 10, 200))
            # Double Arm
            pygame.draw.rect(s, col, (20, 35, 80, 10))
            # Lamps
            for lx in [20, 70]:
                pygame.draw.rect(s, (255, 255, 200), (lx, 20, 30, 15))
                pygame.draw.rect(s, col, (lx, 20, 30, 15), 2)
                # Light Cone (Composite onto the sprite)
                cone_surf = pygame.Surface((100, 200), pygame.SRCALPHA)
                for r in range(1, 40):
                    alpha = int(40 * (1 - r/40))
                    pygame.draw.polygon(cone_surf, (255, 255, 200, alpha), [(50, 0), (50-r*1.2, 200), (50+r*1.2, 200)])
                s.blit(cone_surf, (lx-35, 35))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_neon_sign(cls, text='BAR'):
        key = ('neon', text)
        if key not in cls._CACHE:
            f = pygame.font.SysFont('Arial', 24, bold=True)
            col = (100, 255, 100) if text == 'MARKET' else (100, 200, 255)
            t = f.render(text, True, col)
            s = pygame.Surface((t.get_width()+20, t.get_height()+10), pygame.SRCALPHA)
            # Glow backdrop
            for r in range(5, 0, -1):
                st = f.render(text, True, (col[0], col[1], col[2], 50))
                s.blit(st, (10, 5))
            s.blit(t, (10, 5))
            pygame.draw.rect(s, col, s.get_rect(), 2)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_med_bush(cls):
        key = ('med_bush')
        if key not in cls._CACHE:
            s = pygame.Surface((80, 50), pygame.SRCALPHA)
            col = (30, 80, 20)
            pygame.draw.ellipse(s, col, (0, 10, 80, 40))
            pygame.draw.ellipse(s, (50, 120, 40), (10, 5, 60, 35))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_bat(cls, frame=0, squished=False, flip=False, style=0):
        key = ('bat_v2', frame % 4, squished, flip, style)
        if key not in cls._CACHE:
            s = pygame.Surface((32, 32), pygame.SRCALPHA)
            C_OUT = (0, 0, 0)
            if style == 4: # Urban Surveillance Drone
                col = (80, 80, 90)
                pygame.draw.circle(s, C_OUT, (16, 16), 12)
                pygame.draw.circle(s, col, (16, 16), 10)
                pygame.draw.circle(s, (20, 20, 20), (16, 16), 10, 2)
                pygame.draw.circle(s, C_OUT, (16, 16), 6)
                pygame.draw.circle(s, (255, 50, 50), (16, 16), 4) # Scanning Lens
                # Rotors (Animated)
                wing_y = int(4 * math.sin(frame * math.pi * 0.5))
                pygame.draw.rect(s, C_OUT, (2, 12+wing_y, 12, 8), border_radius=2)
                pygame.draw.rect(s, (200, 200, 200), (4, 14+wing_y, 8, 4))
                pygame.draw.rect(s, C_OUT, (18, 12+wing_y, 12, 8), border_radius=2)
                pygame.draw.rect(s, (200, 200, 200), (20, 14+wing_y, 8, 4))
            elif style == 1: # Jellyfish
                col = (200, 150, 255)
                # Head
                pygame.draw.ellipse(s, C_OUT, (4, 0, 24, 20))
                pygame.draw.ellipse(s, col, (6, 2, 20, 16))
                pygame.draw.ellipse(s, (240, 200, 255), (8, 4, 16, 8)) # Highlight
                # Tentacles
                for tx in [10, 16, 22]:
                    wave = int(4 * math.sin(frame * 0.8 + tx))
                    pygame.draw.line(s, (150, 100, 220), (tx, 16), (tx + wave, 28), 3)
            else:
                col = (80, 50, 120)
                if squished:
                    pygame.draw.ellipse(s, C_OUT, (2, 10, 28, 12))
                    pygame.draw.ellipse(s, col, (4, 12, 24, 8))
                else:
                    wing_y = int(6 * math.sin(frame * math.pi * 0.5))
                    # Wings Behind
                    pygame.draw.polygon(s, C_OUT, [(16,12), (-2, 4+wing_y), (14,-2)])
                    pygame.draw.polygon(s, C_OUT, [(16,12), (34, 4+wing_y), (18,-2)])
                    pygame.draw.polygon(s, col, [(16,12), (0, 6+wing_y), (16,0)])
                    pygame.draw.polygon(s, col, [(16,12), (32, 6+wing_y), (16,0)])
                    # Body
                    pygame.draw.circle(s, C_OUT, (16, 12), 8)
                    pygame.draw.circle(s, col, (16, 12), 6)
                    # Eyes
                    pygame.draw.circle(s, C_OUT, (13, 10), 3)
                    pygame.draw.circle(s, C_OUT, (19, 10), 3)
                    pygame.draw.circle(s, (255,255,0), (13, 10), 2)
                    pygame.draw.circle(s, (255,255,0), (19, 10), 2)
            if flip: s = pygame.transform.flip(s, True, False)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_crab(cls, frame=0, squished=False, flip=False, style=0):
        key = ('crab_v2', frame % 4, squished, flip, style)
        if key not in cls._CACHE:
            s = pygame.Surface((38, 30), pygame.SRCALPHA)
            C_OUT = (0, 0, 0)
            if style == 4: # Security Security Bot
                col = (180, 180, 190)
                if squished: 
                    pygame.draw.rect(s, C_OUT, (0, 18, 38, 14), border_radius=2)
                    pygame.draw.rect(s, col, (2, 20, 34, 10))
                else:
                    pygame.draw.rect(s, C_OUT, (6, 8, 26, 20), border_radius=4)
                    pygame.draw.rect(s, col, (8, 10, 22, 16), border_radius=2) # Main frame
                    pygame.draw.rect(s, C_OUT, (8, 10, 22, 10))
                    pygame.draw.rect(s, (50, 150, 255), (10, 12, 18, 6)) # Visor
                    # Legs
                    walk = 4 if frame % 2 == 0 else -4
                    pygame.draw.line(s, C_OUT, (10, 26), (6+walk, 30), 6)
                    pygame.draw.line(s, (40, 40, 40), (10, 26), (6+walk, 30), 4)
                    pygame.draw.line(s, C_OUT, (28, 26), (32-walk, 30), 6)
                    pygame.draw.line(s, (40, 40, 40), (28, 26), (32-walk, 30), 4)
            else:
                col = (255, 80, 60)
                if squished:
                    pygame.draw.ellipse(s, C_OUT, (0, 18, 38, 14))
                    pygame.draw.ellipse(s, col, (2, 20, 34, 10))
                else:
                    walk = 4 if frame % 2 == 0 else -4
                    # Claws
                    pygame.draw.rect(s, C_OUT, (6+walk, 22, 10, 10))
                    pygame.draw.rect(s, C_OUT, (22-walk, 22, 10, 10))
                    pygame.draw.rect(s, (180, 40, 30), (8+walk, 24, 6, 6))
                    pygame.draw.rect(s, (180, 40, 30), (24-walk, 24, 6, 6))
                    # Body
                    pygame.draw.ellipse(s, C_OUT, (2, 8, 34, 22))
                    pygame.draw.ellipse(s, col, (4, 10, 30, 18))
                    # Eyes
                    pygame.draw.circle(s, C_OUT, (14, 14), 6)
                    pygame.draw.circle(s, C_OUT, (24, 14), 6)
                    pygame.draw.circle(s, (255,255,255), (14, 14), 5)
                    pygame.draw.circle(s, (255,255,255), (24, 14), 5)
                    pygame.draw.circle(s, (0,0,0), (14, 14), 2)
                    pygame.draw.circle(s, (0,0,0), (24, 14), 2)
            if flip: s = pygame.transform.flip(s, True, False)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_trash_can(cls):
        key = ('trash_can')
        if key not in cls._CACHE:
            s = pygame.Surface((40, 50), pygame.SRCALPHA)
            pygame.draw.rect(s, (100, 100, 105), (5, 10, 30, 40)) # Body
            for y in range(15, 50, 8):
                pygame.draw.line(s, (80, 80, 85), (5, y), (35, y), 2)
            pygame.draw.rect(s, (120, 120, 125), (2, 5, 36, 10)) # Lid
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_slime(cls, frame=0, squished=False):
        key = ('slime_v2', frame % 4, squished)
        if key not in cls._CACHE:
            s = pygame.Surface((34, 28), pygame.SRCALPHA)
            col = (100, 255, 80)
            C_OUT = (0, 0, 0)
            if squished:
                pygame.draw.ellipse(s, C_OUT, (0, 16, 34, 14))
                pygame.draw.ellipse(s, col, (2, 18, 30, 10))
            else:
                bounce = int(4 * abs(math.sin(frame * math.pi * 0.25)))
                pygame.draw.ellipse(s, C_OUT, (0, 2 + bounce, 34, 28 - bounce))
                pygame.draw.ellipse(s, col, (2, 4 + bounce, 30, 24 - bounce))
                pygame.draw.ellipse(s, (200, 255, 180), (6, 6 + bounce, 22, 8)) # Highlight
                # Eyes
                pygame.draw.circle(s, C_OUT, (10, 14 + bounce), 5)
                pygame.draw.circle(s, C_OUT, (24, 14 + bounce), 5)
                pygame.draw.circle(s, (255,255,255), (10, 14 + bounce), 4)
                pygame.draw.circle(s, (255,255,255), (24, 14 + bounce), 4)
                pygame.draw.circle(s, C_OUT, (11, 14 + bounce), 2)
                pygame.draw.circle(s, C_OUT, (23, 14 + bounce), 2)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_flower(cls, variant=0):
        key = ('flower', variant)
        if key not in cls._CACHE:
            s = pygame.Surface((24, 24), pygame.SRCALPHA)
            cols = [(255, 50, 50), (255, 255, 50), (255, 255, 255), (150, 100, 255)]
            color = cols[variant % len(cols)]
            pygame.draw.rect(s, (50, 150, 50), (11, 12, 2, 12)) # Stem
            for ang in range(0, 360, 72):
                rx = int(math.cos(math.radians(ang)) * 6) + 12
                ry = int(math.sin(math.radians(ang)) * 6) + 10
                pygame.draw.circle(s, color, (rx, ry), 5)
            pygame.draw.circle(s, (255, 220, 50), (12, 10), 4)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_cactus(cls, h=80):
        key = ('cactus', h)
        if key not in cls._CACHE:
            w = 40
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            col = (50, 140, 40)
            dcol = (30, 90, 25)
            # Main trunk
            pygame.draw.rect(s, dcol, (w//2-6, 10, 12, h-10), border_radius=6)
            pygame.draw.rect(s, col, (w//2-5, 12, 8, h-14), border_radius=4)
            # Arms
            pygame.draw.rect(s, dcol, (4, h//2, 10, 6), border_radius=2)
            pygame.draw.rect(s, dcol, (4, h//4, 6, h//4+2), border_radius=3)
            pygame.draw.rect(s, dcol, (w-14, h//3, 10, 6), border_radius=2)
            pygame.draw.rect(s, dcol, (w-10, h//6, 6, h//6+2), border_radius=3)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_crystal(cls, h=60, col_idx=0):
        key = ('crystal', h, col_idx)
        if key not in cls._CACHE:
            w = h // 2
            s = pygame.Surface((w, h + 20), pygame.SRCALPHA)
            cols = [(100, 200, 255), (255, 100, 255), (100, 255, 150)]
            base_col = cols[col_idx % len(cols)]
            # Glow
            for r in range(w, 0, -2):
                alpha = int(40 * (1 - r/w))
                pygame.draw.ellipse(s, (*base_col, alpha), (w//2-r, h//2-r, r*2, r*2+10))
            # Core
            pts = [(w//2, 0), (w, h//3), (w, h*2//3), (w//2, h), (0, h*2//3), (0, h//3)]
            pygame.draw.polygon(s, base_col, pts)
            pygame.draw.polygon(s, (255, 255, 255, 150), pts, 2)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_forest_bg(cls, w, h):
        key = ('forest_bg', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            col = (30, 70, 20, 180)
            pygame.draw.ellipse(s, col, (0, 0, w, h))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_pyramid(cls, w=400, h=300):
        key = ('pyramid', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            col = (190, 150, 80)
            dcol = (140, 110, 60)
            # Side 1 (Shadow)
            pygame.draw.polygon(s, dcol, [(0, h), (w//2, 0), (w//2, h)])
            # Side 2 (Light)
            pygame.draw.polygon(s, col, [(w//2, 0), (w, h), (w//2, h)])
            # Detail lines
            for i in range(10, h, 30):
                pygame.draw.line(s, (120, 90, 50), (0, i), (w, i), 1)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_spooky_tree(cls, h=200):
        key = ('spooky_tree', h)
        if key not in cls._CACHE:
            w = h
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Twisted, skeletal trunk
            trunk_col = (10, 10, 15)
            # Main Trunk
            pygame.draw.rect(s, trunk_col, (w//2-8, h-60, 16, 60))
            # Twisted branches
            def draw_spooky_branch(surf, x, y, angle, length, depth):
                if depth == 0: return
                rad = math.radians(angle - 90)
                nx = x + math.cos(rad) * length
                ny = y + math.sin(rad) * length
                pygame.draw.line(surf, trunk_col, (int(x), int(y)), (int(nx), int(ny)), depth*2)
                # Spooky glowing bulbs (from the red tree image)
                if depth < 3 and random.random() < 0.4:
                    pygame.draw.circle(surf, (200, 0, 0), (int(nx), int(ny)), 6)
                    pygame.draw.circle(surf, (255, 50, 50, 150), (int(nx), int(ny)), 10)
                
                draw_spooky_branch(surf, nx, ny, angle - random.randint(20, 45), length * 0.7, depth - 1)
                draw_spooky_branch(surf, nx, ny, angle + random.randint(20, 45), length * 0.7, depth - 1)

            draw_spooky_branch(s, w//2, h-60, 0, 50, 5)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_spooky_house(cls, w=300, h=350):
        key = ('spooky_house', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Silhouette with glowing windows
            col = (5, 5, 10)
            glow = (0, 255, 0) # Neon green glow from the image
            # Main house shape
            pygame.draw.rect(s, col, (w//4, h//2, w//2, h//2))
            # Roof
            pygame.draw.polygon(s, col, [(w//6, h//2+20), (w//2, h//4), (w-w//6, h//2+20)])
            # Tower
            pygame.draw.rect(s, col, (w//4-20, h//4, 40, h*3//4))
            pygame.draw.polygon(s, col, [(w//4-40, h//4+10), (w//4, 0), (w//4+20, h//4+10)])
            # Glowing Windows
            for wy in range(h//2+20, h-40, 60):
                for wx in [w//2-40, w//2+10]:
                    pygame.draw.rect(s, glow, (wx, wy, 30, 40))
                    # Glow effect
                    glow_surf = pygame.Surface((50, 60), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, (*glow, 80), (0, 0, 50, 60), border_radius=5)
                    s.blit(glow_surf, (wx-10, wy-10))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_spooky_moon(cls, w=150, h=150):
        key = ('spooky_moon', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 210), (w//2, h//2), w//2)
            pygame.draw.circle(s, (230, 230, 180), (w//2-10, h//2-10), w//8)
            pygame.draw.circle(s, (230, 230, 180), (w//2+15, h//2+5), w//12)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_tombstone(cls, variant=0):
        key = ('tombstone', variant)
        if key not in cls._CACHE:
            s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
            col = (60, 60, 70)
            if variant % 2 == 0: # Stone slab
                pygame.draw.rect(s, col, (10, 10, 28, 38), border_radius=5)
                pygame.draw.line(s, (40, 40, 50), (14, 20), (34, 20), 2) # R.I.P line
            else: # Cross
                pygame.draw.rect(s, col, (20, 5, 8, 43))
                pygame.draw.rect(s, col, (8, 15, 32, 8))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_spooky_fence(cls, w=TILE):
        key = ('spooky_fence', w)
        if key not in cls._CACHE:
            s = pygame.Surface((w, TILE), pygame.SRCALPHA)
            col = (10, 10, 15)
            # Vertical spikes
            for x in range(0, w, 12):
                pygame.draw.rect(s, col, (x, 10, 4, 38))
                pygame.draw.polygon(s, col, [(x-2, 10), (x+2, 0), (x+6, 10)])
            # Horizontal bars
            pygame.draw.rect(s, col, (0, 15, w, 4))
            pygame.draw.rect(s, col, (0, 35, w, 4))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_lollipop(cls, color=(255, 80, 100), h=150):
        key = ('lollipop', color, h)
        if key not in cls._CACHE:
            w = 40
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Stick
            pygame.draw.rect(s, (240, 230, 200), (w//2-3, 30, 6, h-30))
            # Candy Head
            pygame.draw.circle(s, color, (w//2, 20), 20)
            # Swirl
            for r in range(16, 0, -4):
                sw_col = (min(255, color[0]+40), min(255, color[1]+40), min(255, color[2]+40))
                pygame.draw.circle(s, sw_col, (w//2, 20), r, 2)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_candy_cane(cls, h=60):
        key = ('candy_cane', h)
        if key not in cls._CACHE:
            w = 30
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Cane Shape (Hooked)
            pts = [(5, h), (5, 15), (10, 5), (20, 5), (25, 15)]
            pygame.draw.lines(s, (255, 255, 255), False, pts, 8)
            # Stripes
            for i in range(0, h, 15):
                pygame.draw.line(s, (255, 50, 50), (5, h-i), (5, h-i-8), 8)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_cupcake(cls, w=80, h=100):
        key = ('cupcake', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Wrapper
            pygame.draw.polygon(s, (200, 100, 50), [(w//4, h), (w*3//4, h), (w-10, h//2), (10, h//2)])
            # Frosting
            pygame.draw.ellipse(s, (255, 150, 200), (5, h//2-20, w-10, 40))
            pygame.draw.circle(s, (255, 180, 220), (w//2, h//2-30), 25)
            # Cherry
            pygame.draw.circle(s, (220, 20, 40), (w//2, h//2-55), 8)
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_marshmallow_cloud(cls, w=120, h=60):
        key = ('marshmallow_cloud', w, h)
        if key not in cls._CACHE:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            col = (255, 240, 245, 200)
            pygame.draw.ellipse(s, col, (0, 10, 50, 40))
            pygame.draw.ellipse(s, col, (30, 0, 60, 50))
            pygame.draw.ellipse(s, col, (70, 10, 50, 40))
            cls._CACHE[key] = s
        return cls._CACHE[key]

    @classmethod
    def get_wafer_pillar(cls, h=200):
        key = ('wafer_pillar', h)
        if key not in cls._CACHE:
            w = 40
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Base brown
            pygame.draw.rect(s, (150, 100, 60), (0, 0, w, h))
            # Inset stripes
            for y in range(0, h, 20):
                pygame.draw.rect(s, (130, 80, 40), (0, y, w, 10))
            # Cream filling line
            pygame.draw.line(s, (255, 255, 255, 150), (w//2, 0), (w//2, h), 4)
            cls._CACHE[key] = s
        return cls._CACHE[key]

