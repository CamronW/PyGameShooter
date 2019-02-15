import pygame
import math
import random

class Player():
	def __init__(self, x, y):
		self.posX = x
		self.posY = y
		self.movX = 0
		self.movY = 0
		self.velocity = 4
		self.width = 30
		self.height = 30
		self.timeSinceLastShot = 0
		self.shotsPerSec = 5
		self.money = 0
		self.lives = 3
		self.gun = "Assault Rifle"
		self.luck = 5
		self.inShop = False

	def setMov(self, movX, movY):
		self.movX = movX
		self.movY = movY
	def updatePos(self):	
		self.posX = self.posX + (self.movX * self.velocity)
		self.posY = self.posY + (self.movY * self.velocity)
	def addMoney(self, amount):
		self.money += amount
	def addLives(self, amount):
		self.lives += amount

	def pickupGun(self, gun):
		self.gun = gun
		if gun == "Assault Rifle":
			self.shotsPerSec = 5
		if gun == "Machine Gun":
			self.shotsPerSec = 15
		if gun == "Sniper":
			self.shotsPerSec = 2
		if gun == "Laser":
			self.shotsPerSec = 30

	def getBulletObject(self, bullet_move_x, bullet_move_y, degree):
		if self.gun == "Assault Rifle":
			bulletObject = NormalBullet(self.posX, self.posY, bullet_move_x, bullet_move_y, degree)
			return bulletObject
		if self.gun == "Machine Gun":
			bulletObject = FastBullet(self.posX, self.posY, bullet_move_x, bullet_move_y, degree)
			return bulletObject
		if self.gun == "Sniper":
			bulletObject = SniperBullet(self.posX, self.posY, bullet_move_x, bullet_move_y, degree)
			return bulletObject
		if self.gun == "Laser":
			bulletObject = LaserBullet(self.posX, self.posY, bullet_move_x, bullet_move_y, degree)
			return bulletObject


class Enemy():
	def __init__(self, x, y):
		self.posX = x
		self.posY = y
		self.movX = 0
		self.movY = 0
		self.velocity = 2
		self.width = 30
		self.height = 30

	def updatePos(self):
		self.posX = self.posX + (self.movX * self.velocity)
		self.posY = self.posY + (self.movY * self.velocity)

class NormalBullet():
	def __init__(self, x, y, movX, movY, degree):
		self.posX = x
		self.posY = y
		self.movX = movX
		self.movY = movY
		self.degree = degree
		self.velocity = 10
		self.width = 38
		self.height = 8
		self.piercing = False

	def updatePos(self):
		self.posX = self.posX + (self.movX * self.velocity)
		self.posY = self.posY + (self.movY * self.velocity)

class FastBullet():
	def __init__(self, x, y, movX, movY, degree):
		self.posX = x
		self.posY = y
		self.movX = movX
		self.movY = movY
		self.degree = degree
		self.velocity = 25
		self.width = 38
		self.height = 8
		self.piercing = False

	def updatePos(self):
		self.posX = self.posX + (self.movX * self.velocity)
		self.posY = self.posY + (self.movY * self.velocity)

class SniperBullet():
	def __init__(self, x, y, movX, movY, degree):
		self.posX = x
		self.posY = y
		self.movX = movX
		self.movY = movY
		self.degree = degree
		self.velocity = 25
		self.width = 38
		self.height = 8
		self.piercing = True

	def updatePos(self):
		self.posX = self.posX + (self.movX * self.velocity)
		self.posY = self.posY + (self.movY * self.velocity)

class LaserBullet():
	def __init__(self, x, y, movX, movY, degree):
		self.posX = x
		self.posY = y
		self.movX = movX
		self.movY = movY
		self.degree = degree
		self.velocity = 25
		self.width = 38
		self.height = 8
		self.piercing = False

	def updatePos(self):
		self.posX = self.posX + (self.movX * self.velocity)
		self.posY = self.posY + (self.movY * self.velocity)

