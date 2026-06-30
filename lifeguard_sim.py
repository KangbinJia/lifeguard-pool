import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
POOL_Y_START = 100
POOL_Y_END = 450  # Boundary between water and land

# Colors
WHITE = (255, 255, 255)
BLUE = (173, 216, 230)
SAND = (244, 164, 96)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
GRAY = (150, 150, 150)

# Speeds (pixels per second)
V_LAND = 300.0
V_WATER = 120.0

# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lifeguard Simulation - Path Optimization")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Simulation State Variables
lifeguard_start = [WIDTH // 2, HEIGHT - 20]
lifeguard_pos = list(lifeguard_start)
green_lifeguard_pos = list(lifeguard_start)
target_pos = None
entry_point = None
best_entry = None
path = []
best_path = []
current_target_idx = 0
green_target_idx = 0
green_simulating = False
simulating = False
total_time = 0.0


def spawn_target():
    global target_pos, lifeguard_pos, green_lifeguard_pos, entry_point, best_entry, path, best_path, current_target_idx, green_target_idx, green_simulating, simulating, total_time
    tx = random.randint(50, WIDTH - 50)
    ty = random.randint(POOL_Y_START + 20, POOL_Y_END - 20)
    target_pos = [tx, ty]
    lifeguard_pos = list(lifeguard_start)
    green_lifeguard_pos = list(lifeguard_start)
    entry_point = None
    best_entry = None
    path = []
    best_path = []
    current_target_idx = 0
    green_target_idx = 0
    green_simulating = False
    simulating = False
    total_time = 0.0
    find_best_entry()


def compute_time_for_entry(entry_x):
    land_dist = math.hypot(entry_x - lifeguard_start[0], POOL_Y_END - lifeguard_start[1])
    water_dist = math.hypot(target_pos[0] - entry_x, target_pos[1] - POOL_Y_END)
    return land_dist / V_LAND + water_dist / V_WATER


def find_best_entry():
    global best_entry, best_path
    if target_pos is None:
        best_entry = None
        best_path = []
        return

    best_x = 0
    best_time = float('inf')
    for x in range(0, WIDTH + 1, 2):
        t = compute_time_for_entry(x)
        if t < best_time:
            best_time = t
            best_x = x
    best_entry = [best_x, POOL_Y_END]
    best_path = [best_entry, target_pos]


spawn_target()

running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            button_rect = pygame.Rect(20, 20, 150, 40)
            if button_rect.collidepoint(mx, my):
                spawn_target()
            elif not simulating and target_pos is not None:
                entry_point = [mx, POOL_Y_END]
                path = [entry_point, target_pos]
                current_target_idx = 0
                green_target_idx = 0
                simulating = True
                green_simulating = True
                total_time = 0.0
                lifeguard_pos = list(lifeguard_start)
                green_lifeguard_pos = list(lifeguard_start)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spawn_target()

    if simulating and current_target_idx < len(path):
        next_goal = path[current_target_idx]
        dx = next_goal[0] - lifeguard_pos[0]
        dy = next_goal[1] - lifeguard_pos[1]
        dist = math.hypot(dx, dy)

        if dist < 0.1:
            lifeguard_pos = list(next_goal)
            current_target_idx += 1
        else:
            speed = V_LAND if lifeguard_pos[1] >= POOL_Y_END else V_WATER
            travel = min(dist, speed * dt)
            direction_x = dx / dist
            direction_y = dy / dist
            lifeguard_pos[0] += direction_x * travel
            lifeguard_pos[1] += direction_y * travel
            total_time += travel / speed
            if travel >= dist - 1e-6:
                lifeguard_pos = list(next_goal)
                current_target_idx += 1

    if simulating and green_simulating and best_path and green_target_idx < len(best_path):
        best_next = best_path[green_target_idx]
        gdx = best_next[0] - green_lifeguard_pos[0]
        gdy = best_next[1] - green_lifeguard_pos[1]
        gdist = math.hypot(gdx, gdy)

        if gdist < 0.1:
            green_lifeguard_pos = list(best_next)
            green_target_idx += 1
        else:
            gspeed = V_LAND if green_lifeguard_pos[1] >= POOL_Y_END else V_WATER
            gtravel = min(gdist, gspeed * dt)
            gdir_x = gdx / gdist
            gdir_y = gdy / gdist
            green_lifeguard_pos[0] += gdir_x * gtravel
            green_lifeguard_pos[1] += gdir_y * gtravel
            if gtravel >= gdist - 1e-6:
                green_lifeguard_pos = list(best_next)
                green_target_idx += 1

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, POOL_Y_START, WIDTH, POOL_Y_END - POOL_Y_START))
    pygame.draw.rect(screen, SAND, (0, POOL_Y_END, WIDTH, HEIGHT - POOL_Y_END))
    pygame.draw.line(screen, BLACK, (0, POOL_Y_END), (WIDTH, POOL_Y_END), 2)

    button_rect = pygame.Rect(20, 20, 150, 40)
    pygame.draw.rect(screen, GREEN, button_rect)
    btn_text = font.render("Reset (Space)", True, WHITE)
    screen.blit(btn_text, (30, 30))

    instruction_text = font.render("Click the shoreline to choose the entry point for the lifeguard.", True, BLACK)
    screen.blit(instruction_text, (200, 28))

    if target_pos is not None:
        pygame.draw.circle(screen, RED, (int(target_pos[0]), int(target_pos[1])), 8)

    pygame.draw.circle(screen, BLACK, (int(lifeguard_pos[0]), int(lifeguard_pos[1])), 8)

    if best_entry is not None:
        pygame.draw.circle(screen, GREEN, (int(best_entry[0]), int(best_entry[1])), 6)
        pygame.draw.line(screen, GREEN, lifeguard_start, best_entry, 2)
        pygame.draw.line(screen, GREEN, best_entry, target_pos, 2)
        best_text = font.render("Optimal entry path", True, GREEN)
        screen.blit(best_text, (20, 70))

    pygame.draw.circle(screen, GREEN, (int(green_lifeguard_pos[0]), int(green_lifeguard_pos[1])), 8)
    if entry_point is not None:
        pygame.draw.circle(screen, YELLOW, (int(entry_point[0]), int(entry_point[1])), 6)
        pygame.draw.line(screen, GRAY, lifeguard_start, entry_point, 2)
        pygame.draw.line(screen, GRAY, entry_point, target_pos, 2)

    time_text = font.render(f"Elapsed travel time: {total_time:.2f} sec", True, BLACK)
    screen.blit(time_text, (20, 520))

    if entry_point is None:
        info_text = font.render("Choose a shoreline point to begin simulation.", True, BLACK)
        screen.blit(info_text, (20, 560))
    elif simulating:
        info_text = font.render("Simulating...", True, BLACK)
        screen.blit(info_text, (20, 560))
    else:
        info_text = font.render("Simulation complete. Reset to try a new target.", True, BLACK)
        screen.blit(info_text, (20, 560))

    pygame.display.flip()

pygame.quit()
