import unittest

import Pawns as Pa


class PawnsTest(unittest.TestCase):
    """Klasa odpowiadająca za testy."""

    def test_can_capture(self):
        Pa.Pawns.x, Pa.Pawns.y = 1, 3
        self.assertTrue(Pa.can_capture(1, 1))

    def test_winner(self):
        self.assertFalse(Pa.Pawns.winner)

    def test_can_move1(self):
        Pa.board[0][1].player = Pa.NULL
        Pa.Pawns.x, Pa.Pawns.y = 0, 2
        self.assertTrue(Pa.can_move1)

    def test_can_move2(self):
        Pa.board[0][1].player = Pa.NULL
        Pa.Pawns.x, Pa.Pawns.y = 0, 2
        self.assertFalse(Pa.can_move2(0, 1))

    def test_can_select(self):
        Pa.Pawns.x, Pa.Pawns.y = 0, 3
        self.assertTrue(Pa.can_select())

    def test_capture(self):
        Pa.Pawns.x, Pa.Pawns.y = 1, 3
        Pa.capture_or_move((1, 1))
        self.assertEqual(Pa.WHITE, Pa.board[1][1].player)

    def test_move(self):
        Pa.Pawns.x, Pa.Pawns.y = 1, 1
        Pa.board[1][0].player = Pa.NULL
        Pa.capture_or_move((1, 0))
        self.assertEqual(Pa.BLACK, Pa.board[1][0].player)

    def test_can_not_move1(self):
        Pa.Pawns.x, Pa.Pawns.y = 1, 3
        self.assertFalse(Pa.can_move1())

    def test_can_not_move2(self):
        Pa.Pawns.x, Pa.Pawns.y = 2, 3
        self.assertFalse(Pa.can_move2(-1, 10))


if __name__ == '__main__':
    unittest.main()



