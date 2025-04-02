#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer
init()
mixer.init()
font.init()
win_height = 700
win_width = 500
window = display.set_mode((win_height,win_width))
display.set_caption('DOOM')
bg = transform.scale(image.load('1476904401_Steamfire.jpg'), (win_height,win_width))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,size_h,size_v):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_h,size_v))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x <650:
            self.rect.x += self.speed
        if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 450:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet2.png',self.rect.centerx,self.rect.top, -15,30,90)
        bullet.add(bullets)

lost = 0
score = 0
font1 = font.SysFont('Arial',35)
font2 = font.SysFont('Arial',250)
font3 = font.SysFont('Arial',160)
font4 = font.SysFont('Arial',45)
text_loser = font2.render('Death' ,True,(240,0,0))
text_winner = font3.render('Survived',True,(185,0,0))
text_contin = font4.render('Press SPACE to continue',True,(0,0,0))
text_pause = font1.render('ESC - Пауза',True,(240,0,0))
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,620)
            lost += 1

def reset_game():
    global doomguy, monsters, bullets, lost, score, finish, fireballs
    doomguy = Player('b8d96f104b6fd8fdb7767deb4e048962.jpg', 50, 380, 6, 105, 90)
    monsters = sprite.Group()
    for i in range(5):
        monster = Enemy('png-transparent-doom-3-doom-64-doom-ii-doom-video-game-fictional-character-cacodemon.png', randint(0, 620), -50, randint(1, 3), 65, 65)
        monsters.add(monster)
    fireballs = sprite.Group()
    for i in range(3):
        fireball = Enemy('blue-fireball.png',randint(0,620),-50,randint(1,3),65,65)
        fireballs.add(fireball)
    bullets.empty()
    lost = 0
    score = 0
    finish = False


clock = time.Clock()
mixer.music.load('doom-ost-e1m1-at-dooms-gatedodoc.mp3')
fire_sound = mixer.Sound('vistreL.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()
doomguy = Player('b8d96f104b6fd8fdb7767deb4e048962.jpg',50,380,6,105,90)


bullets = sprite.Group()
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()

num_fire = 0
rel_time = False

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('png-transparent-doom-3-doom-64-doom-ii-doom-video-game-fictional-character-cacodemon.png',randint(0,620),-50,randint(1,3),65,65)
    monsters.add(monster)

fireballs = sprite.Group()
for i in range(3):
    fireball = Enemy('blue-fireball.png',randint(0,620),-50,randint(1,3),65,65)
    fireballs.add(fireball)
game = True
paused = False
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                paused = not paused
                while paused:
                    for ev in event.get():
                        if ev.type == KEYDOWN and ev.key == K_ESCAPE:
                            paused = False
                        elif ev.type == QUIT:
                            game = False
                            paused = False
            if e.key == K_SPACE:
                if finish:
                    reset_game()
                    num_fire = 0
                    rel_time = False    
                else:
                    if num_fire < 10 and rel_time == False:
                        num_fire += 1
                        doomguy.fire()
                        fire_sound.play()
                    if num_fire >= 10 and rel_time == False:
                        last_time = timer()
                        rel_time = True
    if not finish:
        bullets.update()
        window.blit(bg,(0,0))
        if rel_time:
            now_time = timer()
            if now_time - last_time < 2:
                reload = font1.render('Wait reload...',True,(150,0,0))
                window.blit(reload,(250,400))
            else:
                num_fire = 0
                rel_time = False
        doomguy.reset()
        doomguy.update()
        monsters.draw(window)
        monsters.update()
        fireballs.draw(window)
        fireballs.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render('Пропущено:' + str(lost),True,(255,0,0))
        text_kill = font1.render('Убито:' + str(score),True,(255,0,0))
        window.blit(text_lose,(10,20))
        window.blit(text_kill,(10,55))
        window.blit(text_pause,(485,20))
        if sprite.spritecollide(doomguy,monsters,False):
            finish = True
            window.blit(text_loser,(25,45))
            window.blit(text_contin,(45,310))
        if sprite.spritecollide(doomguy,fireballs,False):
            finish = True
            window.blit(text_loser,(25,45))
            window.blit(text_contin,(45,310))
        if sprite.groupcollide(monsters,bullets,True,False):
            score += 1
            monster = Enemy('png-transparent-doom-3-doom-64-doom-ii-doom-video-game-fictional-character-cacodemon.png',randint(0,620),-50,randint(1,3),65,65)
            monsters.add(monster)
        if sprite.groupcollide(fireballs,bullets,True,False):
            fireball = Enemy('blue-fireball.png',randint(0,620),-50,randint(1,3),65,65)
            fireballs.add(fireball)
        if score > 9:
            finish = True
            window.blit(text_winner,(25,75))
            window.blit(text_contin,(45,310))
        if lost > 2:
            finish = True
            window.blit(text_loser,(25,45))
            window.blit(text_contin,(45,310))                         
    clock.tick(60)
    display.update()