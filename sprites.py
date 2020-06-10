import pygame as pg
from settings import *
import random
from os import path

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.p_img
        self.rect = self.image.get_rect()
        self.rect.centery = SCREEN_HEIGHT/2
        self.rect.centerx = PLAYER_SPAWN_X
        self.game.all_sprites.add(self)
        self.speed = PLAYER_SPEED
        self.last_shot = 0
        self.lives = PLAYER_LIVES
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.lvl = 1
        self.guns = 1

    def update(self):
        if self.hidden and pg.time.get_ticks() - self.hide_timer > PLAYER_HIDDEN_TIMER:
            self.hidden = False
            self.rect.center = (PLAYER_SPAWN_X, SCREEN_HEIGHT/2)
        self.Get_Keys()
        
    def Get_Keys(self):
        if not self.hidden:
            keys = pg.key.get_pressed()
            if keys[pg.K_a] and self.rect.x > BORDER:
                self.rect.x -= PLAYER_SPEED * self.game.dt
            if keys[pg.K_d] and self.rect.x < SCREEN_WIDTH - self.image.get_width() - BORDER:
                self.rect.x += PLAYER_SPEED * self.game.dt
            if keys[pg.K_w] and self.rect.y > BORDER:
                self.rect.y -= PLAYER_SPEED * self.game.dt
            if keys[pg.K_s] and self.rect.y < SCREEN_HEIGHT - self.image.get_height() - BORDER:
                self.rect.y += PLAYER_SPEED * self.game.dt
            if keys[pg.K_SPACE]:
                now = pg.time.get_ticks()
                if now - self.last_shot > LASER_FIRE_RATE:
                    self.last_shot = now
                    self.Shoot()
    
    def Shoot(self):
        if self.guns == 1:
            laser = Laser(self.game, self.rect.right, self.rect.centery)
        elif self.guns == 2:
            laser = Laser(self.game, self.rect.right, self.rect.top)
            laser = Laser(self.game, self.rect.right, self.rect.bottom)
        elif self.guns == 3:
            laser = Laser(self.game, self.rect.right, self.rect.top)
            laser = Laser(self.game, self.rect.right, self.rect.centery)
            laser = Laser(self.game, self.rect.right, self.rect.bottom)

        self.game.shoot_sound.play()

    def Hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 300)

    def Die(self):
        self.lives -= 1
        self.Hide()
        self.image = self.game.p_img
        self.guns = 1
        self.lvl = 1


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, img, x , y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.initial_y = y
        self.rect.x = x
        self.rect.y = y
        self.game.all_sprites.add(self)
        self.game.enemies.add(self)
        self.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        if random.random() > ENEMY_DIAGONAL_RATE:
            self.speedy = ENEMY_SPEED_Y
        else:
            self.speedy = 0
        self.spawn_time = pg.time.get_ticks()
        self.points = ENEMY_POINTS_VALUE
        
    def update(self):
        self.Auto_Move()
        if self.rect.x < -self.rect.right:
            self.kill()

    def Auto_Move(self):
        self.rect.x -= self.speed * self.game.dt
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.bottom > self.initial_y + ENEMY_RANGE:
            self.speedy *= -1
        elif self.rect.top <= 0 or self.rect.bottom < self.initial_y - ENEMY_RANGE:
            self.speedy = abs(self.speedy)
        self.rect.y += self.speedy * self.game.dt

class Laser(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.l_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - LASER_Y_OFFSET
        self.game.all_sprites.add(self)
        self.game.lasers.add(self)
        self.speed = LASER_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.Auto_Move()
        if self.rect.left > SCREEN_WIDTH + self.image.get_size()[0]:
            self.kill()

    def Auto_Move(self):
        self.rect.x += self.speed * self.game.dt

# TODO: Refactor the code to be more abstract. Explosion and power-up codes are practically the same
class Explosion(pg.sprite.Sprite):
    def __init__(self, game, center, expl_type):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.expl_type = expl_type
        self.game.all_sprites.add(self)
        self.image = self.game.explosion_anim[self.expl_type][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = FPS

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.explosion_anim[self.expl_type]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.explosion_anim[self.expl_type][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, img, center):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.game.all_sprites.add(self)
        self.game.powerups.add(self)
        self.speed = POWER_UP_SPEED

    def update(self):
        self.Auto_Move()
        if self.rect.right < 0:
            self.kill()

    def Auto_Move(self):
        self.rect.x -= self.speed * self.game.dt

    def Evolve(self):
        if self.game.player.lvl <= 2:
            self.game.player.lvl += 1
            self.game.player.guns += 1
        if self.game.player.lvl == 1:
            self.game.player.image = self.game.p_ev_img
        elif self.game.player.lvl == 2:
            self.game.player.image = self.game.p_ev3_img
        

# TODO: Refactor code to merge with Explosions
class PowerUp_Effect(pg.sprite.Sprite):
    def __init__(self, game, center):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.all_sprites.add(self)
        self.image = self.game.powerup_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = FPS

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.powerup_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.powerup_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
