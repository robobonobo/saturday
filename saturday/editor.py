import pygame,sys,ConfigParser,shelve
from pygame.locals import *

class Tile:
	
	def __init__(self,name,x,y,index):
		self.name = name
		self.x = x
		self.y = y
		self.index = index
		self.event = "000"
		self.exit = "999"
		self.rect = pygame.Rect(x*20,y*20,20,20)
		
	def on_click(self):
		pass
		
class Unit:
	
	def __init__(self,name,index):
		self.name = name
		self.index = index
		self.x = 0
		self.y = 0		
		
class Map:

	def __init__(self,xsize,ysize): #x and y size are number of tiles, not pixels
		self.name = "map"
		self.xsize = xsize
		self.ysize = ysize
		self.surface = pygame.Surface((xsize*20,ysize*20))
		self.rect = pygame.Rect(10,80,xsize*20,ysize*20)
		x = 0
		y = 0
		self.s1 = ["000","00","00"]
		self.s2 = ["000","00","00"]
		self.s3 = ["000","00","00"]
		self.s4 = ["000","00","00"]
		self.id = "000"
		self.music = "000"
		self.on_load = "000"
		self.npcs = []
		self.objects = []
		self.tiles = [[ Tile("blank",x,y,0)
			for y in range(self.ysize) ]
				for x in range(self.xsize) ]
		self.dirty = True
		self.draw_tiles()
		main_page.children.append(self)
		
	def draw_tiles(self):
		for x in range(self.xsize):
			for y in range(self.ysize): 
				self.surface.blit(app.sprites[self.tiles[x][y].index],(x*20,y*20))
			
		for entry in self.objects:
			self.surface.blit(app.object_sprites[entry.index],(entry.x*20,entry.y*20))
		for entry in self.npcs:
			self.surface.blit(app.unit_sprites[entry.index],(entry.x*20,entry.y*20))
		self.dirty = True
		
	def draw(self):
		main_page.rect.blit(self.surface,(10,80))
	
	def on_click(self,coords):
		x,y = coords
		x = (x-10)/20
		y = (y-80)/20
		if app.current_selection[0] == "tile":
			self.tiles[x][y].name = app.current_selection[1].name
			self.tiles[x][y].index = app.current_selection[1].index
			print "set " + app.current_selection[1].name
			self.draw_tiles()
			app.dirty = True
		elif app.current_selection[0] == "unit":
			name = app.current_selection[1].name
			index = app.current_selection[1].index
			new_unit = Unit(name,index)
			new_unit.x = x
			new_unit.y = y
			self.npcs.append(new_unit)
			self.draw_tiles()
			app.dirty = True
			print "set " + app.current_selection[1].name
		elif app.current_selection[0] == "object":
			name = app.current_selection[1].name
			index = app.current_selection[1].index
			new_object = Unit(name,index)
			new_object.x = x
			new_object.y = y
			self.objects.append(new_object)
			self.draw_tiles()
			app.dirty = True
			print "set " + app.current_selection[1].name
		elif app.current_selection[0] == "event":
			self.tiles[x][y].event = app.current_selection[1]
			print "set " + app.current_selection[1]
		elif app.current_selection[0] == "exit":
			self.tiles[x][y].exit = app.current_selection[1]
			print "set " + app.current_selection[1]
		elif app.current_selection[0] == "s1":
			self.s1[0] = app.current_selection[1]
			self.s1[1] = str(x)
			self.s1[2] = str(y)
			print "set s1"
		elif app.current_selection[0] == "s2":
			self.s2[0] = app.current_selection[1]
			self.s2[1] = str(x)
			self.s2[2] = str(y)
			print "set s2"
		elif app.current_selection[0] == "s3":
			self.s3[0] = app.current_selection[1]
			self.s3[1] = str(x)
			self.s3[2] = str(y)
			print "set s3"
		elif app.current_selection[0] == "s4":
			self.s4[0] = app.current_selection[1]
			self.s4[1] = str(x)
			self.s4[2] = str(y)
			print "set s4"
				
