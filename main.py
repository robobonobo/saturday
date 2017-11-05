import pygame, random
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
		self.exit = 999

class Screen:
	def __init__(self,id,music_track,map,start_location_1,start_location_2,start_location_3,start_location_4,objects,npcs,startup_event=0):
		self.id = id
		#self.music_track = app.music_index[music_track]
		self.music_track = music_track
		self.map = map
		self.start_location_1 = start_location_1
		self.start_location_2 = start_location_2
		self.start_location_3 = start_location_3
		self.start_location_4 = start_location_4
		self.startup_event = startup_event
		self.objects = objects
		self.npcs = npcs
		self.projectiles = []

class App:
	def __init__(self):
		self.monster_screens = [000,001]
		self.sprite_index = []
		self.font_index = []
		self.tile_index = []
		self.screen_index = []
		self.music_index = []
		self.object_index = []
		self.npc_index = []
		self.item_index = []
		self.animate = []
		self.running = 1
		self.current_screen = 0
		self.previous_screen = 999
		self.screen_dirty = 1
		self.mode = 'game'
		self.message_box = pygame.Surface((800,200))
		self.cursor_pos = (0,0)
		self.event_flags = {"r1_object":1}

class Player:
	def __init__(self):
		self.x = 0
		self.y = 0
		#self.sprites = [3]
		self.sprites = [3]
		self.animation_counter = 0
		self.movement_sprites = [3,3]
		self.up_sprites = [12,13,14,12]
		self.down_sprites = [3,4,5,3]
		self.left_sprites = [6,7,8,6]
		self.right_sprites = [9,10,11,9]
		self.facing = "down"
		self.blocks = True

	def draw(self):
		#print self.animation_counter
		screen.blit(app.sprite_index[self.sprites[self.animation_counter]],(self.x*20,self.y*20))
		app.screen_dirty = True

	def move(self,dx,dy):
		in_bounds = 0
		screen.blit(app.sprite_index[app.screen_index[app.current_screen].map[self.x][self.y].sprite],(self.x*20,self.y*20))
		if dx != 0:
			if dx > 0:
			#set facing
				self.facing = "right"
				self.sprites = self.right_sprites
				self.draw()
				if self.x < 40 and app.screen_index[app.current_screen].map[self.x + dx][self.y].blocks == False:
					in_bounds = 1
			elif dx < 0:
			#set facing
				self.facing = "left"
				self.sprites = self.left_sprites
				self.draw()
				if self.x > 0 and app.screen_index[app.current_screen].map[self.x + dx][self.y].blocks == False:
					in_bounds = 1
		elif dy != 0:
			if dy > 0:
				#set facing
				self.facing = "down"
				self.sprites = self.down_sprites
				self.draw()
				if self.y < 30 and app.screen_index[app.current_screen].map[self.x][self.y + dy].blocks == False:
					in_bounds = 1
			elif dy < 0:
				#set facing
				self.facing = "up"
				self.sprites = self.up_sprites
				self.draw()
				if self.y > 0 and app.screen_index[app.current_screen].map[self.x][self.y + dy].blocks == False:
					in_bounds = 1
		for object in app.screen_index[app.current_screen].objects:
			if object.x == self.x + dx and object.y == self.y + dy and object.blocks == True:
				in_bounds = 0
		for npc in app.screen_index[app.current_screen].npcs:
			if npc.x == self.x + dx and npc.y == self.y + dy and npc.blocks == True:
				in_bounds = 0
		if in_bounds == 1:
			self.x = self.x + dx
			self.y = self.y + dy
			self.animation_counter = 0
			#self.sprites = self.movement_sprites
			app.animate.append(self)
			if app.screen_index[app.current_screen].map[self.x][self.y].event != 0:
				event_parser(app.screen_index[app.current_screen].map[self.x][self.y].event)
			if app.screen_index[app.current_screen].map[self.x][self.y].exit != 999:
				app.previous_screen = app.current_screen
				new_screen_number = app.screen_index[app.current_screen].map[self.x][self.y].exit
				app.current_screen = new_screen_number
				load_current_screen()
						
	def shoot(self):
		origin_x = self.x
		origin_y = self.y
		if self.facing == "up":
			origin_y = origin_y -1
		elif self.facing == "down":
			origin_y = origin_y + 1
		elif self.facing == "left":
			origin_x = origin_x - 1
		elif self.facing == "right":
			origin_x = origin_x + 1
		new_projectile = Projectile("orb",[17,17],origin_x,origin_y,self.facing,1,5,1,"none")
		app.screen_index[app.current_screen].projectiles.append(new_projectile)
		new_projectile.draw()
		app.animate.append(new_projectile)
		app.screen_dirty = True

