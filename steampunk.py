#!/usr/bin/env python3
"""Procedural ASCII Steampunk Machinery Simulator"""
import math, random, time, os, sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

W, H = 72, 36
t = 0
steam_particles = []
sparks = []
oil_drips = []

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_gear(canvas, cx, cy, radius, teeth, angle, char_set=None):
    """Draw a rotating gear at position"""
    if char_set is None:
        char_set = {'rim': 'O', 'tooth': '#', 'center': '*', 'spoke': '-'}

    for i in range(teeth * 2):
        theta = angle + (i * math.pi / teeth)
        # Teeth extend beyond rim
        r = radius + (0.8 if i % 2 == 0 else 0)
        x = int(cx + r * math.cos(theta))
        y = int(cy + r * math.sin(theta) * 0.5)  # Squish vertically for ASCII
        if 0 <= x < W and 0 <= y < H:
            canvas[y][x] = char_set['tooth'] if i % 2 == 0 else char_set['rim']

    # Rim
    for i in range(int(radius * 8)):
        theta = i * math.pi / (radius * 4)
        x = int(cx + radius * math.cos(theta))
        y = int(cy + radius * math.sin(theta) * 0.5)
        if 0 <= x < W and 0 <= y < H and canvas[y][x] == ' ':
            canvas[y][x] = char_set['rim']

    # Spokes
    for i in range(4):
        theta = angle + i * math.pi / 2
        for r in range(1, int(radius)):
            x = int(cx + r * math.cos(theta))
            y = int(cy + r * math.sin(theta) * 0.5)
            if 0 <= x < W and 0 <= y < H:
                canvas[y][x] = char_set['spoke']

    # Center
    if 0 <= int(cx) < W and 0 <= int(cy) < H:
        canvas[int(cy)][int(cx)] = char_set['center']

def draw_piston(canvas, x, y, length, phase):
    """Draw oscillating piston"""
    offset = int(math.sin(phase) * length * 0.4)

    # Cylinder housing
    for i in range(length):
        if 0 <= x < W and 0 <= y + i < H:
            canvas[y + i][x - 1] = '|' if i > 0 else '+'
            canvas[y + i][x + 1] = '|' if i > 0 else '+'
            if i == 0 or i == length - 1:
                canvas[y + i][x] = '='

    # Piston rod
    rod_y = y + length // 2 + offset
    for i in range(-2, 3):
        if 0 <= x + i < W and 0 <= rod_y < H:
            canvas[rod_y][x + i] = '=' if i == 0 else '-'

    # Piston head
    head_y = rod_y - 1
    if 0 <= head_y < H:
        for i in range(-1, 2):
            if 0 <= x + i < W:
                canvas[head_y][x + i] = '#'

def draw_chain(canvas, x1, y1, x2, y2, t):
    """Draw a moving chain/belt"""
    steps = max(abs(x2 - x1), abs(y2 - y1)) + 1
    chain_chars = ['-', '=', '-', '~']

    for i in range(steps):
        frac = i / max(steps - 1, 1)
        x = int(x1 + (x2 - x1) * frac)
        y = int(y1 + (y2 - y1) * frac)
        if 0 <= x < W and 0 <= y < H:
            char_idx = int((t * 3 + i) % len(chain_chars))
            canvas[y][x] = chain_chars[char_idx]