class App:

	def __init__(self):
		self.running = True
		self.dirty = True
		self.current_screen = ''
		self.current_selection = ("tile",None)
		self.sprites = []
		self.unit_sprites = []
		self.object_sprites = []
		self.tileset = []
		self.units = []
		self.objects = []
		self.load_sprites()
		
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.running = False
			elif event.type == MOUSEBUTTONDOWN:
				left,mid,right = pygame.mouse.get_pressed()
				if left == True:
					for child in self.current_screen.children:
						if child.rect.collidepoint(pygame.mouse.get_pos()) == True:
							child.on_click(pygame.mouse.get_pos())
				elif right == True:
					for entry in self.map.objects:
						print entry.x,entry.y
					# if self.current_screen.name == "main_page":
						# for entry in self.current_screen.tiles:
							# if child.rect.collidepoint(pygame.mouse.get_pos()) == True:
								# print entry.name
				
	def load_sprites(self):
		spritesheet = pygame.image.load("images/spritesheet.png").convert_alpha()
		parser = ConfigParser.ConfigParser()
		parser.read("tiles.cfg")
		index = 0
		for entry in parser.sections():
			name = parser.get(entry,"name")
			x = parser.getint(entry,"spritex")
			y = parser.getint(entry,"spritey")
			new_image = pygame.Surface((20,20)).convert_alpha()
			new_image.fill((0,0,0,0))
			new_image.blit(spritesheet,(0,0),(x*20,y*20,20,20))
			self.sprites.append(new_image)
			solid = parser.getboolean(entry,"solid")
			new_tile = Tile(name,0,0,index)
			self.tileset.append(new_tile)
			index = index + 1
		self.current_selection = ("tile",self.tileset[1])
		del parser
		parser = ConfigParser.ConfigParser()
		parser.read("units.cfg")
		for entry in parser.sections():
			index = parser.getint(entry,"index")
			name = parser.get(entry,"name")
			coords = parser.get(entry,"sprites").split(",")
			x = int(coords[0])
			y = int(coords[1])
			new_image = pygame.Surface((20,20)).convert_alpha()
			new_image.fill((0,0,0,0))
			new_image.blit(spritesheet,(0,0),(x*20,y*20,20,20))
			new_image = new_image
			new_image.convert_alpha()
			self.unit_sprites.append(new_image)
			new_unit = Unit(name,index)
			self.units.append(new_unit)
		del parser
		parser = ConfigParser.ConfigParser()
		parser.read("objects.cfg")
		for entry in parser.sections():
			#using class Unit instead of creating Object class
			index = parser.getint(entry,"index")
			name = parser.get(entry,"name")
			coords = parser.get(entry,"sprites").split(",")
			x = int(coords[0])
			y = int(coords[1])
			new_image = pygame.Surface((20,20)).convert_alpha()
			new_image.fill((0,0,0,0))
			new_image.blit(spritesheet,(0,0),(x*20,y*20,20,20))
			new_image = new_image
			new_image.convert_alpha()
			self.object_sprites.append(new_image)
			new_object = Unit(name,index)
			self.objects.append(new_object)
	
	def update(self):
		self.current_screen.draw()
		self.dirty = False
		pygame.display.update()
		
	def run(self):
		while self.running == True:
			self.handle_events()
			if self.dirty == True:
				self.update()
				
class Button:
	
	def __init__(self,parent,name,text,function,x,y,w,h):
		self.parent = parent
		self.parent.children.append(self)
		self.surface = pygame.Surface((w,h))
		self.surface.fill((200,200,200))	
		pygame.draw.line(self.surface,(100,100,100),(0,0),(0,h))
		pygame.draw.line(self.surface,(100,100,100),(0,0),(w,0))
		pygame.draw.line(self.surface,(0,0,0),(0,h-1),(w-1,h-1))
		pygame.draw.line(self.surface,(0,0,0),(w-1,0),(w-1,h-1))
		self.name = name
		self.text = font.render(text,True,(0,0,0))
		self.surface.blit(self.text,((w/2)-self.text.get_width()/2,(h-15)/2))
		self.rect = pygame.Rect(x,y,w,h)
		self.function = function
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		
	def on_click(self,(x,y)):
		self.function()
		
	def draw(self):
		self.parent.rect.blit(self.surface,(self.x,self.y))
		
