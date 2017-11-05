import pygame
from pygame.locals import *

icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800,600))
pygame.key.set_repeat(100,100)	

class Tile:
	def __init__(self,id,sprite,blocks):
		self.id = id
		self.sprite = sprite
		self.blocks = blocks
		self.visible = 1
		self.event = 0
		self.exit = "none"
		
class Screen:
	def __init__(self,id,music_track,map,start_location_1,start_location_2,start_location_3,start_location_4,startup_event=0):
		self.id = id
		#self.music_track = app.music_index[music_track]
		self.music_track = music_track
		self.map = map
		self.start_location_1 = start_location_1
		self.start_location_2 = start_location_2
		self.start_location_3 = start_location_3
		self.start_location_4 = start_location_4
		self.startup_event = startup_event
		self.objects = []
	
class App:
	def __init__(self):
		self.sprite_index = []
		self.font_index = []
		self.tile_index = []
		self.screen_index = []
		self.music_index = []
		self.object_index = []
		self.item_index = []
		self.animate = []
		self.running = 1
		self.current_screen = 0
		self.previous_screen = 999
		self.screen_dirty = 1
		self.mode = 'game'
		self.message_box = pygame.Surface((800,200))
		self.cursor_pos = (0,0)
		
class Player:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.sprites = [3]
		self.animation_counter = 0
		self.movement_sprites = [3,4,5,6,3]
		
	def draw(self):
		screen.blit(app.sprite_index[self.sprites[self.animation_counter]],(self.x*20,self.y*20))
		app.screen_dirty = True
		
	def move(self,dx,dy):
		in_bounds = 0
		if dx != 0:
			if dx > 0:
				if self.x < 40 and app.screen_index[app.current_screen].map[self.x + dx][self.y].blocks == False:
					in_bounds = 1
			elif dx < 0:
				if self.x > 0 and app.screen_index[app.current_screen].map[self.x + dx][self.y].blocks == False:
					in_bounds = 1
		elif dy != 0:
			if dy > 0:
				if self.y < 30 and app.screen_index[app.current_screen].map[self.x][self.y + dy].blocks == False:
					in_bounds = 1
			elif dy < 0:
				if self.y > 0 and app.screen_index[app.current_screen].map[self.x][self.y + dy].blocks == False:
					in_bounds = 1
		for object in app.screen_index[app.current_screen].objects:
			if object.x == self.x + dx and object.y == self.y + dy and object.blocks == True:
				in_bounds = 0
		if in_bounds == 1:
			screen.blit(app.sprite_index[app.screen_index[app.current_screen].map[self.x][self.y].sprite],(self.x*20,self.y*20))
			self.x = self.x + dx
			self.y = self.y + dy
			self.animation_counter = 0
			self.sprites = self.movement_sprites
			app.animate.append(self)
			if app.screen_index[app.current_screen].map[self.x][self.y].event != 0:
				event_parser(app.screen_index[app.current_screen].map[self.x][self.y].event)
			if app.screen_index[app.current_screen].map[self.x][self.y].exit != "none":
				app.previous_screen = app.current_screen
				new_screen_number = app.screen_index[app.current_screen].map[self.x][self.y].exit
				app.current_screen = new_screen_number
				load_current_screen()
		
class NPC:

	def __init__(self,hostile,movement_sprites,action_sprites = [],death_sprites = []):
		self.x = 0
		self.y = 0
		self.visible = True
		self.alive = True
		self.blocks = True
		self.animation_counter = 0
		self.hostile = hostile
		self.movement_sprites = movement_sprites
		self.action_sprites = action_sprites
		self.death_sprites = death_sprites
		self.sprites = movement_sprites
		
	def draw(self):
		screen.blit(app.sprite_index[self.sprites[self.animation_counter]],(self.x*20,self.y*20))
		app.screen_dirty = True
		
class Object:
	
	def __init__(self,id,sprites,blocks,interact_code):
		self.x = 0
		self.y = 0
		self.visible = True
		self.animation_counter = 0
		if len(sprites) > 1:
			self.animated = True
		else:
			self.animated = False
		self.sprites = sprites
		self.blocks = blocks
		self.ineract_code = interact_code
		
	def draw(self):
		screen.blit(app.sprite_index[self.sprites[self.animation_counter]],(self.x*20,self.y*20))
		app.screen_dirty = True
		

def create_sprites():
	#make this better - load from a spritesheet. For now, I'll just load the images individually.
	black = pygame.image.load("images/black.png").convert()
	white = pygame.image.load("images/white.png").convert()
	red = pygame.image.load("images/red.png").convert()
	first = pygame.image.load("images/first.png")
	second = pygame.image.load("images/second.png")
	third = pygame.image.load("images/third.png")
	fourth = pygame.image.load("images/fourth.png")
	enemy = pygame.image.load("images/enemy.png")
	object = pygame.image.load("images/object.png")
	app.sprite_index.append(black)
	app.sprite_index.append(white)
	app.sprite_index.append(red)
	app.sprite_index.append(first)
	app.sprite_index.append(second)
	app.sprite_index.append(third)
	app.sprite_index.append(fourth)
	app.sprite_index.append(enemy)
	app.sprite_index.append(object)
			
