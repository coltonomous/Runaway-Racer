import pygame
import random

########################################################################################################################
############################################# Gamespace Setup ##########################################################
########################################################################################################################

pygame.init()

crash_sound = pygame.mixer.Sound("crash.wav")
game_music = pygame.mixer.music.load("racecar_track.wav")

xDisplay = 800
yDisplay = 600
gameDisplay = pygame.display.set_mode((xDisplay, yDisplay))
clock = pygame.time.Clock()

pygame.display.set_caption("Runaway Racer")
gameLogo = pygame.image.load("RaceFlags.png")
gameIcon = pygame.image.load("car_icon.png")
carSprite = pygame.image.load("car_sprite.png").convert_alpha()
pygame.display.set_icon(gameIcon)

carWidth = int(0.08875 * xDisplay)
carHeight = int(0.2017 * yDisplay)
carSprite = pygame.transform.scale(carSprite, (carWidth, carHeight))

colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "green": (0, 255, 0),
          "yellow": (255, 255, 0), "darkRed": (175, 0, 0), "darkGreen": (0, 175, 0),
          "brown": (121, 67, 33), "grey": (125, 125, 125), "darkGrey": (75, 75, 75), "darkYellow": (175, 175, 0)}

########################################################################################################################
############################################ Game Functions ############################################################
########################################################################################################################

def game_intro():
    """ This function generates the game's start menu. It has a play button and a quit button."""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(colors["black"])
        pygame.draw.rect(gameDisplay, colors["darkGrey"], (10, 10, xDisplay - 20, yDisplay - 20))
        pygame.draw.line(gameDisplay, colors["darkYellow"], (10, (yDisplay / 2 - 15)),
                         (xDisplay - 10, (yDisplay / 2 - 15)), 15)
        pygame.draw.line(gameDisplay, colors["darkYellow"], (10, (yDisplay / 2 + 15)),
                         (xDisplay - 10, (yDisplay / 2 + 15)), 15)

        message_display(xDisplay / 2, yDisplay / 3, 70, "Ready your engines!")
        gameDisplay.blit(gameLogo, (xDisplay * 0.36, yDisplay * 0.46))
        buttons("GO!", 0.1875 * xDisplay, 0.75 * yDisplay, 100, 50, colors["darkGreen"], colors["green"], "play")
        buttons("Quit", 0.6875 * xDisplay, 0.75 * yDisplay, 100, 50, colors["darkRed"], colors["red"], "quit")
        pygame.display.update()
        clock.tick(15)


def buttons(message, x, y, width, height, inactive_color, active_color, action=None):
    """ This function generates a button at (x, y) of width and height. When the mouse is over the button,
    the color changes from inactive_color to active_color. Function is displayed on the button. Clicking
    on the button activates the action."""

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, colors["black"], (x, y, width, height))
        pygame.draw.rect(gameDisplay, active_color, (x + 2, y + 2, width - 4, height - 4))
        if click[0] == 1 and action is not None:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, colors["black"], (x, y, width, height))
        pygame.draw.rect(gameDisplay, inactive_color, (x + 2, y + 2, width - 4, height - 4))

    message_display(x + (width / 2), y + (height / 2), 20, message)


def car(car_x, car_y):
    """ This function draws carSprite to the gameDisplay at position (car_x, car_y)."""
    gameDisplay.blit(carSprite, (car_x, car_y))


def obstacles(obx, oby, obw, obh, color):
    """ This function accepts parameters object_x, object_y, object_width,
    object_height, and color to generate obstacles in game. """
    pygame.draw.rect(gameDisplay, colors["black"], (obx, oby, obw, obh))
    pygame.draw.rect(gameDisplay, color, [obx + 4, oby + 4, obw - 8, obh - 8])


