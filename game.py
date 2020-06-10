import pygame as pg
from sprites import *
from settings import *
import sys
import os

class Game():
    '''
    The class that handles all the game logic. Most of the variables are defined on 'settings.py' for easier reference and modification.
    '''
    def __init__(self):
        # Initializes Pygame module
        pg.init()
        # Initializes Pygame mixer - responsible for handling audio
        pg.mixer.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.dt = self.clock.tick()
        self.Load_Data()

    def New(self):
        '''
        A method to initialize the sprites groups, the player, player lives and score. This method is separated from the __init__() in order to reinitialize the aforementioned variables
        in case the player chooses to play again.
        '''
        # Initialize sprites group
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.lasers = pg.sprite.Group()
        self.powerups = pg.sprite.Group()

        # Initialize the player and set its variables
        self.player = Player(self)
        self.player.lives = PLAYER_LIVES
        self.score = 0

    def Load_Data(self):
        '''
        A method to load all the data (images, animations, sounds and music) that will be used in the game. It also starts the background music.
        '''
        # Set background
        self.background = pg.image.load(path.join(IMG_FOLDER, BACKGROUND_IMG))
        self.background_x = 0

        # Load images - Some of the images had to be rotated on import. Hence, the use of the variable ROTATE ANGLE.
        ## Player image
        self.p_img = pg.transform.rotate(pg.image.load(path.join(IMG_FOLDER , PLAYER_IMG)), ROTATE_ANGLE).convert_alpha()
        self.player_mini_img = pg.transform.rotate(self.p_img, - ROTATE_ANGLE)
        self.player_mini_img = pg.transform.scale(self.player_mini_img, (PLAYER_ICON_LIVES_WIDTH,PLAYER_ICON_LIVES_HEIGHT))
        self.p_ev_img = pg.transform.rotate(pg.image.load(path.join(IMG_FOLDER , PLAYER_EVOLVED_IMG)), ROTATE_ANGLE).convert_alpha()
        self.p_ev3_img = pg.transform.rotate(pg.image.load(path.join(IMG_FOLDER , PLAYER_LV3_IMG)), ROTATE_ANGLE).convert_alpha()

        ## Enemies images
        self.e_imgs = []
        for item in ENEMY_IMAGES:
            img = pg.transform.rotate(pg.image.load(os.path.join(ENEMY_FOLDER, item)), ROTATE_ANGLE).convert_alpha()
            self.e_imgs.append(img)

        ## Laser image
        self.l_img = pg.transform.rotate(pg.image.load(path.join(IMG_FOLDER , LASER_IMG)), ROTATE_ANGLE).convert_alpha()
        
        ## Powerup Image
        self.pow_img = pg.image.load(path.join(IMG_FOLDER, POWER_UP_LV2_IMAGE)).convert_alpha()
        self.pow_3_img = pg.image.load(path.join(IMG_FOLDER, POWER_UP_LV3_IMAGE)).convert_alpha()
        self.powerup_anim = []
        for i in range(len(os.listdir(EVOLVE_FOLDER))):
            filename = 'whitePuff0{}.png'.format(i)
            img = pg.image.load(path.join(EVOLVE_FOLDER, filename)).convert_alpha()
            img = pg.transform.scale(img, (img.get_width()//2,img.get_height()//2))
            self.powerup_anim.append(img)
        
        # Load sounds and music. Starts background music
        self.shoot_sound = pg.mixer.Sound(os.path.join(SOUNDS_FOLDER, SHOOT_SOUND))
        self.shoot_sound.set_volume(0.8)
        self.enemy_explosion_sound = pg.mixer.Sound(os.path.join(SOUNDS_FOLDER, EXPLOSION_ENEMY_SOUND))
        self.enemy_explosion_sound.set_volume(0.3)
        self.player_expllosion_sound = pg.mixer.Sound(os.path.join(SOUNDS_FOLDER, EXPLOSION_PLAYER_SOUND))
        self.player_expllosion_sound.set_volume(0.5)
        self.powerup_sound = pg.mixer.Sound(os.path.join(SOUNDS_FOLDER, POWER_UP_SOUND))
        self.powerup_sound.set_volume(0.5)
        pg.mixer.music.load(os.path.join(SOUNDS_FOLDER, MUSIC_FILE))
        pg.mixer.music.play(-1)

        # Load explosion animations
        self.explosion_anim = {}
        self.explosion_anim['enemy'] = []
        self.explosion_anim['player'] = []
        # Single loop since the folder for the enemy explosion animation has the same number of files as the player's explosion animation.
        for i in range(len(os.listdir(ENEMY_EXPLOSION_FOLDER))):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pg.image.load(os.path.join(ENEMY_EXPLOSION_FOLDER, filename)).convert_alpha()
            img = pg.transform.scale(img,(EXPLOSION_RESCALE_X,EXPLOSION_RESCALE_Y))
            self.explosion_anim['enemy'].append(img)
            filename = 'sonicExplosion0{}.png'.format(i)
            img = pg.image.load(os.path.join(PLAYER_EXPLOSION_FOLDER, filename)).convert_alpha()
            self.explosion_anim['player'].append(img)


    def Enemy_Spawner(self):
        '''
        A method to spawn enemies. It will continue spawning objects if the number of enemies in the game is less the ENEMY_MAX_NUM variable. The method also avoids spawning two
        sequential enemies on the same spawn point.
        '''
        self.enemies_alive = len(self.enemies)
        self.previous_sp = None
        if self.enemies_alive < ENEMY_MAX_NUM:
            self.enemy_image = random.choice(self.e_imgs)
            self.random_spawn_point = random.choice(ENEMY_SPAWN_POINTS)
            while self.random_spawn_point == self.previous_sp:
                self.random_spawn_point = random.choice(ENEMY_SPAWN_POINTS)
            self.previous_sp = self.random_spawn_point
            self.enemy = Enemy(self, self.enemy_image, self.random_spawn_point[0], self.random_spawn_point[1])
    
    
    def Draw_Text(self, text, size, x, y, color, center=False):
        '''
        A method to draw text on the screen.
        Parameters:
        text (str): The text to be displayed.
        size (int): The size of the text to be displayed.
        x (int): The x coordinate for the position of the text.
        y (int): The y coordinate for the position of the text.
        color (tuple(red,green,blue)): The color of the text.
        center (bool): The boolean to indicate if the x and y coordinates should be considered for the center of the text (True) or not (False)
        '''
        self.font = pg.font.Font(os.path.join(FONT_FOLDER, FONT_NAME), size)
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect()
        if center:
            self.text_rect.centerx = x
            self.text_rect.centery = y
        else:
            self.text_rect.x = x
            self.text_rect.y = y
        self.screen.blit(self.text_surface, self.text_rect)

    def Draw_Lives(self, x, y, lives, img):
        '''
        A method to draw the icons for the number of lives on the screen.
        Parameters:
        x (int): The x coordinate for the staring position of the icons.
        y (int): The y coordinate for the position of the icons.
        lives (int): The current number of lives the player has.
        img (pygame.image): The image of the icons for the lives.
        '''
        self.i_lives = pg.transform.scale(pg.transform.rotate(self.player.image, - ROTATE_ANGLE), (PLAYER_ICON_LIVES_WIDTH,PLAYER_ICON_LIVES_HEIGHT))
        for i in range(lives):
            img_rect = self.i_lives.get_rect()
            img_rect.x = x + (PLAYER_ICON_LIVES_WIDTH + PLAYER_ICON_MARGIN) * i
            img_rect.y = y
            self.screen.blit(self.i_lives, img_rect)
        

    def Draw(self):
        '''
        The method that defines what should be draw on the screen.
        '''
        # Continuously loop the background image
        rel_x = self.background_x % self.background.get_rect().width
        self.screen.blit(self.background, (rel_x - self.background.get_rect().width, 0))
        if rel_x < SCREEN_WIDTH:
            self.screen.blit(self.background, (rel_x,0))
        self.background_x -= 1

        # Draw all sprites
        self.all_sprites.draw(self.screen)
        # Draw Score
        self.Draw_Text(str(self.score).zfill(SCORE_SIZE), size=24, x=10, y=10, color=WHITE)
        # Draw Lives
        self.Draw_Lives(SCREEN_WIDTH - 180, 10, self.player.lives, self.player_mini_img)
        # Updates the display
        pg.display.update()

    def Run(self):
        '''
        The game loop method. While the game is playing it will call the methods Events, Enemy_Spawner, Check_For_Collisions, Update and Draw().
        '''
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.Events()
            self.Enemy_Spawner()
            self.Check_For_Collisions()
            self.update()
            self.Draw() 

    def update(self):
        '''
        The method to call the 'update' on all the sprites within the 'all_sprites' group (Pygame).
        '''
        self.all_sprites.update()

    def Events(self):
        '''
        The method to check if the player has quit the game.
        '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.Quit()

    def Remove_Power_Ups(self):
        for pups in self.powerups:
            pups.kill()
    
    # Check for all collisions
    def Check_For_Collisions(self):
        '''
        The method responsible for checking for collision between the player and enemies, enemies and laser, player and power-ups. It will also trigger the game over should the 
        player's lives reach 0.
        '''
        # Check for collisions between player and enemies
        hits_player = pg.sprite.spritecollide(self.player, self.enemies, True)
        if hits_player:
            self.player_expllosion_sound.play()
            self.death_expl = Explosion(self, self.player.rect.center, 'player')
            self.player.Die()
            self.Remove_Power_Ups()

        # Check for collisions between lasers and enemies
        # TODO: Refactor the power-up code to be more dynamic    
        hits_enemies = pg.sprite.groupcollide(self.enemies, self.lasers, True, True)
        for hit in hits_enemies:
            self.score += hit.points
            self.enemy_explosion_sound.play()
            self.expl = Explosion(self, hit.rect.center, 'enemy')
            if random.random() > POWER_UP_RATE and self.score >= POWER_UP_LVL2_MIN_SCORE and self.player.lvl == 1:
                powerup = PowerUp(self, self.pow_img, hit.rect.center)
            if random.random() > POWER_UP_RATE and self.score >= POWER_UP_LVL3_MIN_SCORE and self.player.lvl == 2:
                powerup = PowerUp(self, self.pow_3_img, hit.rect.center)
        
        # Check for collisions between player and power ups
        hits_powerup = pg.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits_powerup:
            if self.player.lvl < 3:
                pu_effect = PowerUp_Effect(self, self.player.rect.center)
                self.powerup_sound.play()
                hit.Evolve()
                self.Remove_Power_Ups()
        
        # Check if the player still has lives and if the death animation has ended before closing the game
        if self.player.lives == 0 and not self.death_expl.alive():
            self.playing = False

    def Show_Start_Screen(self):
        '''
        The method to show the Start Screen.
        '''
        self.screen.blit(self.background, (0,0))

        self.Draw_Text("Space Invaders Knock-Off!", size=48, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 4, color=WHITE, center=True)
        self.Draw_Text("WASD keys to move, Space to fire", size=18, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2, color=WHITE, center=True)
        self.Draw_Text("Press any key to begin", size=14, x=SCREEN_WIDTH /2, y=SCREEN_HEIGHT * 3/4, color=WHITE, center=True)
        pg.display.flip()
        self.Wait_for_key()

    def Show_GO_Screen(self):
        '''
        The method to show the Game Over.
        '''
        self.Draw_Text("GAME OVER", size=64, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 4, color=RED, center=True)
        self.Draw_Text("Press any key to play again.", size=18, x=SCREEN_WIDTH /2, y=SCREEN_HEIGHT * 3/4, color=WHITE, center=True)
        pg.display.flip()
        self.Wait_for_key()
        
    def Wait_for_key(self):
        '''
        The method to wait for the player to press a key on the Start and Game Over screens.
        '''
        self.waiting = True
        while self.waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    self.Quit()
                if event.type == pg.KEYUP:
                    self.waiting = False

    def Quit(self):
        '''
        The method to quit from Pygame and Python.
        '''
        pg.quit()
        sys.exit()