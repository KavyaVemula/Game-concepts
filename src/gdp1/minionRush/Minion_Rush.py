'''

@author: Kavya Reddy Vemula
@author: Priyanka Gadde

Version: 1

The code implements our platform game. 
For now, the player is able to navigate through different levels.
We have included collectibles in its way and added feedback system  at the top.
The default score and lives is displayed for now which will be updated. 

The keyboard keys up, down, left and right can be used for the movement of the player. 
'''

import pygame

 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (237, 90, 242)
SCORE_BOARD_COLOR = (90, 166, 242)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


 
class Player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.image.load("minion.png")
        self.rect = self.image.get_rect()

        self.change_x = 0                   
        self.change_y = 0

        self.level = None
 
    def update(self):

        self.calc_grav()

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list: 
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                
            self.change_y = 0
 
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
 
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6
 
    def go_right(self):
        self.change_x = 6
 
    def stop(self):
        self.change_x = 0
 
class Banana(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("banana.png") 
        self.rect = self.image.get_rect()
 
class Platform(pygame.sprite.Sprite):
 
    def __init__(self, width, height):
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE)
 
        self.rect = self.image.get_rect() 
 
class MovingPlatform(Platform):
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0 
    player = None 
    level = None
 
    def update(self):

        self.rect.x += self.change_x
 
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:

            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        self.rect.y += self.change_y 

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:

            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
 
 
class Level(object):
    
    def __init__(self, player):
            
        self.score = 0
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        
        self.banana_list = pygame.sprite.Group()

        self.background = pygame.image.load("background1.jpg")
        
        self.font = pygame.font.SysFont('Calibri', 25, True, False)

        self.world_shift = 0
        self.level_limit = -1000

    def update(self):
        
        self.platform_list.update()
        self.enemy_list.update()
        self.banana_list.update()

 
    def draw(self, screen):

        screen.blit(self.background, [0, 0])
        
        pygame.draw.ellipse(screen, SCORE_BOARD_COLOR, [550,10,150,50], 0)
        text = self.font.render("Score: " +str(self.score), True, WHITE)
        screen.blit(text, [580, 25])
        
        pygame.draw.ellipse(screen, SCORE_BOARD_COLOR, [390,10,150,50], 0)
        text = self.font.render("Lives: " +str(self.score), True, WHITE)
        screen.blit(text, [420, 25])

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.banana_list.draw(screen)

 
    def shift_world(self, shift_x):

        self.world_shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            
        for banana in self.banana_list:
            banana.rect.x += shift_x
            

class Level_01(Level):
 
    def __init__(self, player):
        
        Level.__init__(self, player)
 
        self.level_limit = -1500        

        level = [[210, 70, 500, 500],
                 [210, 70, 900, 400],
                 [210, 70, 1500, 300],
                 [210, 70, 2120, 280],
                 ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            
            banana=Banana()
            banana.rect.x = platform[2] + 50
            banana.rect.y = platform[3] - 80
            self.banana_list.add(banana)
             
        banana_hit_list = pygame.sprite.spritecollide(banana, self.banana_list, True)
        collect_sound = pygame.mixer.Sound("collectingSound.ogg")
         
        for banana in banana_hit_list:
            self.banana_list.remove(banana)
            collect_sound.play()
            self.score += 1
            print(self.score)
            
        def draw(screen):
            self.banana_list.draw(screen)            

        block = MovingPlatform(70, 40)
        block.rect.x = 1350
        block.rect.y = 380
        block.boundary_left = 1250
        block.boundary_right = 1500
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        
        block = Platform(70, 70)
        block.rect.x = 1850
        block.rect.y = 380
        block.boundary_top = 1050
        block.boundary_bottom = 1500
    #  block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
 

class Level_02(Level):

    def __init__(self, player):

        Level.__init__(self, player)
 
        self.level_limit = -1000  

        level = [[210, 70, 500, 550],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]  

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            
            banana=Banana()
            banana.rect.x = platform[2] + 50
            banana.rect.y = platform[3] - 80
            self.banana_list.add(banana)  

        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)  
 
def main():
    """ Main Program """
    pygame.init()
    
    door_position = [500,500]

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Minion Rush") 

    player = Player()

    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
 
    # sets the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level     
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    
    jump_sound = pygame.mixer.Sound("jumpingSound.ogg")
    
    door_image = pygame.image.load("door.png")    
   
    done = False 

    clock = pygame.time.Clock() 

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    jump_sound.play()
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()       
 
        active_sprite_list.update() 

        current_level.update()
 
        # shifts the world to the left
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
            door_position[0] = door_position[0] + 500
            door_position[1] = door_position[1] + 500
 
        # shifts the world to the right
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
 
        # goes to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            if current_level_no < len(level_list)-1:
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                done = True       
 
        # To draw onto the screen
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        if(current_level_no == 0):
                screen.blit(door_image, [100,500])
                 
        # Clock throttles 60 frames per second
        clock.tick(60)
 
        pygame.display.flip() 

    pygame.quit()
 
if __name__ == "__main__":
    main()