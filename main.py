import pygame

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

#def fonts
fuente = pygame.font.SysFont('Book Antiqua', 20)

#def colors
rojo = (234, 24, 38)
verde = (38, 234, 24)

#background
	#TO DO: Add Parallax animation?
background = pygame.image.load('assets/background.png').convert_alpha()

UI_panel_img = pygame.image.load('assets/ui_panel.png').convert_alpha()

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
		self.muerto = False
		self.animation_list = []
		self.frame_index = 0
		self.accion_actual = 0 # 0: idle / 1: atacar / 2: recibe daño / 3: muerte
		self.update_time = pygame.time.get_ticks()
		# cargar imágenes IDLE

		for a in range (4):

			temp_list = []

			for i in range(10):

				match self.accion_actual:
					case 0:
						#IDLE
						img = pygame.image.load(f'assets/{self.nombre}/Idle/{i}.png')

					case 1:
						#ATAQUE ('Attack')
						img = pygame.image.load(f'assets/{self.nombre}/Attack/{i}.png')

					case 2:
						#RECIBE DAÑO ('Hit')
						img = pygame.image.load(f'assets/{self.nombre}/Hit/{i}.png')

					case 3:
						#MUERTE ('Death')
						img = pygame.image.load(f'assets/{self.nombre}/Death/{i}.png')

					case _:
						#DEFAULT (tomamos Idle)
						img = pygame.image.load(f'assets/{self.nombre}/Idle/{i}.png')

				img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height() * 3.5))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.image = self.animation_list[self.accion_actual][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		animation_cooldown = 100
		#handle update image / animation
		self.image = self.animation_list[self.accion_actual][self.frame_index]

		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1

		# si no quedan frames para animar, reseteamos a index = 0
		if self.frame_index >= len(self.animation_list[self.accion_actual]):
			self.frame_index = 0

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

#Game Loop

game_running = True
while game_running:

	clock.tick(FPS_LIMIT) #Limit the frame rate

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

	#Event Handling
	for event in pygame.event.get():



		if event.type == pygame.QUIT:
			game_running = False

	pygame.display.update()


pygame.quit()