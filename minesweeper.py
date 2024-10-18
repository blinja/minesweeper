import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the game grid
rows, cols = 10, 10
cell_size = width // cols
grid = [[0 for _ in range(cols)] for _ in range(rows)]
revealed = [[False for _ in range(cols)] for _ in range(rows)]
flags = [[False for _ in range(cols)] for _ in range(rows)]
mines = 10

# Place mines randomly
for _ in range(mines):
    x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
    grid[x][y] = 1

# Function to count adjacent mines
def count_adjacent_mines(x, y):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if 0 <= x + dx < rows and 0 <= y + dy < cols:
                count += grid[x + dx][y + dy]
    return count

# Function to reveal cells
def reveal(x, y):
    if revealed[x][y] or grid[x][y] == 1 or flags[x][y]:
        return
    revealed[x][y] = True
    if count_adjacent_mines(x, y) == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < rows and 0 <= y + dy < cols:
                    reveal(x + dx, y + dy)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = y // cell_size, x // cell_size
            if event.button == 1:  # Left click
                if grid[row][col] == 1:
                    reveal(row, col)
                    print("Game Over!")
                    font = pygame.font.Font(None, 72)
                    text = font.render("Game Over!", True, RED)
                    text_rect = text.get_rect(center=(width // 2, height // 2))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    running = False
                else:
                    reveal(row, col)
            elif event.button == 3:  # Right click
                if not revealed[row][col]:
                    flags[row][col] = not flags[row][col]

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid
    for x in range(rows):
        for y in range(cols):
            rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if revealed[x][y]:
                if grid[x][y] == 1:
                    pygame.draw.circle(screen, RED, (y * cell_size + cell_size // 2, x * cell_size + cell_size // 2), cell_size // 4)
                else:
                    count = count_adjacent_mines(x, y)
                    if count > 0:
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(count), True, BLACK)
                        text_rect = text.get_rect(center=(y * cell_size + cell_size // 2, x * cell_size + cell_size // 2))
                        screen.blit(text, text_rect)
                    else:
                        pygame.draw.circle(screen, GREEN, (y * cell_size + cell_size // 2, x * cell_size + cell_size // 2), cell_size // 4)
            elif flags[x][y]:
                font = pygame.font.Font(None, 36)
                text = font.render("F", True, BLUE)
                text_rect = text.get_rect(center=(y * cell_size + cell_size // 2, x * cell_size + cell_size // 2))
                screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
