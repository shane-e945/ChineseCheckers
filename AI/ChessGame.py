from stockfish import Stockfish

class ChessGame:
    def __init__(self, executable_path: str, depth = 20):
        """Initializes a chess game that tracks board state and uses
        the StockFish API to make moves"""
        
        self.exe = executable_path

        self._moves = list()
        self._engine = Stockfish(executable_path, depth)
    
    def __repr__(self):
        return 'ChessGame({})'.format(self.exe)
        
    def __str__(self):
        return '[{}]'.format(','.join(self._moves))
    
    @staticmethod    
    def indices_to_square(row: int, column: int) -> str:
        """Takes a row and column in c-style notation (i.e. starting at 0)
        and returns it in chess notation"""
        
        letters = 'abcdefgh'
        numbers = '87654321'
        
        return '{}{}'.format(letters[column], numbers[row])
    
    @staticmethod 
    def square_to_indices(square: str):
        """Takes in chess notation of a square (two letters– e.g. "a8") and returns
        c-style indices in a tuple"""
        
        col, row = square
        
        print(row, col)
        
        letters = 'abcdefgh'
        numbers = '87654321'
        
        return numbers.index(row), letters.index(col)
        
    def make_move(self, old_position: str, new_position: str) -> bool:
        """Attempts to make a move on the board state, returns a bool
        showing whether that move is legal"""
        
        self._moves.append('{}{}'.format(old_position, new_position))
        self._engine.set_position(self._moves)
    
    def best_move(self) -> str:
        """Returns a string representing the old position of a piece and the
        new position of the piece"""
        
        to_return = self._engine.get_best_move()
        self._moves.append(to_return)

        self._engine.set_position(self._moves)
        
        return to_return
    
    def game_over(self) -> bool:
        """Returns a boolean representing checkmate"""
        
        return not bool(self._moves[-1])
        
