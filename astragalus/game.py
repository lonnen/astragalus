"""
A library for implementin and exploring states of the minigame Knucklebones from Cult of the Lamb
"""

from collections import Counter
import dataclasses

from typing import List, Tuple, Literal, Optional

Player = bool
PLAYERS = [PROTAGONIST, ANTAGONIST] = [True, False]
PlayerName = Literal["protagonist", "antagonist"]
PLAYER_NAMES: List[PlayerName] = ["protagonist", "antagonist"]

STARTING_POSITION = "0000000000000000000"
"""The standard starting position for a game of Knucklebones with an empty board and antagonist
start using Lonnen-Otis Notation (LON)

This notation maps the state of the game:

Protagonist Antagonist*
        0 1 2       3 4 5
        0 1 2       3 4 5
        0 1 2       3 4 0

Into a single LON String:

    0001112223334445500

"""


@dataclasses.dataclass
class Outcome:
    """
    Information about the outcome of a finished game
    """

    termination: bool
    winner: Optional[Player]

    def result(self) -> str:
        """Returns the human-readable indicator of the winner
        """
        return "Protagonist" if self.winner else "Antagonist"


class InvalidMoveError(ValueError):
    """Raised when move notation is not syntactically valid"""


class IllegalMoveError(ValueError):
    """Raised when the attempted move is illegal in the current position"""


class KnucklebonesBoard(object):
    """
    A board representing the position of the current dice scores.

    This board is initialized with the standard, empty starting position, unless otherwise
    specified in the optional *board_lon* argument.
    """
    def __init__(self, board_lon: Optional[str] = STARTING_POSITION) -> None:

        if board_lon is None:
            board_lon = STARTING_POSITION

        # initialize board in STARTING_POSITION
        self.boards = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

        self.moves = []
        self.turn = PROTAGONIST

        # go through setup if an alternatie is provided
        if board_lon is not STARTING_POSITION:
            self.set_board_lon(board_lon)

    def set_board_lon(self, lon: str) -> None:
        """
        Parses *lon* and sets up the board accordingly
        """

        lon = lon.strip()
        if len(lon) != 19:
            raise ValueError(f"expected 3*3*2 +1 values: {lon!r}")

        valid_dice = list(range(7))
        if any([p not in valid_dice for p in lon[:-1]]):
            raise ValueError(f"all rolls must be a d6 or 0: {lon[:-1]!r}")

        if lon[-1] not in ["0", "1"]:
            raise ValueError(f"player must be 0 or 1: {lon[:-1]!r}")

        # load the valid lon
        self.turn = bool(lon[-1])

        for board in range(2):
            for column in range(3):
                for cell in range(3):
                    self.boards[board][column][cell] = int(
                        lon[(board * 3 * 3) + (column * 3) + cell]
                    )

    def board_lon(self) -> str:
        """
        Gets the board LON (e.g. ``0001112223334445500``).
        """
        state = [
            roll for roll in [column for column in [board for board in self.boards]]
        ]
        return "".join([int(i) for i in (state + [self.turn])])

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.board_lon()!r})"

    def __str__(self) -> str:
        return self.board_lon()

    def generate_legal_moves(self) -> List[int]:
        """Return the index of any row with space for another number"""
        board = self.boards[0 if self.turn is PROTAGONIST else 1]
        return tuple(i + 1 for (i, col) in enumerate(board) if 0 in col)

    def is_game_over(self) -> bool:
        """the game is over when either board is full"""
        return any(all(board) for board in self.boards)

    def push(self, column, dice_roll) -> None:
        """apply a move to the board state and push the change to a list of moves"""
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
        self.moves.append([column + 1, dice_roll, *cancelled_positions])

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
        for _ in cancelled_positions:
            other_column[other_column.index(0)] = dice_roll

    def scores(self) -> Tuple[int, int]:
        """The sum of the values of each dice multiplied by the number of
        dice of that value in its column, i.e. 1-2-3 is 1x1 + 2x1 + 3x1 = 6,
        and 4-1-4 is 4x2 + 1x1 + 4x2 = 17."""
        scores = []
        for board in self.boards:
            board_score = 0
            for column in board:
                board_score += sum(
                    [
                        value * count * count
                        for (value, count) in Counter(column).items()
                    ]
                )
            scores.append(board_score)
        return scores

    def state(self):
        """Board state serializes compactly from:

        Protagonist* Antagonist
        0 1 2        3 4 5
        0 1 2        3 4 5
        0 1 2        3 4 0

        Into a single string:

        0001112223334445501

        Where the final bit indiciates which player is active (the Antagonist,
        in this case)
        """
        state = [
            roll for roll in [column for column in [board for board in self.boards]]
        ]
        return [float(i) for i in (state + [self.turn])]

    @classmethod
    def load(cls, state):
        game = KnucklebonesBoard()
        game.turn = bool(state[-1])

        for board in range(2):
            for column in range(3):
                for cell in range(3):
                    game.boards[board][column][cell] = int(
                        state[(board * 3 * 3) + (column * 3) + cell]
                    )

        return game


class KnucklebonesGame(object):
    def __init__(self):
        self.game = KnucklebonesBoard()

    def valid_moves(self):
        return self.game.generate_legal_moves()

    def over(self):
        return self.game.is_game_over()

    def score(self):
        """Positive score means  is ahead, negative score means player 2"""
        protagonist, antagonist = self.game.scores()
        return protagonist - antagonist

    def make_move(self, move):
        self.moves.push()

    def undo_move(self):
        self.moves.pop()

    def state(self):
        return self.game.state()

    def copy(self):
        return self.load(self.state())
