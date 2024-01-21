"""
Main
"""
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import os

from Game import Game

os.environ['SDL_VIDEO_CENTERED'] = '1'


def play_chess():
    """
    Play Chess against a human or computer player
    """
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((400, 150))
    screen.fill((255, 255, 255))
    pygame.display.set_caption('Select Opponent')

    human_opponent_button = Button(screen, 60, 50, 80, 40, text="Human")
    computer_opponent_button = Button(screen, 260, 50, 80, 40, text="Computer")
    white_button = Button(screen, 60, 50, 80, 40, text="White")
    black_button = Button(screen, 260, 50, 80, 40, text="Black")

    difficulty_slider = Slider(screen, 100, 100, 200, 20, min=0, max=4, step=1)
    difficulty = TextBox(screen, 175, 60, 25, 30, fontSize=25)

    white_button.hide()
    black_button.hide()
    difficulty_slider.hide()
    difficulty.hide()

    running = True
    while running:

        # for loop through the event queue
        events = pygame.event.get()
        for event in events:
            human_opponent_button.show()
            computer_opponent_button.show()
            pygame_widgets.update(events)
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False

            if human_opponent_button.clicked:
                # Playing against a Human
                human_opponent_button.hide()
                computer_opponent_button.hide()
                game = Game('H', 'N', 0)
                game.play_game()
                # Clear board and reset the screen
                game.board.clear_board()
                screen = pygame.display.set_mode((400, 150))
                screen.fill((255, 255, 255))
                pygame.display.set_caption('Select Opponent')

            elif computer_opponent_button.clicked:
                # Playing against a Computer
                # User selects a colour
                pygame.display.set_caption('Select Colour and Difficulty')
                screen.fill((255, 255, 255))
                human_opponent_button.hide()
                computer_opponent_button.hide()
                white_button.show()
                black_button.show()
                difficulty_slider.show()
                difficulty.show()

                run = True
                while run:

                    new_events = pygame.event.get()
                    for new_event in new_events:
                        screen.fill((255, 255, 255))
                        difficulty.setText(difficulty_slider.getValue())
                        pygame_widgets.update(new_events)
                        pygame.display.update()

                        # Continue until the user chooses a colour or quita
                        if new_event.type == pygame.QUIT or white_button.clicked or black_button.clicked:
                            run = False

                if white_button.clicked or black_button.clicked:
                    white_button.hide()
                    black_button.hide()
                    difficulty_slider.hide()
                    difficulty.hide()

                    if white_button.clicked:
                        # The User plays as white
                        game = Game('C', 'B', computer_difficulty=difficulty_slider.getValue())
                        game.play_game()
                    else:
                        game = Game('C', 'W', computer_difficulty=difficulty_slider.getValue())
                        game.play_game()

                    # Clear the board
                    game.board.clear_board()
                    screen = pygame.display.set_mode((400, 150))
                    screen.fill((255, 255, 255))
                    pygame.display.set_caption('Select Opponent')


    pygame.quit()


if __name__ == '__main__':
    play_chess()
