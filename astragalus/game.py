"""
A library for the minigame Knucklebones from Cult of the Lamb
"""

from .board import KnucklebonesBoard


class KnucklebonesGame(object):
    def __init__(self):
        self.game = KnucklebonesBoard()
        pass

    def valid_moves(self):
        return self.game.generate_legal_moves()

    def over(self):
        return self.game.is_game_over()

    def make_move(self, move):
        raise NotImplementedError()

    def undo_move(self):
        raise NotImplementedError()

    def score(self):
        return 0

    def state(self):
        raise NotImplementedError()

    @classmethod
    def load(cls, self):
        raise NotImplementedError()

    def copy(self):
        return self.load(self.state())
