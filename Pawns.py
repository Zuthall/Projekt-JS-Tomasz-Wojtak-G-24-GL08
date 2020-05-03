import pygame
import sys
import time
from pygame.locals import *
import math

pygame.init()

# Nazwa oraz romiar okna
pygame.display.set_caption('Four Field Kono')
window = pygame.display.set_mode((220, 220))

# Wczytywanie grafik
pic1 = pygame.image.load('ground.png')
pic2 = pygame.image.load('black.png')
pic3 = pygame.image.load('white.png')
pic4 = pygame.image.load('clear.png')
pic5 = pygame.image.load('white_selected.png')
pic6 = pygame.image.load('black_selected.png')
pic7 = pygame.image.load('turn.png')
pic8 = pygame.image.load('!turn.png')
pic9 = pygame.image.load('win1.png')
pic10 = pygame.image.load('win2.png')

screen = pygame.display.get_surface()


# Player_turn odpowiada turze gracza który właśnie wykonuje ruch.
# Jeśli ktoś wygra, rozgrywka kończy się.
# Selected = 1 pozwala wyświetlić wybrany pionek, po wykonaniu ruch oznaczenie znika.
# Metoda change_player() kończy turę.
class Pawns(object):

    player_turn = 1
    winner = False
    x, y = 0, 0

    def __init__(self, player, selected):
        self.player = player
        self.selected = selected

    def change_player(self):
        if self.player == 1:
            self.player = 0
        elif self.player == 0:
            self.player = 1


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
    if Pawns.player_turn == 1:
        Pawns.player_turn = 0
    elif Pawns.player_turn == 0:
        Pawns.player_turn = 1


# Funkcja sprawdza pozycje myszki podczas wciskania lewgo przycisku myszy i
# przypisuje konkretne wartości odpowaidające romiezczeniu pionków
# do zmiennych statycznych klasy Pawns: Pawns.x oraz Pawns.y
# Sprawdzając, czy współrzędne nie wychodzą poza obszar planszy.
def pos():
    x, y = pygame.mouse.get_pos()
    while not (210 > x >= 10 and 210 > y >= 10):
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
            if board[i][j].player == 1:
                a += 1
            elif board[i][j].player == 0:
                b += 1
    if a == 1:
        screen.blit(pic9, (60, 60))
        pygame.display.flip()
        time.sleep(2)
        Pawns.winner = True
    elif b == 1:
        screen.blit(pic10, (60, 60))
        pygame.display.flip()
        time.sleep(2)
        Pawns.winner = True


# Wyświetla i odświeża tło
def menu():
    screen.blit(pic1, (0, 0))
    pygame.display.flip()


# Sprawdza zmienne odpowiadające wyświetlaniu obrazków,
# jeśli dane są prawdziwe, wyświetla je w odpowiednim miejscu.
def refresh():
    for i in range(0, 4):
        for j in range(0, 4):
            if board[i][j].player == 0:
                screen.blit(pic2, (10 + i * 50, 10 + j * 50))
                if board[i][j].selected == 1:
                    screen.blit(pic6, (10 + i * 50, 10 + j * 50))
            elif board[i][j].player == 1:
                screen.blit(pic3, (10 + i * 50, 10 + j * 50))
                if board[i][j].selected == 1:
                    screen.blit(pic5, (10 + i * 50, 10 + j * 50))
            elif board[i][j].player == -1:
                screen.blit(pic4, (10 + i * 50, 10 + j * 50))
            if Pawns.player_turn == 0:
                screen.blit(pic8, (60, 210))
                screen.blit(pic7, (60, 0))
            elif Pawns.player_turn == 1:
                screen.blit(pic8, (60, 0))
                screen.blit(pic7, (60, 210))
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
    if math.fabs(x1 - x0) > 1 or math.fabs(y1 - y0) > 1:
        return False
    elif (math.fabs(x1 - x0) + math.fabs(y1 - y0)) == 2:
        return False
    return True


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
    board[Pawns.x][Pawns.y].player = Pawns.player_turn
    board[x][y].player = -1
    change_players_turn()
    refresh()


def capture():
    pass


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
                move()

    check_winner()




