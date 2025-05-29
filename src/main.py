from graphics import Window#, Point, Line
from maze import Maze

def main():
    print("Starting the application...")

    window_size_x = 800
    window_size_y = 800
    win = Window(window_size_x, window_size_y)
    
    rows = 20
    columns = 20
    margin = 100
    cell_size_x = (window_size_x - 2 * margin) // columns
    cell_size_y = (window_size_y - 2 * margin) // rows

    maze = Maze(margin, margin, rows, columns, cell_size_x, cell_size_y, win, 10)

    if maze.solve():
        print("Maze solved successfully!")
    else:
        print("Maze can not be solved.")

    win.wait_for_close()

if __name__ == "__main__":
    main()