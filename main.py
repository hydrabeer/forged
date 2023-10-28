"""The main module is the entry point for the game."""

from game.game import Game


if __name__ == '__main__':
    # Initialize the game and the title screen and run the game.
    game = Game()
    game.ui.title_elements.initialize(game.ui.font, game.ui.title_font)
    game.run()