class Select_Button(Button):
	
	def __init__(self,parent,x,y,w,h,type,instance):
		self.parent = parent
		self.parent.children.append(self)
		self.x = x
		self.y = y 
		self.w = w
		self.h = h
		self.rect = pygame.Rect(x,y,w,h)
		self.type = type
		self.instance = instance		
		
	def on_click(self,hi):
		if self.type == "tile":
			app.current_selection = ("tile",self.instance)
		elif self.type == "unit":
			app.current_selection = ("unit",self.instance)
		elif self.type == "object":
			app.current_selection = ("object",self.instance)
		for entry in main_page.children:
			if entry.name == "current_selection":
				entry.surface.fill((200,200,200))
				entry.text = font.render(app.current_selection[1].name + " " + app.current_selection[0],True,(0,0,0))
				entry.surface.blit(entry.text,((entry.w/2)-entry.text.get_width()/2,(entry.h-15)/2))
	
	def draw(self):
		if self.type == "tile":
			self.parent.rect.blit(app.sprites[self.instance.index],(self.x,self.y))
		elif self.type == "unit":
			self.parent.rect.blit(app.unit_sprites[self.instance.index],(self.x,self.y))
		elif self.type == "object":
			self.parent.rect.blit(app.object_sprites[self.instance.index],(self.x,self.y))
		
class Screen:

	def __init__(self,name,color,x,y,w=900,h=700):
		self.name = name
		self.x = x
		self.y = y
		self.children = []
		self.rect = pygame.Surface((w,h))
		self.rect.fill(color)
		self.dirty = True
		
	def draw(self):
		for child in self.children:
			child.draw()
		screen.blit(self.rect,(0,0))
		self.dirty = False
	
	def set_current(self):
		app.current_screen = self
		app.dirty = True
	
def get_event_number():
	app.current_selection = ("event",raw_input("event > "))
	for entry in main_page.children:
			if entry.name == "current_selection":
				entry.surface.fill((200,200,200))
				entry.text = font.render("event " + app.current_selection[1],True,(0,0,0))
				entry.surface.blit(entry.text,((entry.w/2)-entry.text.get_width()/2,(entry.h-15)/2))
	app.dirty = True
	
def get_s1_number():
	app.current_selection = ("s1",raw_input("start 1 > "))
	for entry in main_page.children:
			if entry.name == "current_selection":
				entry.surface.fill((200,200,200))
				entry.text = font.render("start 1 " + app.current_selection[1],True,(0,0,0))
				entry.surface.blit(entry.text,((entry.w/2)-entry.text.get_width()/2,(entry.h-15)/2))
	app.dirty = True
	
def get_s2_number():
	app.current_selection = ("s2",raw_input("start 2 > "))
	for entry in main_page.children:
			if entry.name == "current_selection":
				entry.surface.fill((200,200,200))
				entry.text = font.render("start 2 " + app.current_selection[1],True,(0,0,0))
				entry.surface.blit(entry.text,((entry.w/2)-entry.text.get_width()/2,(entry.h-15)/2))
	app.dirty = True

def get_s3_number():
	app.current_selection = ("s3",raw_input("start 3 > "))
	for entry in main_page.children:
			if entry.name == "current_selection":
				entry.surface.fill((200,200,200))
				entry.text = font.render("start 3 " + app.current_selection[1],True,(0,0,0))
				entry.surface.blit(entry.text,((entry.w/2)-entry.text.get_width()/2,(entry.h-15)/2))
	app.dirty = True
	
def get_s4_number():
	app.current_selection = ("s1",raw_input("start 4 > "))
	for entry in main_page.children:
			if entry.name == "current_selection":
				entry.surface.fill((200,200,200))
				entry.text = font.render("start 4 " + app.current_selection[1],True,(0,0,0))
				entry.surface.blit(entry.text,((entry.w/2)-entry.text.get_width()/2,(entry.h-15)/2))
	app.dirty = True	
	
