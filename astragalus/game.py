from collections import Counter

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
        self.boards = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

        self.moves = []
        self.turn = PROTAGONIST

    def generate_legal_moves(self) -> List[int]:
        """Return the index of any row with space for another number"""
        return [index for (index, col) in enumerate(self.columns) if 0 in col]

    def is_game_over(self) -> bool:
        """the game is over when either board is full"""
        return any(all(board) for board in self.boards)

    def push(self, column, dice_roll) -> None:
        column -= 1
        board_number = 0 if self.turn is PROTAGONIST else 1
        opposing_board_number = (board_number + 1) % 2

        board = self.boards[board_number]
        board_column = board[column]
        board_column[board_column.index(0)] = dice_roll

        # caclulate any placement cancelled out on the opposing board
        other_board = self.boards[opposing_board_number]

        cancelled_positions = [
            pos for pos, value in enumerate(other_board[column]) if value == dice_roll
        ]

        # apply the move
        for cancellation in cancelled_positions:
            other_board[column][cancellation] = 0

        # cycle turn
        self.turn = not self.turn
        self.moves.append([column+1, dice_roll, *cancelled_positions])

    def pop(self) -> None:
        """Restores the previous board position"""
        column, dice_roll, *cancelled_positions = self.moves.pop()
        column -= 1
        self.turn = not self.turn

        board_number = 0 if self.turn is PROTAGONIST else 1
        opposing_board_number = (board_number + 1) % 2

        board_column = self.boards[board_number][column]

        # undo the move
        board_column[board_column.index(dice_roll)] = 0

        # undo the cancellations
        other_board = self.boards[opposing_board_number]
        other_column = other_board[column]
        for cancellation in cancelled_positions:
            other_column[other_column.index(0)] = dice_roll

    def scores(self) -> Tuple[int, int]:
        """The sum of the values of each dice multiplied by the number of
        dice of that value in its column, i.e. 1-2-3 is 1x1 + 2x1 + 3x1 = 6,
        and 4-1-4 is 4x2 + 1x1 + 4x2 = 17."""
        scores = []
        for board in self.boards:
            board_score = 0
            for column in board:
                board_score += sum([
                    value * count * count
                    for (value, count) in Counter(column).items()
                ])
            scores.append(board_score)
        return scores