class NPC:

	def __init__(self,id,ai,hostile,origin,movement_sprites,action_sprites = [],death_sprites = []):
		self.id = id
		self.ai = ai
		self.x = 0
		self.y = 0
		self.visible = True
		self.alive = True
		self.blocks = True
		self.facing = "down"
		self.animation_counter = 0
		self.hostile = hostile
		self.origin_x = origin[0]
		self.origin_y = origin[1]
		self.movement_sprites = movement_sprites
		self.action_sprites = action_sprites
		self.death_sprites = death_sprites
		self.sprites = movement_sprites
		self.move_cooldown = 0
		self.action_cooldown = 0

	def draw(self):
		screen.blit(app.sprite_index[self.sprites[self.animation_counter]],(self.x*20,self.y*20))
		app.screen_dirty = True
		
	def move(self,dx,dy):
		in_bounds = 0
		screen.blit(app.sprite_index[app.screen_index[app.current_screen].map[self.x][self.y].sprite],(self.x*20,self.y*20))
		if dx != 0:
			if dx > 0:
			#set facing
				self.facing = "right"
				#self.sprites = self.right_sprites
				self.draw()
				if self.x < 40 and app.screen_index[app.current_screen].map[self.x + dx][self.y].blocks == False:
					in_bounds = 1
			elif dx < 0:
			#set facing
				self.facing = "left"
				#self.sprites = self.left_sprites
				self.draw()
				if self.x > 0 and app.screen_index[app.current_screen].map[self.x + dx][self.y].blocks == False:
					in_bounds = 1
		elif dy != 0:
			if dy > 0:
				#set facing
				self.facing = "down"
				#self.sprites = self.movement_sprites[0]
				self.draw()
				if self.y < 30 and app.screen_index[app.current_screen].map[self.x][self.y + dy].blocks == False:
					in_bounds = 1
			elif dy < 0:
				#set facing
				self.facing = "up"
				#self.sprites = self.up_sprites
				self.draw()
				if self.y > 0 and app.screen_index[app.current_screen].map[self.x][self.y + dy].blocks == False:
					in_bounds = 1
		for object in app.screen_index[app.current_screen].objects:
			if object.x == self.x + dx and object.y == self.y + dy and object.blocks == True:
				in_bounds = 0
		for npc in app.screen_index[app.current_screen].npcs:
			if npc.x == self.x + dx and npc.y == self.y + dy and npc.blocks == True:
				in_bounds = 0
		if in_bounds == 1:
			self.x = self.x + dx
			self.y = self.y + dy
			self.animation_counter = 0
			#self.sprites = self.movement_sprites
			app.animate.append(self)
			
	def take_turn(self):
		if self.ai == 1:
			if self.move_cooldown == 0:
				direction = random.randint(1,4)
				if direction == 1:
					self.move(0,-1)
				elif direction == 2:
					self.move(0,1)
				elif direction == 3:
					self.move(-1,0)
				else:
					self.move(1,0)
				self.move_cooldown = 5
			else:
				self.move_cooldown = self.move_cooldown - 1
			
		
		