def create_tiles():
	solid_black = Tile(000,000,True)
	app.tile_index.append(solid_black)
	blank_white = Tile(001,001,False)
	app.tile_index.append(blank_white)
	solid_red = Tile(002,002,True)
	app.tile_index.append(solid_red)
	
def create_font():
	font_tileset = pygame.image.load("images/16x16.png").convert()
	for y in range(16):
		for x in range(16):
			new_entry = pygame.Surface((16,16))
			new_entry.blit(font_tileset,(0,0),(x*16,y*16,16,16))
			app.font_index.append(new_entry)

def create_screens():
	#this function will eventually create multiple screens after loading multiple files. For now, it will just load one file.
	load_files = ["newmap.map","second_screen.map"]
	for entry in load_files:
		file = open(entry,"r")
		id = int(file.read(3))
		music_track = int(file.read(3))
		start_location_1 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		start_location_2 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		start_location_3 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		start_location_4 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		exit_location_1 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		exit_location_2 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		exit_location_3 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		exit_location_4 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		event_1 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		event_2 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		event_3 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		event_4 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		event_5 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		event_6 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		#objects 1 - 10
		map = [[ Tile(000,000,True)
			for y in range(30) ]
				for x in range(40) ]
		for counter_y in range(30):
			for counter_x in range(40):
				tile_id = int(file.read(3))
				for tile in app.tile_index:
					if tile_id == tile.id:
						map[counter_x][counter_y].id = tile.id
						map[counter_x][counter_y].sprite = tile.sprite
						map[counter_x][counter_y].blocks = tile.blocks
						map[counter_x][counter_y].visible = tile.visible
						map[counter_x][counter_y].event = tile.event
						map[counter_x][counter_y].exit = tile.exit
		#event_1 is the only place to put startup_events. I don't like using less than 100 to designate startup events. Have to find another way.
		startup_event = 0
		if event_1[0] < 100:
			startup_event = event_1[0]
		else:
			map[event_1[1]][event_1[2]].event = event_1[0]
		map[event_2[1]][event_2[2]].event = event_2[0]
		map[event_3[1]][event_3[2]].event = event_3[0]
		map[event_4[1]][event_4[2]].event = event_4[0]
		map[event_5[1]][event_5[2]].event = event_5[0]
		map[event_6[1]][event_6[2]].event = event_6[0]
		map[exit_location_1[1]][exit_location_1[2]].exit = exit_location_1[0]
		map[exit_location_2[1]][exit_location_2[2]].exit = exit_location_2[0]
		map[exit_location_3[1]][exit_location_3[2]].exit = exit_location_3[0]
		map[exit_location_4[1]][exit_location_4[2]].exit = exit_location_4[0]
		new_screen = Screen(id,music_track,map,start_location_1,start_location_2,start_location_3,start_location_4,startup_event)
		app.screen_index.append(new_screen)
		file.close()

	
def draw():
	for x in range(40):
		for y in range(30):
			screen.blit(app.sprite_index[app.screen_index[app.current_screen].map[x][y].sprite],(x*20,y*20))
	for object in app.screen_index[app.current_screen].objects:
		object.draw()
	if app.mode == 'message' or app.mode == "option_box":
		screen.blit(app.message_box,(0,400))
	pygame.display.flip()
	app.screen_dirty = 0
	
def event_parser(event):
	if event == 001: #test room startup event.
		new_npc_sprites = [7]
		new_npc = NPC(True,new_npc_sprites)
		new_npc.x = 1
		new_npc.y = 1
		new_object = Object(1,[8],True,1)
		new_object.x = 3
		new_object.y = 1
		app.screen_index[app.current_screen].objects.append(new_npc)
		app.screen_index[app.current_screen].objects.append(new_object)
	elif event == 101:
		message("ughhghghghghghgh")


def handle_input(event):
	if event.type == QUIT:
		app.running = 0
	else:
		if app.mode == 'game':
			if event.type == KEYDOWN:
				if event.key == K_w:
					player.move(0,-1)
				elif event.key == K_s:
					player.move(0,1)
				elif event.key == K_a:
					player.move(-1,0)
				elif event.key == K_d:
					player.move(1,0)
				elif event.key == K_z:
					option_box("this is a test. lol.","Yes","No")
		elif app.mode == 'message':
			if event.type == KEYDOWN and event.key == K_RETURN:
				app.mode = 'game'
				app.screen_dirty = 1
		elif app.mode == 'option_box':
			if event.type == KEYDOWN and event.key == K_RETURN:
				app.mode = 'game'
				app.screen_dirty = 1
			# elif event.key == K_a:
				# if app.cursor_pos[0] == 26:
					# 14, 26
			# elif event.key == K_d:
		
