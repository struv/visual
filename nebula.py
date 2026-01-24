#!/usr/bin/env python3
"""Procedural ASCII Cosmic Nebula Simulator"""
import math, random, time, os, sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

W, H = 65, 32
t = 0
stars = []
flares = []

def noise(x, y, seed=0):
    """Simple pseudo-noise via sine mixing"""
    return (math.sin(x * 0.3 + seed) * math.cos(y * 0.4 + seed * 0.7) +
            math.sin((x + y) * 0.2 + seed * 1.3)) / 2

def smooth_noise(x, y, t, scale=0.1):
    """Smoothed noise for gas clouds"""
    nx = noise(x * scale, y * scale, t * 0.05)
    return (nx + 1) / 2

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def density_char(d):
    """Character by density level for nebula gas"""
    if d > 0.9: return '@'
    if d > 0.75: return '#'
    if d > 0.6: return '%'
    if d > 0.45: return '*'
    if d > 0.3: return '+'
    if d > 0.15: return '.'
    return ' '

def star_char(brightness, twinkle):
    """Star character based on brightness and twinkle phase"""
    if brightness > 0.9:
        return random.choice(['*', '+', '@']) if twinkle > 0.5 else random.choice(['.', '*'])
    if brightness > 0.6:
        return '*' if twinkle > 0.3 else '+'
    if brightness > 0.3:
        return '+' if twinkle > 0.4 else '.'
    return '.'

def polar_to_cart(r, theta, cx, cy):
    """Convert polar to cartesian coordinates"""
    x = cx + r * math.cos(theta)
    y = cy + r * math.sin(theta)
    return int(x), int(y)

def spiral_density(x, y, cx, cy, t, arms=3):
    """Calculate spiral arm density at a point"""
    dx, dy = x - cx, y - cy
    r = math.sqrt(dx * dx + dy * dy)
    if r < 0.1:
        return 0.3  # Central void area

    theta = math.atan2(dy, dx)
    # Rotation over time
    theta_rot = theta - t * 0.1

    # Spiral arm formula
    arm_density = 0
    for arm in range(arms):
        arm_angle = arm * (2 * math.pi / arms)
        # Logarithmic spiral
        expected_theta = arm_angle + r * 0.3
        angle_diff = abs(math.sin(theta_rot - expected_theta))
        arm_contribution = math.exp(-angle_diff * 3) * math.exp(-r * 0.05)
        arm_density += arm_contribution

    return min(arm_density, 1.0)

def init_stars():
    """Initialize background stars"""
    global stars
    stars = []
    for _ in range(80):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        brightness = random.uniform(0.2, 1.0)
        twinkle_speed = random.uniform(0.5, 2.0)
        stars.append([x, y, brightness, twinkle_speed])

def render(t):
    global flares
    canvas = [[' ' for _ in range(W)] for _ in range(H)]
    cx, cy = W // 2, H // 2

    # Layer 1: Deep background - distant stars
    for star in stars:
        x, y, brightness, twinkle_speed = star
        twinkle = (math.sin(t * twinkle_speed + x * 0.5 + y * 0.3) + 1) / 2
        effective_brightness = brightness * (0.5 + twinkle * 0.5)
        if effective_brightness > 0.3:
            canvas[y][x] = star_char(effective_brightness, twinkle)

    # Layer 2: Nebula gas clouds (spiral arms)
    for y in range(H):
        for x in range(W):
            r = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)

            # Spiral arm density
            sp_density = spiral_density(x, y, cx, cy, t, arms=2)

            # Add noise for cloud texture
            cloud_noise = smooth_noise(x, y, t * 0.5, 0.15)

            # Expansion effect
            expansion = math.sin(t * 0.05) * 0.2 + 1.0

            # Combined density
            density = sp_density * cloud_noise * expansion

            # Distance falloff
            density *= math.exp(-r * 0.04)

            if density > 0.1:
                char = density_char(density)
                if char != ' ':
                    canvas[y][x] = char

    # Layer 3: Bright core region
    core_radius = 4 + math.sin(t * 0.3) * 1
    for y in range(H):
        for x in range(W):
            r = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            if r < core_radius:
                # Central void with gentle distortion
                distort = math.sin(t * 0.5 + r * 0.8) * 0.5 + 0.5
                if r < core_radius * 0.5:
                    # Dark core
                    if distort > 0.7:
                        canvas[y][x] = '.'
                    else:
                        canvas[y][x] = ' '
                else:
                    # Bright ring around core
                    ring_brightness = (1 - r / core_radius) * distort
                    if ring_brightness > 0.5:
                        canvas[y][x] = random.choice(['@', '#', '*'])
                    elif ring_brightness > 0.2:
                        canvas[y][x] = random.choice(['*', '+'])

    # Layer 4: Supernova flares (occasional)
    if random.random() > 0.98:
        fx = random.randint(5, W - 5)
        fy = random.randint(5, H - 5)
        flares.append([fx, fy, 0])

    new_flares = []
    for flare in flares:
        fx, fy, age = flare
        age += 0.2
        if age < 2:
            radius = int(age * 3)
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    d = math.sqrt(dx * dx + dy * dy)
                    if d <= radius:
                        px, py = fx + dx, fy + dy
                        if 0 <= px < W and 0 <= py < H:
                            intensity = 1 - d / (radius + 1)
                            if intensity > 0.7:
                                canvas[py][px] = '@'
                            elif intensity > 0.4:
                                canvas[py][px] = '*'
                            elif intensity > 0.1:
                                canvas[py][px] = '+'
            new_flares.append([fx, fy, age])
    flares = new_flares

    # Layer 5: Bright foreground stars (twinkling)
    for _ in range(5):
        sx = random.randint(0, W - 1)
        sy = random.randint(0, H - 1)
        if canvas[sy][sx] == ' ' and random.random() > 0.7:
            canvas[sy][sx] = random.choice(['.', '*', '+'])

    return canvas

def display(canvas):
    clear()
    print('\033[35m' + '~' * W + '\033[0m')  # Purple border
    for i, row in enumerate(canvas):
        line = ''.join(row)
        # Color gradient: outer=blue/purple, inner=pink/white
        if i < H // 3:
            print('\033[38;5;93m' + line + '\033[0m')  # Purple
        elif i < 2 * H // 3:
            print('\033[38;5;141m' + line + '\033[0m')  # Lighter purple
        else:
            print('\033[38;5;183m' + line + '\033[0m')  # Pink
    print('\033[35m' + '~' * W + '\033[0m')
    sys.stdout.flush()

def main():
    global t
    init_stars()
    print('\033[?25l', end='')  # Hide cursor
    try:
        while True:
            canvas = render(t)
            display(canvas)
            t += 0.25
            time.sleep(0.25)
    except KeyboardInterrupt:
        print('\033[?25h', end='')  # Show cursor
        print('\n\033[35mThe cosmos drifts into silence...\033[0m')

if __name__ == '__main__':
    main()
