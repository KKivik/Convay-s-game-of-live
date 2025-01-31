import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 20
        self.top = 20
        self.cell_size = 15

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        x = self.left
        y = self.top
        for i in self.board:
            for j in i:
                if j:
                    color = 'Green'
                else:
                    color = 'Black'
                pygame.draw.rect(screen, pygame.Color(color), (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color('White'), (x, y, self.cell_size, self.cell_size), 1)

                x += self.cell_size
            y += self.cell_size
            x = self.left

    def get_cell(self, mouse_pos):  # mouse_pos - кортеж
        x, y = mouse_pos
        if x >= self.left and x <= self.left + self.cell_size * len(
                self.board[0]) and y >= self.top and y <= self.top + self.cell_size * len(self.board):
            x -= self.left
            y -= self.top
            x_r = x // self.cell_size + bool(x % self.cell_size)
            y_r = y // self.cell_size + bool(y % self.cell_size)
            return (x_r, y_r)
        return None

    def on_click(self, pos):
        if pos != None:
            x, y = pos
            x -= 1
            y -= 1
            self.board[y][x] = int(not (bool(self.board[y][x])))

    def get_click(self, pos):
        coord = self.get_cell(pos)
        self.on_click(coord)

    def near(self, pos: list, system=[[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]):
        count = 0
        for i in system:
            if pos[0] + i[0] < 0 or pos[0] + i[0] > self.width - 1 or pos[1] + i[1] < 0 or pos[1] + i[
                1] > self.height - 1:
                continue
            if self.board[pos[0] + i[0]][pos[1] + i[1]]:
                count += 1
        return count

    def next_move(self):
        board2 = [[0 for j in range(len(self.board[0]))] for i in range(len(self.board))]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]:
                    if self.near([i, j]) not in (2, 3):
                        board2[i][j] = 0
                    else:
                        board2[i][j] = 1
                else:
                    if self.near([i, j]) == 3:
                        board2[i][j] = 1
                    else:
                        board2[i][j] = 0
        self.board = board2


if __name__ == '__main__':
    pygame.init()
    size = width, height = 950, 950
    screen = pygame.display.set_mode(size)

    fps = 50  # количество кадров в секунду
    clock = pygame.time.Clock()
    running = True

    board = Board(60, 60)

    fl = False
    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    board.get_click(event.pos)
                if event.button == 3:
                    fl = not fl

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fl = not fl
                    board.next_move()
            if event.type == pygame.MOUSEWHEEL:
                if fps + event.y <= 0:
                    fps = 1
                else:
                    fps += event.y * 2

        if fl:
            board.next_move()
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
