import tkinter as tk
from collections import deque

import ChineseCheckers as CC
from ChineseCheckers import ChineseCheckers

class ChineseCheckerBoard:
    def __init__(self, dimension: int, board_color: str, color_one, color_two) -> None:
        """Creates the GUI representation of a two-player Chinese Checker board"""

        # Ensuring window size is a positive integer
        assert isinstance(dimension, int) and dimension > 0

        self.dimension = dimension

        self.board_color = board_color
        self.color_one, self.color_two = color_one, color_two

        self.to_color = deque()
        self.to_delete = deque()

        self.x, self.y = 0, 0
        self.clicked = False

        # Simple window properties
        self.root = tk.Tk()
        self.root.title('Chinese Checkers')
        self.root.resizable(False, False)

        self.board = tk.Canvas(self.root, width=dimension, height=dimension)
        self.board.configure(background='black')
        self.board.grid(row=0, column=0)

        self.AI = CC.ChineseCheckers()
        self.turn_counter = 0

        self._draw_board()

        self.root.after(100, self.get_move)
        
    def _draw_board(self) -> None:
        """Draws the board on the canvas"""
        half = self.dimension/2

        # Creates diamond representation of the board
        self.board.create_polygon(0, half, half, 0,
                                  half, 0, self.dimension, half,
                                  self.dimension, half, half, self.dimension,
                                  half, self.dimension, 0, half,
                                  fill=self.board_color)

        width_dict = dict()
        self.marbles = list()

        counter = 0
        for i in range(17):
            # Draw first half of the board
            if i < 9:
                row_h = self.dimension / 17 * i + self.dimension / 34
                row_w = row_h * 2
                start_x = half - row_h

                width_dict[i] = (row_w, start_x)

                marble_space = row_w / (i+1)
                for j in range(i+1):
                    marb_x = start_x + marble_space * j + marble_space/2
                    marb_y = row_h

                    x0, y0, x1, y1 = self.circle_coordinates(marb_x, marb_y,
                                                             self.dimension/81)

                    self.board.create_oval(x0, y0, x1, y1)
                    self.marbles.append((x0, y0, x1, y1))

                    self.board.create_text(marb_x, marb_y - self.dimension / 34, text = str(counter))
                    counter += 1

            # Draw second half of the board
            elif i >= 9:
                row_h = self.dimension / 17 * i + self.dimension / 34

                row_w, start_x = width_dict[17-i-1]

                marble_space = row_w / (17-i)
                for j in range(17 - i):
                    marb_x = start_x + marble_space * j + marble_space/2
                    marb_y = row_h

                    x0, y0, x1, y1 = self.circle_coordinates(marb_x, marb_y,
                                                             self.dimension / 81)
                    
                    self.board.create_oval(x0, y0, x1, y1)
                    self.marbles.append((x0, y0, x1, y1))

                    self.board.create_text(marb_x, marb_y - self.dimension / 34, text = str(counter))
                    counter += 1

    def color_marbles(self) -> None:
        """Colors marbles from animation queue"""

        if self.to_color:
            marble, color = self.to_color.popleft()

            x0, y0, x1, y1 = self.marbles[marble]
            self.board.create_oval(x0, y0, x1, y1, fill=color)

            self.color_marbles()

        self.root.update()

    def move_marble(self, one, two, color):
        """Adds coordinates and a colors to the queue for a move"""

        self.to_color.append((one, self.board_color))
        self.to_color.append((two, color))

    def get_move(self):
        """Depending on turn counter, gets AI or human move"""

        # AI Turn, deleting old line (if there are any)
        if self.turn_counter % 2 == 0:
            while self.to_delete:
                self.board.delete(self.to_delete.pop())

            # Updating Canvas after deletion
            self.root.update()
            
            start, end = self.AI.get_move(2, True) # Getting one-d representation

            # "Moves" marble on cavas
            self.move_marble(start, end, self.color_one)
            s_row, s_col = CC._reverse[start]
            e_row, e_col = CC._reverse[end]
        
            # Walks coordinates back until original point found, draws red lines back
            while (e_row, e_col) != (s_row, s_col):
                prev_row, prev_col = e_row, e_col

                if e_col > s_col:
                    e_col -= 1
                e_row -= 1

                # Getting position of last passed through point
                x0, y0, *_ = self.marbles[CC._translation[prev_row][prev_col]]
                x0 += self.dimension/81
                y0 += self.dimension/81

                # Getting position of next passed through point
                x1, y1, *_ = self.marbles[CC._translation[e_row][e_col]]
                x1 += self.dimension/81
                y1 += self.dimension/81

                self.to_delete.append(self.board.create_line(x0, y0, x1, y1, fill = 'red'))
            
        else:
            start, end= int(input('Start: ')), int(input('End  : '))
            self.move_marble(start, end, self.color_two)
            print()

        # Updating AI's representation of the board
        self.AI._marbles[start], self.AI._marbles[end] =\
                                     self.AI._marbles[end], self.AI._marbles[start]

        self.color_marbles()
        self.turn_counter += 1

        self.root.after(100, self.get_move)

    @staticmethod
    def circle_coordinates(center_x, center_y, radius):
        """Returns coordinates to draw a circle with draw oval tkinter functikon"""
        return center_x - radius, center_y - radius, center_x + radius, center_y + radius


if __name__ == '__main__':
    global board
    
    from multiprocessing import Process
    board = ChineseCheckerBoard(750, 'white', 'orangered2', 'green')

    for i in range(10):
        board.to_color.append((i, 'orangered2'))

    for i in range(71, 81):
        board.to_color.append((i, 'green'))

    board.root.mainloop()
