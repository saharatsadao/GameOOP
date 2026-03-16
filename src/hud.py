import pygame, math, random
from .constants import *
from .assets.sprites import SpriteFactory

def get_font(size, bold=True):
    # 'Tahoma' and 'Leelawadee' are standard Thai fonts on Windows.
    # 'Angsana New', 'Cordia New', 'TH Sarabun New' are also common.
    font_names = ['tahoma', 'leelawadee', 'microsoftsansserif', 'arial', 'angsananew', 'cordianew', 'thsarabunnew']
    for f in font_names:
        try:
            return pygame.font.SysFont(f, size, bold=bold)
        except:
            continue
    return pygame.font.Font(None, size)

class HUD:
    def __init__(self):
        self.f_lbl = get_font(16, bold=False)
        self.f_val = get_font(24)

    def draw(self, surf, score, coins, hp, world_str="1-1"):
        # Dark Bar
        bar = pygame.Surface((SCREEN_W, 52), pygame.SRCALPHA)
        bar.fill((0, 0, 0, 155))
        surf.blit(bar, (0, 0))

        # Stats
        def draw_text(text, x, y, font, color=UI_WHITE):
            img = font.render(text, True, color)
            surf.blit(img, (x, y))

        draw_text("HEALTH", 20, 2, self.f_lbl, (180, 180, 180))
        # Heart Icons
        for i in range(3):
            is_active = i < hp
            # Pulsing effect
            pulse = 0
            if is_active:
                speed = 0.01 if hp > 1 else 0.02
                pulse = int(4 * math.sin(pygame.time.get_ticks() * speed))
            
            size = 28 + pulse
            img = SpriteFactory.get_heart(size)
            
            if not is_active:
                # Ghost heart: Dark grey and semi-transparent
                ghost = img.copy()
                ghost.fill((40, 40, 40, 100), special_flags=pygame.BLEND_RGBA_MULT)
                img = ghost
            
            surf.blit(img, (20 + i*32 - (size-28)//2, 20 - (size-28)//2))
        
        draw_text("SCORE", 200, 4, self.f_lbl, (180, 180, 180))
        draw_text(f"{score:07d}", 200, 22, self.f_val)

        # Coins
        coin_sprite = SpriteFactory.get_coin(0)
        surf.blit(coin_sprite, (390, 18))
        draw_text(f"x{coins:02d}", 425, 22, self.f_val, UI_GOLD)

        draw_text("WORLD", 550, 4, self.f_lbl, (180, 180, 180))
        draw_text(world_str, 550, 22, self.f_val)

        # Back Button
        self.back_btn_rect = pygame.Rect(SCREEN_W - 140, 6, 120, 40)
        btn_surf = pygame.Surface((120, 40), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (255, 255, 255, 40), (0, 0, 120, 40), border_radius=8)
        pygame.draw.rect(btn_surf, (255, 255, 255, 80), (0, 0, 120, 40), 2, border_radius=8)
        surf.blit(btn_surf, self.back_btn_rect)
        
        btn_text = self.f_lbl.render("< BACK(ESC)", True, UI_WHITE)
        surf.blit(btn_text, (SCREEN_W - 140 + 60 - btn_text.get_width()//2, 6 + 20 - btn_text.get_height()//2))

class MenuScreen:
    def __init__(self):
        self.ft = get_font(56)
        self.fs = get_font(32)
        self.time = 0.0
        try:
            self.bg = pygame.image.load(r'src\assets\bg_select.png').convert()
            self.bg = pygame.transform.smoothscale(self.bg, (SCREEN_W, SCREEN_H))
        except:
            self.bg = None

    def update(self, dt):
        self.time += dt

    def draw(self, surf):
        if self.bg:
            surf.blit(self.bg, (0, 0))
            # Dark overlay for readability
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 10, 80))
            surf.blit(overlay, (0, 0))
        else:
            # Background Gradient fallback
            for y in range(SCREEN_H):
                t = y / SCREEN_H
                r = int(15 + (60-15)*t)
                g = int(20 + (100-20)*t)
                b = int(50 + (180-50)*t)
                pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_W, y))

        # Title with Premium Glow (Static)
        title_text = "Eden of the Continuum"
        
        # 1. Deep Shadow
        title_sh = self.ft.render(title_text, True, (0, 0, 10))
        # 2. Outer Glow Layer
        title_glow = self.ft.render(title_text, True, (255, 100, 0)) # Orange-ish glow
        # 3. Main Text
        title = self.ft.render(title_text, True, (255, 240, 150)) # Pale Gold
        
        tx = SCREEN_W // 2 - title.get_width() // 2
        ty = 180
        
        # Draw layers
        surf.blit(title_sh, (tx + 5, ty + 5)) # Deep shadow
        
        # Subtle glow offset
        for offset in [(2,2), (-2,-2), (2,-2), (-2,2)]:
            glow_alpha = int(100 + 50 * math.sin(self.time * 3))
            scaled_glow = title_glow.copy()
            scaled_glow.set_alpha(glow_alpha)
            surf.blit(scaled_glow, (tx + offset[0], ty + offset[1]))
            
        surf.blit(title, (tx, ty))

        # --- SHIMMER EFFECT (Strict Masking) ---
        tw, th = title.get_width(), title.get_height()
        # Use a non-alpha surface with black background for colorkey masking
        shimmer_surf = pygame.Surface((tw, th))
        shimmer_surf.fill((0, 0, 0))
        
        s_prog = (self.time % 3.0) / 3.0
        sx = -200 + s_prog * (tw + 400)
        
        # Draw the glossy beam (White on Black)
        for xo in range(60):
            a = int(140 * (1.0 - abs(xo - 30) / 30))
            pygame.draw.line(shimmer_surf, (a, a, a), (sx + xo, 0), (sx + xo - 40, th), 3)
        
        # Mask with the title's shape (Multiply by mask)
        mask = self.ft.render(title_text, True, (255, 255, 255))
        shimmer_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Make black transparent
        shimmer_surf.set_colorkey((0, 0, 0))
        
        # Blit to screen with ADD for that glowing glossy look
        surf.blit(shimmer_surf, (tx, ty), special_flags=pygame.BLEND_RGBA_ADD)

        # Pulse "Press ENTER" with subtle shadow
        alpha = int(180 + 75 * math.sin(self.time * 4))
        prompt_sh = self.fs.render("Press ENTER to Start", True, (20, 20, 20))
        prompt_img = self.fs.render("Press ENTER to Start", True, (alpha, alpha, alpha))
        px = SCREEN_W // 2 - prompt_img.get_width() // 2
        py = 420
        surf.blit(prompt_sh, (px+2, py+2))
        surf.blit(prompt_img, (px, py))

