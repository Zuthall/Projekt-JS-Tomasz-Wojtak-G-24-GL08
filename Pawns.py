""" -- STEROWANIE --

Aby wybrać a następnie poruszyć pionek, trzeba użyć lewego przycisku myszy.
!! Jeśli chcemy anulować wybór pionka należy wcisnąć prawy przycisk myszy. !!
Wciśnij klawisz escape aby wyłączyć program."""


import sys
import time

import pygame
from pygame import locals


LENGTH, WIDTH = 220, 220
WINDOW_SIZE = (LENGTH, WIDTH)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
MIDDLE = (75, 100)
PLAYER1_TURN = (60, 210)
PLAYER2_TURN = (60, 0)
BOARD_SIZE = 4
WAIT_2_SECONDS = 2
LEFT_BUTTON_PRESSED = (1, 0, 0)
RIGHT_BUTTON_PRESSED = (0, 0, 1)
PAWN_SIZE = 50
FRAME_WIDTH = 10
RESET_HEIGHT = 180
WINNER_HEIGHT = (60, 60)
POINT_ZERO = (0, 0)
NULL, BLACK, WHITE = range(-1, 2)


class Assets:
    """Wczytuje grafiki."""

    @staticmethod
    def load():
        Assets.screen = pygame.display.get_surface()
        Assets.background = pygame.image.load('ground.png')
        Assets.black_pawn = pygame.image.load('black.png')
        Assets.white_pawn = pygame.image.load('white.png')
        Assets.blank_slot = pygame.image.load('clear.png')
        Assets.white_pawn_selected = pygame.image.load('white_selected.png')
        Assets.black_pawn_selected = pygame.image.load('black_selected.png')
        Assets.turn = pygame.image.load('turn.png')
        Assets.no_turn = pygame.image.load('!turn.png')
        Assets.win_white = pygame.image.load('win1.png')
        Assets.win_black = pygame.image.load('win2.png')
        Assets.wrong_move = pygame.image.load('wrong.png')
        Assets.choose = pygame.image.load('choose.png')


class Pawns(object):
    """ Pozwala na utworzenie pionków oraz modyfikacje ich atrybutów.

     Pionki przechwoują informacje o tym, czy są w danej chwili wybrane oraz o ich właścicielu.
     Selected = True pozwala wyświetlić wybrany pionek, po wykonaniu ruch oznaczenie jest usuwane.
     Współrzędne x oraz y pozwalają przekazać zapamiętane dane, potrzebne do wykonania np. ruchu.
     """
    player_turn = WHITE

    def __init__(self, player=NULL, selected=False):
        self.player = player
        self.selected = selected

    def change_player(self):
        if self.player == BLACK:
            self.player = WHITE
        elif self.player == WHITE:
            self.player = BLACK


