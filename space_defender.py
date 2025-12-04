"""
SPACE DEFENDER - Juego  con PyGame

Autor: Luz Zaparan
Fecha: Diciembre 2025
"""
import pygame
import random
import sys

# Inicializar Pygame
pygame.init()
pygame.mixer.init()  # Inicializar el sistema de sonido

#Constantes del juego
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60

# Colores (RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 100, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
GRIS = (128, 128, 128)

# Configuración de ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Space Defender - ¡Defiende la Tierra!")
reloj = pygame.time.Clock()

# Sonidos
def generar_sonido_disparo():
    """Genera un sonido de disparo láser"""
    sonido = pygame.mixer.Sound(buffer=bytes([
        int(128 + 127 * ((i % 100) / 100)) for i in range(2000)
    ]))
    sonido.set_volume(0.3)
    return sonido

def generar_sonido_explosion():
    """Genera un sonido de explosión"""
    sonido = pygame.mixer.Sound(buffer=bytes([
        int(128 + 127 * random.random() * (1 - i/4000)) for i in range(4000)
    ]))
    sonido.set_volume(0.4)
    return sonido

def generar_sonido_game_over():
    """Genera un sonido de game over"""
    sonido = pygame.mixer.Sound(buffer=bytes([
        int(128 + 100 * ((8000 - i) / 8000)) for i in range(8000)
    ]))
    sonido.set_volume(0.5)
    return sonido

