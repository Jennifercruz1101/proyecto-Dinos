import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 1200, 600

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (180, 95, 4)

# Creación de la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Cargar imágenes
dino_images = [pygame.image.load("d1.png"),
            pygame.image.load("d2.png"),
            pygame.image.load("d3.png")]
tree_img = pygame.image.load("arbol.png")
background_img = pygame.image.load("fondo.jpeg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

pygame.mixer.init()

# Cargar música de fondo
pygame.mixer.music.load("musica.mpeg")

# Establecer el volumen de la música (0.1 para un volumen bajo)
pygame.mixer.music.set_volume(0.9)

# Reproducir música en un bucle infinito
pygame.mixer.music.play(-1)



# Variables del juego
dinosaur = {
    "x": 200,
    "y": HEIGHT - 38,  # Posición en el centro vertical
    "width": 30,
    "height": 38,
    "jump": 4,
    "fall": 0,
    "jumping": False,
    "image_index": 0,  # Índice de la imagen del dinosaurio
}
image_change_time = 0
trees = []
tree_speed = 4
clouds = []
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

running = True

def create_tree(last_tree_x):
    # Crea un árbol en la posición (WIDTH, HEIGHT // 4) y lo agrega a la lista
    min_distance = 400
    x = last_tree_x + min_distance + random.randint(50, 100)
    y = HEIGHT - HEIGHT //8 - 70   # Posición en el centro vertical
    trees.append({"x": x, "y": y, "width": 50, "height": 70})

    last_tree_x = x  # Almacena la posición del último árbol


def draw_trees():
    # Dibuja los árboles en la pantalla
    for tree in trees:
        screen.blit(tree_img, (tree["x"], tree["y"]))

def draw_dinosaur():
    # Dibuja el dinosaurio en la pantalla
    dino_img = dino_images[dinosaur["image_index"]]
    screen.blit(dino_img, (dinosaur["x"], dinosaur["y"]))

def draw_score():
    # Dibuja la puntuación en la pantalla
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))



def check_collisions():
    # Comprueba colisiones entre el dinosaurio y los árboles
    dinosaur_rect = pygame.Rect(dinosaur["x"], dinosaur["y"], dinosaur["width"], dinosaur["height"])
    
    for tree in trees:
        tree_rect = pygame.Rect(tree["x"], tree["y"], tree["width"], tree["y"] + tree["height"])
        if dinosaur_rect.colliderect(tree_rect):
            return True
    return False


def reset_game():
    # Restablece el juego al reiniciar la puntuación, velocidad de los árboles y lista de árboles
    global score, tree_speed, trees, running
    score = 0
    tree_speed = 6
    trees = []
    running = True

last_tree_x = WIDTH

# Ciclo principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not dinosaur["jumping"]:
                dinosaur["jumping"] = True

    image_change_time += clock.get_rawtime()  # Obtén el tiempo transcurrido desde la última iteración         

    if image_change_time >= 300:  # 300 milisegundos (0.3 segundos)
                # Cambiar image_index y reiniciar el temporizador
                dinosaur["image_index"] = (dinosaur["image_index"] + 1) % 3
                image_change_time = 0

    if dinosaur["jumping"]:
        # Controla el salto del dinosaurio y la caída
        if dinosaur["y"] > HEIGHT // 2:
            dinosaur["y"] -= dinosaur["jump"]
            dinosaur["fall"] += 1
        else:
            dinosaur["jumping"] = False
    else:
        if dinosaur["y"] < HEIGHT - dinosaur["height"]:
            # Controla la caída del dinosaurio
            dinosaur["y"] += dinosaur["jump"]
        else:
            # El dinosaurio ha tocado el suelo, por lo que no está cayendo
            dinosaur["fall"] = 0

            

    screen.blit(background_img, (0, 0))
    
    draw_trees()
    draw_dinosaur()
    draw_score()


    if random.randint(0, 100) == 0:
        # Crea árboles de forma aleatoria
        create_tree(last_tree_x)
        last_tree_x = trees[-1]["x"]


    for tree in trees:
        # Verifica si el dinosaurio ha superado un árbol en el eje x
        if dinosaur["x"] > tree["x"] + tree["width"]:
            score += 1  # Incrementar el score en 1 cada vez que se supera un árbol


        # Mueve los árboles hacia la izquierda para simular el movimiento del juego
        tree["x"] -= tree_speed


    if trees and trees[0]["x"] < -50:
        # Elimina árboles que están fuera de la pantalla
        trees.pop(0)
        

    if check_collisions():
        # Finaliza el juego si hay colisiones
        running = False

    pygame.display.update()
# Juego terminado
game_over = True
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            reset_game()
            game_over = False

    screen.fill(BROWN)
    message = font.render("Extinto - Presiona ENTER para jugar ", True, WHITE)
    screen.blit(message, (WIDTH // 2 - 230, HEIGHT // 2))

    pygame.display.update()

# Cierre de Pygame
pygame.quit()
