from itertools import chain


class KnucklebonesGame(object):
    def __init__(self):
        self.game = KnucklebonesBoard()

    def valid_moves(self):
        return self.game.generate_legal_moves()

    def over(self):
        return self.game.is_game_over()

    def make_move(self, move):
        self.moves.push()

    def undo_move(self):
        self.moves.pop()

    def score(self):
        '''Positive score means player 1 is ahead,
        negative score means player 2'''
        p1, p2 = self.game.scores()
        return p1 - p2

    def state(self):
        return self.game.state()

    @classmethod
    def load(cls, self):
        pass

    def copy(self):
        return self.load(self.state())

class KnucklebonesBoard(object):
    def __init__(self):
        self.raw_board = [0] * 18 # 2x3x3
        self.moves = []

    def rows(self):
        return list(zip(*[iter(self.raw_board)]*3))

    def boards(self):
        return list(zip(*[iter(self.rows())]*3))

    def generate_legal_moves(self):
        """Check to see if either player board is full, indicating the game is over"""
        #rows = [self.board[i : i + 3] for i in range(0, len(self.board), 3)]
        #empty_spaces = [index for (index, cell) in enumerate(self.board) if cell == 0]
        boards = [chain.from_iterable(player_board) for player_board in self.board]
        return any(all(cell is not 0 for cell in board) for board in boards)


    def is_game_over():
        pass

    def push(move):
        pass

    def pop():
        """
        Restores the previous board position
        """
        pass