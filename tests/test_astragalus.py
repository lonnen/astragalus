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
        assert True