def generar_sonido_perder_vida():
    """Genera un sonido cuando pierdes una vida"""
    sonido = pygame.mixer.Sound(buffer=bytes([
        int(128 + 80 * ((3000 - i) / 3000) * (1 if (i // 100) % 2 == 0 else -1)) for i in range(3000)
    ]))
    sonido.set_volume(0.4)
    return sonido

def iniciar_musica_fondo():
    """Inicia una música de fondo simple y repetitiva"""
    # Crear un patrón musical 
    duracion = 44100 * 8  # 8 segundos de música 
    musica = []
    
    # Crear una melodía espacial 
    for i in range(duracion):
        # Onda base con variaciones más lentas
        frecuencia = 150 + 30 * ((i // 44100) % 4)  # Cambia cada 2 segundos
        valor = int(128 + 40 * (i % int(44100 / frecuencia)) / int(44100 / frecuencia))
        musica.append(valor)
    
    sonido = pygame.mixer.Sound(buffer=bytes(musica))
    sonido.set_volume(0.12)  # Volumen más bajo
    return sonido

# Generar sonidos al inicio
try:
    SONIDO_DISPARO = generar_sonido_disparo()
    SONIDO_EXPLOSION = generar_sonido_explosion()
    SONIDO_GAME_OVER = generar_sonido_game_over()
    SONIDO_PERDER_VIDA = generar_sonido_perder_vida()
    MUSICA_FONDO = iniciar_musica_fondo()
    SONIDOS_ACTIVOS = True
except:
    SONIDOS_ACTIVOS = False
    print("No se pudieron cargar los sonidos")



def dibujar_nave(x, y, color=AZUL):
    """
    Dibuja la nave del jugador en la pantalla
    
    Parámetros:
        x : Posición horizontal de la nave
        y : Posición vertical de la nave
        color : Color de la nave en formato RGB
    """
    # Cuerpo de la nave 
    pygame.draw.polygon(ventana, color, [
        (x, y - 20),           # Punta superior
        (x - 15, y + 20),      # Esquina inferior izquierda
        (x + 15, y + 20)       # Esquina inferior derecha
    ])
    # Cabina (círculo pequeño)
    pygame.draw.circle(ventana, AMARILLO, (x, y), 5)


def dibujar_enemigo(x, y, tipo=1):
    """
    Parámetros:
        x : Posición horizontal del enemigo
        y : Posición vertical del enemigo
        tipo : Tipo de enemigo (1: nave alienígena, 2: monstruo espacial)
    """
    if tipo == 1:
        # Nave Alienígena 
        # Cuerpo principal 
        pygame.draw.ellipse(ventana, GRIS, (x - 20, y - 8, 40, 16))
        pygame.draw.ellipse(ventana, (100, 100, 100), (x - 18, y - 6, 36, 12))
        
        # Cúpula superior
        pygame.draw.ellipse(ventana, VERDE, (x - 12, y - 15, 24, 14))
        pygame.draw.ellipse(ventana, (0, 200, 0), (x - 10, y - 13, 20, 10))
        
        # Luces de la nave
        pygame.draw.circle(ventana, AMARILLO, (x - 12, y), 3)
        pygame.draw.circle(ventana, ROJO, (x, y), 3)
        pygame.draw.circle(ventana, AMARILLO, (x + 12, y), 3)
        
        # Alas laterales
        puntos_izq = [(x - 20, y), (x - 28, y + 5), (x - 22, y + 2)]
        puntos_der = [(x + 20, y), (x + 28, y + 5), (x + 22, y + 2)]
        pygame.draw.polygon(ventana, (150, 150, 150), puntos_izq)
        pygame.draw.polygon(ventana, (150, 150, 150), puntos_der)
    else:
        # Monstruo Espacial 
        # Cuerpo principal 
        pygame.draw.circle(ventana, (150, 0, 150), (x, y), 18)
        pygame.draw.circle(ventana, (180, 0, 180), (x, y), 15)
        
        # Ojos 
        pygame.draw.circle(ventana, BLANCO, (x - 8, y - 3), 6)
        pygame.draw.circle(ventana, BLANCO, (x + 8, y - 3), 6)
        pygame.draw.circle(ventana, ROJO, (x - 8, y - 3), 4)
        pygame.draw.circle(ventana, ROJO, (x + 8, y - 3), 4)
        pygame.draw.circle(ventana, NEGRO, (x - 8, y - 3), 2)
        pygame.draw.circle(ventana, NEGRO, (x + 8, y - 3), 2)
        
        # Boca 
        pygame.draw.arc(ventana, NEGRO, (x - 8, y + 3, 16, 10), 3.14, 6.28, 2)
        
        # Tentáculos ondulantes (6 tentáculos)
        tentaculos = [
            [(x - 12, y + 15), (x - 15, y + 22), (x - 13, y + 28)],
            [(x - 6, y + 16), (x - 8, y + 24), (x - 6, y + 30)],
            [(x, y + 17), (x - 1, y + 25), (x + 1, y + 32)],
            [(x + 6, y + 16), (x + 8, y + 24), (x + 6, y + 30)],
            [(x + 12, y + 15), (x + 15, y + 22), (x + 13, y + 28)],
            [(x - 9, y + 14), (x - 11, y + 20), (x - 10, y + 26)]
        ]
        
        for tentaculo in tentaculos:
            pygame.draw.lines(ventana, (120, 0, 120), False, tentaculo, 3)


def dibujar_disparo(x, y):
    """
    Parámetros:
        x : Posición horizontal del disparo
        y : Posición vertical del disparo
    """
    pygame.draw.rect(ventana, AMARILLO, (x - 2, y - 10, 4, 10))


def dibujar_explosion(x, y, tamaño):
    """
    Parámetros:
        x : Posición horizontal de la explosión
        y : Posición vertical de la explosión
        tamaño : Tamaño de la explosión
    """
    pygame.draw.circle(ventana, AMARILLO, (x, y), tamaño)
    pygame.draw.circle(ventana, ROJO, (x, y), tamaño - 5)
    pygame.draw.circle(ventana, AMARILLO, (x, y), tamaño - 10)



def crear_enemigo():
    """
    Retorna:
        dict: Diccionario con datos del enemigo (x, y, velocidad, tipo)
    """
    return {
        'x': random.randint(20, ANCHO_VENTANA - 20),
        'y': -20,
        'velocidad': random.randint(2, 5),
        'tipo': random.randint(1, 2)
    }


def mover_enemigos(enemigos):
    """
    Parámetros:
        enemigos: Lista de enemigos activos
    
    Retorna:
        list: Lista actualizada de enemigos (elimina los que salieron de pantalla)
    """
    enemigos_activos = []
    for enemigo in enemigos:
        enemigo['y'] += enemigo['velocidad']
        # Solo mantener enemigos que estén dentro de la pantalla
        if enemigo['y'] < ALTO_VENTANA + 50:
            enemigos_activos.append(enemigo)
    return enemigos_activos


def mover_disparos(disparos):
    """
    Parámetros:
        disparos: Lista de disparos activos
    
    Retorna:
        list: Lista actualizada de disparos (elimina los que salieron de pantalla)
    """
    disparos_activos = []
    for disparo in disparos:
        disparo['y'] -= 10
        # Solo mantener disparos que estén dentro de la pantalla
        if disparo['y'] > -10:
            disparos_activos.append(disparo)
    return disparos_activos


def verificar_colisiones(disparos, enemigos, puntuacion):
    """
    Parámetros:
        disparos: Lista de disparos activos
        enemigos: Lista de enemigos activos
        puntuacion: Puntuación actual del jugador
    
    Retorna:
        tuple: (disparos actualizados, enemigos actualizados, nueva puntuación, explosiones)
    """
    disparos_restantes = []
    enemigos_restantes = []
    explosiones = []
    puntos_ganados = 0
    
    for disparo in disparos:
        colision = False
        for enemigo in enemigos:
            # Calcular distancia entre disparo y enemigo
            distancia = ((disparo['x'] - enemigo['x'])**2 + 
                        (disparo['y'] - enemigo['y'])**2)**0.5
            
            # Si hay colisión (distancia menor a 20 píxeles)
            if distancia < 20:
                colision = True
                # Crear explosión en la posición del enemigo
                explosiones.append({
                    'x': enemigo['x'],
                    'y': enemigo['y'],
                    'tamaño': 20,
                    'tiempo': 10
                })
                # Reproducir sonido de explosión
                if SONIDOS_ACTIVOS:
                    SONIDO_EXPLOSION.play()
                # Sumar puntos según tipo de enemigo
                puntos_ganados += 10 if enemigo['tipo'] == 1 else 25
                break
        
        # Si el disparo no colisionó, mantenerlo activo
        if not colision:
            disparos_restantes.append(disparo)
        else:
            # Si hubo colisión, eliminar el enemigo
            enemigos_restantes = [e for e in enemigos if 
                                 not ((e['x'] == enemigo['x']) and (e['y'] == enemigo['y']))]
            enemigos = enemigos_restantes.copy()
    
    # Mantener enemigos que no fueron impactados
    for enemigo in enemigos:
        if enemigo not in enemigos_restantes:
            enemigos_restantes.append(enemigo)
    
    return disparos_restantes, enemigos_restantes, puntuacion + puntos_ganados, explosiones


def verificar_colision_jugador(nave_x, nave_y, enemigos):
    """
    Parámetros:
        nave_x: Posición horizontal de la nave
        nave_y: Posición vertical de la nave
        enemigos: Lista de enemigos activos
    """
    for enemigo in enemigos:
        distancia = ((nave_x - enemigo['x'])**2 + 
                    (nave_y - enemigo['y'])**2)**0.5
        if distancia < 25:
            return True
    return False


def mostrar_texto(texto, x, y, tamaño=36, color=BLANCO):
    """
    Parámetros:
        texto: Texto a mostrar
        x: Posición horizontal
        y: Posición vertical
        tamaño: Tamaño de la fuente
        color: Color del texto en RGB
    """
    fuente = pygame.font.Font(None, tamaño)
    superficie = fuente.render(texto, True, color)
    rectangulo = superficie.get_rect(center=(x, y))
    ventana.blit(superficie, rectangulo)


def menu_principal():

    # Para animación de estrellas en el menú
    contador_estrellas = 0
    
    while True:
        ventana.fill(NEGRO)
        
        # Dibujar estrellas de fondo animadas
        for i in range(100):
            x = (i * 47) % ANCHO_VENTANA
            y = (i * 83 + contador_estrellas) % ALTO_VENTANA
            tamaño = 1 if i % 3 == 0 else 2
            pygame.draw.circle(ventana, BLANCO, (x, y), tamaño)
        
        # Algunas estrellas brillantes de colores
        for i in range(20):
            x = (i * 127) % ANCHO_VENTANA
            y = (i * 93 + contador_estrellas // 2) % ALTO_VENTANA
            color = AZUL if i % 2 == 0 else AMARILLO
            pygame.draw.circle(ventana, color, (x, y), 1)
        
        contador_estrellas += 1
        
        # Título del juego
        mostrar_texto("SPACE DEFENDER", ANCHO_VENTANA // 2, 150, 72, AZUL)
        mostrar_texto("¡Defiende la Tierra!", ANCHO_VENTANA // 2, 220, 36, BLANCO)
        
        # Instrucciones
        mostrar_texto("CONTROLES:", ANCHO_VENTANA // 2, 300, 32, AZUL)
        mostrar_texto("TECLAS <--IZQUIERDA/DERECHA-->: Mover Nave", ANCHO_VENTANA // 2, 340, 26, BLANCO)
        mostrar_texto("ESPACIO: Disparar ", ANCHO_VENTANA // 2, 370, 28, BLANCO)

        # Indicación para comenzar
        mostrar_texto("Presiona ENTER para jugar", ANCHO_VENTANA // 2, 450, 32, AMARILLO)
        mostrar_texto("ESC - Salir del juego", ANCHO_VENTANA // 2, 480, 32, GRIS)

        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'salir'
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return 'jugar'
                if evento.key == pygame.K_ESCAPE:
                    return 'salir'
        
        reloj.tick(FPS)


def menu_game_over(puntuacion_final):

    while True:
        ventana.fill(NEGRO)
        
        # Mensaje de Game Over
        mostrar_texto("GAME OVER", ANCHO_VENTANA // 2, 150, 72, ROJO)
        mostrar_texto(f"Puntuación Final: {puntuacion_final}", 
                     ANCHO_VENTANA // 2, 250, 48, AMARILLO)
        
        # Opciones
        mostrar_texto("ENTER - Jugar de nuevo", ANCHO_VENTANA // 2, 350, 32, BLANCO)
        mostrar_texto("M - Menú principal", ANCHO_VENTANA // 2, 390, 32, BLANCO)
        mostrar_texto("ESC - Salir", ANCHO_VENTANA // 2, 430, 32, GRIS)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'salir'
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return 'reintentar'
                if evento.key == pygame.K_m:
                    return 'menu'
                if evento.key == pygame.K_ESCAPE:
                    return 'salir'
        
        reloj.tick(FPS)


def menu_pausa(fondo_pantalla):
    
    # Limpiar eventos antiguos
    pygame.event.clear()
    
    # Esperar hasta que ESC esté suelto
    while pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.event.pump()
        reloj.tick(FPS)
    
    # Limpiar nuevamente después de esperar
    pygame.event.clear()
    
    while True:
        # Restaurar el fondo del juego
        ventana.blit(fondo_pantalla, (0, 0))
        
        # Dibujar overlay semitransparente
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        overlay.set_alpha(128)
        overlay.fill(NEGRO)
        ventana.blit(overlay, (0, 0))
        
        mostrar_texto("PAUSA", ANCHO_VENTANA // 2, 200, 72, AMARILLO)
        mostrar_texto("ENTER - Continuar", ANCHO_VENTANA // 2, 320, 32, BLANCO)
        mostrar_texto("M - Menú principal", ANCHO_VENTANA // 2, 360, 32, BLANCO)
        mostrar_texto("ESC - Salir del juego", ANCHO_VENTANA // 2, 400, 32, GRIS)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.event.clear()
                return 'salir'
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    # Esperar a que se suelte la tecla antes de continuar
                    while pygame.key.get_pressed()[pygame.K_RETURN]:
                        pygame.event.pump()
                        reloj.tick(FPS)
                    pygame.event.clear()
                    return 'continuar'
                if evento.key == pygame.K_m:
                    pygame.event.clear()
                    return 'menu'
                if evento.key == pygame.K_ESCAPE:
                    # Esperar a que se suelte ESC
                    while pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        pygame.event.pump()
                        reloj.tick(FPS)
                    pygame.event.clear()
                    return 'salir'
        
        reloj.tick(FPS)

#Función principal del juego
def jugar():

    # Iniciar música de fondo
    if SONIDOS_ACTIVOS:
        MUSICA_FONDO.play(loops=-1)  # -1 significa reproducir en bucle infinito
    
    # Variables del jugador
    nave_x = ANCHO_VENTANA // 2
    nave_y = ALTO_VENTANA - 80
    velocidad_nave = 7
    
    # Variables del juego
    disparos = []
    enemigos = []
    explosiones = []
    puntuacion = 0
    vidas = 3
    
    # Control de dificultad
    contador_frames = 0
    frecuencia_enemigos = 60  # Cada cuántos frames aparece un enemigo
    
    # Bucle principal del juego
    jugando = True
    while jugando:
        # Procesar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'salir'
            
            if evento.type == pygame.KEYDOWN:
                # Disparar con barra espaciadora
                if evento.key == pygame.K_SPACE:
                    disparos.append({'x': nave_x, 'y': nave_y - 30})
                    # Reproducir sonido de disparo
                    if SONIDOS_ACTIVOS:
                        SONIDO_DISPARO.play()
                
                # Pausar con ESC
                if evento.key == pygame.K_ESCAPE:
                    # Guardar el estado actual de la pantalla
                    fondo_pantalla = ventana.copy()
                    
                    # Detener música
                    if SONIDOS_ACTIVOS:
                        MUSICA_FONDO.stop()
                    
                    # Mostrar menú de pausa
                    accion = menu_pausa(fondo_pantalla)
                    
                    # Limpiar eventos después de salir del menú de pausa
                    pygame.event.clear()
                    
                    while any(pygame.key.get_pressed()):
                        pygame.event.pump()
                        reloj.tick(FPS)
                    
                    # Limpiar eventos una vez más
                    pygame.event.clear()
                    
                    # Reanudar música si continúa jugando
                    if accion == 'continuar':
                        if SONIDOS_ACTIVOS:
                            MUSICA_FONDO.play(loops=-1)
                        # Continuar el juego sin hacer return
                    elif accion == 'salir' or accion == 'menu':
                        if SONIDOS_ACTIVOS:
                            MUSICA_FONDO.stop()
                        return accion
        
        # Controles de movimiento 
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_x > 20:
            nave_x -= velocidad_nave
        if teclas[pygame.K_RIGHT] and nave_x < ANCHO_VENTANA - 20:
            nave_x += velocidad_nave
        
        # Crear nuevos enemigos
        contador_frames += 1
        if contador_frames >= frecuencia_enemigos:
            enemigos.append(crear_enemigo())
            contador_frames = 0
            # Aumentar dificultad gradualmente
            if frecuencia_enemigos > 20:
                frecuencia_enemigos -= 1
        
        # Mover elementos
        disparos = mover_disparos(disparos)
        enemigos = mover_enemigos(enemigos)
        
        # Verificar colisiones
        disparos, enemigos, puntuacion, nuevas_explosiones = verificar_colisiones(
            disparos, enemigos, puntuacion
        )
        explosiones.extend(nuevas_explosiones)
        
        # Verificar colisión con jugador
        if verificar_colision_jugador(nave_x, nave_y, enemigos):
            vidas -= 1
            enemigos = []  # Limpiar enemigos después de ser golpeado
            
            # Reproducir sonido de perder vida
            if SONIDOS_ACTIVOS:
                SONIDO_PERDER_VIDA.play()
            
            # Game Over si no quedan vidas
            if vidas <= 0:
                # Detener música de fondo
                if SONIDOS_ACTIVOS:
                    MUSICA_FONDO.stop()
                    SONIDO_GAME_OVER.play()
                accion = menu_game_over(puntuacion)
                if accion == 'reintentar':
                    return jugar()  # Reiniciar juego
                elif accion == 'menu':
                    return 'menu'
                else:
                    return 'salir'
        
        # Dibujar todo
        ventana.fill(NEGRO)
        
        # Dibujar estrellas de fondo 
        for i in range(50):
            x = (i * 37) % ANCHO_VENTANA
            y = (i * 73 + contador_frames * 2) % ALTO_VENTANA
            pygame.draw.circle(ventana, BLANCO, (x, y), 1)
        
        # Dibujar nave del jugador
        dibujar_nave(nave_x, nave_y)
        
        # Dibujar enemigos
        for enemigo in enemigos:
            dibujar_enemigo(enemigo['x'], enemigo['y'], enemigo['tipo'])
        
        # Dibujar disparos
        for disparo in disparos:
            dibujar_disparo(disparo['x'], disparo['y'])
        
        # Dibujar explosiones
        explosiones_activas = []
        for explosion in explosiones:
            if explosion['tiempo'] > 0:
                dibujar_explosion(explosion['x'], explosion['y'], explosion['tamaño'])
                explosion['tiempo'] -= 1
                explosion['tamaño'] += 1
                explosiones_activas.append(explosion)
        explosiones = explosiones_activas
        
        # Dibujar Información en pantalla
        mostrar_texto(f"Puntuación: {puntuacion}", 100, 30, 32, AMARILLO)
        mostrar_texto(f"Vidas: {vidas}", ANCHO_VENTANA - 100, 30, 32, ROJO)
        
        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(FPS)
    
    # Detener música al salir del bucle
    if SONIDOS_ACTIVOS:
        MUSICA_FONDO.stop()
    
    return 'menu'


def main():

    ejecutando = True
    
    while ejecutando:
        # Mostrar menú principal
        accion = menu_principal()
        
        if accion == 'jugar':
            # Iniciar el juego
            resultado = jugar()
            if resultado == 'salir':
                ejecutando = False
        elif accion == 'salir':
            ejecutando = False
    
    # Cerrar pygame y salir
    pygame.quit()
    sys.exit()


# Ejecutar el juego
if __name__ == "__main__":
    main()
