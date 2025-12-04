# Descripción del Proyecto SPACE DEFENDER

Es un juego  desarrollado en Python usando la librería PyGame. 
El objetivo es defender la Tierra de monstruos y naves alienígenas que caen desde el espacio. 
El jugador controla una nave espacial que puede moverse horizontalmente y disparar para destruir a los enemigos antes de que lleguen al planeta.


## Características del Juego

### Funcionalidades Principales:
**Menú Principal**: Pantalla de inicio con instrucciones claras
**Sistema de Vidas**: El jugador comienza con 3 vidas
**Sistema de Puntuación**: Gana puntos al destruir enemigos
**Múltiples Tipos de Enemigos**: 
  - Monstruo Espacial (25 puntos)
  - Naves alienígenas (10 puntos)
**Sistema de Disparos**: Dispara proyectiles para destruir enemigos
**Efectos Visuales**: Explosiones animadas al destruir enemigos
**Efectos de Sonido**: Sonidos de disparos, explosiones, perder vida y game over
**Música de Fondo**: Música ambiental espacial durante el juego
**Menú de Pausa**: Pausa el juego y continuarlo en cualquier momento
**Game Over**: Pantalla final con puntuación y opciones
**Dificultad Progresiva**: Los enemigos aparecen más rápido con el tiempo
**Fondo Animado**: Estrellas en movimiento para simular el espacio

## Controles

| Tecla           |         Acción                        |
|-----------------|---------------------------------------|
| **←**           | Mover nave a la izquierda             |
| **→**           | Mover nave a la derecha               |
| **ESPACIO**     | Disparar                              |
| **ESC**         | Pausar / Salir del juego              |
| **ENTER**       | Iniciar / Continuar juego             |
| **M**           | Volver al menú principal (desde pausa)|

## Instalación

### Requisitos Previos:
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación:

1. **Clonar o descargar el proyecto**


2. **Instalar dependencias**
   ```bash
   python -m pip install pygame
   o
   py -m pip install pygame

      ```

3. **Ejecutar el juego**
   ```bash
   python space_defender.py
   o
   py space_defender.py
   ```

## Estructura del Código

El código está organizado en secciones definidas para facilitar su comprensión:

### 1. **Constantes y Configuración** (líneas 1-70)
- Colores del juego
- Dimensiones de la ventana
- Configuración de FPS
- Inicialización de PyGame
- Generación de efectos de sonido

### 2. **Funciones de Sonido** (líneas 35-70)
Funciones que generan efectos de sonido:
- `generar_sonido_disparo()`: Sonido de láser al disparar
- `generar_sonido_explosion()`: Sonido al destruir enemigos
- `generar_sonido_game_over()`: Sonido cuando pierdes
- `generar_sonido_perder_vida()`: Sonido al recibir daño
- `iniciar_musica_fondo()`: Música ambiental del juego

### 3. **Funciones de Dibujo** (líneas 75-130)
Funciones que dibujan elementos visuales en la pantalla:
- `dibujar_nave()`: Dibuja la nave del jugador
- `dibujar_enemigo()`: Dibuja monstruos y naves enemigas
- `dibujar_disparo()`: Dibuja los proyectiles
- `dibujar_explosion()`: Dibuja efectos de explosión

### 4. **Funciones de Lógica del Juego** (líneas 135-250)
Funciones que controlan el comportamiento del juego:
- `crear_enemigo()`: Genera nuevos enemigos aleatorios
- `mover_enemigos()`: Actualiza posiciones de enemigos
- `mover_disparos()`: Actualiza posiciones de disparos
- `verificar_colisiones()`: Detecta impactos entre disparos y enemigos
- `verificar_colision_jugador()`: Detecta si un enemigo golpeó al jugador
- `mostrar_texto()`: Muestra texto en pantalla

### 5. **Funciones de Menús** (líneas 255-350)
Interfaces de usuario del juego:
- `menu_principal()`: Pantalla de inicio con fondo de estrellas animado
- `menu_game_over()`: Pantalla de fin de juego
- `menu_pausa()`: Pantalla de pausa

### 6. **Función Principal del Juego** (líneas 355-490)
- `jugar()`: Contiene el bucle principal del juego
  - Inicia y controla la música de fondo
  - Procesa eventos del teclado
  - Actualiza posiciones de todos los elementos
  - Detecta colisiones y reproduce sonidos
  - Dibuja todos los elementos en pantalla
  - Controla el sistema de vidas y puntuación

### 7. **Bucle Principal del Programa** (líneas 495-515)
- `main()`: Controla el flujo entre menús y el juego


