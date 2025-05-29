from __future__ import annotations
from graphics import Window, Point, Line

class Cell:
    def __init__(self, window: Window|None = None):
        self.__window = window
        self.__x1 = -1
        self.__y1 = -1
        self.__x2 = -1
        self.__y2 = -1
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
    
    def draw(self, x1: int, y1: int, x2: int, y2: int):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.__window is None:
            return
        if self.has_left_wall:
            self.__window.draw_line(Line(Point(x1, y1), Point(x1, y2)), width=4)
        else:
            self.__window.draw_line(Line(Point(x1, y1), Point(x1, y2)), width=4, fill_color="white")

        if self.has_right_wall:
            self.__window.draw_line(Line(Point(x2, y1), Point(x2, y2)), width=4)
        else:
            self.__window.draw_line(Line(Point(x2, y1), Point(x2, y2)), width=4, fill_color="white")

        if self.has_top_wall:
            self.__window.draw_line(Line(Point(x1, y1), Point(x2, y1)), width=4)
        else:
            self.__window.draw_line(Line(Point(x1, y1), Point(x2, y1)), width=4, fill_color="white")

        if self.has_bottom_wall:
            self.__window.draw_line(Line(Point(x1, y2), Point(x2, y2)), width=4)
        else:
            self.__window.draw_line(Line(Point(x1, y2), Point(x2, y2)), width=4, fill_color="white")
    
    def draw_move(self, to_cell: Cell, undo: bool = False):
        if self.__window is None:
            return
        center_self_x = (self.__x1 + self.__x2) // 2
        center_self_y = (self.__y1 + self.__y2) // 2
        center_other_x = (to_cell.__x1 + to_cell.__x2) // 2
        center_other_y = (to_cell.__y1 + to_cell.__y2) // 2

        color = "red"
        if undo:
            color = "gray"

        self.__window.draw_line(Line(Point(center_self_x, center_self_y), Point(center_other_x, center_other_y)), width=2, fill_color=color)