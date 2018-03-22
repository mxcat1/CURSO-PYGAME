#importar las librerias necesarias q se van a usar
import sys
import time
import pygame

#definir la resolucion de la pantalla del juego

ANCHO = 640
ALTO = 420
color_fondo=(0,0,64) #color de fondo

#funcion nesesaria para usar las fuentes

pygame.init()

#clase nueva bolita
class Bolita(pygame.sprite.Sprite):
    #Constructor
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cargar imagen
        self.image = pygame.image.load('Recursos/bolita.png')
        #Obtener Rectangulo de la imagen
        self.rect = self.image.get_rect()
        #Ubicacion dela bolita
        self.rect.centerx = ANCHO/2
        self.rect.centery = ALTO/2
        #MOVIMIENTO DE LA BOLA
        self.speed = [4, 4]

    #Funcion de actualizacion constante del objeto

    def update(self):
        #para evitar q se salga de la pantalla por abajo o por arriva
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        #para evitar que se salga de la pantalla por la derecha o por la izquierda
        elif self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        self.rect.move_ip(self.speed)


#CLASE NUEVA DEL JUGADOR
class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Recursos/paleta.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = (ANCHO/2, ALTO-20)
        self.speed =[0, 0]

    def Update(self, evento):

        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-8, 0]
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed = [8, 0]
        else:
            self.speed = [0, 0]

        self.rect.move_ip(self.speed)

#ladrillo del muro clase
class Ladrillo(pygame.sprite.Sprite):
    def __init__(self,posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Recursos/ladrillo.png')
        self.rect =self.image.get_rect()
        self.rect.topleft = posicion

class Muro(pygame.sprite.Group):
    def __init__(self,cantidadladrillos):
        pygame.sprite.Group.__init__(self)
        pos_x = 0
        pos_y = 20
        for i in range(cantidadladrillos):
            ladrillo = Ladrillo((pos_x,pos_y))
            self.add(ladrillo)
            pos_x += ladrillo.rect.width
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += ladrillo.rect.height

#Funcion llamada cuando sale la bolita por abajo

def juego_terminado():
    fuente = pygame.font.SysFont('Arial', 50)
    texto = fuente.render('Juego Terminado :V', True, (255, 255, 255))
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO / 2, ALTO / 2]
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    # Pausar 3 seg
    time.sleep(3)
    sys.exit()



#generar la pantalla con los dos datos anteriores

pantalla = pygame.display.set_mode((ANCHO,ALTO))

#configurar caracteristicas de la pantalla

pygame.display.set_caption('Juego de Ladrillos')#titulo de la pantalla

#RELOJ DE FRAMES

reloj=pygame.time.Clock()

#RETASO DE PRESION DE LA TECLA

pygame.key.set_repeat(30)

#INSTANCIAR CLASE BOLITA

bolita = Bolita()
jugador = Paleta()
muro = Muro(100)

#buclee infinito para que no se cierre automaticamente la pantalla
while True:
    #Cantidada de Frames
    reloj.tick(60)
    #bucle for para controlar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            jugador.Update(evento)

    #llamando al metodo update
    bolita.update()

    #Coliciones
    if pygame.sprite.collide_rect(bolita,jugador):
        bolita.speed[1] = - bolita.speed[1]

    lista = pygame.sprite.spritecollide(bolita, muro, False)

    if lista:
        ladrillo = lista[0]
        cx = bolita.rect.centerx
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            bolita.speed[0] = -bolita.speed[0]
        else:
            bolita.speed[1] = -bolita.speed[1]
        muro.remove(ladrillo)

    if bolita.rect.top > ALTO:
        juego_terminado()


    pantalla.fill(color_fondo)
    pantalla.blit(bolita.image,bolita.rect)
    pantalla.blit(jugador.image, jugador.rect)
    muro.draw(pantalla)
    pygame.display.flip()