def load_current_screen():
	global player
	app.screen_index[app.current_screen].objects = []
	app.screen_index[app.current_screen].objects.append(player)
	if app.previous_screen == app.screen_index[app.current_screen].start_location_1[0]:
		player.x = app.screen_index[app.current_screen].start_location_1[1]
		player.y = app.screen_index[app.current_screen].start_location_1[2]
	elif app.previous_screen == app.screen_index[app.current_screen].start_location_2[0]:
		player.x = app.screen_index[app.current_screen].start_location_2[1]
		player.y = app.screen_index[app.current_screen].start_location_2[2]
	elif app.previous_screen == app.screen_index[app.current_screen].start_location_3[0]:
		player.x = app.screen_index[app.current_screen].start_location_3[1]
		player.y = app.screen_index[app.current_screen].start_location_3[2]
	elif app.previous_screen == app.screen_index[app.current_screen].start_location_4[0]:
		player.x = app.screen_index[app.current_screen].start_location_4[1]
		player.y = app.screen_index[app.current_screen].start_location_4[2]
	if app.screen_index[app.current_screen].startup_event != 0:
		print "startup event detected ",str(app.screen_index[app.current_screen].startup_event)
		event_parser(app.screen_index[app.current_screen].startup_event)
	app.screen_dirty = 1
	
def check_animation():
	for entry in app.animate:
		if entry.animation_counter < len(entry.sprites)-1:
			entry.animation_counter = entry.animation_counter + 1
			entry.draw()
		else:
			entry.animation_counter = 0
			app.animate.remove(entry)

def message(string):
	translation = []
	for entry in string:
		translation.append(ord(entry))
	app.mode = "message"
	app.message_box.fill((0,0,0))
	app.message_box.blit(app.font_index[201],(0,0))
	app.message_box.blit(app.font_index[187],(784,0))
	app.message_box.blit(app.font_index[188],(784,184))
	app.message_box.blit(app.font_index[200],(0,184))
	x_cursor = 3
	y_cursor = 1
	for entry in translation:
		app.message_box.blit(app.font_index[entry],(x_cursor*16,y_cursor*16))
		if x_cursor < 44:
			x_cursor = x_cursor + 1
		else:
			x_cursor = 3
			y_cursor = y_cursor + 1 #need bounds checking on y. Also need to have a way of splitting up words across multiple lines using -
	app.screen_dirty = 1
	
def option_box(message,option1,option2):
	#assumes that option1 and option2 will be approximately 1 word each, so no line wrapping. Draws them at the same line on the bottom of the box
	translation = []
	translated_option1 = []
	translated_option2 = []
	for entry in message:
		translation.append(ord(entry))
	for entry in option1:
		translated_option1.append(ord(entry))
	for entry in option2:
		translated_option2.append(ord(entry))
	app.mode = "option_box"
	app.message_box.fill((0,0,0))
	app.message_box.blit(app.font_index[201],(0,0))
	app.message_box.blit(app.font_index[187],(784,0))
	app.message_box.blit(app.font_index[188],(784,184))
	app.message_box.blit(app.font_index[200],(0,184))
	x_cursor = 3
	y_cursor = 1
	for entry in translation:
		app.message_box.blit(app.font_index[entry],(x_cursor*16,y_cursor*16))
		if x_cursor < 44:
			x_cursor = x_cursor + 1
		else:
			x_cursor = 3
			y_cursor = y_cursor + 1 #need bounds checking on y. Also need to have a way of splitting up words across multiple lines using -
	y_cursor = y_cursor + 2
	x_cursor = 15
	app.message_box.blit(app.font_index[16],(14*16,y_cursor*16)) #draw the arrow
	app.cursor_pos = (x_cursor,y_cursor)
	for entry in translated_option1:
		app.message_box.blit(app.font_index[entry],(x_cursor*16,y_cursor*16))
		x_cursor = x_cursor + 1
	x_cursor = 27
	for entry in translated_option2:
		app.message_box.blit(app.font_index[entry],(x_cursor*16,y_cursor*16))
		x_cursor = x_cursor + 1
	app.screen_dirty = 1
	
			
app = App()
create_sprites()
create_font()
create_tiles()
create_screens()
player = Player()
load_current_screen()
clock = pygame.time.Clock()
while app.running == 1:
	clock.tick(60)
	check_animation()
	if app.screen_dirty == 1:
		draw()
	for event in pygame.event.get():
		handle_input(event)