def render(t):
    global steam_particles, sparks, oil_drips
    canvas = [[' ' for _ in range(W)] for _ in range(H)]

    # Layer 1: Background pipes and framework
    for y in [5, 15, 25, 33]:
        for x in range(W):
            if canvas[y][x] == ' ':
                canvas[y][x] = '-'

    for x in [10, 35, 60]:
        for y in range(H):
            if canvas[y][x] == ' ':
                canvas[y][x] = '|'

    # Pipe joints
    for y in [5, 15, 25, 33]:
        for x in [10, 35, 60]:
            if 0 <= y < H and 0 <= x < W:
                canvas[y][x] = '+'

    # Layer 2: Main gears (different sizes and speeds)
    # Large main gear
    draw_gear(canvas, 20, 12, 6, 12, t * 0.5,
              {'rim': 'O', 'tooth': '#', 'center': '@', 'spoke': '/'})

    # Medium gear (meshed, opposite rotation)
    draw_gear(canvas, 32, 12, 4, 8, -t * 0.75,
              {'rim': 'o', 'tooth': '%', 'center': '*', 'spoke': '\\'})

    # Small fast gear
    draw_gear(canvas, 40, 12, 3, 6, t * 1.0,
              {'rim': 'o', 'tooth': '*', 'center': '+', 'spoke': '-'})

    # Bottom gears
    draw_gear(canvas, 50, 28, 5, 10, -t * 0.6,
              {'rim': 'O', 'tooth': '#', 'center': '@', 'spoke': '|'})

    draw_gear(canvas, 62, 28, 3, 6, t * 1.0,
              {'rim': 'o', 'tooth': '%', 'center': '*', 'spoke': '-'})

    # Layer 3: Pistons (harmonic oscillation)
    draw_piston(canvas, 8, 18, 10, t * 2)
    draw_piston(canvas, 55, 5, 8, t * 2 + math.pi / 2)

    # Layer 4: Connecting rods and chains
    draw_chain(canvas, 28, 12, 45, 12, t)
    draw_chain(canvas, 40, 15, 50, 23, t)

    # Layer 5: Steam venting (particle system)
    # Steam sources
    steam_sources = [(12, 5), (38, 5), (65, 15)]
    for sx, sy in steam_sources:
        if random.random() > 0.7:
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-1.5, -0.5)
            steam_particles.append([float(sx), float(sy), vx, vy, 0])

    new_steam = []
    for particle in steam_particles:
        x, y, vx, vy, age = particle
        # Apply physics
        vy *= 0.95  # Drag
        vx += random.uniform(-0.1, 0.1)  # Turbulence
        x += vx
        y += vy
        age += 0.1

        if age < 2 and 0 <= int(x) < W and 0 <= int(y) < H:
            ix, iy = int(x), int(y)
            if age < 0.5:
                canvas[iy][ix] = '~'
            elif age < 1.0:
                canvas[iy][ix] = '-'
            else:
                canvas[iy][ix] = '.'
            new_steam.append([x, y, vx, vy, age])
    steam_particles = new_steam

    # Layer 6: Sparks (occasional)
    if random.random() > 0.95:
        # Spark near gears
        spark_sources = [(20, 15), (50, 31)]
        sx, sy = random.choice(spark_sources)
        for _ in range(random.randint(2, 5)):
            vx = random.uniform(-2, 2)
            vy = random.uniform(-1, 1)
            sparks.append([float(sx), float(sy), vx, vy, 0])

    new_sparks = []
    for spark in sparks:
        x, y, vx, vy, age = spark
        vy += 0.2  # Gravity
        x += vx
        y += vy
        age += 0.15

        if age < 0.8 and 0 <= int(x) < W and 0 <= int(y) < H:
            ix, iy = int(x), int(y)
            canvas[iy][ix] = '*' if age < 0.3 else '.'
            new_sparks.append([x, y, vx, vy, age])
    sparks = new_sparks

    # Layer 7: Oil drips
    if random.random() > 0.97:
        drip_x = random.choice([20, 32, 50])
        oil_drips.append([drip_x, 18, 0.3])

    new_drips = []
    for drip in oil_drips:
        x, y, speed = drip
        speed = min(speed * 1.05, 1.5)
        y += speed
        ix, iy = int(x), int(y)

        if iy < H - 2 and 0 <= ix < W and 0 <= iy < H:
            canvas[iy][ix] = 'o' if speed > 0.8 else '.'
            new_drips.append([x, y, speed])
    oil_drips = new_drips

    # Layer 8: Pressure gauges
    gauge_positions = [(3, 3), (68, 3), (3, 30)]
    for gx, gy in gauge_positions:
        # Gauge frame
        for dx in range(-2, 3):
            for dy in range(-1, 2):
                px, py = gx + dx, gy + dy
                if 0 <= px < W and 0 <= py < H:
                    if abs(dx) == 2 or abs(dy) == 1:
                        canvas[py][px] = '|' if abs(dx) == 2 else '-'
                    elif dx == 0 and dy == 0:
                        # Needle
                        needle_angle = t * 0.5 + gx * 0.1
                        needle_char = '/' if math.sin(needle_angle) > 0 else '\\'
                        canvas[py][px] = needle_char

    # Layer 9: Rhythmic indicators (LEDs/lights)
    indicator_y = 2
    for i, x in enumerate([15, 25, 45, 55]):
        if 0 <= x < W:
            phase = (t * 2 + i * 0.5) % (math.pi * 2)
            if math.sin(phase) > 0.3:
                canvas[indicator_y][x] = '@'
            else:
                canvas[indicator_y][x] = 'o'

    return canvas

def display(canvas):
    clear()
    print('\033[33m' + '#' * W + '\033[0m')  # Bronze/gold border
    for i, row in enumerate(canvas):
        line = ''.join(row)
        # Color: copper/bronze tones
        if i < H // 3:
            print('\033[38;5;94m' + line + '\033[0m')  # Dark bronze
        elif i < 2 * H // 3:
            print('\033[38;5;136m' + line + '\033[0m')  # Bronze
        else:
            print('\033[38;5;178m' + line + '\033[0m')  # Light bronze/gold
    print('\033[33m' + '#' * W + '\033[0m')
    sys.stdout.flush()

def main():
    global t
    print('\033[?25l', end='')  # Hide cursor
    try:
        while True:
            canvas = render(t)
            display(canvas)
            t += 0.22
            time.sleep(0.22)
    except KeyboardInterrupt:
        print('\033[?25h', end='')  # Show cursor
        print('\n\033[33mThe machinery winds down to silence...\033[0m')

if __name__ == '__main__':
    main()
