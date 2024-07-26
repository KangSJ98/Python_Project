import pygame
import random

pygame.init()

# 색 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
purple = (128, 0, 128)
cyan = (0, 255, 255)

# 화면 크기
width, height = 800, 700
play_width = 300  # 300 // 10 = 30 width per block
play_height = 600  # 600 // 20 = 20 height per block
block_size = 30

top_left_x = (width - play_width) // 2
top_left_y = height - play_height - 50

# 도형 정의
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [green, red, blue, yellow, orange, purple, cyan]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[black for _ in range(10)] for _ in range(20)]
    for y in range(20):
        for x in range(10):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid

def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == black] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape(bag):
    if not bag:
        bag.extend(random.sample(shapes, len(shapes)))
    return Piece(5, 0, bag.pop())

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (top_left_x + x * block_size, top_left_y + y * block_size, block_size, block_size), 0)
    for y in range(len(grid)):
        pygame.draw.line(surface, white, (top_left_x, top_left_y + y * block_size), (top_left_x + play_width, top_left_y + y * block_size))
        for x in range(len(grid[y])):
            pygame.draw.line(surface, white, (top_left_x + x * block_size, top_left_y), (top_left_x + x * block_size, top_left_y + play_height))

def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if black not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    return increment

def draw_window(surface, grid, score=0, next_piece=None):
    surface.fill(black)
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, white)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, white)
    surface.blit(label, (width - 200, height // 2 - 100))
    draw_grid(surface, grid)
    pygame.draw.rect(surface, red, (top_left_x, top_left_y, play_width, play_height), 5)
    if next_piece:
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next:', 1, white)
        surface.blit(label, (width - 200, height // 2 - 200))
        format = next_piece.shape[next_piece.rotation % len(next_piece.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, next_piece.color, (width - 200 + j * block_size, height // 2 - 150 + i * block_size, block_size, block_size), 0)

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    bag = []
    current_piece = get_shape(bag)
    next_piece = get_shape(bag)
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0
    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True
        shape_pos = convert_shape_format(current_piece)
        for pos in shape_pos:
            x, y = pos
            if y > -1:
                grid[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape(bag)
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
        draw_window(win, grid, score, next_piece)
        pygame.display.update()
        if check_lost(locked_positions):
            run = False
    draw_text_middle(win, "You Lost", 80, red)
    pygame.display.update()
    pygame.time.delay(1500)
    pygame.quit()

def main_menu():
    run = True
    while run:
        win.fill(black)
        draw_text_middle(win, 'Press Any Key to Play', 60, white)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris')
main_menu()