class Object:

	def __init__(self,id,origin,sprites,blocks,interact_code):
		self.x = 0
		self.y = 0
		self.animation_counter = 0
		self.toggle_state = 0
		self.id = id
		self.visible = True
		self.origin_x = origin[0]
		self.origin_y = origin[1]
		if len(sprites) > 1:
			self.animated = True
		else:
			self.animated = False
		self.sprites = sprites
		self.blocks = blocks
		self.interact_code = interact_code

	def draw(self):
		screen.blit(app.sprite_index[self.sprites[self.animation_counter]],(self.x*20,self.y*20))
		app.screen_dirty = True

	def interact(self):
		if self.interact_code == 000:
			pass
		elif self.interact_code == 001:
			message("Hello!")
			if app.event_flags["r1_object"] == 1:
				app.event_flags["r1_object"] = 0
				app.screen_index[app.current_screen].objects.remove(self)
				screen.blit(app.sprite_index[1],(self.x*20,self.y*20))
				app.screen_dirty = True

class Projectile():

	def __init__(self,name,sprites,origin_x,origin_y,direction,speed,range,damage,effect):
		self.name = name
		self.sprites = sprites
		self.damage = damage
		self.effect = effect
		self.origin_x = origin_x
		self.origin_y = origin_y
		self.x = origin_x
		self.y = origin_y
		self.direction = direction
		self.speed = speed
		self.range = range
		self.damage = damage
		self.effect = effect
		self.animation_counter = 0
		self.distance_traveled = 0
		
	def draw(self):
		screen.blit(app.sprite_index[self.sprites[self.animation_counter]],(self.x*20,self.y*20))
		app.screen_dirty = True
		
	def take_turn(self):
		if self.distance_traveled > self.range:
			app.screen_index[app.current_screen].projectiles.remove(self)
			app.screen_dirty = True
		else:
			speed_counter = 0
			while speed_counter < self.speed:
				in_bounds = 0
				if self.direction == "up":
					if self.y - 1 > 0 and app.screen_index[app.current_screen].map[self.x][self.y-1].blocks == False:
						#check for npc or player colision, run self.on_hit()
						in_bounds = 1
						self.y = self.y-1
				elif self.direction == "down":
					if self.y + 1 < 30 and app.screen_index[app.current_screen].map[self.x][self.y+1].blocks == False:
						in_bounds = 1
						self.y = self.y+1
				elif self.direction == "left":
					if self.x - 1 > 0 and app.screen_index[app.current_screen].map[self.x-1][self.y].blocks == False:
						in_bounds = 1
						self.x = self.x-1
				elif self.direction == "right":
					if self.x + 1 < 40 and app.screen_index[app.current_screen].map[self.x+1][self.y].blocks == False:
						in_bounds = 1
						self.x = self.x+1
				if in_bounds == 1:
					self.distance_traveled = self.distance_traveled + 1
					speed_counter = speed_counter + 1
				else:
					if self in app.screen_index[app.current_screen].projectiles:
						app.screen_index[app.current_screen].projectiles.remove(self)
					speed_counter = self.speed
			app.screen_dirty = True

def create_sprites():
	#make this better - load from a spritesheet. For now, I'll just load the images individually.
	# black = pygame.image.load("images/black.png").convert()
	# white = pygame.image.load("images/white.png").convert()
	# red = pygame.image.load("images/red.png").convert()
	# enemy = pygame.image.load("images/enemy.png")
	# object = pygame.image.load("images/object.png")
	# d1 = pygame.image.load("images/down1.png")
	# d2 = pygame.image.load("images/down2.png")
	# d3 = pygame.image.load("images/down3.png")
	# u1 = pygame.image.load("images/up1.png")
	# u2 = pygame.image.load("images/up2.png")
	# u3 = pygame.image.load("images/up3.png")
	# l1 = pygame.image.load("images/left1.png")
	# l2 = pygame.image.load("images/left2.png")
	# l3 = pygame.image.load("images/left3.png")
	# r1 = pygame.image.load("images/right1.png")
	# r2 = pygame.image.load("images/right2.png")
	# r3 = pygame.image.load("images/right3.png")
	# app.sprite_index.append(black)
	# app.sprite_index.append(white)
	# app.sprite_index.append(red)
	# app.sprite_index.append(enemy)
	# app.sprite_index.append(object)
	# app.sprite_index.append(d1)
	# app.sprite_index.append(d2)
	# app.sprite_index.append(d3)
	# app.sprite_index.append(u1)
	# app.sprite_index.append(u2)
	# app.sprite_index.append(u3)
	# app.sprite_index.append(l1)
	# app.sprite_index.append(l2)
	# app.sprite_index.append(l3)
	# app.sprite_index.append(r1)
	# app.sprite_index.append(r2)
	# app.sprite_index.append(r3)
	spritesheet = pygame.image.load("images/spritesheet.png")
	counter_x = 0
	#counter_y = 0
	while counter_x < 40:
		new_image = pygame.Surface((20,20)).convert_alpha()
		new_image.fill((0,0,0,0))
		new_image.blit(spritesheet,(0,0),(counter_x*20,0,20,20))
		app.sprite_index.append(new_image)
		counter_x = counter_x+1
	
	