def message_display(horiz, vert, text_size, text):
    """ This function handles the message display settings including position, size,
    and text."""
    print_text = pygame.font.Font("fixedsys.ttf", text_size)
    text_surface = print_text.render(text, True, colors["black"])
    text_rect = text_surface.get_rect()
    text_rect.center = (horiz, vert)
    gameDisplay.blit(text_surface, text_rect)


def count(game_count):
    """ This function prints the updating score to the gameDisplay. """
    score_text = "Score: " + str(game_count)
    message_display(xDisplay * 0.9, yDisplay * 0.025, 25, score_text)


def crash():
    """ This function prints to the gameDisplay 'You crashed!' and offers buttons to
     try again or quit."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        message_display(xDisplay / 2, yDisplay / 3, 75, "You Crashed!")
        buttons("Play Again?", 0.2125 * xDisplay, 0.75 * yDisplay, 130, 50, colors["darkGreen"],
                colors["green"], "play")
        buttons("Quit", 0.6875 * xDisplay, 0.75 * yDisplay, 100, 50, colors["darkRed"],
                colors["red"], "quit")
        pygame.display.update()
        clock.tick(15)


def paused(pause):
    """ This function pauses the game state."""
    pygame.mixer.music.pause()

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                    pygame.mixer.music.unpause()

        message_display(xDisplay / 2, yDisplay / 3, 75, "Paused")
        pygame.display.update()
        clock.tick(15)


########################################################################################################################
############################################# Main Game Loop ###########################################################
########################################################################################################################

def game_loop():
    x_pos = xDisplay * 0.455
    y_pos = yDisplay * 0.78
    x_change = 0

    block_speed = 0.00833 * yDisplay
    block_width = 0.125 * xDisplay
    block_height = 0.0833 * yDisplay
    block_x = random.randrange(25, int(xDisplay - (block_width + 25)))
    block_y = -yDisplay

    score = 0

    pygame.mixer.music.play(-1)

    while True:

        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -0.01 * xDisplay
                elif event.key == pygame.K_RIGHT:
                    x_change = 0.01 * xDisplay
                elif event.key == pygame.K_p:
                    paused(True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x_pos += x_change

        # Handles crashing into boundaries
        if x_pos + carWidth >= xDisplay or x_pos <= 0:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(crash_sound)
            crash()

        # Handles crashing into obstacles
        if y_pos < block_y + block_height - (0.0166 * yDisplay) and \
                (block_x + (0.0075 * xDisplay) < x_pos < block_x + block_width - (0.0075 * xDisplay) or block_x +
                    (0.0075 * xDisplay) < x_pos + carWidth < block_x + block_width - (0.0075 * xDisplay)):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(crash_sound)
            crash()

        # Handles drawing of obstacles
        if block_y > yDisplay:
            block_y = 0 - block_height
            block_x = random.randrange(25, int(xDisplay - (block_width + 25)))
            # Updates score and difficulty
            score += 1
            if block_speed < 0.0275 * yDisplay:
                block_speed += 0.00075 * yDisplay
                block_width += 0.00125 * xDisplay

        # "Graphic" rendering
        gameDisplay.fill(colors["darkGreen"])
        pygame.draw.rect(gameDisplay, colors["darkGrey"], (25, 0, xDisplay - 50, yDisplay))
        pygame.draw.line(gameDisplay, colors["darkYellow"], (xDisplay / 2 + 15, 0), (xDisplay / 2 + 15, yDisplay), 15)
        pygame.draw.line(gameDisplay, colors["darkYellow"], (xDisplay / 2 - 15, 0), (xDisplay / 2 - 15, yDisplay), 15)
        pygame.draw.line(gameDisplay, colors["white"], (40, 0), (40, yDisplay), 15)
        pygame.draw.line(gameDisplay, colors["white"], (xDisplay - 40, 0), (xDisplay - 40, yDisplay), 15)
        obstacles(block_x, block_y, block_width, block_height, colors["brown"])
        block_y += block_speed
        car(x_pos, y_pos)
        count(score)

        pygame.display.update()
        clock.tick(60)


game_intro()
