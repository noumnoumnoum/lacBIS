# Pacman Game

import pygame
import sys
import random

pygame.init()

TILE_SIZE = 24
GRID_WIDTH = 28
GRID_HEIGHT = 31
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT
FPS = 10

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 105, 180)

maze_layout = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W............WW............W",
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
    "W..........................W",
    "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
    "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
    "W......WW....WW....WW......W",
    "WWWWWW.WWWWW WW WWWWW.WWWWWW",
    "     W.WWWWW WW WWWWW.W     ",
    "     W.WW          WW.W     ",
    "     W.WW WWW--WWW WW.W     ",
    "WWWWWW.WW W      W WW.WWWWWW",
    "      .   W      W   .      ",
    "WWWWWW.WW W      W WW.WWWWWW",
    "     W.WW WWWWWWWW WW.W     ",
    "     W.WW          WW.W     ",
    "     W.WW WWWWWWWW WW.W     ",
    "WWWWWW.WW WWWWWWWW WW.WWWWWW",
    "W............WW............W",
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
    "W...WW................WW...W",
    "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",
    "W......WW....WW....WW......W",
    "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",
    "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",
    "W..........................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW"]

maze = [list(row) for row in maze_layout]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Ghosts Exit Start Box")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("Arial", 72)
font_small = pygame.font.SysFont("Arial", 32)

pacman_x, pacman_y = 14, 23
direction = (0, 0)
win = False
game_over = False
lives = 3

# Define start box area where ghosts begin and can't return
START_BOX_TOP = 13
START_BOX_BOTTOM = 15
START_BOX_LEFT = 12
START_BOX_RIGHT = 15

def is_in_start_box(x, y):
    return START_BOX_LEFT <= x <= START_BOX_RIGHT and START_BOX_TOP <= y <= START_BOX_BOTTOM

def can_move(x, y):
    if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
        return maze[y][x] != 'W'
    return False

def count_dots():
    return sum(row.count('.') for row in maze)

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.exited_start_box = False

    def move(self, *_):
        if not self.exited_start_box and is_in_start_box(self.x, self.y):
            def dist_to_outside(nx, ny):
                if not is_in_start_box(nx, ny):
                    return 0
                left_dist = abs(nx - START_BOX_LEFT)
                right_dist = abs(nx - START_BOX_RIGHT)
                top_dist = abs(ny - START_BOX_TOP)
                bottom_dist = abs(ny - START_BOX_BOTTOM)
                return min(left_dist, right_dist, top_dist, bottom_dist)

            candidates = []
            for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
                nx = (self.x + dx) % GRID_WIDTH
                ny = self.y + dy
                if can_move(nx, ny):
                    candidates.append((dx, dy, dist_to_outside(nx, ny)))

            if candidates:
                candidates.sort(key=lambda c: c[2])
                dx, dy, dist = candidates[0]
                self.direction = (dx, dy)
                self.x = (self.x + dx) % GRID_WIDTH
                self.y = self.y + dy
                if not is_in_start_box(self.x, self.y):
                    self.exited_start_box = True
            return
        
        next_x = (self.x + self.direction[0]) % GRID_WIDTH
        next_y = self.y + self.direction[1]

        if 0 <= next_y < GRID_HEIGHT and can_move(next_x, next_y) and not is_in_start_box(next_x, next_y):
            self.x, self.y = next_x, next_y
        else:
            valid_dirs = []
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx = (self.x + dx) % GRID_WIDTH
                ny = self.y + dy
                if 0 <= ny < GRID_HEIGHT and can_move(nx, ny) and not is_in_start_box(nx, ny):
                    valid_dirs.append((dx, dy))
            if valid_dirs:
                self.direction = random.choice(valid_dirs)
                self.x = (self.x + self.direction[0]) % GRID_WIDTH
                self.y = self.y + self.direction[1]
    def draw(self):
        px = self.x * TILE_SIZE + TILE_SIZE // 2
        py = self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, self.color, (px, py), TILE_SIZE // 2 - 2)

ghosts = [
        Ghost(13, 14, RED),
        Ghost(14, 14, PINK)
]

def reset_game():
    global pacman_x, pacman_y, direction, win
    pacman_x, pacman_y = 14, 23
    direction = (0, 0)
    win = False
    ghosts[0].x, ghosts[0].y = 13, 14
    ghosts[0].exited_start_box = False
    ghosts[0].direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    ghosts[1].x, ghosts[1].y = 14, 14
    ghosts[1].exited_start_box = False
    ghosts[1].direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

def reset_level():
    global lives, game_over, win
    lives -=1
    reset_game()
    if lives <= 0:
        game_over = True
    win = False

while True:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if not (win or game_over):
                if event.key == pygame.K_LEFT:
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    direction = (1, 0)
                elif event.key == pygame.K_UP:
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    direction = (0, 1)
            elif game_over:
                # Restarts game on any keypress if game is over
                lives = 3
                game_over = False
                #Reset maze dots
                maze = [list(row) for row in maze_layout]
                reset_game()

    if not (win or game_over):
        next_x = (pacman_x + direction[0]) % GRID_WIDTH
        next_y = pacman_y + direction[1]

        if 0 <= next_y < GRID_HEIGHT and can_move(next_x, next_y):
            pacman_x, pacman_y = next_x, next_y
            if maze[pacman_y][pacman_x] == '.':
                maze[pacman_y][pacman_x] = ' '
    
        for ghost in ghosts:
            ghost.move()

        for ghost in ghosts:
            if ghost.x == pacman_x and ghost.y == pacman_y:
                reset_level()

        if count_dots() == 0:
            win = True

    # Draw maze
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 'W':
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == '.':
                pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2), 4)

    # Draw Pac-Man
    pygame.draw.circle(screen, YELLOW, (pacman_x * TILE_SIZE + TILE_SIZE // 2, pacman_y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 2)

    # Draw ghosts
    for ghost in ghosts:
        ghost.draw()

    # Draw lives
    lives_text = font_small.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, SCREEN_HEIGHT - 40))

    if win:
        text = font_big.render("YOU WIN!", True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text, rect)
    elif game_over:
        text = font_big.render("GAME OVER", True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        screen.blit(text, rect)
        restart_text = font_small.render("Press any key to restart", True, WHITE)
        rect2 = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        screen.blit(restart_text, rect2)

    pygame.display.flip()

