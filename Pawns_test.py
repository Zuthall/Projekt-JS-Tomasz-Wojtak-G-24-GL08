import unittest
import Pawns as Pa
import assets

# wizualizacja planszy, gdzie 1 - białe, 0 - czarne. Zaczynają białe.

# (0,0)     (3,0)
#   0  0  0  0
#   0  0  0  0
#   1  1  1  1
#   1  1  1  1
# (0,3)     (3,3)


class PawnsTest(unittest.TestCase):
    """Klasa odpowiadająca za testy."""

    # Test sprawdzający, czy można przejąć inny pionek.
    def test_can_capture(self):
        Pa.Pawns.x, Pa.Pawns.y = 1, 3
        x, y = 1, 1
        self.assertTrue(Pa.can_capture(x, y))

    def test_winner(self):
        self.assertFalse(Pa.Pawns.winner)

    # Test sprawdzający, czy można wykonać ruch.
    def test_can_move(self):
        x, y = 0, 1
        Pa.board[x][y].player = Pa.none
        Pa.Pawns.x, Pa.Pawns.y = 0, 2
        self.assertFalse(Pa.can_move1() and Pa.can_move2(x, y))

    # Test sprawdzający, czy można wybrać biały pionek.
    def test_can_select(self):
        Pa.Pawns.x, Pa.Pawns.y = 0, 3    # lewy dolny pionek.
        self.assertTrue(Pa.can_select())


if __name__ == '__main__':
    unittest.main()



