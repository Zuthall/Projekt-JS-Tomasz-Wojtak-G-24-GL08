# -- STEROWANIE --
# Aby wybrać a następnie poruszyć pionek, trzeba użyć lewego przycisku myszy.
# !! Jeśli chcemy anulować wybór pionka należy wcisnąć prawy przycisk myszy. !!
# Wciśnij klawisz escape aby wyłączyć program.

# Wczytanie wymaganych bibliotek.
import sys

import time

import pygame
from pygame.locals import *

import math

import assets
import Pawns_test

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


# Player_turn odpowiada turze gracza który właśnie wykonuje ruch.
# Jeśli ktoś wygra, rozgrywka kończy się.
# Selected = 1 pozwala wyświetlić wybrany pionek, po wykonaniu ruch oznaczenie jest usuwane.
# Metoda change_player() kończy turę.
class Pawns(object):
    """Pozwala na utworzenie pionków które przechwoują informacje o tym,
     czy są w danej chwili wybrane oraz o ich właścicielu."""
    reset = False       # Zmienna służąca do restartowania rozgrywki.
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
def create_board():
    return [[Pawns(black, False) if i < 2 else Pawns(white, False) for i in range(0, 4)] for j in range(0, 4)]


# Funkcja tworzy plansze wypełnioną pionkami.
board = create_board()


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
    if 210 > x > 180 and 220 > y > 210:
        Pawns.reset = True
    reset()
    while not (length > x >= 10 and width > y >= 10):
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
        assets.Assets.screen.blit(assets.Assets.win_white, (60, 60))
        pygame.display.flip()
        time.sleep(2)
        Pawns.winner = True
    elif b == 1:
        assets.Assets.screen.blit(assets.Assets.win_black, (60, 60))
        pygame.display.flip()
        time.sleep(2)
        Pawns.winner = True


# Wyświetla i odświeża tło.
def menu():
    assets.Assets.screen.blit(assets.Assets.background, (0, 0))
    pygame.display.flip()


# Sprawdza zmienne odpowiadające wyświetlaniu obrazków,
# jeśli dane są prawdziwe, wyświetla je w odpowiednim miejscu.
def refresh():
    for i in range(0, 4):
        place1 = 10 + i * 50
        for j in range(0, 4):
            place2 = 10 + j * 50
            if board[i][j].player == black:
                assets.Assets.screen.blit(assets.Assets.black_pawn, (place1, place2))
                if board[i][j].selected == 1:
                    assets.Assets.screen.blit(assets.Assets.black_pawn_selected, (place1, place2))
            elif board[i][j].player == white:
                assets.Assets.screen.blit(assets.Assets.white_pawn, (place1, place2))
                if board[i][j].selected == 1:
                    assets.Assets.screen.blit(assets.Assets.white_pawn_selected, (place1, place2))
            elif board[i][j].player == none:
                assets.Assets.screen.blit(assets.Assets.no_turn, player1_turn)
                assets.Assets.screen.blit(assets.Assets.blank_slot, (place1, place2))
                assets.Assets.screen.blit(assets.Assets.no_turn, player2_turn)
            if Pawns.player_turn == black:
                assets.Assets.screen.blit(assets.Assets.no_turn, player1_turn)
                assets.Assets.screen.blit(assets.Assets.turn, player2_turn)
            elif Pawns.player_turn == white:
                assets.Assets.screen.blit(assets.Assets.no_turn, player2_turn)
                assets.Assets.screen.blit(assets.Assets.turn, player1_turn)
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
            print(Pawns.x, Pawns.y)
            return True
        else:
            assets.Assets.screen.blit(assets.Assets.wrong_move, mid)
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
        assets.Assets.screen.blit(assets.Assets.wrong_move, mid)
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
            if board[Pawns.x][Pawns.y].player == Pawns.player_turn and (Pawns.x != x and Pawns.y != y) and reset():
                pygame.display.flip()
                assets.Assets.screen.blit(assets.Assets.wrong_move, mid)
        if pygame.mouse.get_pressed() == (0, 0, 1):
            deselect(x, y)
            refresh()
            return False
    if board[Pawns.x][Pawns.y].player == Pawns.player_turn and (Pawns.x != x and Pawns.y != y) and reset():
        pygame.display.flip()
        assets.Assets.screen.blit(assets.Assets.wrong_move, mid)
    board[Pawns.x][Pawns.y].player = Pawns.player_turn
    board[x][y].player = none
    change_players_turn()
    refresh()
    return True


def choose():
    """Funkcja pozwalająca wybrać gracza zaczynającego rozgrywkę."""
    assets.Assets.screen.blit(assets.Assets.choose, (0, 0))
    pygame.display.flip()
    Pawns.player_turn = none
    while Pawns.player_turn == none:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                sys.exit(0)
            elif pygame.mouse.get_pressed() == (1, 0, 0):
                x, y = pygame.mouse.get_pos()
                if 200 > x > 20 and 185 > y > 100:
                    if 105 > x > 20:
                        Pawns.player_turn = black
                    elif 200 > x > 115:
                        Pawns.player_turn = white


def reset():
    """Funkcja ta pozwala resetować rozgrywkę podczas jej trwania - wystarczy kliknąc w pole 'reset'"""
    if Pawns.reset:
        Pawns.reset = False
        Pawns.player_turn = none
        for i in range(0, 4):
            for j in range(0, 4):
                board[j][i].selected = False
                if i < 2:
                    board[j][i].player = black
                else:
                    board[j][i].player = white
        choose()
        menu()
        refresh()
    return False


# Odpowiada za poprawne uruchomienie i działanie programu.
def main():
    # Wczytuje obrazy a następnie je wyświetla
    assets.Assets.load()
    choose()
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

    # Wywołanie głównej funkcji.
    main()

