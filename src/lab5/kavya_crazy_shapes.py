'''
Created on 28-Sep-2017

@author: kavyareddy
'''

 
import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Rectangle():
    def __init__(self):
        #Rectangle position
        self.x = random.randint(0,700)
        self.y = random.randint(0,500)
        
        self.height = random.randint(20,70)
        self.width = random.randint(20,70)
        
        self.change_x = random.randint(-3,3)
        self.change_y = random.randint(-3,3)
        
        self.COLOR = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, [self.x,self.y,self.height,self.width], 0)
    
    def move(self):
        self.x = self.x + self.change_x
        self.y = self.y + self.change_y
        
class Ellipse(Rectangle):
    def draw(self,screen):
        pygame.draw.ellipse(screen, self.COLOR, [self.x,self.y,self.height,self.width], 0)
    
        
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()


my_list=[]
for x in range (0,1000):
    my_object = Rectangle()
    my_list.append(my_object)
for x in range(0,1000):
    my_obj = Ellipse()
    my_list.append(my_obj)

my_object.x = 100
my_object.y = 200
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Game logic should go here
    
        
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
 
    # --- Drawing code should go here
    for x in my_list:
        x.draw(screen)
        x.move()
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()