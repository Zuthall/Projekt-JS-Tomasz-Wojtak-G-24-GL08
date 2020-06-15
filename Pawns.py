# -- STEROWANIE --
# Aby wybrać a następnie poruszyć pionek, trzeba użyć lewego przycisku myszy.
# !! Jeśli chcemy anulować wybór pionka należy wcisnąć prawy przycisk myszy. !!
# Wciśnij klawisz escape aby wyłączyć program.

# Wczytanie wymaganych bibliotek.
import sys

import unittest

import time

import pygame
from pygame.locals import *

import math

pygame.init()

# Nazwa oraz wymiary okna.
pygame.display.set_caption('Four Field Kono')
length, width = 220, 220
window_size = (length, width)
window = pygame.display.set_mode(window_size)

# Stałe wskazujące pewne miejsca na ekranie (środek okna, nazwa gracza, itp.).
mid = (75, 100)
player1_turn = (60, 210)
player2_turn = (60, 0)

# Przypisanie wartosci określających gracza
none, black, white = range(-1, 2)


# Wczytywanie grafik.
class Assets:
    """Wczytuje grafiki."""

    @staticmethod
    def load():
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
        Assets.screen = pygame.display.get_surface()


# Player_turn odpowiada turze gracza który właśnie wykonuje ruch.
# Jeśli ktoś wygra, rozgrywka kończy się.
# Selected = 1 pozwala wyświetlić wybrany pionek, po wykonaniu ruch oznaczenie jest usuwane.
# Metoda change_player() kończy turę.
class Pawns(object):
    """Pozwala na utworzenie pionków które przechwoują informacje o tym,
     czy są w danej chwili wybrane oraz o ich właścicielu."""
    player_turn = white     # Zaczynaja biale, zmiana wartosci to zmiana tury gracza.
    winner = False
    x, y = 0, 0

    def __init__(self, player, selected):
        self.player = player
        self.selected = selected

    def change_player(self):
        if self.player == black:
            self.player = white
        elif self.player == white:
            self.player = black


# Dwuwymiaorwa plansza, na wzór:

#   0 0 0 0
#   0 0 0 0
#   1 1 1 1
#   1 1 1 1

# Jedynki oznaczają pionki gracza drugiego, natomiast zera, gracza pierwszego.
# Jedynki oraz zera są zapisane są w komórkach 'player'.
board = [[Pawns(0, False) if i < 2 else Pawns(1, False) for i in range(0, 4)] for j in range(0, 4)]


# Funkcja change_player() kończy bieżącą turę
def change_players_turn():
    if Pawns.player_turn == white:
        Pawns.player_turn = black
    elif Pawns.player_turn == black:
        Pawns.player_turn = white


# Funkcja sprawdza pozycje myszki podczas wciskania lewgo przycisku myszy i
# przypisuje konkretne wartości odpowaidające romiezczeniu pionków
# do zmiennych statycznych klasy Pawns: Pawns.x oraz Pawns.y
# Sprawdzając, czy współrzędne nie wychodzą poza obszar planszy.
def pos():
    x, y = pygame.mouse.get_pos()
    while not (length > x >= 10 and width> y >= 10):
        pygame.event.get()
        if pygame.mouse.get_pressed() == (1, 0, 0):
            x, y = pygame.mouse.get_pos()
    x, y = (x - 10) // 55, (y - 10) // 55
    Pawns.x, Pawns.y = x, y


# Funkcja sprawdza, czy ktoryś z graczy wygrał, jeśli tak, ustawia
# wartość Pawns.winner na True i wyświetla odpowiedni obrazek.
def check_winner():
    a, b = 0, 0
    for i in range(0, 4):
        for j in range(0, 4):
            if board[i][j].player == white:
                a += 1
            elif board[i][j].player == black:
                b += 1
    if a == 1:
        Assets.screen.blit(Assets.win_white, (60, 60))
        pygame.display.flip()
        time.sleep(2)
        Pawns.winner = True
    elif b == 1:
        Assets.screen.blit(Assets.win_black, (60, 60))
        pygame.display.flip()
        time.sleep(2)
        Pawns.winner = True


# Wyświetla i odświeża tło.
def menu():
    Assets.screen.blit(Assets.background, (0, 0))
    pygame.display.flip()


# Sprawdza zmienne odpowiadające wyświetlaniu obrazków,
# jeśli dane są prawdziwe, wyświetla je w odpowiednim miejscu.
def refresh():
    for i in range(0, 4):
        place1 = 10 + i * 50
        for j in range(0, 4):
            place2 = 10 + j * 50
            if board[i][j].player == black:
                Assets.screen.blit(Assets.black_pawn, (place1, place2))
                if board[i][j].selected == 1:
                    Assets.screen.blit(Assets.black_pawn_selected, (place1, place2))
            elif board[i][j].player == white:
                Assets.screen.blit(Assets.white_pawn, (place1, place2))
                if board[i][j].selected == 1:
                    Assets.screen.blit(Assets.white_pawn_selected, (place1, place2))
            elif board[i][j].player == none:
                Assets.screen.blit(Assets.blank_slot, (place1, place2))
            if Pawns.player_turn == black:
                Assets.screen.blit(Assets.no_turn, player1_turn)
                Assets.screen.blit(Assets.turn, player2_turn)
            elif Pawns.player_turn == white:
                Assets.screen.blit(Assets.no_turn, player2_turn)
                Assets.screen.blit(Assets.turn, player1_turn)
    pygame.display.flip()
    pygame.event.get()


