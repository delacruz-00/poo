import pygame
from pygame.locals import *
import random

pygame.init()

# Crear la ventana
ancho = 500
alto = 500
tamaño_pantalla = (ancho, alto)
pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption('carros ')

# Colores
gris = (100, 100, 100)
verde = (76, 208, 56)
rojo = (200, 0, 0)
blanco = (255, 255, 255)
amarillo = (255, 232, 0)

# Tamaños de la carretera y marcadores
ancho_carretera = 300
ancho_marcador = 10
alto_marcador = 50

# Coordenadas de los carriles
carril_izquierdo = 150
carril_central = 250
carril_derecho = 350
carriles = [carril_izquierdo, carril_central, carril_derecho]

# Carretera y marcadores de borde
carretera = (100, 0, ancho_carretera, alto)
marcador_borde_izquierdo = (95, 0, ancho_marcador, alto)
marcador_borde_derecho = (395, 0, ancho_marcador, alto)

# Para animar el movimiento de los marcadores de los carriles
movimiento_marcador_y = 0

# Coordenadas iniciales del jugador
jugador_x = 250
jugador_y = 400

# Configuración del reloj
reloj = pygame.time.Clock()
fps = 120

# Configuración del juego
fin_juego = False
velocidad = 2
puntaje = 0

# Clase para los vehículos
class Vehiculo(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Escalar la imagen para que no sea más ancha que el carril
        escala_imagen = 45 / imagen.get_rect().width
        nuevo_ancho = int(imagen.get_rect().width * escala_imagen)
        nuevo_alto = int(imagen.get_rect().height * escala_imagen)
        self.image = pygame.transform.scale(imagen, (nuevo_ancho, nuevo_alto))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# Clase para el vehículo del jugador
class VehiculoJugador(Vehiculo):
    def __init__(self, x, y):
        imagen = pygame.image.load('images/car.png')
        super().__init__(imagen, x, y)

# Grupos de sprites
grupo_jugador = pygame.sprite.Group()
grupo_vehiculos = pygame.sprite.Group()

# Crear el auto del jugador
jugador = VehiculoJugador(jugador_x, jugador_y)
grupo_jugador.add(jugador)

# Cargar imágenes de vehículos
nombres_imagenes = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
imagenes_vehiculos = []
for nombre in nombres_imagenes:
    imagen = pygame.image.load('images/' + nombre)
    imagenes_vehiculos.append(imagen)

# Cargar la imagen de colisión
colision = pygame.image.load('images/crash.png')
rect_colision = colision.get_rect()

# Bucle principal del juego
corriendo = True
while corriendo:
    reloj.tick(fps)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            corriendo = False
        # Mover el auto del jugador con las teclas izquierda/derecha
        if evento.type == KEYDOWN:
            if evento.key == K_LEFT and jugador.rect.center[0] > carril_izquierdo:
                jugador.rect.x -= 100
            elif evento.key == K_RIGHT and jugador.rect.center[0] < carril_derecho:
                jugador.rect.x += 100
            # Verificar colisión lateral después de cambiar de carril
            for vehiculo in grupo_vehiculos:
                if pygame.sprite.collide_rect(jugador, vehiculo):
                    fin_juego = True
                    if evento.key == K_LEFT:
                        jugador.rect.left = vehiculo.rect.right
                        rect_colision.center = [jugador.rect.left, (jugador.rect.center[1] + vehiculo.rect.center[1]) / 2]
                    elif evento.key == K_RIGHT:
                        jugador.rect.right = vehiculo.rect.left
                        rect_colision.center = [jugador.rect.right, (jugador.rect.center[1] + vehiculo.rect.center[1]) / 2]

    # Dibujar el césped
    pantalla.fill(verde)

    # Dibujar la carretera
    pygame.draw.rect(pantalla, gris, carretera)

    # Dibujar los marcadores de borde
    pygame.draw.rect(pantalla, amarillo, marcador_borde_izquierdo)
    pygame.draw.rect(pantalla, amarillo, marcador_borde_derecho)

    # Dibujar los marcadores de los carriles
    movimiento_marcador_y += velocidad * 2
    if movimiento_marcador_y >= alto_marcador * 2:
        movimiento_marcador_y = 0
    for y in range(alto_marcador * -2, alto, alto_marcador * 2):
        pygame.draw.rect(pantalla, blanco, (carril_izquierdo + 45, y + movimiento_marcador_y, ancho_marcador, alto_marcador))
        pygame.draw.rect(pantalla, blanco, (carril_central + 45, y + movimiento_marcador_y, ancho_marcador, alto_marcador))

    # Dibujar el auto del jugador
    grupo_jugador.draw(pantalla)

    # Añadir un vehículo
    if len(grupo_vehiculos) < 2:
        añadir_vehiculo = True
        for vehiculo in grupo_vehiculos:
            if vehiculo.rect.top < vehiculo.rect.height * 1.5:
                añadir_vehiculo = False
        if añadir_vehiculo:
            carril = random.choice(carriles)
            imagen = random.choice(imagenes_vehiculos)
            vehiculo = Vehiculo(imagen, carril, alto / -2)
            grupo_vehiculos.add(vehiculo)

    # Mover los vehículos
    for vehiculo in grupo_vehiculos:
        vehiculo.rect.y += velocidad
        if vehiculo.rect.top >= alto:
            vehiculo.kill()
            puntaje += 1
            if puntaje > 0 and puntaje % 5 == 0:
                velocidad += 1

    # Dibujar los vehículos
    grupo_vehiculos.draw(pantalla)

    # Mostrar el puntaje
    fuente = pygame.font.Font(pygame.font.get_default_font(), 16)
    texto = fuente.render(f'Puntaje: {puntaje}', True, blanco)
    pantalla.blit(texto, (50, 400))

    # Verificar colisión frontal
    if pygame.sprite.spritecollide(jugador, grupo_vehiculos, True):
        fin_juego = True
        rect_colision.center = [jugador.rect.center[0], jugador.rect.top]

    # Mostrar "Game Over"
    if fin_juego:
        pantalla.blit(colision, rect_colision)
        pygame.draw.rect(pantalla, rojo, (0, 50, ancho, 100))
        texto = fuente.render('Juego terminado. ¿Jugar de nuevo? (Y o N)', True, blanco)
        pantalla.blit(texto, (ancho / 2 - 100, 100))

    pygame.display.update()

    while fin_juego:
        reloj.tick(fps)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                fin_juego = False
                corriendo = False
            if evento.type == KEYDOWN:
                if evento.key == K_y:
                    fin_juego = False
                    velocidad = 2
                    puntaje = 0
                    grupo_vehiculos.empty()
                    jugador.rect.center = [jugador_x, jugador_y]
                elif evento.key == K_n:
                    fin_juego = False
                    corriendo = False

pygame.quit()
