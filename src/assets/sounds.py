import math
import array
import pygame
import random
from ..constants import *

SR = 22050

def _sound_from_samples(samples):
    buf = bytearray()
    for s in samples:
        v = int(max(-1.0, min(1.0, s)) * 32767)
        lo, hi = v & 0xFF, (v >> 8) & 0xFF
        buf.extend([lo, hi, lo, hi]) # Stereo
    return pygame.mixer.Sound(buffer=bytes(buf))

def _sine(freq, dur, vol=0.5):
    n = int(SR * dur)
    return [vol * math.sin(2 * math.pi * freq * i / SR) for i in range(n)]

def _square(freq, dur, vol=0.4):
    n = int(SR * dur)
    return [vol * (1.0 if math.sin(2*math.pi*freq*i/SR) >= 0 else -1.0) for i in range(n)]

def _sweep(f0, f1, dur, vol=0.5, wave='sine'):
    n = int(SR * dur)
    out = []
    for i in range(n):
        f = f0 + (f1 - f0) * (i / n)
        v = math.sin(2 * math.pi * f * (i/SR)) if wave == 'sine' else (1.0 if math.sin(2*math.pi*f*(i/SR)) >= 0 else -1.0)
        out.append(vol * v * (1.0 - i/n))
    return out

class SoundManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def init(self):
        if not self.initialized:
            pygame.mixer.stop() # Ensure clean start
            self.sounds = {
                'jump': _sound_from_samples(_sweep(300, 800, 0.2, wave='square')),
                'coin': _sound_from_samples(_sine(1047, 0.08) + _sine(1319, 0.15)),
                'stomp': _sound_from_samples([0.5*(random.random()*2-1)*(1-i/(SR*0.1)) for i in range(int(SR*0.1))]),
                'block': _sound_from_samples(_square(180, 0.1)),
                'death': _sound_from_samples(_sweep(600, 80, 0.8, wave='square'))
            }
            self.muted = False
            self.initialized = True

    def play(self, name):
        if self.initialized and not self.muted:
            s = self.sounds.get(name)
            if s: s.play()

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted: pygame.mixer.pause()
        else: pygame.mixer.unpause()

# Global Instance
sounds = SoundManager()
