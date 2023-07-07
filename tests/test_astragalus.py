import unittest

from astragalus import KnucklebonesBoard

class TestBoard(unittest.TestCase):

    def test_relative_positon_to_raw_board_position(self):
        rp2rbp = KnucklebonesBoard.relative_positon_to_raw_board_position

        positions = []
        for board in (0,1):
            for col in (0, 1, 2):
                for row in (0, 1, 2):
                    positions.append(rp2rbp(board, col, row))

        self.assertEqual(positions, list(range(2 * 3 * 3)))

    def test_board(self):
        rolls = [1,3,2,3,3]
        board = KnucklebonesBoard()
        raw_board_states = []
        for roll in rolls:
            board.push(1, roll)
            board.raw_board.copy()

        for s in raw_board_states[:-1]:
            board.pop()
            self.assertEqual(s, board.raw_board)

    def test_game(self):
        '''verify that the game board can match the inputs and outputs of a
        playthrough from Jul 6, 2023 against Shrumy, ending in victory for
        Shrumy
        '''
        state_log = [
            # roll, column, antagonist total, protagonist total
            (1, 1, 1, 0),
            (1, 1, 0, 1),
            (6, 2, 6, 1),
            (2, 3, 6, 3),
            (4, 1, 10, 3),
            (5, 2, 10, 8),
            (5, 2, 15, 3),
            (1, 1, 15, 6),
            (3, 2, 18, 6),
            (4, 1, 14, 10),
            (1, 1, 15, 6),
            (5, 2, 10, 11),
            (3, 2, 19, 11),
            (5, 2, 19, 26),
            (2, 3, 21, 24),
            (6, 2, 15, 30),
            (5, 2, 20, 10),
            (4, 1, 20, 22),
            (1, 1, 23, 22),
            (3, 1, 23, 25),
            (4, 1, 17, 9),
            (5, 2, 22, 14),
            (6, 2, 28, 8),
            (6, 2, 22, 14),
            (4, 2, 26, 14),
            (3, 2, 14, 17),
            (5, 2, 14, 17),
            (2, 3, 17, 14),
            (3, 2, 20, 11),
            (4, 1, 16, 15),
            (5, 3, 21, 15),
            (1, 2, 21, 16),
            (4, 1, 25, 12),
            (2, 1, 25, 14),
            (6, 3, 31, 14),
            (6, 3, 25, 20),
            (6, 3, 31, 14),
            (5, 3, 26, 19),
            (4, 3, 30, 19),
            (3, 2, 27, 22),
            (6, 3, 45, 22),
            (2, 1, 46, 28),
            (1, 2, 46, 27),
        ]
        board = KnucklebonesBoard()
        for roll, column, antagonist_total, protagonist_total in state_log:
            board.push(column, roll)
            self.assertEqual(board.scores(), (protagonist_total, antagonist_total))
        self.assertTrue(board.is_game_over())
        # assert Antagonist victory