import unittest

import Pawns as Pa

board = Pa.create_board()

do_reset = False
winner = False
save = False

remembered_x, remembered_y = Pa.POINT_ZERO
player_turn = Pa.WHITE


class PawnsTest(unittest.TestCase):
    """Klasa odpowiadająca za testy."""

    def test_can_capture(self):
        remembered_x, remembered_y = 1, 3
        self.assertTrue(Pa.can_capture(1, 1, board, remembered_x, remembered_y, player_turn))

    def test_winner(self):
        self.assertFalse(winner)

    def test_can_move1(self):
        board[0][1].player = Pa.NULL
        remembered_x, remembered_y = 0, 2
        self.assertFalse(Pa.can_move1(board, remembered_x, remembered_y, player_turn))

    def test_can_move2(self):
        board[0][1].player = Pa.NULL
        Pa.remembered_x,remembered_y = 0, 2
        self.assertFalse(Pa.can_move2(0, 1, board, remembered_x, remembered_y))

    def test_can_select(self):
        remembered_x, remembered_y = 0, 3
        self.assertTrue(Pa.can_select(board, remembered_x, remembered_y, player_turn))

    def test_capture(self):
        remembered_x, remembered_y = 1, 3
        Pa.capture_or_move(board, do_reset, remembered_x, remembered_y, player_turn, (1, 1))
        self.assertEqual(Pa.WHITE, board[1][1].player)

    def test_move(self):
        remembered_x, remembered_y = 1, 1
        board[1][0].player = Pa.NULL
        Pa.capture_or_move(board, do_reset, remembered_x, remembered_y, player_turn, (1, 0))
        self.assertEqual(Pa.WHITE, board[1][0].player)

    def test_can_not_move1(self):
        remembered_x, remembered_y = 1, 3
        self.assertFalse(Pa.can_move1(board, remembered_x, remembered_y, player_turn))

    def test_can_not_move2(self):
        remembered_x, remembered_y = 2, 3
        self.assertFalse(Pa.can_move2(-1, 10, board, remembered_x, remembered_y))


if __name__ == '__main__':
    unittest.main()



