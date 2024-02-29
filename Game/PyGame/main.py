import pygame
import math
import os

pygame.init()


class Cell:
    def __init__(self, x, y, side, can_play):
        self.x = x
        self.y = y
        self.side = side
        self.can_play = can_play

    def getter(self):
        return self.x, self.y, self.side, self.can_play


# Screen
WIDTH = 300
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
images_folder = os.path.join(os.path.dirname(__file__), '..', 'Images')
x_image_path = os.path.join(images_folder, 'x.png')
o_image_path = os.path.join(images_folder, 'o.png')
X_IMAGE = pygame.transform.scale(pygame.image.load(x_image_path), (80, 80))
O_IMAGE = pygame.transform.scale(pygame.image.load(o_image_path), (80, 80))

# Fonts
END_FONT = pygame.font.SysFont('arial', 40)


def draw_rect(cell):
    x, y, _, _ = cell.getter()
    gap = WIDTH // ROWS
    half_gap = gap // 2
    pygame.draw.rect(win, (0, 255, 0), (x - half_gap, y - half_gap, gap, gap), 3)


def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)


def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = Cell(x, y, "", True)

    return game_array


def click(game_array, pos):
    global x_turn, o_turn, images

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()
    if pos is not None:
        m_x, m_y, _, _ = game_array[pos[0]][pos[1]].getter()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j].getter()

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                if x_turn:  # If it's X's turn
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = Cell(x, y, 'x', False)

                elif o_turn:  # If it's O's turn
                    images.append((x, y, O_IMAGE))
                    x_turn = True
                    o_turn = False
                    game_array[i][j] = Cell(x, y, 'o', False)


# Checking if someone has won
def has_won(game_array):
    # Checking rows
    for row in range(len(game_array)):
        if (game_array[row][0].side == game_array[row][1].side == game_array[row][2].side) and game_array[row][
            0].side != "":
            display_message(game_array[row][0].side.upper() + " has won!")
            return True

    # Checking columns
    for col in range(len(game_array)):
        if (game_array[0][col].side == game_array[1][col].side == game_array[2][col].side) and game_array[0][
            col].side != "":
            display_message(game_array[0][col].side.upper() + " has won!")
            return True

    # Checking main diagonal
    if (game_array[0][0].side == game_array[1][1].side == game_array[2][2].side) and game_array[0][0].side != "":
        display_message(game_array[0][0].side.upper() + " has won!")
        return True

    # Checking reverse diagonal
    if (game_array[0][2].side == game_array[1][1].side == game_array[2][0].side) and game_array[0][2].side != "":
        display_message(game_array[0][2].side.upper() + " has won!")
        return True

    return False


def has_won_minimax(game_array):
    # for i in range(3):
    #     for j in range(3):
    #         print(game_array[i][j].side, end = ' ')
    #     print("\n---\n")

    for row in range(len(game_array)):
        if (game_array[row][0].side == game_array[row][1].side == game_array[row][2].side) and game_array[row][
            0].side != "":
            return game_array[row][0].side

    for col in range(len(game_array)):
        if (game_array[0][col].side == game_array[1][col].side == game_array[2][col].side) and game_array[0][
            col].side != "":
            return game_array[0][col].side

    if (game_array[0][0].side == game_array[1][1].side == game_array[2][2].side) and game_array[0][0].side != "":
        return game_array[0][0].side

    if (game_array[0][2].side == game_array[1][1].side == game_array[2][0].side) and game_array[0][2].side != "":
        return game_array[0][2].side

    return None


def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j].side == "":
                return False

    display_message("It's a draw!")
    return True

def has_drawn_minimax(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j].side == "":
                return False

    return True

def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render(game_array, current_cell):
    if pygame.display.get_init():
        win.fill(WHITE)
        draw_grid()
        draw_rect(game_array[current_cell[0]][current_cell[1]])

        for image in images:
            x, y, IMAGE = image
            win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

        pygame.display.update()


def change_cell(event, current_cell):
    if event.key == pygame.K_UP:
        if current_cell[0] == 0:
            return [2, current_cell[1]]
        else:
            return [current_cell[0] - 1, current_cell[1]]
    elif event.key == pygame.K_DOWN:
        if current_cell[0] == 2:
            return [0, current_cell[1]]
        else:
            return [current_cell[0] + 1, current_cell[1]]
    elif event.key == pygame.K_LEFT:
        if current_cell[1] == 0:
            return [current_cell[0], 2]
        else:
            return [current_cell[0], current_cell[1] - 1]
    elif event.key == pygame.K_RIGHT:
        if current_cell[1] == 2:
            return [current_cell[0], 0]
        else:
            return [current_cell[0], current_cell[1] + 1]
    return current_cell

def minimax(game_array, depth, is_maximizing):
    winner = has_won_minimax(game_array)
    if winner == 'x':
        return 10 - depth, None
    elif winner == 'o':
        return depth - 10, None

    if has_drawn_minimax(game_array):
        return 0, None

    if is_maximizing:
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if game_array[i][j].side == "":
                    game_array[i][j].side = 'x'
                    score, _ = minimax(game_array, depth + 1, False)
                    game_array[i][j].side = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if game_array[i][j].side == "":
                    game_array[i][j].side = 'o'
                    score, _ = minimax(game_array, depth + 1, True)
                    game_array[i][j].side = ""
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)
        return best_score, best_move



def main():
    global x_turn, o_turn, images, draw

    images = []
    draw = False

    run = True

    x_turn = True
    o_turn = False

    game_array = initialize_grid()
    current_cell = [0, 0]

    grid_changed = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array, None)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    click(game_array, current_cell)
                    grid_changed = True
                else:
                    current_cell = change_cell(event, current_cell)

        if o_turn:
            best_move = minimax(game_array, 10, o_turn)
            click(game_array, best_move[1])

        if grid_changed:
            render(game_array, current_cell)

        if grid_changed:
            if has_won(game_array) or has_drawn(game_array):
                run = False
    return True


is_game = True
while is_game:
    if __name__ == '__main__':
        is_game = main()