class LevelSelectScreen:
    def __init__(self):
        self.ft = get_font(52)
        self.fn = get_font(28)
        self.fs = get_font(18, bold=False)
        self.sel = 0
        self.time = 0.0
        try:
            self.bg = pygame.image.load(r'C:\Users\asus\.gemini\antigravity\brain\08d7ff1c-0d25-4c8e-80a3-7a55b4d81555\media__1773633266353.jpg').convert()
            self.bg = pygame.transform.smoothscale(self.bg, (SCREEN_W, SCREEN_H))
        except:
            self.bg = None
        self.thumbnails = {}

    def _get_thumbnail(self, name, col):
        if name not in self.thumbnails:
            tw, th = 130, 80
            s = pygame.Surface((tw, th), pygame.SRCALPHA)
            if name == "1-1":
                # Sky Kingdom: Bright sky + Fluffy Clouds
                for y in range(th):
                    pygame.draw.line(s, (100, 180, 255 - y//4), (0, y), (tw, y))
                # Fluffy clouds
                for _ in range(3):
                    cx, cy = random.randint(20, tw-20), random.randint(20, th-40)
                    pygame.draw.circle(s, (255, 255, 255, 200), (cx, cy), 12)
                    pygame.draw.circle(s, (255, 255, 255, 200), (cx-8, cy+4), 8)
                    pygame.draw.circle(s, (255, 255, 255, 200), (cx+8, cy+4), 8)
                # Sun hint
                pygame.draw.circle(s, (255, 255, 200, 100), (20, 15), 10)
            elif name == "1-2":
                # Halloween: Dark purple + Detailed Moon + Tombstones
                for y in range(th):
                    pygame.draw.line(s, (15, 0, 30 + y//8), (0, y), (tw, y))
                # Moon with crater detail
                pygame.draw.circle(s, (255, 255, 210), (tw-30, 22), 14)
                pygame.draw.circle(s, (230, 230, 180), (tw-35, 18), 3)
                pygame.draw.circle(s, (230, 230, 180), (tw-25, 26), 2)
                # Tombstone silhouettes
                for x in (20, 50, 80):
                    pygame.draw.rect(s, (5, 5, 10), (x, th-15, 12, 15), border_top_left_radius=4, border_top_right_radius=4)
                # Bat silhouettes
                pygame.draw.polygon(s, (0,0,0), [(30,20), (25,18), (35,18)])
                pygame.draw.polygon(s, (0,0,0), [(70,30), (65,28), (75,28)])
            elif name == "1-3":
                # Candy Land: Peach-Pink Gradient + Detailed Lollipops
                for y in range(th):
                    t = y / th
                    r = 255
                    g = int(180 + 40 * t)
                    b = int(210 + 20 * t)
                    pygame.draw.line(s, (r, g, b), (0, y), (tw, y))
                # Lollipops with swirls
                for x, h in [(30, 30), (70, 40), (105, 35)]:
                    pygame.draw.rect(s, (245, 235, 215), (x-1, th-h, 2, h))
                    col = random.choice([(255,100,100), (100,255,150), (150,200,255)])
                    pygame.draw.circle(s, col, (x, th-h), 10)
                    pygame.draw.circle(s, (255,255,255,150), (x, th-h), 6, 1) # Swirl
            elif name == "1-4":
                # Urban Night: Cityscape + Glowing Windows
                for y in range(th):
                    pygame.draw.line(s, (5, 5, 20 + y//4), (0, y), (tw, y))
                # Skyscraper silhouettes
                for x, w, h, c in [(15, 25, 50, 15), (45, 35, 65, 10), (85, 30, 45, 20)]:
                    pygame.draw.rect(s, (c, c, c+10), (x, th-h, w, h))
                    # Individual windows
                    for wy in range(th-h+5, th-5, 8):
                        for wx in range(x+4, x+w-4, 8):
                            if random.random() < 0.6:
                                pygame.draw.rect(s, (255, 220, 100), (wx, wy, 3, 3))
            else:
                s.fill(col)
            pygame.draw.rect(s, (0,0,0,100), (0, 0, tw, th), 2, border_radius=8)
            self.thumbnails[name] = s
        return self.thumbnails[name]

    def update(self, dt):
        self.time += dt

    def draw(self, surf, unlocked_levels={(1,1)}):
        # Background Image or Solid Color
        if self.bg:
            surf.blit(self.bg, (0, 0))
            # Dark Overlay for cool/dark look and readability
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 10, 160))
            surf.blit(overlay, (0, 0))
        else:
            surf.fill((5, 5, 15))
        
        # Animated Neon Grid (Slightly more subtle over image)
        grid_col = (40, 60, 100, 80)
        spacing = 40
        offset = (self.time * 20) % spacing
        s_grid = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for x in range(0, SCREEN_W + spacing, spacing):
            pygame.draw.line(s_grid, grid_col, (x - offset, 0), (x - offset - 100, SCREEN_H))
        for y in range(0, SCREEN_H + spacing, spacing):
            progress = y / SCREEN_H
            a = int(80 * progress)
            pygame.draw.line(s_grid, (*grid_col[:3], a), (0, y), (SCREEN_W, y))
        surf.blit(s_grid, (0, 0))

        # Title with Glow
        title_text = "SELECT MISSION"
        title_img = self.ft.render(title_text, True, (100, 200, 255))
        glow_img = self.ft.render(title_text, True, (0, 100, 200))
        glow_off = int(2 * math.sin(self.time * 3))
        surf.blit(glow_img, (SCREEN_W//2 - title_img.get_width()//2 + glow_off, 54))
        surf.blit(title_img, (SCREEN_W//2 - title_img.get_width()//2, 50))

        worlds = [
            ("1-1", "SKY KINGDOM", (100, 180, 255)),
            ("1-2", "HALLOWEEN", (180, 50, 255)),
            ("1-3", "CANDY LAND", (255, 150, 200)),
            ("1-4", "URBAN NIGHT", (60, 100, 200))
        ]

        for i, (name, d, col) in enumerate(worlds):
            x = 80 + i * 180
            rect = pygame.Rect(x, 200, 150, 180)
            
            # Glassmorphism Card
            card = pygame.Surface((150, 180), pygame.SRCALPHA)
            alpha = 40 if i != self.sel else 80
            pygame.draw.rect(card, (255, 255, 255, alpha), (0, 0, 150, 180), border_radius=12)
            pygame.draw.rect(card, (255, 255, 255, 60), (0, 0, 150, 180), 2, border_radius=12)
            surf.blit(card, (x, 200))

            # Selection Glow
            if i == self.sel:
                glow_alpha = int(155 + 100 * math.sin(self.time * 6))
                s_col = (*col, glow_alpha)
                pygame.draw.rect(surf, s_col, rect.inflate(8, 8), 3, border_radius=14)
                pygame.draw.rect(surf, s_col, rect.inflate(16, 16), 1, border_radius=16)

            # Check if unlocked
            is_unlocked = (int(name.split('-')[0]), int(name.split('-')[1])) in unlocked_levels

            # World Theme Icon/Preview (Procedural)
            thumb = self._get_thumbnail(name, col)
            if not is_unlocked:
                locked_thumb = thumb.copy()
                locked_thumb.fill((40, 40, 40, 255), special_flags=pygame.BLEND_RGBA_MULT)
                thumb = locked_thumb

            surf.blit(thumb, (x + 10, 210))
            pygame.draw.rect(surf, (255,255,255,40), (x+10, 210, 130, 80), 1, border_radius=8)

            # Lock Icon if locked
            if not is_unlocked:
                pygame.draw.circle(surf, (20, 20, 20, 200), (x + 75, 250), 20)
                # Simple padlock draw
                pygame.draw.rect(surf, (180, 180, 180), (x+75-8, 250-2, 16, 12))
                pygame.draw.rect(surf, (180, 180, 180), (x+75-5, 250-10, 10, 10), 2)

            # Text Labels
            lbl_col = UI_WHITE if is_unlocked else (100, 100, 100)
            lbl = self.fn.render(name, True, lbl_col)
            surf.blit(lbl, (x + 75 - lbl.get_width()//2, 305))
            
            desc_col = (180, 180, 180) if is_unlocked else (70, 70, 70)
            desc = self.fs.render(d, True, desc_col)
            surf.blit(desc, (x + 75 - desc.get_width()//2, 340))

        # Bottom UI hint
        hint = self.fs.render("USE ARROWS TO NAVIGATE • SPACE TO DEPLOY", True, (100, 100, 100))
        surf.blit(hint, (SCREEN_W//2 - hint.get_width()//2, 550))

        # Back Button
        self.back_btn_rect = pygame.Rect(20, 20, 120, 40)
        btn_surf = pygame.Surface((120, 40), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (255, 255, 255, 40), (0, 0, 120, 40), border_radius=8)
        pygame.draw.rect(btn_surf, (255, 255, 255, 80), (0, 0, 120, 40), 2, border_radius=8)
        surf.blit(btn_surf, self.back_btn_rect)
        
        btn_text = self.fs.render("< BACK", True, UI_WHITE)
        surf.blit(btn_text, (20 + 60 - btn_text.get_width()//2, 20 + 20 - btn_text.get_height()//2))

class GameOverScreen:
    def __init__(self):
        self.ft = get_font(64)
        self.fs = get_font(32)
        self.btn_font = get_font(24)
        self.time = 0
        self.retry_rect = pygame.Rect(SCREEN_W//2 - 160, 350, 140, 50)
        self.menu_rect = pygame.Rect(SCREEN_W//2 + 20, 350, 140, 50)

    def update(self, dt):
        self.time += dt

    def draw(self, surf):
        # Dim background
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surf.blit(overlay, (0, 0))

        # Message
        msg = "คุณตายแล้ว"
        pulse = int(5 * math.sin(self.time * 4))
        
        # Shadow for better readability
        sh_img = self.ft.render(msg, True, (20, 0, 0))
        surf.blit(sh_img, (SCREEN_W//2 - sh_img.get_width()//2 + 4, 180 + pulse + 4))
        
        msg_img = self.ft.render(msg, True, (255, 50, 50))
        surf.blit(msg_img, (SCREEN_W//2 - msg_img.get_width()//2, 180 + pulse))

        # Buttons
        for rect, text in [(self.retry_rect, "เล่นใหม่"), (self.menu_rect, "หน้าหลัก")]:
            # Highlight on hover
            mx, my = pygame.mouse.get_pos()
            hover = rect.collidepoint(mx, my)
            
            # Use a temporary surface for transparency
            btn_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            bg_alpha = 100 if hover else 60
            pygame.draw.rect(btn_surf, (255, 255, 255, bg_alpha), (0, 0, rect.width, rect.height), border_radius=10)
            pygame.draw.rect(btn_surf, (255, 255, 255, 200 if hover else 120), (0, 0, rect.width, rect.height), 2, border_radius=10)
            surf.blit(btn_surf, rect.topleft)
            
            t_img = self.btn_font.render(text, True, UI_WHITE)
            surf.blit(t_img, (rect.centerx - t_img.get_width()//2, rect.centery - t_img.get_height()//2))

class LevelClearScreen:
    def __init__(self):
        self.ft = get_font(64)
        self.fs = get_font(32)
        self.btn_font = get_font(24)
        self.time = 0
        self.menu_rect = pygame.Rect(SCREEN_W//2 - 160, 350, 140, 50)
        self.next_rect = pygame.Rect(SCREEN_W//2 + 20, 350, 140, 50)

    def update(self, dt):
        self.time += dt

    def draw(self, surf):
        # Dim background
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surf.blit(overlay, (0, 0))

        # Message with Heroic Glow (Static)
        msg = "ยินดีด้วย!"
        
        # Layers
        sh_img = self.ft.render(msg, True, (10, 40, 10)) # Dark green shadow
        glow_img = self.ft.render(msg, True, (255, 255, 100)) # Yellow glow
        msg_img = self.ft.render(msg, True, (100, 255, 100)) # Bright green
        
        mx = SCREEN_W//2 - msg_img.get_width()//2
        my = 180
        
        # Draw shadow
        surf.blit(sh_img, (mx + 4, my + 4))
        
        # Glow pulses
        g_alpha = int(120 + 80 * math.sin(self.time * 6))
        scaled_glow = glow_img.copy()
        scaled_glow.set_alpha(g_alpha)
        for ox, oy in [(2,0), (-2,0), (0,2), (0,-2)]:
            surf.blit(scaled_glow, (mx + ox, my + oy))
            
        surf.blit(msg_img, (mx, my))

        # --- SHIMMER EFFECT (Strict Masking) ---
        mw, mh = msg_img.get_width(), msg_img.get_height()
        sh_surf = pygame.Surface((mw, mh))
        sh_surf.fill((0, 0, 0))
        
        s_prog = (self.time % 2.0) / 2.0
        sx = -100 + s_prog * (mw + 200)
        for xo in range(40):
            a = int(160 * (1.0 - abs(xo - 20) / 20))
            pygame.draw.line(sh_surf, (a, a, a), (sx + xo, 0), (sx + xo - 20, mh), 2)
            
        v_mask = self.ft.render(msg, True, (255, 255, 255))
        sh_surf.blit(v_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        sh_surf.set_colorkey((0, 0, 0))
        surf.blit(sh_surf, (mx, my), special_flags=pygame.BLEND_RGBA_ADD)

        # Buttons
        for rect, text in [(self.next_rect, "ด่านถัดไป"), (self.menu_rect, "หน้าหลัก")]:
            mx, my = pygame.mouse.get_pos()
            hover = rect.collidepoint(mx, my)
            
            btn_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            bg_alpha = 100 if hover else 60
            pygame.draw.rect(btn_surf, (255, 255, 255, bg_alpha), (0, 0, rect.width, rect.height), border_radius=10)
            pygame.draw.rect(btn_surf, (255, 255, 255, 200 if hover else 120), (0, 0, rect.width, rect.height), 2, border_radius=10)
            surf.blit(btn_surf, rect.topleft)
            
            t_img = self.btn_font.render(text, True, UI_WHITE)
            surf.blit(t_img, (rect.centerx - t_img.get_width()//2, rect.centery - t_img.get_height()//2))