def get_exit_number():
	app.current_selection = ("exit",raw_input("exit > "))
	for entry in main_page.children:
			if entry.name == "current_selection":
				entry.surface.fill((200,200,200))
				entry.text = font.render("exit " + app.current_selection[1],True,(0,0,0))
				entry.surface.blit(entry.text,((entry.w/2)-entry.text.get_width()/2,(entry.h-15)/2))
	app.dirty = True
	
def get_header_info():
	app.map.id = raw_input("ID > ")
	app.map.music = raw_input("Music > ")
	app.map.on_load = raw_input("On_Load > ")
	
		
def populate_screeens():
	global main_page,terrain_palette,unit_palette,object_palette,event_palette
	main_page = Screen("main",(100,100,100),0,0)
	terrain_palette = Screen("main",(100,100,100),0,0)
	unit_palette = Screen("main",(100,100,100),0,0)
	object_palette = Screen("main",(100,100,100),0,0)
	populate_main_page()
	populate_terrain_palette()
	populate_unit_palette()
	populate_object_palette()
	
def populate_main_page():
	global main_page
	button_new_map = Button(main_page,"button_new_map","New",reset,10,10,50,50)
	button_save = Button(main_page,"button_save","Save",save_map,70,10,50,50)
	button_open = Button(main_page,"button_open","Load",load_map,140,10,50,50)
	button_open = Button(main_page,"get_header_info","Header",get_header_info,200,10,50,50)
	button_map_pallet = Button(main_page,"map_pallet","Terrain",terrain_palette.set_current,330,10,50,50)
	button_unit_pallet = Button(main_page,"unit_pallet","NPCs",unit_palette.set_current,390,10,50,50)
	button_unit_pallet = Button(main_page,"unit_pallet","Objects",object_palette.set_current,450,10,50,50)
	button_event_pallet = Button(main_page,"get_event_number","Events",get_event_number,510,10,50,50)
	button_event_pallet = Button(main_page,"get_s1_number","St1",get_s1_number,570,10,30,50)
	button_event_pallet = Button(main_page,"get_s2_number","St2",get_s2_number,605,10,30,50)
	button_event_pallet = Button(main_page,"get_s3_number","St3",get_s3_number,640,10,30,50)
	button_event_pallet = Button(main_page,"get_s4_number","St4",get_s4_number,675,10,30,50)
	button_event_pallet = Button(main_page,"get_exit_number","Exits",get_exit_number,710,10,50,50)
	button_selection = Button(main_page,"current_selection",app.current_selection[1].name + " " + app.current_selection[0],do_nothing,770,10,100,50)
	app.map = Map(40,30)

def populate_object_palette():
	global object_palette
	button_to_main_page = Button(object_palette,"back_to_main","Main",main_page.set_current,10,10,100,50)
	x = 10
	y = 100
	for entry in app.objects:
		new_button = Select_Button(object_palette,x,y,20,20,"object",entry)
		if x <= 780:
			x = x + 18
		else:
			x = 10
			y = y + 18
	
def reset():
	del app.map
	app.map = Map(40,30)
	app.dirty = True
	
def populate_terrain_palette():
	global terrain_palette
	button_to_main_page = Button(terrain_palette,"back_to_main","Main",main_page.set_current,10,10,100,50)
	x = 10
	y = 100
	for entry in app.tileset:
		new_button = Select_Button(terrain_palette,x,y,20,20,"tile",entry)
		if x <= 780:
			x = x + 18
		else:
			x = 10
			y = y + 18
		
def do_nothing():
	pass

def populate_unit_palette():
	global unit_palette
	button_to_main_page = Button(unit_palette,"back_to_main","Main",main_page.set_current,30,10,100,50)
	x = 10
	y = 100
	for entry in app.units:
		new_button = Select_Button(unit_palette,x,y,20,20,"unit",entry)
		if x <= 780:
			x = x + 18
		else:
			x = 10
			y = y + 18
	
def set_screen_main():
	app.current_screen = main_page
	app.dirty = True
	
