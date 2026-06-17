import pygame, random, os

#------------------------------------Iniciar pygame, pantalla y reloj--------------------------------------
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Crazy Snack Rush")

#Crear un reloj para estandarizar la velocidad de los personajes
clock=pygame.time.Clock()

#Labels letra
Letra=pygame.font.SysFont("Comic relif", 30)

#Monedas
coins=0
coin_text=Letra.render(f"{coins}", True, (255,255,255))

#Tiempo
Tiempo_partida=4*60*1000 #4 minutos
tiempo_inicio=pygame.time.get_ticks() 
Time_game=0
label_text=Letra.render(f"{Time_game}", True, (255,255,255))

#-----------------------------------Clase Ingredientes-----------------------------------------
class Ingrediente():
    def __init__(self, nombre):
        self.nombre=nombre
        self.estado=None
    def __repr__(self):
        return self.nombre

class Vegetales_y_Frutas(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.estado="Frescos"
        self.picados=False
        self.frito=False
    def picar(self):
        self.picados=True
        self.estado="Picado"
        print(self.nombre, "esta en este estado: ", self.estado)
    def freir(self):
        self.estado="Frito"
        self.frito=True
        print(self.nombre, "esta en este estado: ", self.estado)


class Panes_y_Bases(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.estado="Entero"

class Proteina(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.estado="Crudo"
        self.cocinada=False
    def cocinar(self):
        self.estado="Cocinado"
        self.cocinada=True
        print(self.nombre, "esta en este estado: ", self.estado)

Macdonals_Ingredientes={"Papas":Vegetales_y_Frutas,
                        "Tomate": Vegetales_y_Frutas,
                        "Lechuga": Vegetales_y_Frutas,
                        "Queso":Panes_y_Bases,
                        "Pan": Panes_y_Bases,
                        "Carne": Proteina}
#-----------------------------------------Restaurantes--------------------------------------------------
class Restaurante():
    def __init__(self, nombre, fondo, area_piso, bloqueo): #$$$$$$$$$$(, lista_estaciones) para agregar las estaciones posteriormente
        self.nombre=nombre
        self.fondo=fondo
        self.area_piso=area_piso
        self.bloqueo=bloqueo 
        self.macdonals_catalogo=Macdonals_Ingredientes
        #self.lista_estaciones=lista_estaciones
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #Las estaciones se agregaran posteriormente, por ahora solo se muestra el fondo del restaurante
    def draw(self): #$$$$$$$$$$$$$$$$$ #Lista de chefs (, lista_chefs) para hacer el reconocimiento de colisiones con las estaciones, se agregara posteriormente
        screen.blit(self.fondo, (0, 0))
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$44$$$
        #for estaciones in self.lista_estaciones:
        #  estaciones.draw(screen, lista_chefs) #Se agregara posteriormente para mostrar las estaciones y el reconocimiento de colisiones con los chefs


#Restaurante 1 Macdonals 
Fondo_Restaurante1=os.path.join("assets", "Fondo", "Macdonals.png")
Macdonals_Fondo = pygame.image.load(Fondo_Restaurante1).convert() 
Bloqueo_Macdonals=pygame.Rect(440,140,80, 120)
Fondo_Restaurante2=os.path.join("assets", "Fondo", "Pizzeria.png")
Pizzeria_Fondo = pygame.image.load(Fondo_Restaurante2).convert()

#Espaxio para el fondo de la panaderia, que se agregara posteriormente
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#Rectangulo y objeto
piso_macdonals=pygame.Rect(78,200,640,240)
Macdonals=Restaurante("Macdonals", Macdonals_Fondo, piso_macdonals, Bloqueo_Macdonals)

piso_pizzeria=pygame.Rect(78,200,640,240)
Pizzeria=Restaurante("Pizzeria", Pizzeria_Fondo, piso_pizzeria, None)

#Lista de restaurantes disponibles
Restaurantes=[Macdonals, Pizzeria] #Panaderia se agregara posteriormente, por ahora solo se muestran dos restaurantes

restaurante_activo=Macdonals
def cambiar_restaurante(indice):
    global restaurante_activo
    restaurante_activo=Restaurantes[indice]

#------------------------------------Clase Character y Chef--------------------------------------
class Character():
    def __init__(self,x,y,color, img_down):
        self.rect=pygame.Rect(0,0,90,107) #x,y,weight and height
        self.rect.center=(x,y)
        self.color=color
        self.img_down=img_down
        self.speed=3
    def move(self, dx,dy, restaurante, bloqueo): #(area objeto)
        self.rect.y +=dy
        self.rect.x +=dx
        if self.rect.colliderect(bloqueo):
           self.rect.y -=dy
           self.rect.x -=dx
        self.rect.clamp_ip(restaurante)
    def draw(self,surface):
        #pygame.draw.rect(surface, self.color, self.rect,2)
        surface.blit(self.img_down, self.rect)

class Chef():
    def __init__(self, nombre, cuerpo_fisico):
        self.nombre=nombre
        self.puntos=0 #Coins
        self.agarrar=None
        self.cuerpo_fisico=cuerpo_fisico
    
    def sacar_despensa(self, objeto_ingrediente):
        self.agarrar=objeto_ingrediente
        print(self.nombre, self.agarrar)
    
    def soltar(self, estacion):
        if self.agarrar is not None:
            estacion.recibir_ingrediente(self.agarrar)

#Color personajes      
COLOR_MIKU=(57,197,187) #Tambien se puede con el codigo hexadecimal pero se llamaria con pygame.Color("#39C5BB")
COLOR_TETO=(210,43,83) #Codigo RGB (Red,Green,Blue)

MIKU_DOWN=os.path.join("assets", "Miku", "Miku_down.png")
TETO_DOWN=os.path.join("assets", "Teto", "Teto_down.png")

miku_image=pygame.image.load(MIKU_DOWN).convert_alpha()
teto_image=pygame.image.load(TETO_DOWN).convert_alpha()

#Characteres
Miku= Character(250,380,COLOR_MIKU,miku_image)
Teto= Character(150,380,COLOR_TETO, teto_image)

Miku_Chef=Chef("Miku", Miku)
Teto_Chef=Chef("Teto", Teto)

#---------------------------Logica recetas y cocina-----------------------------------------

class Cocina():
    def __init__(self,chefs):
        self.tiempo=0
        self.chefs=chefs
        self.ordenes=[]
        self.time_ult_receta=0
        self.intervalo_generar=0 #10 segundos para la generacion

    def generar_receta(self, nombre_restaurante, tiempo_actual): #Recibe el nombre de restaurante_actual.nombre
        self.intervalo_generar=5000
        if len(self.ordenes) < 3:
            if tiempo_actual - self.time_ult_receta >=self.intervalo_generar:
                recetas_disponibles=[]
                if nombre_restaurante=="Macdonals":
                    recetas_disponibles=Macdonals_Recetas
                #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ (Agregar los otros restaurantes)
                if recetas_disponibles:
                    receta_molde= random.choice(recetas_disponibles)
                    Nueva_orden=Recetas(receta_molde.nombre, receta_molde.lista_ingredientes, receta_molde.puntos_receta, receta_molde.maxtime_receta)
                    self.ordenes.append(Nueva_orden)
                    self.time_ult_receta=tiempo_actual
    def draw_ordenes(self, lista_posiciones):
        for i, receta in enumerate (self.ordenes):
            if i > len(lista_posiciones):
                break
            x,y=lista_posiciones[i]
            Receta_Dibujo=None
            if receta.nombre=="Hamburguesa_Queso":
                Receta_Dibujo=Receta_Queso
            elif receta.nombre=="Hamburguesa_Lechuga":
                Receta_Dibujo=Receta_Lechuga
            elif receta.nombre=="Hamburguesa_Completa":
                Receta_Dibujo=Receta_Completa
            elif receta.nombre=="Papas_Fritas":
                Receta_Dibujo=Receta_Papas_Fritas
            
            if Receta_Dibujo:
                screen.blit(Receta_Dibujo, (x,y))

Cocina_Madre=Cocina([Miku_Chef, Teto_Chef])
Ubicacion_ordenes={
            "Macdonals": [(224, 90),(300,90), (364,90)]} #$$$$$$$$$$$$$$$$(Agregar otros restaurantes)

class Recetas():
    def __init__(self, nombre, lista_ingredientes, puntos_receta, maxtime_receta):
        self.nombre=nombre
        self.lista_ingredientes=lista_ingredientes
        self.puntos_receta=puntos_receta
        self.maxtime_receta=maxtime_receta
        self.tiempo_trascurrido=0 #tiempo desde que se genero

    def __repr__(self):
        return self.nombre #Para imprimir recetas en el proceso de revision
    
    def COMPARAR_RECETA(receta, chef):
        if receta in Cocina_Madre.ordenes:
            posicion=Cocina_Madre.ordenes.index(receta)
            Cocina_Madre.ordenes[posicion].remove
            chef.puntos=chef.puntos+receta.puntos_receta
    def Calcular_puntos(receta, chef1, chef2):
        if receta in Cocina_Madre.ordenes:
            chef1.puntos=chef1.puntos+receta.puntos_receta
            chef2.puntos=chef2.puntos+receta.puntos_receta
            global coins
            coins += receta.puntos_receta


#-------------------------------Lista_restaurantes y recetas----------------------------------
Papas_fritas=Recetas("Papas_Fritas", ["Papas"], 50, 40000) #Las papas deben estar papas.estado=="Fritas", el valor de puntos son 50 monedas y el tiempo 40 s
Hamburguesa_Queso=Recetas("Hamburguesa_Queso", ["Pan","Queso","Carne", "Tomate"],100,80000) # 1 min y 20s, la carne debe estar cocida
Hamburguesa_Lechuga=Recetas("Hamburguesa_Lechuga", ["Pan", "Lechuga", "Carne", "Tomate"], 100,80000)
Hamburguesa_Completa=Recetas("Hamburguesa_Completa", ["Pan","Queso","Carne","Lechuga","Tomate"], 150,80000)

Mac_Recetas_Rutas_Queso=os.path.join("assets", "Recetas_Macdonals", "Queso.png")
Mac_Recetas_Rutas_Completa=os.path.join("assets", "Recetas_Macdonals", "Completa.png")
Mac_Recetas_Rutas_Lechuga=os.path.join("assets", "Recetas_Macdonals", "Lechuga.png")
Mac_Recetas_Papas_Fritas=os.path.join("assets", "Recetas_Macdonals", "Papas_Fritas.png")

Receta_Queso=pygame.image.load(Mac_Recetas_Rutas_Queso).convert_alpha()
Receta_Lechuga=pygame.image.load(Mac_Recetas_Rutas_Lechuga).convert_alpha()
Receta_Papas_Fritas=pygame.image.load(Mac_Recetas_Papas_Fritas).convert_alpha()
Receta_Completa=pygame.image.load(Mac_Recetas_Rutas_Completa).convert_alpha()

Macdonals_Recetas=[Papas_fritas, Hamburguesa_Completa, Hamburguesa_Lechuga, Hamburguesa_Queso]
#---------------------------------Estaciones Clase----------------------------------------
class Estacion_Trabajo():
    def __init__(self, nombre, ingredientes_aceptados, x, y, ancho, alto, ampliar1, ampliar2):
        self.nombre=nombre
        self.ingredientes_aceptados=ingredientes_aceptados
        self.rect=pygame.Rect(0,0,ancho, alto)
        self.rect.center =(x,y)
        self.ampliar1=ampliar1
        self.ampliar2=ampliar2
    
    def draw(self, chef1, chef2, click_izquierdo):
        activar_zona_trabajo=False
        zona_proximidad=self.rect.inflate(self.ampliar1, self.ampliar2)
        chef_zona=[]

        if chef1.agarrar is not None:
            if chef1.agarrar.nombre in self.ingredientes_aceptados:
                if zona_proximidad.colliderect(chef2.cuerpo_fisico.rect):
                    activar_zona_trabajo=True
                    chef_zona.append(chef1)

        if chef2.agarrar is not None:
            if chef2.agarrar.nombre in self.ingredientes_aceptados:
                if zona_proximidad.colliderect(chef2.cuerpo_fisico.rect):
                    activar_zona_trabajo=True
                    chef_zona.append(chef2)

        if activar_zona_trabajo:
            pygame.draw.rect(screen, (0,255,255), self.rect,2)

        if click_izquierdo:
            for chef in chef_zona:
                self.recibir_procesar(chef.agarrar)

class Freidora(Estacion_Trabajo):
    def __init__(self, x, y, ancho, alto, ampliar1, ampliar2):
        super().__init__("Freidora", ["Papas"], x, y, ancho, alto, ampliar1, ampliar2)
    def recibir_procesar(self, ingrediente):
        if ingrediente.nombre in self.ingredientes_aceptados:
            ingrediente.freir()

freidora_1=Freidora(590,200,70,54,10,10)
freidora_2=Freidora(665, 200,70,54,10,10)

class Tabla_picar(Estacion_Trabajo):
    def __init__(self, x, y, ancho, alto, ampliar1, ampliar2):
        super().__init__("Tabla_picar", ["Lechuga", "Tomate"], x, y, ancho, alto, ampliar1, ampliar2)
    def recibir_procesar(self, ingrediente):
        if ingrediente.nombre in self.ingredientes_aceptados:
            ingrediente.picar()
            

Tabla_picar_1=Tabla_picar(250,215,70,54,10,10)
Tabla_picar_2=Tabla_picar(350,215,70,54,10,10)

class Horno_Parrilla (Estacion_Trabajo):
    def __init__(self, x, y, ancho, alto, ampliar1, ampliar2):
        super().__init__("Horno_Parrilla", ["Carne", "Pizza", "Masa"], x, y, ancho, alto, ampliar1, ampliar2)
    def recibir_procesar(self, ingrediente):
        if ingrediente.nombre in self.ingredientes_aceptados:
            ingrediente.cocinar()

Parrilla=Horno_Parrilla(550, 450, 137, 42,10,10)


    

 # class Entrega_y_Ensamblaje(Estacion_Trabajo):
    #def __init__(self, nombre, ingredientes_aceptados, x, y, ancho, alto, ampliar1, ampliar2, catalogo_recetas):
        #super().__init__(nombre, ingredientes_aceptados, x, y, ancho, alto, ampliar1, ampliar2)
        #self.catalogo_recetas=catalogo_rec
        #self_orden_en_proceso=[]  


Lista_estaciones_trabajo=[freidora_1, freidora_2, Tabla_picar_1, Tabla_picar_2,Parrilla]

#------------------------------Clase diseño despensas-------------------------------------
class Estacion_Despensa():
    def __init__(self, nombre_ingrediente, restaurante, catalogo, x,y, ancho, alto, ampliar1, ampliar2):
        self.nombre_ingrediente=nombre_ingrediente
        self.restaurante=restaurante
        self.catalogo=catalogo
        self.rect=pygame.Rect(0,0,ancho,alto) #x,y,weight and height
        self.rect.center=(x,y)
        self.ampliar1=ampliar1
        self.ampliar2=ampliar2

    def draw(self, chef1, chef2, click_izquierdo):
        activar_despensa=False
        zona_proximidad= self.rect.inflate(self.ampliar1,self.ampliar2)
        chefs_zona=[]

        if chef1.agarrar is None and zona_proximidad.colliderect(chef1.cuerpo_fisico.rect):
            activar_despensa=True
            chefs_zona.append(chef1)
        if chef2.agarrar is None and zona_proximidad.colliderect(chef2.cuerpo_fisico.rect):
            activar_despensa=True
            chefs_zona.append(chef2)
            
        if activar_despensa:
            pygame.draw.rect(screen, (255,255,0), self.rect,2)
        if click_izquierdo:
            for chef in chefs_zona:
                self.generar_ingrediente(self.nombre_ingrediente, chef) 
            
            
    def generar_ingrediente(self, nombre_ingrediente, chef):
        if nombre_ingrediente in self.catalogo:
            Clase_objeto_generar=self.catalogo[nombre_ingrediente]
            Objeto_ingrediente=Clase_objeto_generar(nombre_ingrediente)
            chef.sacar_despensa(Objeto_ingrediente)

#--------------------------------------Despensas ------------------------------------------
#Despensas
despensa_tomates=Estacion_Despensa("Tomate", "Macdonals",Macdonals_Ingredientes, 62, 276, 64, 55,10,10)
despensa_lechuga=Estacion_Despensa("Lechuga", "Macdonals", Macdonals_Ingredientes, 62, 412, 64, 55,10,10)
despensa_Queso=Estacion_Despensa("Queso", "Macdonals",Macdonals_Ingredientes, 118, 176, 127, 42,20,20) 
despensa_Pan=Estacion_Despensa("Pan", "Macdonals", Macdonals_Ingredientes, 121, 225, 127, 42,20,20)
despensa_Carne=Estacion_Despensa("Carne", "Macdonals", Macdonals_Ingredientes, 480, 195, 130, 66,20,20)
despensa_Papas=Estacion_Despensa("Papas","Macdonals", Macdonals_Ingredientes, 480, 275, 130, 62,10,10) #&&&&&&&&&&&&&&&&&&&&&&&&&

listas_despensas=[despensa_tomates, despensa_lechuga, despensa_Queso, despensa_Pan, despensa_Carne, despensa_Papas]
#-------------------------------Movimiento personajes--------------------------------------
def movimiento_characters(keys, character_1, character_2): #Falta (area_objeto) para agregar el cuadro de colision con el piso, se agregara posteriormente
    character_1_dx=0
    character_1_dy=0
    
    if keys[pygame.K_a]:
        character_1_dx-=character_1.speed
    if keys[pygame.K_d]:
         character_1_dx+=character_1.speed 
    if keys[pygame.K_s]:
        character_1_dy+=character_1.speed 
    if keys[pygame.K_w]:
        character_1_dy-=character_1.speed
    
    character_1.move(character_1_dx, character_1_dy, restaurante_activo.area_piso, restaurante_activo.bloqueo)

    character_2_dx=0
    character_2_dy=0

    if keys[pygame.K_UP]:
        character_2_dy=-character_2.speed
    if keys[pygame.K_DOWN]:
        character_2_dy=character_2.speed
    if keys[pygame.K_LEFT]:
        character_2_dx=-character_2.speed
    if keys[pygame.K_RIGHT]:
        character_2_dx=character_2.speed

    character_2.move(character_2_dx, character_2_dy, restaurante_activo.area_piso, restaurante_activo.bloqueo)


#------------------------------------Fuera del bucle principal--------------------------------------
#Bucle principal del juego
run=True

while run:
    click_izquierdo=False
    restaurante_activo.draw()

    #Monedas, edita ek valor de los puntos en la pantalla
    rect_text=coin_text.get_rect()
    rect_text=(85,482)
    screen.blit(coin_text,rect_text)

    #Tiempo, edita el valor del tiempo en la pantalla
    rect_time=label_text.get_rect()
    rect_time=(705,470)
    screen.blit(label_text,rect_time)

    #Tiempo de juego
    tiempo_actual=pygame.time.get_ticks()
    tiempo_transcurrido=tiempo_actual - tiempo_inicio
    tiempo_restante=Tiempo_partida - tiempo_transcurrido

    #Controlar cambios en los frames
    clock.tick(60) #60 frames por segundo
    tt=clock.tick(60) #Cocina requiere saber

    if tiempo_restante > 0:
        Cocina_Madre.generar_receta(restaurante_activo.nombre, tiempo_actual)
    if tiempo_restante <= 0:
        tiempo_restante=0
        print(f"Se acabo el tiempo, obtuviste: {coins} monedas") #¿Podriamos agregar la cantidad de recetas completadas?
        run=False
    
    #Conversion a tiempo humano, minutos y segundos
    minutos=tiempo_restante // 60000
    segundos=(tiempo_restante % 60000) // 1000

    #Labels de tiempo y monedas
    label_text=Letra.render(f"{minutos}:{segundos:02d}", True, (255,255,255))
    coin_text=Letra.render(f"{coins}", True, (255,255,255))

    #-------------------------------------Personajes control--------------------------------
    #Evento cerrar pantalla
    for event in pygame.event.get():
        if event.type==pygame.QUIT: #Desactiva los modulos pygame
            run=False

        if event.type == pygame.KEYDOWN:
            #Cambio de restaurante
            if event.key == pygame.K_1:
                cambiar_restaurante(0)
            elif event.key == pygame.K_2:
                cambiar_restaurante(1)
            elif event.key == pygame.K_3:
                cambiar_restaurante(2)
            
            #Cambio personajes
            elif event.key == pygame.K_0:
                Miku, Teto= Teto, Miku
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_izquierdo=True

    Miku.draw(screen)
    Teto.draw(screen)

    movimiento_characters(pygame.key.get_pressed(), Miku, Teto)
    
    posicion_ordenes=Ubicacion_ordenes[restaurante_activo.nombre] #Revisa la posicion de las ordenes en el diccionario
    Cocina_Madre.draw_ordenes(posicion_ordenes)

    for despensa in listas_despensas:
        despensa.draw(Miku_Chef, Teto_Chef, click_izquierdo)
    for estacion in Lista_estaciones_trabajo:
        estacion.draw(Miku_Chef, Teto_Chef, click_izquierdo)

   
    pygame.display.update()
pygame.quit()