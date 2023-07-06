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
