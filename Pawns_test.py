import unittest

import Pawns as Pa

do_reset = False
winner = False
save = False

remembered_x, remembered_y = Pa.POINT_ZERO
player_turn = Pa.WHITE


class PawnsTest(unittest.TestCase):
    """Klasa odpowiadająca za testy."""

    def setUp(self):
        self.board = Pa.create_board()

    def test_can_capture(self):
        remembered_x, remembered_y = 1, 3
        self.assertTrue(Pa.can_capture(1, 1, self.board, remembered_x, remembered_y, player_turn))

    def test_can_move1(self):
        self.board[0][1].player = Pa.NULL
        remembered_x, remembered_y = 0, 2
        self.assertFalse(Pa.can_move1(self.board, remembered_x, remembered_y, player_turn))

    def test_can_move2(self):
        self.board[0][1].player = Pa.NULL
        Pa.remembered_x,remembered_y = 0, 2
        self.assertFalse(Pa.can_move2(0, 1, self.board, remembered_x, remembered_y))

    def test_can_select(self):
        remembered_x, remembered_y = 0, 3
        self.assertTrue(Pa.can_select(self.board, remembered_x, remembered_y, player_turn))

    def test_capture(self):
        remembered_x, remembered_y = 1, 3
        Pa.capture_or_move(self.board, do_reset, remembered_x, remembered_y, player_turn, (1, 1))
        self.assertEqual(Pa.WHITE, self.board[1][1].player)

    def test_move(self):
        remembered_x, remembered_y = 1, 1
        self.board[1][0].player = Pa.NULL
        Pa.capture_or_move(self.board, do_reset, remembered_x, remembered_y, player_turn, (1, 0))
        self.assertEqual(Pa.WHITE, self.board[1][0].player)

    def test_can_not_move1(self):
        remembered_x, remembered_y = 1, 3
        self.assertFalse(Pa.can_move1(self.board, remembered_x, remembered_y, player_turn))

    def test_can_not_move2(self):
        remembered_x, remembered_y = 2, 3
        self.assertFalse(Pa.can_move2(-1, 10, self.board, remembered_x, remembered_y))


if __name__ == '__main__':
    unittest.main()



