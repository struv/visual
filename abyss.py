#!/usr/bin/env python3
"""Underwater abyss - procedural ASCII deep sea explorer."""

import math, time, random, sys, os

sys.stdout.reconfigure(encoding='utf-8')
W, H = 75, 38
CHARS = " .,-~:;=*#%@░▒▓█"

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

class Abyss:
    def __init__(self):
        self.coral = [[0]*W for _ in range(H)]
        self.bubbles, self.fish, self.particles = [], [], []
        self.kelp = [{'x': random.randint(5,W-5), 'h': random.randint(8,18)} for _ in range(12)]
        self._seed_coral()
        for _ in range(6): self.fish.append(self._new_fish())
        for _ in range(40): self.particles.append([random.random()*W, random.random()*H])

    def _seed_coral(self):
        for _ in range(8):
            x, y = random.randint(10,W-10), random.randint(H-8,H-2)
            for _ in range(random.randint(15,40)):
                if 0<=x<W and 0<=y<H: self.coral[y][x] = min(self.coral[y][x]+1, 5)
                x += random.choice([-1,0,0,1]); y += random.choice([-1,0,0,1,1])

    def _new_fish(self):
        return {'x': random.random()*W, 'y': random.randint(5,H-10),
                'vx': random.choice([-1,1])*random.uniform(0.3,1.2), 'vy': 0,
                'char': random.choice(["><>", "<><", ">->", "<-<", "°bg", "db°"])}

    def _grow_coral(self):
        if random.random() < 0.02:
            y, x = random.randint(H-10,H-1), random.randint(0,W-1)
            if self.coral[y][x] > 0:
                nx, ny = x+random.choice([-1,0,1]), y+random.choice([-1,0,1])
                if 0<=nx<W and 0<=ny<H: self.coral[ny][nx] = min(self.coral[ny][nx]+1, 5)

    def render(self, t):
        grid = [[' ']*W for _ in range(H)]
        current = math.sin(t*0.3)*2 + math.sin(t*0.7)*0.5
        pressure_wave = t % 12 < 0.5

        # Light gradient from surface
        for y in range(H):
            for x in range(W):
                depth = y / H
                light = max(0, 1 - depth*1.2) * (0.8 + 0.2*math.sin(t*0.5 + x*0.1))
                if light > 0.6: grid[y][x] = '.'
                elif light > 0.3 and random.random() < 0.1: grid[y][x] = ','

        # Coral reef (cellular automata growth)
        self._grow_coral()
        coral_chars = " .;*#%@▒▓"
        for y in range(H):
            for x in range(W):
                if self.coral[y][x] > 0:
                    biolum = (math.sin(t*2 + x*0.3 + y*0.2) + 1) / 2
                    idx = min(self.coral[y][x] + int(biolum*2), len(coral_chars)-1)
                    grid[y][x] = coral_chars[idx]

        # Kelp (wave equation with damping)
        for k in self.kelp:
            base_x, h = k['x'], k['h']
            for i in range(h):
                y = H - 2 - i
                damping = 1 - (i / h) * 0.3
                sway = math.sin(t*1.5 + i*0.4) * (i/h) * 3 * damping
                x = int(base_x + sway + current*0.3) % W
                if 0 <= y < H:
                    char = '|' if i % 3 == 0 else ('/' if sway > 0 else '\\')
                    if random.random() < 0.05: char = '*'  # biolum spore
                    grid[y][x] = char

        # Particles (Brownian motion)
        for p in self.particles:
            p[0] += random.gauss(0, 0.5) + current*0.15
            p[1] += random.gauss(0, 0.3)
            p[0], p[1] = p[0] % W, max(0, min(H-1, p[1]))
            px, py = int(p[0]), int(p[1])
            if grid[py][px] == ' ': grid[py][px] = '.' if random.random() > 0.3 else ','

        # Fish (path math with schooling tendency)
        for f in self.fish:
            f['vy'] = math.sin(t*2 + f['x']*0.1) * 0.3
            f['x'] += f['vx'] + current*0.2
            f['y'] += f['vy']
            f['y'] = max(3, min(H-8, f['y']))
            if f['x'] < -5 or f['x'] > W+5: f['vx'] *= -1; f['x'] = max(-4, min(W+4, f['x']))
            if random.random() < 0.01: f['vy'] += random.gauss(0, 0.5)
            fx, fy = int(f['x']), int(f['y'])
            chars = f['char'] if f['vx'] > 0 else f['char'][::-1]
            for i, c in enumerate(chars):
                nx = fx + i
                if 0 <= nx < W and 0 <= fy < H and grid[fy][nx] in ' .,':
                    grid[fy][nx] = c

        # Bubbles (rising with wobble)
        if random.random() < 0.15:
            self.bubbles.append([random.randint(5,W-5), H-1, random.uniform(0.3,0.8)])
        for b in self.bubbles[:]:
            b[1] -= b[2]
            b[0] += math.sin(t*4 + b[0]) * 0.3 + current*0.1
            if b[1] < 0: self.bubbles.remove(b); continue
            bx, by = int(b[0]) % W, int(b[1])
            if 0 <= by < H and grid[by][bx] in ' .,':
                grid[by][bx] = 'O' if b[2] > 0.6 else 'o' if b[2] > 0.4 else '°'

        # Anemone tendrils at coral bases
        for y in range(H-6, H):
            for x in range(W):
                if self.coral[y][x] > 2 and y > 0 and grid[y-1][x] == ' ':
                    wave = math.sin(t*3 + x*0.5)
                    if abs(wave) > 0.5:
                        grid[y-1][x] = '~' if wave > 0 else '-'

        # Bioluminescent pulse (deep zone)
        for y in range(H*2//3, H):
            for x in range(W):
                pulse = math.sin(t*1.2 + x*0.15 + y*0.1)
                if pulse > 0.85 and grid[y][x] == ' ':
                    grid[y][x] = '●' if pulse > 0.95 else '○' if pulse > 0.9 else '*'

        # Pressure wave distortion
        if pressure_wave:
            wave_y = int((t % 12) / 0.5 * H) % H
            if 0 <= wave_y < H:
                shift = random.randint(1, 3)
                grid[wave_y] = grid[wave_y][shift:] + grid[wave_y][:shift]

        # Occasional deep shadow
        if random.random() < 0.01:
            sy = random.randint(H//2, H-1)
            for x in range(W):
                if random.random() < 0.3: grid[sy][x] = '░'

        return grid

    def display(self, grid):
        clear()
        sys.stdout.write('\n'.join(''.join(r) for r in grid) + '\n')
        sys.stdout.flush()

def main():
    abyss = Abyss()
    t0 = time.time()
    try:
        while True:
            abyss.display(abyss.render(time.time() - t0))
            time.sleep(0.18)
    except KeyboardInterrupt:
        clear(); print("Surfacing...")

if __name__ == "__main__": main()
