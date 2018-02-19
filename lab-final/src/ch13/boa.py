'''
Created on 14-Dec-2017

@author: kavyareddy

 Simple snake example.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

'''

import pygame

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

NUMBER_OF_SEGMENTS = 15

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3

game_over = None

# Set initial speed
x_change = segment_width + segment_margin
y_change = 0


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class HeadSegment(Segment):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(GREEN)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class GameOver(object):
    def __init__(self):
        super().__init__()
        font = pygame.font.SysFont("serif", 25)
        self.text = font.render("Game Over, click to restart", True, WHITE)
        self.text_rect = self.text.get_rect()
        self.center_x = (SCREEN_WIDTH / 2) - (self.text_rect.width / 2)
        self.center_y = (SCREEN_HEIGHT / 2) - (self.text_rect.height / 2)

    def display(self, screen):
        screen.blit(self.text, [self.center_x, self.center_y])

pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('Snake Example')

allspriteslist = pygame.sprite.Group()
segment_group = pygame.sprite.Group()

# Create an initial snake
snake_segments = []
for segno in range(NUMBER_OF_SEGMENTS):
    x = 250 - (segment_width + segment_margin) * segno
    y = 30
    segment = Segment(x, y)

    # Handles case when snake appears in first frame
    if segno == 0:
        segment = HeadSegment(x, y)
        snake_segments.append(segment)
        allspriteslist.add(segment)
        segment_group.add(segment)
    # Creates to tail for the snake
    else:
        snake_segments.append(segment)
        allspriteslist.add(segment)


clock = pygame.time.Clock()
done = False
font = pygame.font.Font(None, 36)
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN and game_over is None:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) * - 1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) * - 1
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)

        elif event.type == pygame.MOUSEBUTTONDOWN and game_over is not None:
            done = True

    # Get rid of last segment of the snake
    # .pop() command removes last item in list
    if game_over is None:
        old_segment = snake_segments.pop()
        allspriteslist.remove(old_segment)
        segment_group.remove(old_segment)

        # Figure out where new segment will be
        x = snake_segments[0].rect.x + x_change
        y = snake_segments[0].rect.y + y_change
        head = HeadSegment(x, y)

        hit_list = pygame.sprite.spritecollide(head, segment_group, True)

        segment_group.add(head)

        snake_segments.insert(0, head)
        allspriteslist.add(head)

        segment_group.add(snake_segments[1])
        snake_segments[1].image.fill(WHITE)

    screen.fill(BLACK)

    if len(hit_list) > 0 and game_over is None:
        game_over = GameOver()
        print("game over")

    if game_over is not None:
        game_over.display(screen)

    # -- Draw everything
    # Clear screen

    allspriteslist.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(5)

pygame.quit()
