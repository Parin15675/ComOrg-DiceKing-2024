# Set map_tiles to match the block positions in the image provided
map_tiles = [
    (70, 420),    # Tile 1 (brown)
    (170, 420),   # Tile 2 (brown)
    (270, 420),   # Tile 3 (brown)
    (370, 420),   # Tile 4 (green)
    (470, 420),   # Tile 5 (brown)
    (570, 420),   # Tile 6 (brown)
    (670, 420),   # Tile 7 (green)
    (770, 420),   # Tile 8 (brown)
    (870, 420),   # Tile 9 (brown)
    (970, 420),   # Tile 10 (green)
]


import pygame

# Set screen size
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dice Quest")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tile size in the map
tile_size = 60
num_tiles = 16  # Total number of tiles

# Create map (20 tiles) and place enemies on certain tiles
map_tiles = [
    (70, 420),    # Tile 1 (brown)
    (170, 420),   # Tile 2 (brown)
    (270, 420),   # Tile 3 (brown)
    (370, 420),   # Tile 4 (green)
    (470, 420),   # Tile 5 (brown)
    (570, 420),   # Tile 6 (brown)
    (670, 420),   # Tile 7 (green)
    (770, 420),   # Tile 8 (brown)
    (870, 420),   # Tile 9 (brown)
    (970, 420),   # Tile 10 (green)
]
enemy_positions = [5, 10]  # Enemies are on tiles 5 and 10
item_positions = [7, 13]   # HP recovery items are on tiles 7 and 13

# Player position (circle)
player_pos = 0  # Start at the first tile
player_hp = 300  # Player's initial HP

last_step_time = 0  # Store the time of the last step
