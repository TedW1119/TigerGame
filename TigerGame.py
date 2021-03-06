import pygame
import sys
import random

pygame.init()

width = 995
height = 774
road = 570

tiger_pos = 0
gravity = 0.30

background = pygame.image.load("assets/background.jpg")
background_x_pos = 0

line = pygame.image.load("assets/dash_line.png")
line_x_pos = 0
line_rect = line.get_rect(center = (line_x_pos, 700))

tiger = pygame.image.load("assets/tiger.png")
tiger_rect = tiger.get_rect(center = (50, road))

rabbit = pygame.image.load("assets/rabbits.png")
rabbit_surface = pygame.transform.rotozoom(rabbit, 0, 0.5) 
rabbit_rect = rabbit_surface.get_rect(center = (900, 570))
spawn_list = [[rabbit_rect.centerx, rabbit_rect.centery]]

SPAWNRABBIT = pygame.USEREVENT
pygame.time.set_timer(SPAWNRABBIT, 1400)

score = 0
myFont = pygame.font.SysFont("monospace", 35)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

still_running = True

jumping = False

def draw_background():
	screen.blit(background, (background_x_pos, 0))
	screen.blit(background, (background_x_pos + 995, 0))

def draw_line():
	screen.blit(line, (line_x_pos, 565))
	screen.blit(line, (line_x_pos + 995, 565))

def tiger_running():
	if tiger_rect.colliderect(line_rect):
		return False
	else:
		return True

def drop_rabbit(spawn_list):
	random_num = random.randint(1, 11)
	if random_num < 6:
		spawn_list.append([rabbit_rect.centerx, rabbit_rect.centery])

def draw_rabbit(spawn_list):
	for rabbit in spawn_list:
		screen.blit(rabbit_surface, (rabbit[0], rabbit[1]))

def move_rabbit(spawn_list, score):
	for idx, rabbit in enumerate(spawn_list):
		if rabbit[0] <= 900 and rabbit[0] > -150:
			rabbit[0] -= 5
		else:
			spawn_list.pop(idx)
			score += 1
	return score

def check_collision(spawn_list):
	for rabbit in spawn_list:
		p_x = tiger_rect.centerx
		p_y = tiger_rect.centery

		e_x = rabbit[0]
		e_y = rabbit[1]

		if p_x >= e_x and p_x < (e_x + 180):
			if p_y >= e_y and p_y < (e_y + 70):
				return False
	return True

while still_running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and not tiger_running():
				if not jumping:
					jumping = True
					tiger_pos = 0
					tiger_pos -= 10
					tiger_rect.centery += tiger_pos

		if event.type == SPAWNRABBIT:
			drop_rabbit(spawn_list)

	# displaying background
	background_x_pos -= 5
	draw_background()
	if background_x_pos <= -995:
		background_x_pos = 0
	line_x_pos -= 5
	draw_line()
	if line_x_pos <= -995:
		line_x_pos = 0

	# movement of the tiger
	if not tiger_running():
		jumping = False
	
	if tiger_rect.centery < road:
		tiger_pos += gravity
		tiger_rect.centery += tiger_pos

	score = move_rabbit(spawn_list, score)

	# displaying the score board
	text = "Score: " + str(score)
	label = myFont.render(text, 1, YELLOW)
	screen.blit(label, (width - 200, height - 40))

	draw_rabbit(spawn_list)
	still_running = check_collision(spawn_list)

	screen.blit(tiger, tiger_rect)

	clock.tick(60)

	pygame.display.update()