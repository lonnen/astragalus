==========
ASTRAGALUS
==========

An set of utilities for playing `Cult of the Lamb <https://www.cultofthelamb.com/>`_'s minigame `Knucklebones <https://cult-of-the-lamb.fandom.com/wiki/Knucklebones>`_.

:Code:          https://github.com/lonnen/astragalus
:Issues:        https://github.com/lonnen/astragalus/issues
:Releases:      https://pypi.org/project/astragalus/#history
:License:       MIT; See LICENSE

Install
=======

To install astragalus, run:

.. code-block:: shell

    $ pip install git+https://github.com/lonnen/astragalus.git

Example Usage
=============

Here's the basic idea:

.. code-block:: python

    >>> from random import randint
    >>> from astragalus import KnucklebonesBoard
    >>> board = KnucklebonesBoard()
    >>> column = 2
    >>> dice_roll = randint(1, 6)
    >>> board.push(column, dice_roll)
    >>> print(board)

.. code-block:: python

    "0006000000000000001"

Status
======

The board is implemented with all the constraintes necessary to make legal moves, but the game is
is not implemented. For the moment you'll need to implement rolling your own `d6` every round.