class HealthPickup():
	def __init__(self, x, y):
		self.posX = x
		self.posY = y
		self.width = 30
		self.height = 30
		self.livesBonus = 1

	def collected(self, player):
		player.addLives(1)

class MachineGunPickup():
	def __init__(self, x, y):
		self.posX = x
		self.posY = y
		self.width = 30
		self.height = 30

	def collected(self, player):
		player.pickupGun("Machine Gun")

class SniperPickup():
	def __init__(self, x, y):
		self.posX = x
		self.posY = y
		self.width = 30
		self.height = 30

	def collected(self, player):
		player.pickupGun("Sniper")

class LaserPickup():
	def __init__(self, x, y):
		self.posX = x
		self.posY = y
		self.width = 30
		self.height = 30

	def collected(self, player):
		player.pickupGun("Laser")

class ShopButton():
	def __init__(self):
		self.posX = 700
		self.posY = 0
		self.width = 100
		self.height = 50
		self.normalColour = (234,234,234)
		self.hoveredColour = (255,255,255)
		self.currentColour = self.normalColour
		self.text = "Shop"
		self.textColour = (0,0,0)
		self.textPosX = (self.posX + self.width / 6) 
		self.textPosY = self.posY
		self.buttonCooldown = 100
		self.timeSinceLastClick = 0

class ShopWindow():
	def __init__(self):
		self.posX = 100
		self.posY = 100
		self.width = 880
		self.height = 500
		self.show = False
		self.backgroundColour = (234,234,234)

def isTouching(objectA, objectB):
	yTouching = False
	xTouching = False
	if objectA.posY > objectB.posY and objectA.posY < (objectB.posY + objectB.height) or objectA.posY == objectB.posY:
		#print("top point within or equal to same Y")
		yTouching = True
	if (objectA.posY + objectA.height) > objectB.posY and (objectA.posY + objectA.height) < (objectB.posY + objectB.height):
		#print("bottom point within or equal to same Y")
		yTouching = True
	if objectA.posX > objectB.posX and objectA.posX < (objectB.posX + objectB.width) or objectA.posX == objectB.posX:
		#print("top point within or equal to same X")
		xTouching = True
	if (objectA.posX + objectA.width) > objectB.posX and (objectA.posX + objectA.width) < (objectB.posX + objectB.width):
		#print("bottom point within or equal to same X")
		xTouching = True

	if xTouching and yTouching:
		#print("TOUCHING!!")
		return True
	else:
		#print("no :(")
		return False

def isMouseOver(mousePos, objectB):
	mouseX, mouseY = mousePos
	yTouching = False
	xTouching = False
	if mouseY > objectB.posY and mouseY < (objectB.posY + objectB.height) or mouseY == objectB.posY:
		#print("top point within or equal to same Y")
		yTouching = True
	if (mouseY) > objectB.posY and (mouseY) < (objectB.posY + objectB.height):
		#print("bottom point within or equal to same Y")
		yTouching = True
	if mouseX > objectB.posX and mouseX < (objectB.posX + objectB.width) or mouseX == objectB.posX:
		#print("top point within or equal to same X")
		xTouching = True
	if (mouseX) > objectB.posX and (mouseX) < (objectB.posX + objectB.width):
		#print("bottom point within or equal to same X")
		xTouching = True

	if xTouching and yTouching:
		#print("TOUCHING!!")
		return True
	else:
		#print("no :(")
		return False
