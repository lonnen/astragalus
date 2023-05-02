from itertools import chain


class KnucklebonesGame(object):
    def __init__(self):


    def valid_moves(self):
        rows = [self.board[i : i + 3] for i in range(0, len(self.board), 3)]
        empty_spaces = [index for (index, cell) in enumerate(self.board) if cell == 0]
        # incomplete
        return []

    def over(self):
        """Check to see if either player board is full, indicating the game is over"""
        boards = [chain.from_iterable(player_board) for player_board in self.board]
        return any(all(cell is not 0 for cell in board) for board in boards)

    def make_move(self, move):
        self.moves.push()

    def undo_move(self):
        self.moves.pop()

    def score(self):
        return 0

    def state(self):
        pass

    @classmethod
    def load(cls, self):
        pass

    def copy(self):
        #return self.load(self.state())
        pass

class KnucklebonesBoard(object):
    def __init__(self):
        self.raw_board = [0] * 18 # 2x3x3
        self.moves = []

    def rows(self):
        return list(zip(*[iter(self.raw_board)]*3))

    def boards(self):
        return list(zip(*[iter(self.rows())]*3))

    def generate_legal_moves(self):
        empty_spaces = [index for (index, cell) in enumerate(self.board) if cell == 0]
        return

    def is_game_over():
        pass

    def push(move):
        pass

    def pop():
        """
        Restores the previous board position
        """
        pass