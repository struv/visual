#!/usr/bin/env python3
"""Cyber-noir ASCII metropolis - a mathematically evolving cyberpunk city."""

import math
import time
import random
import sys
import os

WIDTH, HEIGHT = 80, 40
CHARS = " .,-~:;=!*#%@░▒▓█"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def noise(x, y, t, scale=0.1):
    """Pseudo-noise function using trig combinations."""
    return (math.sin(x * scale + t) * math.cos(y * scale * 0.7 + t * 0.5) +
            math.sin((x + y) * scale * 0.5 + t * 1.3) * 0.5)

def building_height(x, t):
    """Procedural building heights with subtle temporal glitch."""
    base = abs(math.sin(x * 0.3) * 20 + math.cos(x * 0.17) * 10)
    glitch = random.random() * 0.5 if random.random() < 0.02 else 0
    return int(base + 5 + glitch)

class City:
    def __init__(self):
        self.buildings = []
        self.rain = [[0.0] * WIDTH for _ in range(HEIGHT)]
        self.holograms = []
        self.traffic = []
        self.puddles = []
        self.matrix_drips = []
        self._init_city()

    def _init_city(self):
        # Generate building positions and base heights
        x = 2
        while x < WIDTH - 2:
            w = random.randint(4, 12)
            h = random.randint(12, 30)
            self.buildings.append({'x': x, 'w': w, 'h': h, 'neon': random.random()})
            x += w + random.randint(1, 4)

        # Initialize holograms
        for _ in range(3):
            self.holograms.append({
                'x': random.randint(10, WIDTH - 20),
                'y': random.randint(5, 15),
                'phase': random.random() * math.pi * 2,
                'freq': random.uniform(0.5, 2.0),
                'char': random.choice(['▓', '▒', '░', '@', '#'])
            })

        # Traffic positions on street level
        for _ in range(5):
            self.traffic.append({
                'x': random.randint(0, WIDTH),
                'speed': random.uniform(0.3, 1.5),
                'char': random.choice(['>', '»', '→', '*'])
            })

        # Puddle positions
        for _ in range(8):
            self.puddles.append({
                'x': random.randint(5, WIDTH - 5),
                'w': random.randint(3, 8)
            })

        # Matrix drips
        for _ in range(15):
            self.matrix_drips.append({
                'x': random.randint(0, WIDTH - 1),
                'y': random.random() * HEIGHT,
                'speed': random.uniform(0.5, 2.0),
                'length': random.randint(3, 8)
            })

    def render(self, t):
        grid = [[' '] * WIDTH for _ in range(HEIGHT)]

        # Street level (ground)
        street_y = HEIGHT - 5

        # Draw fog in lower section
        for y in range(street_y, HEIGHT):
            for x in range(WIDTH):
                fog_intensity = noise(x, y, t * 0.3, 0.15) * 0.5 + 0.5
                fog_intensity *= (y - street_y) / 5
                if fog_intensity > 0.3:
                    grid[y][x] = '░' if fog_intensity < 0.6 else '▒'

        # Draw perspective street lines converging to center
        vanish_x, vanish_y = WIDTH // 2, street_y - 10
        for x in range(WIDTH):
            # Street markings with perspective
            dist_from_center = abs(x - WIDTH // 2)
            if dist_from_center > 5:
                perspective_y = street_y + int((HEIGHT - street_y) * (1 - dist_from_center / (WIDTH // 2)) * 0.3)
                if 0 <= perspective_y < HEIGHT:
                    grid[perspective_y][x] = '-' if (x + int(t * 3)) % 4 == 0 else ' '

        # Draw buildings
        for b in self.buildings:
            bx, bw, bh = b['x'], b['w'], b['h']
            neon_phase = b['neon']

            # Building glitch offset
            glitch_offset = 1 if random.random() < 0.01 else 0

            for by in range(max(0, street_y - bh), street_y):
                for dx in range(bw):
                    x = bx + dx + glitch_offset
                    if 0 <= x < WIDTH:
                        # Building edge
                        if dx == 0 or dx == bw - 1:
                            grid[by][x] = '|'
                        # Building top
                        elif by == street_y - bh:
                            grid[by][x] = '='
                        # Windows / neon
                        else:
                            window_on = (dx % 3 == 1 and by % 4 == 2)
                            neon_pulse = math.sin(t * 2 + neon_phase * 10 + bx * 0.1)

                            if window_on and neon_pulse > 0.3:
                                intensity = int((neon_pulse + 1) * 3)
                                grid[by][x] = CHARS[min(intensity + 8, len(CHARS) - 1)]
                            elif random.random() < 0.02:  # Glitch
                                grid[by][x] = random.choice(['#', '%', '@', '░'])
                            else:
                                grid[by][x] = '.' if window_on else ' '

            # Rooftop antenna
            if bx + bw // 2 < WIDTH:
                antenna_x = bx + bw // 2
                for ay in range(max(0, street_y - bh - 3), street_y - bh):
                    if 0 <= antenna_x < WIDTH:
                        blink = '*' if math.sin(t * 5 + bx) > 0.7 else '|'
                        grid[ay][antenna_x] = blink if ay == street_y - bh - 3 else '|'

        # Draw holograms (floating, pulsing)
        for h in self.holograms:
            visibility = (math.sin(t * h['freq'] + h['phase']) + 1) / 2
            if visibility > 0.3:
                hx, hy = h['x'], h['y']
                warp = int(math.sin(t * 3 + h['phase']) * 2)

                # Hologram shape (simple rectangle with distortion)
                for dy in range(-2, 3):
                    for dx in range(-4, 5):
                        nx = hx + dx + warp
                        ny = hy + dy
                        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                            if abs(dy) == 2 or abs(dx) == 4:
                                char = '░' if visibility < 0.6 else '▒'
                            else:
                                char = h['char'] if visibility > 0.7 else '~'
                            if grid[ny][nx] == ' ':
                                grid[ny][nx] = char

        # Rain simulation with gravity
        rain_intensity = (math.sin(t * 0.2) + 1) / 2 * 0.3 + 0.1
        for y in range(HEIGHT - 1, -1, -1):
            for x in range(WIDTH):
                # Rain falls diagonally
                wind = math.sin(t * 0.5) * 2
                src_x = int(x - wind) % WIDTH
                src_y = y - 1

                if src_y >= 0:
                    self.rain[y][x] = self.rain[src_y][src_x] * 0.8

                # New rain at top
                if y < 3 and random.random() < rain_intensity:
                    self.rain[y][x] = random.random()

                # Render rain
                if self.rain[y][x] > 0.3 and grid[y][x] == ' ':
                    if self.rain[y][x] > 0.7:
                        grid[y][x] = '|'
                    elif self.rain[y][x] > 0.5:
                        grid[y][x] = ':'
                    else:
                        grid[y][x] = '.'

        # Puddle reflections (rippling)
        for p in self.puddles:
            py = HEIGHT - 3
            for dx in range(p['w']):
                px = p['x'] + dx
                if 0 <= px < WIDTH:
                    ripple = math.sin(t * 4 + dx * 0.5 + p['x'] * 0.1)
                    if ripple > 0.3:
                        grid[py][px] = '~'
                    elif ripple > -0.3:
                        grid[py][px] = '-'
                    else:
                        grid[py][px] = '_'

        # Traffic lights moving along street
        traffic_y = HEIGHT - 4
        for tr in self.traffic:
            tr['x'] = (tr['x'] + tr['speed']) % WIDTH
            tx = int(tr['x'])
            if 0 <= tx < WIDTH and grid[traffic_y][tx] == ' ':
                grid[traffic_y][tx] = tr['char']

        # Matrix code drips (falling characters in gaps)
        matrix_chars = "01アイウエオカキクケコ"
        for m in self.matrix_drips:
            m['y'] = (m['y'] + m['speed']) % (HEIGHT + m['length'])
            for i in range(m['length']):
                my = int(m['y']) - i
                if 0 <= my < HEIGHT and 0 <= m['x'] < WIDTH:
                    if grid[my][m['x']] == ' ':
                        fade = 1 - (i / m['length'])
                        if fade > 0.7:
                            grid[my][m['x']] = random.choice(matrix_chars[:2])
                        elif fade > 0.3:
                            grid[my][m['x']] = '.'

        # Random glitch artifacts
        if random.random() < 0.05:
            gx, gy = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
            grid[gy][gx] = random.choice(['█', '▓', '▒', '░', '#', '%', '@', '!'])

        # Horizontal glitch line (rare)
        if random.random() < 0.02:
            gy = random.randint(0, HEIGHT - 1)
            shift = random.randint(-3, 3)
            grid[gy] = grid[gy][shift:] + grid[gy][:shift]

        return grid

    def display(self, grid):
        clear_screen()
        frame = '\n'.join(''.join(row) for row in grid)
        sys.stdout.write(frame)
        sys.stdout.write('\n')
        sys.stdout.flush()

def main():
    city = City()
    start_time = time.time()

    try:
        while True:
            t = time.time() - start_time
            grid = city.render(t)
            city.display(grid)
            time.sleep(0.2)
    except KeyboardInterrupt:
        clear_screen()
        print("City powered down.")

if __name__ == "__main__":
    main()
