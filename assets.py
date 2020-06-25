# Wczytywanie zasobów.

import pygame


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
        Assets.choose = pygame.image.load('choose.png')
        Assets.screen = pygame.display.get_surface()