def create_font():
	font_tileset = pygame.image.load("images/16x16.png").convert()
	for y in range(16):
		for x in range(16):
			new_entry = pygame.Surface((16,16))
			new_entry.blit(font_tileset,(0,0),(x*16,y*16,16,16))
			app.font_index.append(new_entry)

def create_npcs():
	new_npc = NPC(000,1,True,(0,0),[3])
	app.npc_index.append(new_npc)

def create_objects():
	new_object = Object(000,(0,0),[4],True,001)
	app.object_index.append(new_object)

def create_screens():
	#this function will eventually create multiple screens after loading multiple files. For now, it will just load hardcoded files.
	load_files = ["newmap.map","second_screen.map"]
	for entry in load_files:
		file = open(entry,"r")
		id = int(file.read(3))
		music_track = int(file.read(3))
		start_location_1 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		start_location_2 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		start_location_3 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		start_location_4 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
		startup_event = int(file.read(3))
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
		#set event data
		for counter_y in range(30):
			for counter_x in range(40):
				map[counter_x][counter_y].event = int(file.read(3))
		for counter_y in range(30): #set exit data
			for counter_x in range(40):
				map[counter_x][counter_y].exit = int(file.read(3))
		objects = [] #create objects
		for counter_y in range(30):
			for counter_x in range(40):
				object_id = int(file.read(3))
				if object_id != 999:
					for object in app.object_index:
						if object.id == object_id:
							new_object = Object(object_id,(counter_x,counter_y),object.sprites,object.blocks,object.interact_code)
							new_object.x = counter_x
							new_object.y = counter_y
							objects.append(new_object)
					#spawn new object, set values to index, append to object list
		npcs = [] # create npcs
		for counter_y in range(30):
			for counter_x in range(40):
				npc_id = int(file.read(3))
				if npc_id != 999:
					for entry in app.npc_index:
						if entry.id == npc_id:
							new_npc = NPC(npc_id,1,entry.hostile,(counter_x,counter_y),entry.movement_sprites,entry.action_sprites,entry.death_sprites)
							new_npc.x = counter_x
							new_npc.y = counter_y
							npcs.append(new_npc)
		new_screen = Screen(id,music_track,map,start_location_1,start_location_2,start_location_3,start_location_4,objects,npcs,startup_event)
		app.screen_index.append(new_screen)
		file.close()

def create_tiles():
	solid_black = Tile(000,000,True)
	app.tile_index.append(solid_black)
	blank_white = Tile(001,001,False)
	app.tile_index.append(blank_white)
	solid_red = Tile(002,002,True)
	app.tile_index.append(solid_red)


def draw():
	if app.mode == "game" or app.mode == "message" or app.mode == "option_box":
		for x in range(40):
			for y in range(30):
				screen.blit(app.sprite_index[app.screen_index[app.current_screen].map[x][y].sprite],(x*20,y*20))
		for entry in app.screen_index[app.current_screen].objects:
			entry.draw()
		for npc in app.screen_index[app.current_screen].npcs:
			npc.draw()
		for projectile in app.screen_index[app.current_screen].projectiles:
			projectile.draw()
		if app.mode == 'message':
			screen.blit(app.message_box,(0,400))
		elif app.mode == "option_box":
			app.message_box.blit(app.font_index[16],(app.cursor_pos[0]*16,app.cursor_pos[1]*16))
			screen.blit(app.message_box,(0,400))
	# elif app.mode == "battle":
		# draw hud
		# draw values menu, hp, etc)
		
		# screen.blit(app.battle_screen,(0,0))
		# battle.dirty = 0
		
	pygame.display.flip()
	app.screen_dirty = 0

