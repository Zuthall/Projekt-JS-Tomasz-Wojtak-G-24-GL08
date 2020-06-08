import pygame
import sys
import time
from pygame.locals import *
import math

pygame.init()

# Nazwa oraz romiar okna
pygame.display.set_caption('Four Field Kono')
length, width = 220, 220
window_size = (length, width)
window = pygame.display.set_mode(window_size)
none, black, white = range(-1, 2)

# Wczytywanie grafik
background = pygame.image.load('ground.png')
black_pawn = pygame.image.load('black.png')
white_pawn = pygame.image.load('white.png')
blank_slot = pygame.image.load('clear.png')
white_pawn_selected = pygame.image.load('white_selected.png')
black_pawn_selected = pygame.image.load('black_selected.png')
turn = pygame.image.load('turn.png')
noturn = pygame.image.load('!turn.png')
win_white = pygame.image.load('win1.png')
win_black = pygame.image.load('win2.png')
wrong_move = pygame.image.load('wrong.png')

screen = pygame.display.get_surface()


# Player_turn odpowiada turze gracza który właśnie wykonuje ruch.
# Jeśli ktoś wygra, rozgrywka kończy się.
# Selected = 1 pozwala wyświetlić wybrany pionek, po wykonaniu ruch oznaczenie znika.
# Metoda change_player() kończy turę.
class Pawns(object):

    player_turn = white     # Zaczynaja biale
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
# 0 0 0 0
# 0 0 0 0
# 1 1 1 1
# 1 1 1 1
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
        screen.blit(win_white, (60, 60))
        pygame.display.flip()
        time.sleep(2)
        Pawns.winner = True
    elif b == 1:
        screen.blit(win_black, (60, 60))
        pygame.display.flip()
        time.sleep(2)
        Pawns.winner = True


# Wyświetla i odświeża tło
def menu():
    screen.blit(background, (0, 0))
    pygame.display.flip()


# Sprawdza zmienne odpowiadające wyświetlaniu obrazków,
# jeśli dane są prawdziwe, wyświetla je w odpowiednim miejscu.
def refresh():
    for i in range(0, 4):
        for j in range(0, 4):
            if board[i][j].player == black:
                screen.blit(black_pawn, (10 + i * 50, 10 + j * 50))
                if board[i][j].selected == 1:
                    screen.blit(black_pawn_selected, (10 + i * 50, 10 + j * 50))
            elif board[i][j].player == white:
                screen.blit(white_pawn, (10 + i * 50, 10 + j * 50))
                if board[i][j].selected == 1:
                    screen.blit(white_pawn_selected, (10 + i * 50, 10 + j * 50))
            elif board[i][j].player == none:
                screen.blit(blank_slot, (10 + i * 50, 10 + j * 50))
            if Pawns.player_turn == black:
                screen.blit(noturn, (60, 210))
                screen.blit(turn, (60, 0))
            elif Pawns.player_turn == white:
                screen.blit(noturn, (60, 0))
                screen.blit(turn, (60, 210))
    pygame.display.flip()
    pygame.event.get()


# Sprawdza czy ruch może się odbyć.
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
    return False


# Zaznacza pionek
def select():
    board[Pawns.x][Pawns.y].selected = 1
    refresh()


# Odznacza pionek
def deselect():
    board[Pawns.x][Pawns.y].selected = 0


# Przesuwa pionek
def move():
    x, y = Pawns.x, Pawns.y
    deselect()
    while not (can_move2(x, y) and can_move1()):
        pygame.event.get()
        if pygame.mouse.get_pressed() == (1, 0, 0):
            pos()
    if Pawns.x == x and Pawns.y == y:
        return False
    if board[Pawns.x][Pawns.y].player == none:
        board[Pawns.x][Pawns.y].player = Pawns.player_turn
        board[x][y].player = none
        change_players_turn()
        refresh()
        return True


def can_capture(x0, y0):
    x1, y1 = Pawns.x, Pawns.y
    if (board[(x1 + x0) // 2][(y1 + y0) // 2].player == Pawns.player_turn) and\
            ((math.fabs(x1 - x0) == 2 and math.fabs(y1 - y0) == 0)
             or (math.fabs(y1 - y0) == 2 and math.fabs(x1 - x0) == 0))\
            and board[Pawns.x][Pawns.y].player != none:
        return True
    else:
        pygame.display.flip()
        screen.blit(wrong_move, (100, 100))
        return False


def capture():

    x, y = Pawns.x, Pawns.y
    deselect()
    while not (can_move1() and (can_capture(x, y) or can_move2(x, y))):
        pygame.event.get()
        if pygame.mouse.get_pressed() == (1, 0, 0):
            pos()
    board[Pawns.x][Pawns.y].player = Pawns.player_turn
    board[x][y].player = none
    change_players_turn()
    refresh()
    return True


def start():
    menu()
    refresh()

    while not Pawns.winner:

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                sys.exit(0)
            elif pygame.mouse.get_pressed() == (1, 0, 0):
                pos()
                if can_select():
                    select()
                    if not capture():
                        continue

        check_winner()


start()

