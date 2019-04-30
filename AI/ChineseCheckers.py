import numpy as np
from collections import deque

# Used to translate board positions in [col][row] to 1-d
_translation = {
                0 : (0,),
                1 : (1, 2),
                2 : (3, 4, 5),
                3 : (6, 7, 8, 9),
                4 : (10, 11, 12, 13, 14),
                5 : (15, 16, 17, 18, 19, 20),
                6 : (21, 22, 23, 24, 25, 26, 27),
                7 : (28, 29, 30, 31, 32, 33, 34, 35),
                8 : (36, 37, 38, 39, 40, 41, 42, 43, 44),
                9 : (45, 46, 47, 48, 49, 50, 51, 52),
                10: (53, 54, 55, 56, 57, 58, 59),
                11: (60, 61, 62, 63, 64, 65),
                12: (66, 67, 68, 69, 70),
                13: (71, 72, 73, 74),
                14: (75, 76, 77),
                15: (78, 79),
                16: (80,)
                }

# Makes the 1-d to [row][col] from the _translation dict
_reverse = {slot: (key, index) for key in _translation for index, slot in enumerate(_translation[key])}

class ChineseCheckers:
    def __init__(self):
        """Represents a ChineseCheckers board with a BFS AI"""
        
        # Settings board of empty spaces
        self._marbles = np.full(81, 0)

        self._marbles[:10] = 2 # Two represents player two's marbles
        self._marbles[71:] = 1 # One represents player one's marbles

    def __repr__(self):
        return 'ChineseCheckers()'

    def __str__(self):
        """Prints an ascii representation of the board"""
        
        return '\n'.join(' '.join(map(str, self._marbles[row[0]:(row[-1] + 1)])).center(18) for row in _translation.values())

    def  __len__(self):
        return len(self._marbles)

    def __getitem__(self, indices):
        """Returns slot contents from board"""
        
        if isinstance(indices, tuple):
            row, col = indices

            if row > len(_translation) or col > len(self):
                raise IndexError
            
            return self._marbles[_translation[row][col]]

        if indices >= len(_translation):
            raise IndexError

        line = _translation[indices]
        start, end = line[0], line[-1]
        return self._marbles[start:(end + 1)]

    def __setitem__(self, indices, value):
        """Sets slot content at indices"""
        row, col = indices
        self._marbles[_translation[row][col]] = value

    def get_move(self, player_num):
        """Returns ideal move in row, col form"""

        paths = ((index[0], self._BFS_marble(*_reverse[index[0]])) for index in np.argwhere(self._marbles == player_num))
        paths = filter(lambda p: p[1] is not None, paths)

        try:
            start, path = max(paths, key = lambda p: p[1][-1])
            return _reverse[start], _reverse[path[1]]

        except IndexError: # If AI cannot make a move
            return None

    def is_over(self) -> int:
        """Returns 0 if no winner, 1 if player one win, or 2 if player two win"""

        if np.all(self._marbles[71:] == 2):
            return 1
        elif np.all(self._marbles[:9] == 1):
            return 2
        else:
            return 0
    
    def _BFS_marble(self, row, col):
        """Looks for all paths on the board for a certain marble"""

        paths = dict() # Representing all possible shortest paths
        search_q = deque() # Start search from given marble
        search_q.append((None, _translation[row][col]))

        while search_q:
            parent, slot = search_q.popleft()

            if slot not in paths: # Checking if already visited and if empty
                paths[slot] = paths.get(parent, tuple()) + (slot,)

                row, col = _reverse[slot]

                # Attempts to enqueue new search slots, but will catch errors of nonexistent vertices
                try:
                    next_slot = _translation[row + 1][col]

                    if self._marbles[next_slot] == 0:
                        search_q.append((slot, next_slot))
                    else:
                        jump_slot = _translation[row + 2][col]

                        if self._marbles[jump_slot] == 0:
                            search_q.append((slot, jump_slot))
                
                except (IndexError, KeyError):
                    pass

                try:
                    next_slot = _translation[row + 1][col + 1]

                    if self._marbles[next_slot] == 0:
                        search_q.append((slot, next_slot))
                    else:
                        jump_slot = _translation[row + 2][col + 2]
                        if self._marbles[jump_slot] == 0:
                            search_q.append((slot, jump_slot))
                            
                except (IndexError, KeyError):
                    pass

            
        if paths:
            return paths[max(paths.keys())]


if __name__ == '__main__':
    import time
    
    board = ChineseCheckers()
    for _ in range(10):
        print(board)

        # AI makes P2 Move
        start, end = board.get_move(2)
        board[start], board[end] = board[end], board[start]

        print('AI moved from {} to {}'.format(start, end))
        print(board)

        # Player makes P1 move
        srow, scol = map(int, input('Enter start : ').split())
        mrow, mcol = map(int, input('Enter end   : ').split())

        board[srow, scol], board[mrow, mcol] = board[mrow, mcol], board[srow, scol]

    print(board)
