import pygame
import random

pygame.init()

clock = pygame.time.Clock()
FPS_LIMIT = 60

#Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#UI
UI_PANEL_HEIGHT = 150

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Juego')

#img loaders
#background
	#TO DO: Add Parallax animation?
background = pygame.image.load('assets/background.png').convert_alpha()
UI_panel_img = pygame.image.load('assets/ui_panel.png').convert_alpha()
cursor_atk = pygame.image.load('assets/Ico/atk.png').convert_alpha()
icono_pocion = pygame.image.load('assets/Ico/potion.png').convert_alpha()

#def fonts
fuente = pygame.font.SysFont('Book Antiqua', 20)

#def colors
rojo = (234, 24, 38)
verde = (38, 234, 24)
detalle = (203, 254, 254) #(95, 134, 168)



#draw functions

def draw_background():
	screen.blit(background, (0,0))

def draw_ui_panel():
	# Base del panel
	screen.blit((UI_panel_img), (0, (SCREEN_HEIGHT - UI_PANEL_HEIGHT)))

	#mostrar stats Player
	draw_text(f'{player.nombre} | Salud: {player.salud}', fuente, rojo, 100, (SCREEN_HEIGHT - UI_PANEL_HEIGHT + 10))

	#mostrar stats enemigos
	for count, i in enumerate(lista_enemigos):
		#mostrar nombres
		draw_text(f'{i.nombre} | Salud: {i.salud}', fuente, rojo, 550, (SCREEN_HEIGHT - UI_PANEL_HEIGHT + 10 + count * 60))

def draw_text(texto, fuente, color_txt, x_pos_txt, y_pos_txt):
	img = fuente.render(texto, True, color_txt)
	screen.blit(img, (x_pos_txt, y_pos_txt))

#Classes

