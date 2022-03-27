#Создай собственный Шутер!
from pygame  import * 
from random import *
win_width = 700
win_height = 500 
window = display.set_mode((win_width,win_height))
display.set_caption('SHOOTER')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
clock = time.Clock()
FPS = 120
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
lost=0
killed=0
font.init()
font=font.SysFont('Arial',36)
text=font.render('Счет: '+str(killed),True,(255,255,255))
text2=font.render('Пропущено: '+str(lost),True,(255,255,255))
#########################################################
class GameSprite(sprite.Sprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__()
		self.height=height
		self.width=width
		self.speed = speed
		self.image = transform.scale(image.load(img),(self.width,self.height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	def reset(self):
		window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__(img, x, y, speed, width, height)
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x>0:
			self.rect.x-=self.speed
		elif keys[K_RIGHT] and self.rect.x+self.width<win_width:
			self.rect.x+=self.speed
	def fire(self):
		bullet = Bullet('bullet.png',self.rect.x,self.rect.y,1,20,20)
		bullets.add(bullet)
class UFO(GameSprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__(img, x, y, speed, width, height)
	def update(self):
		global lost,text2
		self.rect.y+=self.speed
		if self.rect.y>=win_height:
			lost+=1
			text2=font.render('Пропущено: '+str(lost),True,(255,255,255))
			self.rect.y = 0
			self.rect.x = randint(0 , win_width-self.width)
class Bullet(GameSprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__(img, x, y, speed, width, height)
	def update(self):
		self.rect.y-=self.speed
		if self.rect.y<=0:
			self.kill()
#########################################################
rocket = Player('rocket.png',win_width//2,win_height-80,1,80,80)
bullets = sprite.Group()
#Создаем группу врагов
enemies = sprite.Group()
for i in range(5):
	enemy = UFO('ufo.png',randint(0,win_width-80),0,1,80,80)
	enemies.add(enemy)

while True:
	window.blit(background,(0,0))
	window.blit(text,(0,20))
	window.blit(text,(0,50))
	enemies.update()
	enemies.draw(window)
	bullets.update()
	bullets.draw(window)
	rocket.update()
	rocket.reset()
	display.update()
	hits = sprite.groupcollide(bullets,enemies, True, True)
	for i in hits:
		killed+=1
		text=font.render('Счет: '+str(killed),True,(255,255,255))
		enemy = UFO('ufo.png',randint(0,win_width-80),0,1,80,80)
		enemies.add(enemy)
	for i in event.get():
		if i.type==QUIT:
			quit()
		if i.type==KEYDOWN:
			if i.key==K_SPACE:
				rocket.fire()
	clock.tick(FPS)