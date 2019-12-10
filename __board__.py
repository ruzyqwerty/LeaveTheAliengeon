import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        color = pygame.Color('white')
        for row in range(self.height):
            for cell in range(self.width):
                pygame.draw.rect(surface, color, (
                    self.left + cell * self.cell_size,
                    self.top + row * self.cell_size,
                    self.cell_size, self.cell_size
                ), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if self.left < mouse_x < self.left + self.cell_size * self.width and self.top < mouse_y < self.top + self.cell_size * self.height:
            mouse_x -= self.left
            mouse_y -= self.top
            cell_col = mouse_x // self.cell_size
            cell_row = mouse_y // self.cell_size
            if cell_col >= self.width:
                cell_col = self.width - 1
            if cell_row >= self.height:
                cell_row = self.height - 1
            cell_x = self.left + cell_col * self.cell_size
            cell_y = self.top + cell_row * self.cell_size
            return cell_row, cell_col
        return None

    def on_click(self, cell_coords):
        pass
