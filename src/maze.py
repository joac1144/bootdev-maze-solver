import time
import random

from graphics import Window
from cell import Cell

class Maze:
    def __init__(self, x1: int, y1: int, num_rows: int, num_cols: int, cell_size_x: int, cell_size_y: int, window: Window|None = None, seed: int|None = None):
        self.__window = window
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__cells: list[list[Cell]] = []

        if seed != None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for _ in range(self.__num_cols):
            columns: list[Cell] = []
            for _ in range(self.__num_rows):
                columns.append(Cell(self.__window))
            self.__cells.append(columns)
        
        if self.__window is None:
            return

        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)
    
    def __draw_cell(self, i: int, j: int):
        if self.__window is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()
    
    def __animate(self):
        if self.__window is None:
            return
        self.__window.redraw()
        time.sleep(0.005)
    
    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__cells[self.__num_cols-1][self.__num_rows-1].has_bottom_wall = False
        self.__draw_cell(0, 0)
        self.__draw_cell(self.__num_cols-1, self.__num_rows-1)
    
    def __break_walls_r(self, i: int, j: int):
        self.__cells[i][j].visited = True
        while True:
            queue: list[tuple[int, int]] = []

            if j > 0 and not self.__cells[i][j-1].visited:
                queue.append((i, j-1))
            if j < self.__num_rows - 1 and not self.__cells[i][j+1].visited:
                queue.append((i, j+1))
            if i > 0 and not self.__cells[i-1][j].visited:
                queue.append((i-1, j))
            if i < self.__num_cols - 1 and not self.__cells[i+1][j].visited:
                queue.append((i+1, j))

            if len(queue) == 0:
                self.__draw_cell(i, j)
                return
            
            direction = random.randrange(len(queue))
            chosen_cell = queue[direction]

            if chosen_cell[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False
            if chosen_cell[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False
            if chosen_cell[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False
            if chosen_cell[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False

            self.__break_walls_r(chosen_cell[0], chosen_cell[1])
        
    def __reset_cells_visited(self):
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__cells[i][j].visited = False

    def solve(self):
        return self.__solve_r(0, 0)
    
    def __solve_r(self, i: int, j: int):
        current_cell = self.__cells[i][j]
        self.__animate()
        current_cell.visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        if j > 0:
            other = self.__cells[i][j-1]
            if other.has_bottom_wall == False and current_cell.has_top_wall == False and other.visited == False:
                current_cell.draw_move(other)
                if self.__solve_r(i, j-1):
                    return True
                current_cell.draw_move(other, undo=True)
        if j < self.__num_rows - 1:
            other = self.__cells[i][j+1]
            if other.has_top_wall == False and current_cell.has_bottom_wall == False and other.visited == False:
                current_cell.draw_move(other)
                if self.__solve_r(i, j+1):
                    return True
                current_cell.draw_move(other, undo=True)
        if i > 0:
            other = self.__cells[i-1][j]
            if other.has_right_wall == False and current_cell.has_left_wall == False and other.visited == False:
                current_cell.draw_move(other)
                if self.__solve_r(i-1, j):
                    return True
                current_cell.draw_move(other, undo=True)
        if i < self.__num_cols - 1:
            other = self.__cells[i+1][j]
            if other.has_left_wall == False and current_cell.has_right_wall == False and other.visited == False:
                current_cell.draw_move(other)
                if self.__solve_r(i+1, j):
                    return True
                current_cell.draw_move(other, undo=True)

        return False
