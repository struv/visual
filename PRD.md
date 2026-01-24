# PRD: ASCII Terminal Animations

## Overview
Create three self-contained Python terminal animation scripts using only built-in modules.

## Tasks

### Task 1: Organic Jungle Animation
- [x] Create `jungle.py`
- Canvas: 70 x 35, Delay: 0.15s
- Tangled vines, layered canopy, light shafts, breathing foliage, rain/drips
- Use sine/cosine for sway, noise for density, exponential decay for droplets

### Task 2: Cosmic Nebula Animation
- [x] Create `nebula.py`
- Canvas: 65 x 32, Delay: 0.25s
- Swirling spiral gas arms, twinkling stars, rotation + expansion, central void
- Use polar coordinates, Gaussian noise, time-seeded flow fields

### Task 3: Steampunk Machinery Animation
- [x] Create `steampunk.py`
- Canvas: 72 x 36, Delay: 0.22s
- Interlocking gears, oscillating pistons, steam venting, sparks/oil drips
- Use angle-based rotation, harmonic oscillators, particle paths

## Rules (apply to all)
- Only built-in modules: math, time, random, sys, os
- Infinite loop with time.sleep(delay)
- Clear screen each frame: `os.system('cls' if os.name == 'nt' else 'clear')`
- 100% procedural (math + time), no static data
- Character density for brightness/depth