class Personaje():
	def __init__(self, x, y, nombre, salud_max, danio, pociones):
		self.nombre = nombre
		self.salud_max = salud_max
		self.salud = salud_max
		self.danio = danio
		self.pociones_restantes = pociones
		self.pociones = pociones
		self.sigue_vivo = True
		self.animation_list = []
		self.frame_index = 0
		self.accion_actual = 0 # 0: idle / 1: atacar / 2: recibe daño / 3: muerte
		self.update_time = pygame.time.get_ticks()
		
		# cargar imágenes IDLE
		temp_list = []
		for i in range(10):
			img = pygame.image.load(f'assets/{self.nombre}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height() * 3.5))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		# cargar imágenes ATK
		temp_list = []
		for i in range(6):
			img = pygame.image.load(f'assets/{self.nombre}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height() * 3.5))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		# cargar imágenes HIT
		temp_list = []
		for i in range(1):
			img = pygame.image.load(f'assets/{self.nombre}/Hit/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height() * 3.5))
			temp_list.append(img)
		self.animation_list.append(temp_list)

		# cargar imágenes DEATH
		temp_list = []
		for i in range(10):
			img = pygame.image.load(f'assets/{self.nombre}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height() * 3.5))
			temp_list.append(img)
		self.animation_list.append(temp_list)



		self.image = self.animation_list[self.accion_actual][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		animation_cooldown = 120
		#handle update image / animation
		self.image = self.animation_list[self.accion_actual][self.frame_index]

		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1

		# si no quedan frames para animar, volvemos a estado Idle
		if self.frame_index >= len(self.animation_list[self.accion_actual]):
			self.idle()

	def idle(self):
		#resetea la animación a estado idle
		self.accion_actual = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def atacar(self, objetivo):
		#Hacer daño al enemigo
		abs_modif_danio = (self.danio // 2) # modificador de daño
		modif_danio_azar = random.randint(-abs_modif_danio, abs_modif_danio)
		danio_causado = self.danio + modif_danio_azar
		objetivo.salud -= danio_causado

		# Comprobamos si el objetivo muere
		if objetivo.salud <1:
			objetivo.salud = 0
			objetivo.sigue_vivo = False

		#cambiar animacion actual a ataque
		self.accion_actual = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def draw(self):
		screen.blit(self.image, self.rect)

class BarraSalud():
	def __init__(self, x, y, ps, ps_max):
		self.x = x
		self.y = y
		self.ps = ps
		self.ps_max = ps_max

	def draw(self, ps):
		# actualizar salud
		self.ps = ps
		pygame.draw.rect(screen, rojo, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, verde, (self.x, self.y, (150 * (self.ps / self.ps_max)), 20))


#button class
class Button():
	def __init__(self, surface, x, y, image, size_x, size_y):
		self.image = pygame.transform.scale(image, (size_x, size_y))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

# Object Creation

player = Personaje(180, 240, 'Player', 30, 10, 3)
bandido_1 = Personaje(490, 310, 'Bandido', 20, 5, 1)
bandido_2 = Personaje(640, 310, 'Bandido', 20, 5, 1)


lista_enemigos = []
lista_enemigos.append(bandido_1)
lista_enemigos.append(bandido_2)

# Creamos barra de salud del PJ
player_barra_salud = BarraSalud(100, SCREEN_HEIGHT - UI_PANEL_HEIGHT + 40, player.salud, player.salud_max)

# Creamos barras de salud para los enemigos
bandido_1_barra_salud = BarraSalud(550, SCREEN_HEIGHT - UI_PANEL_HEIGHT + 40, bandido_1.salud, bandido_1.salud_max)
bandido_2_barra_salud = BarraSalud(550, SCREEN_HEIGHT - UI_PANEL_HEIGHT + 100, bandido_2.salud, bandido_2.salud_max)

# Creamos botones
boton_usar_pocion = Button(screen, 100, SCREEN_HEIGHT - UI_PANEL_HEIGHT + 70, icono_pocion, 64, 64)

# Variables de juego
personaje_actual = 1
personajes_en_total = 3
pausa_entre_acciones = 100
contador_entre_acciones = 0
curacion_pociones_base = 15
pj_atacar = False
pj_usar_pocion = False
clicked = False

#Game Loop
game_running = True
while game_running:

	clock.tick(FPS_LIMIT) #Limitamos el frame rate

	draw_background()

	draw_ui_panel()
	player_barra_salud.draw(player.salud)
	bandido_1_barra_salud.draw(bandido_1.salud)
	bandido_2_barra_salud.draw(bandido_2.salud)

	#draw entities
	player.update()
	player.draw()

	for Personaje in lista_enemigos:
		Personaje.update()
		Personaje.draw()

	#Acciones del jugador

	# Resetear acciones
	pj_atacar = False
	pj_usar_pocion = False
	objetivo_actual = None

	pygame.mouse.set_visible(True) # Nos aseguramos que el cursor sea visible

	# Control del cursor
	mouse_pos = pygame.mouse.get_pos()
	for count, Personaje in enumerate(lista_enemigos):
		if Personaje.rect.collidepoint(mouse_pos):
			#Si el mouse está sobre un enemigo...
			pygame.mouse.set_visible(False) # ocultamos cursor
			screen.blit(cursor_atk, mouse_pos) # reemplazamos con icono de ataque
			if clicked:
				pj_atacar = True
				objetivo_actual = lista_enemigos[count]

	if boton_usar_pocion.draw():
		pj_usar_pocion = True

	if player.pociones_restantes > 0:
		#Mostrar pociones restantes
		draw_text(str(player.pociones_restantes),fuente, detalle, 147, SCREEN_HEIGHT - UI_PANEL_HEIGHT + 75 )
	else:
		boton_usar_pocion.image = pygame.transform.scale(pygame.image.load('assets/Ico/potion_disabled.png').convert_alpha(), (64, 64))

	#Acciones del jugador
	if player.sigue_vivo:
		if personaje_actual == 1:
			contador_entre_acciones += 1
			if contador_entre_acciones >= pausa_entre_acciones:
				# ejecutar acción del Jugador

				# Atacar
				if pj_atacar and objetivo_actual != None:
					player.atacar(objetivo_actual)
					personaje_actual += 1
					contador_entre_acciones = 0

				# Usar pocion
				if pj_usar_pocion:
					if player.pociones_restantes > 0:
						#curacion_pociones_base
						#player.curar(self)
						player.pociones_restantes -= 1
						personaje_actual += 1
						contador_entre_acciones = 0

	# Acciones de los enemigos
	for count, Personaje in enumerate(lista_enemigos):
		if personaje_actual == 2 + count:
			if Personaje.sigue_vivo:
				contador_entre_acciones += 1
				if contador_entre_acciones >= pausa_entre_acciones:
					# Atacar
					objetivo_tmp = player
					Personaje.atacar(objetivo_tmp)
					personaje_actual += 1
					contador_entre_acciones = 0
			else:
				personaje_actual += 1

			# Cuando todos los pesonajes han actuado, reseteamos al PJ
			if (personaje_actual > personajes_en_total):
						personaje_actual = 1


	#Event Handling
	for event in pygame.event.get():

		key = pygame.key.get_pressed()
		if key[pygame.K_p] == True:
			print('ACCION: ', player.accion_actual)
			if (player.accion_actual < 3):
				player.accion_actual += 1
			else:
				player.idle()

		if event.type == pygame.QUIT:
			game_running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False

	pygame.display.update()


pygame.quit()