def save_map():
	filename = raw_input("filename > ")
	write_string = ""
	write_string += "%0*d" % (3, int(app.map.id))
	write_string += "%0*d" % (3, int(app.map.music))
	write_string += "%0*d" % (3, int(app.map.s1[0]))
	write_string += "%0*d" % (2, int(app.map.s1[1]))
	write_string += "%0*d" % (2, int(app.map.s1[2]))
	write_string += "%0*d" % (3, int(app.map.s2[0]))
	write_string += "%0*d" % (2, int(app.map.s2[1]))
	write_string += "%0*d" % (2, int(app.map.s2[2]))
	write_string += "%0*d" % (3, int(app.map.s3[0]))
	write_string += "%0*d" % (2, int(app.map.s3[1]))
	write_string += "%0*d" % (2, int(app.map.s3[2]))
	write_string += "%0*d" % (3, int(app.map.s4[0]))
	write_string += "%0*d" % (2, int(app.map.s4[1]))
	write_string += "%0*d" % (2, int(app.map.s4[2]))
	write_string += "%0*d" % (3, int(app.map.on_load))
	print write_string
	#tiles
	for y in range(30):
		for x in range(40):
			write_string += "%0*d" % (3, int(app.map.tiles[x][y].index))
	#events
	for y in range(30):
		for x in range(40):
			write_string += "%0*d" % (3, int(app.map.tiles[x][y].event))
	#exits
	for y in range(30):
		for x in range(40):
			write_string += "%0*d" %  (3, int(app.map.tiles[x][y].exit))
	#objects
	for y in range(30):
		for x in range(40):
			addition = "999"
			for entry in app.map.objects:
				if entry.x == x and entry.y == y:
					addition = "%0*d" % (3, int(entry.index))
			write_string += addition
	#npcs
	for y in range(30):
		for x in range(40):
			addition = "999"
			for entry in app.map.npcs:
				if entry.x == x and entry.y == y:
					addition = "%0*d" % (3, int(entry.index))
			write_string += addition
	write_file = open(filename + ".map","w")
	write_file.write(write_string)
	write_file.close()
	print "Saved."
	
def load_map():
	filename = raw_input("filename > ")
	file = open(filename + ".map","r")
	app.map.id = int(file.read(3))
	app.map.music_track = int(file.read(3))
	app.map.s1 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
	app.map.s2 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
	app.map.s3 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
	app.map.s4 = [int(file.read(3)),int(file.read(2)),int(file.read(2))]
	app.map.on_load = int(file.read(3))
	for counter_y in range(30):
		for counter_x in range(40):
			tile_id = int(file.read(3))
			app.map.tiles[counter_x][counter_y].index = tile_id
	#set event data
	for counter_y in range(30):
		for counter_x in range(40):
			app.map.tiles[counter_x][counter_y].event = int(file.read(3))
	#set exit data
	for counter_y in range(30): 
		for counter_x in range(40):
			app.map.tiles[counter_x][counter_y].exit = int(file.read(3))
	#create objects
	for counter_y in range(30):
		for counter_x in range(40):
			object_id = int(file.read(3))
			if object_id != 999:
				for entry in app.objects:
					if object_id == entry.index:
						new_object = Unit(entry.name,entry.index)
						new_object.x = counter_x
						new_object.y = counter_y
						app.map.objects.append(new_object)
					#spawn new object, set values to index, append to object list
	# create npcs 
	for counter_y in range(30):
		for counter_x in range(40):
			npc_id = int(file.read(3))
			if npc_id != 999:
				for entry in app.units:
					if npc_id == entry.index:
						new_unit = Unit(entry.name,entry.index)
						new_unit.x = counter_x
						new_unit.y = counter_y
						app.map.npcs.append(new_unit)
	file.close()
	app.map.draw_tiles()
	app.dirty = True
	
pygame.init()
pygame.display.set_caption('Editor')
pygame.mouse.set_visible(1)
font = pygame.font.SysFont("Arial",10)
screen = pygame.display.set_mode((900,800))
app = App()
populate_screeens()
app.current_screen = main_page
app.run()