"""
A library for implementin and exploring states of the minigame Knucklebones from Cult of the Lamb
"""

from collections import Counter
import dataclasses
from itertools import chain

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

    def result(self) -> Optional[str]:
        """Returns the human-readable indicator of the winner, or None if there is no winner"""
        if self.winner is None:
            return None
        return "Protagonist" if self.winner else "Antagonist"


class InvalidMoveError(ValueError):
    """Raised when move notation is not syntactically valid"""


class IllegalMoveError(ValueError):
    """Raised when the attempted move is illegal in the current position"""


@dataclasses.dataclass
class Move:
    """
    Represents a move as the player who made it, the dice roll, placement, and how many
    cancellations it caused
    """

    player: bool
    """Which player made the move"""

    column: int
    """the column where the roll was placed"""

    roll: int
    """The value of the dice roll bing placed"""

    cancellations: int
    """how many values were cancelld from the opposing column"""


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
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # ANTAGONIST
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # PROTAGONIST
        ]

        self.moves = []
        self.turn = ANTAGONIST

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

        # string into a list
        lon = [int(x) for x in [*lon]]

        if any([p not in set(range(7)) for p in lon[:-1]]):
            raise ValueError(f"all rolls must be a d6 or 0: {lon[:-1]!r}")

        if lon[-1] not in [0, 1]:
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
        state = list(chain.from_iterable(chain.from_iterable(self.boards))) + [
            1 if self.turn else 0
        ]
        return "".join(str(r) for r in state)

    def __str__(self) -> str:
        return self.board_lon()

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.board_lon()!r})"

    def copy(self):
        """Creates a copy of the board."""
        board = type(self)(None)
        board.boards = self.boards
        board.moves = self.moves
        board.turn = self.turn

        return board

    def get_board(self, agonist: Optional[Player] = None):
        """Return the board for either the antagonist or protagonist

        :param agonist: the player whose board should be retrieved, or the current player if None
        """
        if agonist is None:
            agonist = self.turn
        return self.boards[1 if agonist else 0]

    def generate_legal_moves(self) -> List[int]:
        """Return the index of any row with space for another number"""
        board = self.get_board()
        return tuple(i + 1 for (i, col) in enumerate(board) if 0 in col)

    def is_game_over(self) -> bool:
        """the game is over when either board is full"""
        for board in self.boards:
            if all(all(rows) for rows in board):
                return True
        return False

    def push(self, column: int, dice_roll: int) -> None:
        """apply a move to the board state and push the change to a list of moves

        :param column: 1, 2, or 3
        :param dice_roll: 1, 2, 3, 4, 5, or 6
        """
        column -= 1

        if not (dice_roll > 0 and dice_roll < 7):
            raise IllegalMoveError(f"Dice Rolls must be a d6, not {dice_roll!s}")

        board_column = self.get_board()[column]
        try:
            board_column[board_column.index(0)] = dice_roll
        except ValueError:
            raise IllegalMoveError(f"There is no empty value in {board_column!s}")

        # caclulate any cancellations out on the opposing board
        other_board = self.get_board(not self.turn)
        other_column = other_board[column]

        # this loop is unrolled, resulting in some duplication
        # but a loop that actually mutates in place is not much
        # prettier
        cancellations = 0
        if other_column[0] == dice_roll:
            other_column[0] = 0
            cancellations += 1
        if other_column[1] == dice_roll:
            other_column[1] = 0
            cancellations += 1
        if other_column[2] == dice_roll:
            other_column[2] = 0
            cancellations += 1

        # cycle turn
        self.moves.append(Move(self.turn, column + 1, dice_roll, cancellations))
        self.turn = not self.turn

    def pop(self) -> Move:
        """Restores the previous board position"""
        move = self.moves.pop()
        player, column, dice_roll, cancellations = (
            move.player,
            move.column - 1,  # columns are written 1-indexed but stored 0-indexed
            move.roll,
            move.cancellations,
        )

        board_column = self.get_board(player)[column]

        # we're now back to the turn of the player who made the move
        self.turn = player

        # undo the move
        try:
            board_column[board_column.index(dice_roll)] = 0
        except ValueError:
            raise IllegalMoveError(f"There is no {dice_roll!r} in {board_column!r}")

        # undo the cancellations
        other_board = self.get_board(not self.turn)
        other_column = other_board[column]
        for _ in range(cancellations):
            try:
                other_column[other_column.index(0)] = dice_roll
            except ValueError:
                raise IllegalMoveError(f"There is no empty value in {other_column!r}")

        return move

    def outcome(self) -> Outcome:
        """Check if the game is over"""
        if self.is_game_over():
            protagonist_score, antagonist_score = self.scores()
            return Outcome(True, (protagonist_score > antagonist_score))
        return Outcome(False, None)

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
