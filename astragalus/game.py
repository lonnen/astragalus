from itertools import chain
from typing import List, Tuple

PLAYERS = [PROTAGONIST, ANTAGONIST] = [True, False]


class KnucklebonesGame(object):
    def __init__(self):
        self.game = KnucklebonesBoard()

    def valid_moves(self):
        return self.game.generate_legal_moves()

    def over(self):
        return self.game.is_game_over()

    def score(self):
        """Positive score means player 1 is ahead,
        negative score means player 2"""
        p1, p2 = self.game.scores()
        return p1 - p2

    def make_move(self, move):
        self.moves.push()

    def undo_move(self):
        self.moves.pop()

    def state(self):
        return self.game.state()

    @classmethod
    def load(cls, self):
        pass

    def copy(self):
        return self.load(self.state())


class KnucklebonesBoard(object):
    def __init__(self):
        self.raw_board = board = [0] * 18  # 2x3x3
        self.boards = [
            [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]],

            [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]],
        ]

        self.moves = []
        self.turn = PROTAGONIST

    @staticmethod
    def relative_positon_to_raw_board_position(board, column, row):
        return (board * 3 * 3) + (column * 3) + row

    def generate_legal_moves(self) -> List[int]:
        """Return the index of any row with space for another number"""
        return [index for (index, col) in enumerate(self.columns) if 0 in col]

    def is_game_over(self) -> bool:
        """the game is over when either board is full"""
        return any(all(board) for board in self.boards)

    def push(self, column, dice_roll) -> None:
        move = {}

        board_number = (0 if self.turn is PROTAGONIST else 1)
        board = self.boards[board_number]
        row = board[column].index(0)

        move[self.relative_positon_to_raw_board_position(board, column, row)] = dice_roll

        # caclulate any placement cancelled out on the opposing board
        other_board = self.boards[(board_number + 1) % 2]

        cancelled_placements = (pos for pos, value in enumerate(other_board[column]) if value == dice_roll)

        for cancellation in cancelled_placements:
            move[self.relative_positon_to_raw_board_position(board, column, cancellation)] = 0

        # apply the move
        for position, value in move:
            self.raw_board[position] = value

        self.turn = not self.turn
        self.moves.push(move)

    def pop(self) -> None:
        """Restores the previous board position"""
        move = self.moves.pop()
        self.turn = not self.turn

        # reverse apply the move
        val = 0
        positions_to_zero = []
        positions_to_restore = []
        for position, value in move.items():
            if value > 0:
                val = value
                positions_to_zero.append(position)
            else:
                positions_to_restore.append(position)

    def scores(self) -> Tuple[int, int]:
        """The score is the sum of the pieces of each board"""
        return (sum(board) for board in self.boards)