# Sprawdza czy ruch może się odbyć.
# Jeśli użytkownik kliknie poza planszę lub wybierze własny pionek to funkcja zwróci False.
def can_move1():
    if board[Pawns.x][Pawns.y].player != Pawns.player_turn:
        if (4 > (Pawns.x + i) >= 0 and 4 > (Pawns.y + i) >= 0 for i in [-1, 1]):
            return True
    return False


# Kolejne warunki, sprawdzające czy ruch może się odbyć.
def can_move2(x0, y0):
    x1, y1 = Pawns.x, Pawns.y
    if (math.fabs(x1 - x0) == 1 and math.fabs(y1 - y0) == 0) \
            or (math.fabs(y1 - y0) == 1 and math.fabs(x1 - x0) == 0):
        if board[x1][y1].player == none:
            return True
    else:
        return False


# Sprawdza czy wybór pionka może się odbyć.
def can_select():
    if (4 > (Pawns.x + i) >= 0 and 4 > (Pawns.y + i) >= 0 for i in [-1, 1]):
        if board[Pawns.x][Pawns.y].player == Pawns.player_turn:
            return True
        else:
            Assets.screen.blit(Assets.wrong_move, mid)
            pygame.display.flip()
    return False


# Zaznacza pionek.
def select(x, y):
    board[x][y].selected = 1
    refresh()


# Odznacza pionek
def deselect(x, y):
    board[x][y].selected = 0


# Funkcja sprawdzająca czy można przejąc pionek w określonej sytuacji.
def can_capture(x0, y0):
    x1, y1 = Pawns.x, Pawns.y
    if (board[(x1 + x0) // 2][(y1 + y0) // 2].player == Pawns.player_turn) and\
            ((math.fabs(x1 - x0) == 2 and math.fabs(y1 - y0) == 0)
             or (math.fabs(y1 - y0) == 2 and math.fabs(x1 - x0) == 0))\
            and board[Pawns.x][Pawns.y].player != none:
        return True
    else:
        pygame.display.flip()
        Assets.screen.blit(Assets.wrong_move, mid)
        return False


# Jeśli wszystkie wymagania do wykonania ruchu/przejęcia są spełnione to
# zostanie wykonany, odpowiednio, ruch bądź przejęcie.
def capture_or_move():

    x, y = Pawns.x, Pawns.y
    deselect(x, y)
    while not (can_move1() and (can_capture(x, y) or can_move2(x, y))):
        pygame.event.get()
        if pygame.mouse.get_pressed() == (1, 0, 0):
            pos()
            if board[Pawns.x][Pawns.y].player == Pawns.player_turn and (Pawns.x != x and Pawns.y != y):
                pygame.display.flip()
                Assets.screen.blit(Assets.wrong_move, mid)
        if pygame.mouse.get_pressed() == (0, 0, 1):
            print("elo")
            deselect(x, y)
            refresh()
            return False
    if board[Pawns.x][Pawns.y].player == Pawns.player_turn and (Pawns.x != x and Pawns.y != y):
        pygame.display.flip()
        Assets.screen.blit(Assets.wrong_move, mid)
    board[Pawns.x][Pawns.y].player = Pawns.player_turn
    board[x][y].player = none
    change_players_turn()
    refresh()
    return True


class PawnsTest(unittest.TestCase):
    """Klasa odpowiadająca za testy."""

    # Test rozmiaru okna.
    def test_size(self):
        self.assertEqual(window_size, (210, 220))

    # Failed if winner = True.
    # Jeśli program nie został wcześniej uruchomiony to Winner = False
    def test_winner(self):
        self.assertFalse(Pawns.winner)


# Odpowiada za poprawne uruchomienie i działanie programu.
def main():
    # Wczytuje obrazy a następnie je wyświetla
    Assets.load()
    menu()
    refresh()

    # Włącza grę i odpowiednio reaguje na napotkane wydarzenia.
    while not Pawns.winner:

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                sys.exit(0)
            elif pygame.mouse.get_pressed() == (1, 0, 0):
                pos()
                if can_select():
                    select(Pawns.x, Pawns.y)
                    if not capture_or_move():
                        continue

        check_winner()


if __name__ == '__main__':

    # Testy, zakomentowane na czas sprawdzania programu.
    # unittest.main()

    # Wywołanie głównej funkcji.
    main()

