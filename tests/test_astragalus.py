import unittest

from astragalus import KnucklebonesBoard, PROTAGONIST, ANTAGONIST, STARTING_POSITION


NEW_STARTING_POSITION = "0001112223334445500"

class TestBoard(unittest.TestCase):
    state_log = [
        # roll, column, antagonist total, protagonist total, columns (0-based)
        (1, 1, 1, 0, (1, 2, 3)),
        (1, 1, 0, 1, (1, 2, 3)),
        (6, 2, 6, 1, (1, 2, 3)),
        (2, 3, 6, 3, (1, 2, 3)),
        (4, 1, 10, 3, (1, 2, 3)),
        (5, 2, 10, 8, (1, 2, 3)),
        (5, 2, 15, 3, (1, 2, 3)),
        (1, 1, 15, 6, (1, 2, 3)),
        (3, 2, 18, 6, (1, 2, 3)),
        (4, 1, 14, 10, (1, 2, 3)),
        (1, 1, 15, 6, (1, 3)),
        (5, 2, 10, 11, (1, 2, 3)),
        (3, 2, 19, 11, (1, 2, 3)),
        (5, 2, 19, 26, (1, 2, 3)),
        (2, 3, 21, 24, (1, 3)),
        (6, 2, 15, 30, (1, 2, 3)),
        (5, 2, 20, 10, (1, 2, 3)),
        (4, 1, 20, 22, (1, 2, 3)),
        (1, 1, 23, 22, (1, 3)),
        (3, 1, 23, 25, (1, 2, 3)),
        (4, 1, 27, 9, (1, 3)),
        (5, 2, 22, 14, (1, 2, 3)),
        (6, 2, 28, 8, (2, 3)),
        (6, 2, 22, 14, (1, 2, 3)),
        (4, 2, 26, 14, (2, 3)),
        (3, 2, 14, 17, (1, 2, 3)),
        (5, 2, 19, 12, (2, 3)),
        (2, 3, 17, 14, (1, 2, 3)),
        (3, 2, 20, 11, (2, 3)),
        (4, 1, 16, 15, (1, 2, 3)),
        (5, 3, 21, 15, (1, 3)),
        (1, 2, 21, 16, (1, 2, 3)),
        (4, 1, 25, 12, (1, 3)),
        (2, 1, 25, 14, (1, 2, 3)),
        (6, 3, 31, 14, (3,)),
        (6, 3, 25, 20, (1, 2, 3)),
        (6, 3, 31, 14, (3,)),
        (5, 3, 26, 19, (1, 2, 3)),
        (4, 3, 30, 19, (3,)),
        (3, 2, 27, 22, (1, 2, 3)),
        (6, 3, 45, 22, (2, 3)),
        (2, 1, 45, 28, (1, 3)),
        (1, 2, 46, 27, (2,)),
    ]
    """A game played in Jul 6, 2023 against Shrumy, ending in victory for Shrumy"""

    def test_init(self):
        """a board should initialize empty"""
        board = KnucklebonesBoard()
        self.assertEqual(str(board), STARTING_POSITION)
        board = KnucklebonesBoard(NEW_STARTING_POSITION)
        self.assertEqual(str(board), NEW_STARTING_POSITION)

    def test_repr(self):
        """a board should initialize empty"""
        board = KnucklebonesBoard(NEW_STARTING_POSITION)
        self.assertEqual(repr(board), "KnucklebonesBoard('0001112223334445500')")

    def test_push(self):
        """push should mutate the board"""
        board = KnucklebonesBoard()
        board.push(2, 6)
        self.assertEqual(str(board), "0006000000000000001")
        board.push(2, 5)
        self.assertEqual(str(board), "0006000000005000000")
        # this should cancel an opposing value
        board.push(2, 5)
        self.assertEqual(str(board), "0006500000000000001")

        # load values
        board.push(1, 1)
        self.assertEqual(str(board), "0006500001000000000")
        board.push(2, 1)
        self.assertEqual(str(board), "0006510001000000001")

        # same value twice should cause no problems
        board.push(1, 1)
        self.assertEqual(str(board), "0006510001100000000")

        # this should overflow column 2, causing an illegal push
        with self.assertRaises(ValueError):
            board.push(2, 6)

    def test_outcome(self):
        """verify that the board can detect an accurate game outcome
        """
        # ANTAGONIST has all the points, board full
        outcome = KnucklebonesBoard("0000000002222222221").outcome()
        self.assertEqual(outcome.termination, True)
        self.assertEqual(outcome.winner, ANTAGONIST)
        self.assertEqual(outcome.result(), "Antagonist")
        # Both players have some points, PROTAGONIST has more
        outcome = KnucklebonesBoard("3333333332222222200").outcome()
        self.assertEqual(outcome.termination, True)
        self.assertEqual(outcome.winner, PROTAGONIST)
        self.assertEqual(outcome.result(), "Protagonist")
        # Neither board is full, so there is no outcome yet
        outcome = KnucklebonesBoard("3333333302222222201").outcome()
        self.assertEqual(outcome.termination, False)
        self.assertEqual(outcome.winner, None)
        self.assertEqual(outcome.result(), None)

    def test_game(self):
        """verify that the game board can match the inputs and outputs of a
        playthrough
        """
        board = KnucklebonesBoard()
        for roll, column, antagonist_total, protagonist_total, _ in self.state_log:
            board.push(column, roll)
            self.assertEqual(board.scores(), [antagonist_total, protagonist_total])
        self.assertTrue(board.is_game_over())
        self.assertTrue(board.turn == ANTAGONIST)

    def test_pop(self):
        """verify that a game in its end state can be undone step by step"""
        board = KnucklebonesBoard()
        for roll, column, _, _, _ in self.state_log:
            board.push(column, roll)

        # now again, in reverse!
        for _, _, ant_total, pro_total, _ in self.state_log[::-1][1:]:
            board.pop()
            self.assertEqual(board.scores(), [ant_total, pro_total])

        self.assertEqual(len(board.moves), 1)
        self.assertEqual(board.turn, ANTAGONIST)

    def test_generate_legal_moves(self):
        """verify that the board can generate complete and accurate available moves"""
        board = KnucklebonesBoard()
        for roll, column, _ant, _pro, moves in self.state_log:
            self.assertEqual(board.generate_legal_moves(), moves)
            board.push(column, roll)