def main():
	screenWidth = 1080
	screenHeight = 720
	screen = pygame.display.set_mode((screenWidth,screenHeight))
	bg = pygame.image.load("bg.jpg")
	bulletImg = pygame.image.load("bullet.png")
	gamefont = pygame.font.SysFont("Comic Sans MS", 30)
	pickupList = ["HealthPickup", "MachineGunPickup", "SniperPickup", "LaserPickup"]
	player = Player(250, 250)
	shopButton = ShopButton()
	shopWindow = ShopWindow()
	buttons = []
	bullets = []
	enemies = []
	currentPickups = []
	buttons.append(shopButton)

	def redrawGameWindow():
		screen.blit(bg, (0,0))	
		#Draw all bullets
		for bullet in bullets:
			currentBulletImg = pygame.transform.rotate(bulletImg, -bullet.degree)
			screen.blit(currentBulletImg, (bullet.posX, bullet.posY))
			#pygame.draw.rect(screen, (255,0,0), (bullet.posX, bullet.posY, 10, 10))

		#Draw all enemies
		for enemy in enemies:
			pygame.draw.rect(screen, (255,0,0), (enemy.posX, enemy.posY, enemy.width, enemy.height))
		#Draw the player
		pygame.draw.rect(screen, (0,255,255), (player.posX - (player.width / 4), player.posY - (player.height / 4), player.width, player.height))
		
		#Draw pickups
		for pickup in currentPickups:
			if pickup.__class__.__name__ == "HealthPickup":
				pygame.draw.rect(screen, (0,255,0), (pickup.posX, pickup.posY, pickup.height, pickup.width))
			if pickup.__class__.__name__ == "MachineGunPickup":
				pygame.draw.rect(screen, (255,255,0), (pickup.posX, pickup.posY, pickup.height, pickup.width))
			if pickup.__class__.__name__ == "SniperPickup":
				pygame.draw.rect(screen, (255,0,255), (pickup.posX, pickup.posY, pickup.height, pickup.width))
			if pickup.__class__.__name__ == "LaserPickup":
				pygame.draw.rect(screen, (255,255,255), (pickup.posX, pickup.posY, pickup.height, pickup.width))


		#Render all text
		moneytext = "Money: " + str(player.money)
		moneytextRender = gamefont.render(moneytext, False, (0,0,0))
		livestext = "Lives:" + str(player.lives)
		livetextRender = gamefont.render(livestext, False, (0,0,0))
		guntext = "Gun:" + str(player.gun)
		guntextRender = gamefont.render(guntext, False, (0,0,0))

		#Draw text
		screen.blit(moneytextRender,(0,0))
		screen.blit(livetextRender,(200,0))
		screen.blit(guntextRender,(400,0))

		#Draw all buttons
		for button in buttons:
			pygame.draw.rect(screen, button.currentColour, (button.posX, button.posY, button.width, button.height))
			screen.blit(gamefont.render(button.text, False, button.textColour), (button.textPosX,button.textPosY))

		#If player in shop, draw over the top
		if shopWindow.show:
			pygame.draw.rect(screen, shopWindow.backgroundColour, (shopWindow.posX, shopWindow.posY, shopWindow.width, shopWindow.height))
		pygame.display.update()

	def spawnPickup():
		pickupChoice = random.choice(pickupList)
		if pickupChoice == "HealthPickup":
			currentPickups.append(HealthPickup(random.randint(0,screenWidth), random.randint(0,screenHeight)))
		if pickupChoice == "MachineGunPickup":
			currentPickups.append(MachineGunPickup(random.randint(0,screenWidth), random.randint(0,screenHeight)))
		if pickupChoice == "SniperPickup":
			currentPickups.append(SniperPickup(random.randint(0,screenWidth), random.randint(0,screenHeight)))
		if pickupChoice == "LaserPickup":
			currentPickups.append(LaserPickup(random.randint(0,screenWidth), random.randint(0,screenHeight)))

	def handlePlayerMovement():
		#Handle 8 directional movement
		keys_pressed = pygame.key.get_pressed()
		movX = 0
		movY = 0
		if keys_pressed[pygame.K_w]:
			movY = -1
		elif keys_pressed[pygame.K_s]:
			movY = 1
		else:
			movY = 0
		if keys_pressed[pygame.K_d]:
			movX = 1
		elif keys_pressed[pygame.K_a]:
			movX = -1
		else:
			movX = 0
		player.setMov(movX, movY)
		player.updatePos()

	def handleBulletMovement():
		#Handle bullet movement
		for bullet in bullets:
			bullet.updatePos()
			if bullet.posY < 0 or bullet.posY > screenHeight or bullet.posX < 0 or bullet.posX > screenWidth:
				bullets.remove(bullet)

	def handleEnemyColision():
		#Handle enemy colision
		for enemy in enemies:
			#Check if hit by bullet
			if isTouching(enemy, player):
				#Player is hit by enemy
				player.addLives(-1)
				enemies.remove(enemy)
			else:
				for bullet in bullets:
					if isTouching(bullet, enemy):
						#Enemy is killed
						enemies.remove(enemy)
						player.addMoney(1)
						#If the bullet isn't piercing, delete it
						if bullet.piercing == False:
							bullets.remove(bullet)
						#Now decide whether a pickup drops or not
						pickupChance = random.randint(0,100)
						if pickupChance < player.luck:
							spawnPickup()

	def handlePickupColision():
		#Handle pickup colision
		for pickup in currentPickups:
			if isTouching(pickup, player):
				#Call the specific pickup's collected function
				pickup.collected(player)
				currentPickups.remove(pickup)

	def handleBulletSpawning():
		#Handle bullet spawning
		if (pygame.mouse.get_pressed()[0]) == 1  and player.timeSinceLastShot > (1000 / player.shotsPerSec):
			mouseX, mouseY = pygame.mouse.get_pos()
			#Get Y distance to draw 1 line of triangle
			diffY = player.posY - mouseY
			#Get X distance
			diffX = player.posX - mouseX
			bullet_move_x = math.cos(math.atan2(diffY, diffX))
			bullet_move_y = math.sin(math.atan2(diffY, diffX))
			degree = math.degrees(math.atan2(diffY, diffX))
			bullets.append(player.getBulletObject(-bullet_move_x, -bullet_move_y, degree))
			player.timeSinceLastShot = 0

	def handleEnemies():
		#Handle enemy spawning
		if len(enemies) < 3:
			#Spawn enemy along top of screen with random X
			enemies.append(Enemy(random.randint(0,screenWidth), 0))

		#Handle enemy movement
		for enemy in enemies:
			#Get Y distance to draw 1 line of triangle
			diffY = enemy.posY - player.posY
			#Get X distance
			diffX = enemy.posX - player.posX
			enemy_move_x = math.cos(math.atan2(diffY, diffX))
			enemy_move_y = math.sin(math.atan2(diffY, diffX))
			enemy.movX = -enemy_move_x
			enemy.movY = -enemy_move_y
			enemy.updatePos()	

	def clickedShop():
		if player.inShop == True:
			exitShop()
		elif player.inShop == False:
			print("Clicked shop")
			shopWindow.show = True
			player.inShop = True
	def exitShop():
		player.inShop = False
		shopWindow.show = False
		print("Exit shop")
	def handleButtons():
		#Check if mouse is over button
		for button in buttons:
			button.timeSinceLastClick += dt
			if isMouseOver(pygame.mouse.get_pos(), button):
				button.currentColour = button.hoveredColour
				#Now check if the player clicked the mouse:
				if (pygame.mouse.get_pressed()[0]) == 1 and button.buttonCooldown < button.timeSinceLastClick:
					button.timeSinceLastClick = 0
					if button.text == "Shop":
						clickedShop()
			else:
				button.currentColour = button.normalColour
	###Main Loop
	running = True
	while running:
		print(shopWindow.show)
		clock = pygame.time.Clock()
		dt = clock.tick(144)
		player.timeSinceLastShot += dt
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		if player.inShop:
			handleButtons()
		
		#If not, make the game play normally
		else:
			handlePlayerMovement()
			handleBulletMovement()
			handleEnemyColision()
			handlePickupColision()
			handleBulletSpawning()
			handleEnemies()
			handleButtons()


		redrawGameWindow()



if __name__ == "__main__":
	pygame.init()
	pygame.font.init()
	main()