def create_board():
    """" Funkcja pozwala na utworzenie planszy.

    Dwuwymiaorwa plansza, na wzór, gdzie 1 to białe, natomiast 0 to czarne.:

   (0,0)      (3,0)

      0  0  0  0
      0  0  0  0
      1  1  1  1
      1  1  1  1

   (0,3)      (3,3)

  """
    return [[Pawns(BLACK, False) if i < BOARD_SIZE/2 else Pawns(WHITE, False)
             for i in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def change_players_turn():
    """Funkcja kończy bieżącą ture."""
    if Pawns.player_turn == WHITE:
        Pawns.player_turn = BLACK
    elif Pawns.player_turn == BLACK:
        Pawns.player_turn = WHITE


def get_position(board, do_reset):
    """Funkcja sprawdza pozycje myszki.

    Przypisuje konkretne wartości odpowaidające romiezczeniu pionków
    do zmiennych statycznych klasy Pawns: Pawns.x oraz Pawns.y
    Sprawdzając, czy wybrane współrzędne nie wychodzą poza obszar planszy."""
    x, y = pygame.mouse.get_pos()
    if LENGTH > y > LENGTH - FRAME_WIDTH > x > RESET_HEIGHT:
        do_reset = True
    reset(board, do_reset)
    while not (LENGTH - FRAME_WIDTH > x >= FRAME_WIDTH and WIDTH - FRAME_WIDTH > y >= FRAME_WIDTH):
        pygame.event.get()
        if pygame.mouse.get_pressed() == LEFT_BUTTON_PRESSED:
            x, y = pygame.mouse.get_pos()
    x, y = (x - FRAME_WIDTH) // PAWN_SIZE, (y - FRAME_WIDTH) // PAWN_SIZE
    return x, y


def check_winner(board):
    """Funkcja sprawdza czy rozgrywka nadal trwa, jeśli nie, wyświetla odpowiedni komunikat."""
    player1_pawns, player2_pawns = POINT_ZERO
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j].player == WHITE:
                player1_pawns += 1
            elif board[i][j].player == BLACK:
                player2_pawns += 1
    if player1_pawns == 1:
        Assets.screen.blit(Assets.win_white, WINNER_HEIGHT)
        pygame.display.flip()
        time.sleep(WAIT_2_SECONDS)
        return True
    elif player2_pawns == 1:
        Assets.screen.blit(Assets.win_black, WINNER_HEIGHT)
        pygame.display.flip()
        time.sleep(WAIT_2_SECONDS)
        return True


def menu():
    """Wyświetla i odświeża tło."""
    Assets.screen.blit(Assets.background, POINT_ZERO)
    pygame.display.flip()


def refresh(board):
    """Odpowiada za wyświetlnaie grafik."""
    for i in range(BOARD_SIZE):
        place1 = FRAME_WIDTH + i * PAWN_SIZE
        for j in range(BOARD_SIZE):
            place2 = FRAME_WIDTH + j * PAWN_SIZE
            if board[i][j].player == BLACK:
                Assets.screen.blit(Assets.black_pawn, (place1, place2))
                if board[i][j].selected:
                    Assets.screen.blit(Assets.black_pawn_selected, (place1, place2))
            elif board[i][j].player == WHITE:
                Assets.screen.blit(Assets.white_pawn, (place1, place2))
                if board[i][j].selected:
                    Assets.screen.blit(Assets.white_pawn_selected, (place1, place2))
            elif board[i][j].player == NULL:
                Assets.screen.blit(Assets.no_turn, PLAYER1_TURN)
                Assets.screen.blit(Assets.blank_slot, (place1, place2))
                Assets.screen.blit(Assets.no_turn, PLAYER2_TURN)
            if Pawns.player_turn == BLACK:
                Assets.screen.blit(Assets.no_turn, PLAYER1_TURN)
                Assets.screen.blit(Assets.turn, PLAYER2_TURN)
            elif Pawns.player_turn == WHITE:
                Assets.screen.blit(Assets.no_turn, PLAYER2_TURN)
                Assets.screen.blit(Assets.turn, PLAYER1_TURN)
    pygame.display.flip()
    pygame.event.get()


def can_move1(board, remembered_x, remembered_y):
    """Sprawdza czy ruch może się odbyć."""
    if board[remembered_x][remembered_y].player != Pawns.player_turn:
        if (BOARD_SIZE > (remembered_x + i) >= 0 and BOARD_SIZE > (remembered_y + i) >= 0 for i in [-1, 1]):
            return True
    return False


def can_move2(x0, y0, board, remembered_x, remembered_y):
    """Sprawdza czy ruch może się odbyć. Kolejne warunki."""
    x1, y1 = remembered_x, remembered_y
    if abs(x1 - x0) + abs(y1 - y0) == 1:
        if board[x1][y1].player == NULL:
            return True
    else:
        return False


def can_select(board, remembered_x, remembered_y):
    """Sprawdza czy wybór pionka może się odbyć."""
    if (4 > (remembered_x + i) >= 0 and 4 > (remembered_y + i) >= 0 for i in [-1, 1]):
        if board[remembered_x][remembered_y].player == Pawns.player_turn:
            return True
        else:
            Assets.screen.blit(Assets.wrong_move, MIDDLE)
            pygame.display.flip()
    return False


def select(x, y, board):
    board[x][y].selected = True
    refresh(board)


def deselect(x, y, board):
    board[x][y].selected = False


def can_capture(x0, y0, board, remembered_x, remembered_y):
    """Funkcja sprawdzająca czy można przejąc pionek w określonej sytuacji."""
    x1, y1 = remembered_x, remembered_y
    if (board[(x1 + x0) // 2][(y1 + y0) // 2].player == Pawns.player_turn) and\
            ((abs(x1 - x0) == 2 and abs(y1 - y0) == 0)
             or (abs(y1 - y0) == 2 and abs(x1 - x0) == 0))\
            and board[remembered_x][remembered_y].player != NULL:
        return True

    else:
        pygame.display.flip()
        Assets.screen.blit(Assets.wrong_move, MIDDLE)
    return False


def capture_or_move(board, do_reset, remembered_x, remembered_y, go_to=(-1, -1)):
    """Odpowiada za przemieszczanie się pionków.

    Jeśli wszystkie wymagania do wykonania ruchu/przejęcia są spełnione to
    zostanie wykonany, odpowiednio, ruch bądź przejęcie."""

    x, y = remembered_x, remembered_y
    deselect(x, y, board)
    if go_to == (-1, -1):
        while not (can_move1(board, remembered_x, remembered_y) and (
                can_capture(x, y, board, remembered_x, remembered_y) or
                can_move2(x, y, board, remembered_x, remembered_y))):
            pygame.event.get()
            if pygame.mouse.get_pressed() == LEFT_BUTTON_PRESSED:
                remembered_x, remembered_y = get_position(board, do_reset)
                if board[remembered_x][remembered_y].player == Pawns.player_turn and (
                        remembered_x != x and remembered_y != y) and reset(board, do_reset):
                    pygame.display.flip()
                    Assets.screen.blit(Assets.wrong_move, MIDDLE)
            if pygame.mouse.get_pressed() == RIGHT_BUTTON_PRESSED:
                deselect(x, y, board)
                refresh(board)
                return False
        if board[remembered_x][remembered_y].player == Pawns.player_turn and (
                remembered_x != x and remembered_y != y) and reset(board, do_reset):
            pygame.display.flip()
            Assets.screen.blit(Assets.wrong_move, MIDDLE)
        board[remembered_x][remembered_y].player = Pawns.player_turn
        board[x][y].player = NULL
        change_players_turn()
        refresh(board)
    else:
        remembered_x, remembered_y = go_to
        if board[remembered_x][remembered_y] != Pawns.player_turn:
            board[remembered_x][remembered_y].player = Pawns.player_turn
            board[x][y].player = NULL
            change_players_turn()
    return True


def choose():
    """Funkcja pozwalająca, w menu, wybrać gracza zaczynającego rozgrywkę."""
    Assets.screen.blit(Assets.choose, POINT_ZERO)
    pygame.display.flip()
    Pawns.player_turn = NULL
    while Pawns.player_turn == NULL:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.locals.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
                sys.exit(0)
            elif pygame.mouse.get_pressed() == LEFT_BUTTON_PRESSED:
                x, y = pygame.mouse.get_pos()
                if 200 > x > 2*FRAME_WIDTH and 185 > y > 100:
                    if 105 > x > 2*FRAME_WIDTH:
                        Pawns.player_turn = BLACK
                    elif 200 > x > 115:
                        Pawns.player_turn = WHITE


def reset(board, do_reset):
    """Funkcja ta pozwala resetować rozgrywkę podczas jej trwania - należy kliknąć w pole 'reset'. """
    if do_reset:
        do_reset = False
        Pawns.player_turn = NULL
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                board[j][i].selected = False
                if i < 2:
                    board[j][i].player = BLACK
                else:
                    board[j][i].player = WHITE
        choose()
        menu()
        refresh(board)
    return False


def main():
    """Odpowiada za poprawne uruchomienie oraz działanie programu."""
    board = create_board()
    do_reset = False
    winner = False
    remembered_x, remembered_y = POINT_ZERO

    pygame.init()
    Assets.load()
    pygame.display.set_caption('Four Field Kono')
    choose()
    menu()
    refresh(board)

    while not winner:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.locals.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
                sys.exit(0)
            elif pygame.mouse.get_pressed() == LEFT_BUTTON_PRESSED:
                remembered_x, remembered_y = get_position(board, do_reset)
                if can_select(board, remembered_x, remembered_y):
                    select(remembered_x, remembered_y, board)
                    if not capture_or_move(board, do_reset, remembered_x, remembered_y):
                        continue
            winner = check_winner(board)


if __name__ == '__main__':

    main()