def event_parser(event):
	if event == 001: #test room startup event.
		new_npc_sprites = [7]
		new_npc = NPC(1,1,True,new_npc_sprites)
		new_npc.x = 1
		new_npc.y = 1
		new_object = Object(1,[8],True,1)
		new_object.x = 3
		new_object.y = 1
		app.screen_index[app.current_screen].objects.append(new_npc)
		app.screen_index[app.current_screen].objects.append(new_object)
	elif event == 101:
		result = option_box("Select an option","Yes","No")
		print result


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
					option_box("What do you think?","Yes","No")
				elif event.key == K_RETURN:
					x_coord = player.x
					y_coord = player.y
					if player.facing == "up":
						y_coord = y_coord - 1
					elif player.facing == "down":
						y_coord = y_coord + 1
					elif player.facing == "left":
						x_coord = x_coord - 1
					elif player.facing == "right":
						x_coord = x_coord + 1
					for object in app.screen_index[app.current_screen].objects:
						if object.x == x_coord and object.y == y_coord and object.interact_code != 000:
							object.interact()
				elif event.key == K_j:
					player.shoot()
		elif app.mode == 'message':
			if event.type == KEYDOWN and event.key == K_RETURN:
				app.mode = 'game'
				app.screen_dirty = 1
		elif app.mode == 'option_box':
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				return "escape"
			elif event.type == KEYDOWN and event.key == K_RETURN:
				return "return"
			elif event.type == KEYDOWN and event.key == K_a:
				return "left"
			elif event.type == KEYDOWN and event.key == K_d:
				return "right"
			else:
				return "none"

def load_current_screen():
	global player
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
	if player not in app.screen_index[app.current_screen].objects:
		app.screen_index[app.current_screen].objects.append(player)
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
	app.cursor_pos = (14,y_cursor)
	for entry in translated_option1:
		app.message_box.blit(app.font_index[entry],(x_cursor*16,y_cursor*16))
		x_cursor = x_cursor + 1
	x_cursor = 27
	for entry in translated_option2:
		app.message_box.blit(app.font_index[entry],(x_cursor*16,y_cursor*16))
		x_cursor = x_cursor + 1
	app.screen_dirty = 1
	draw()
	running = True
	while running == True:
		input = "none"
		if app.screen_dirty == 1:
			draw()
		for event in pygame.event.get():
			input = handle_input(event)
		if input == "escape":
			running = False
			app.mode = "game"
			app.screen_dirty = 1
			return "cancel"
		elif input == "return":
			print app.cursor_pos
			running = False
			app.mode = "game"
			app.screen_dirty = 1
			if app.cursor_pos[0] == 14:
				return option1
			elif app.cursor_pos[0] == 26:
				return option2
		elif input == "left":
			if app.cursor_pos[0] == 26:
				app.message_box.blit(app.font_index[0],(26*16,y_cursor*16))
			#	app.message_box.blit(app.font_index[0],(x_cursor*16,y_cursor*16))
				app.cursor_pos = (14,y_cursor)
				app.screen_dirty = 1
		elif input == "right":
			if app.cursor_pos[0] == 14:
			#	app.message_box.blit(app.font_index[0],(x_cursor*16,y_cursor*16))
				app.message_box.blit(app.font_index[0],(14*16,y_cursor*16))
				app.cursor_pos = (26,y_cursor)
				app.screen_dirty = 1

app = App()
create_sprites()
create_font()
create_tiles()
create_objects()
create_npcs()
create_screens()
player = Player()
load_current_screen()
clock = pygame.time.Clock()
while app.running == 1:
	clock.tick(30)
	check_animation()
	if app.screen_dirty == 1:
		draw()
	for entry in app.screen_index[app.current_screen].projectiles:
		entry.take_turn()
	for event in pygame.event.get():
		handle_input(event)
	for entry in app.screen_index[app.current_screen].npcs:
		entry.take_turn()
