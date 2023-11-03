# Necessary imports and activation of Pygame
import pygame
import random
pygame.init()
pygame.display.set_caption("Snake")

# Functions
def random_apple_location():
    apple_x = generate_random_location()
    apple_y = generate_random_location()
    for loc in previous_locations:
        in_snake = apple_x == loc[0] and apple_y == loc[1]
        in_player = apple_x == player_rect.x and apple_y == player_rect.y
        if in_snake or in_player:
            apple_x = generate_random_location()
            apple_y = generate_random_location()
    return (apple_x, apple_y)

def generate_random_location():
    return random.randrange(0,(screen_dimension/grid_size).__int__())*grid_size
# Could also write the above function as a lambda function:
# generate_random_location = lambda : random.randrange(0,(screen_dimension/grid_size).__int__())*grid_size

def player_movement_direction(x_toggle, y_toggle):
    key = pygame.key.get_pressed()

    if y_toggle != 0:
        if key[pygame.K_a]:
            y_toggle = 0
            x_toggle = -1
        if key[pygame.K_d]:
            y_toggle = 0
            x_toggle = 1
    elif x_toggle != 0:
        if key[pygame.K_s]:
            y_toggle = 1 
            x_toggle = 0
        if key[pygame.K_w]:
            y_toggle = -1 
            x_toggle = 0
    elif y_toggle == 0 and x_toggle == 0:
        if key[pygame.K_s]:
            y_toggle = 1 
            x_toggle = 0
        if key[pygame.K_w]:
            y_toggle = -1 
            x_toggle = 0
        if key[pygame.K_a]:
            y_toggle = 0
            x_toggle = -1
        if key[pygame.K_d]:
            y_toggle = 0
            x_toggle = 1

    return (x_toggle, y_toggle)

def extend_snake():
    previous_locations.append((player_rect.x, player_rect.y))
    if len(previous_locations) > snake_size:
        previous_locations.pop(0)

def snake_extension_movement():
    for value in previous_locations:
        snake_rect = player_surf.get_rect(topleft = value)
        screen.blit(player_surf, snake_rect)
        if player_rect.colliderect(snake_rect):
            pygame.quit()
            exit()

def death_from_border():
    player_hit_left_right = player_rect.x <= -grid_size or player_rect.x >= screen_dimension
    player_hit_top_bottom = player_rect.y <= -grid_size or  player_rect.y >= screen_dimension
    if  player_hit_left_right or player_hit_top_bottom:
        pygame.quit()
        exit()

# Creates Display
screen_dimension = 900
screen = pygame.display.set_mode((screen_dimension, screen_dimension))

# Allows game to run
clock = pygame.time.Clock()
running = True

# Movement Variables
grid_size = 50
player_y_toggle = 0
player_x_toggle = 0

# Creates player
player_surf = pygame.Surface((grid_size-1, grid_size-1)).convert_alpha()
player_surf.fill('Red')
player_rect = player_surf.get_rect(topleft = (screen_dimension/2,screen_dimension/2))

# Creates Snake
previous_locations = []
snake_size = 0

# Creates Apple 
apple_surf = pygame.Surface((grid_size-1, grid_size-1))
apple_surf.fill('Blue')
apple_rect = apple_surf.get_rect(topleft = random_apple_location())

while running:
    # Rest of the code doesn't work without this for loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    extend_snake()

    player_direction = player_movement_direction(player_x_toggle, player_y_toggle)
    player_x_toggle = player_direction[0]
    player_y_toggle = player_direction[1]

    player_rect.x += player_x_toggle*grid_size
    player_rect.y += player_y_toggle*grid_size
    screen.blit(player_surf, player_rect)

    snake_extension_movement()

    if player_rect.colliderect(apple_rect):
        new_apple_loc = random_apple_location()
        apple_rect.x = new_apple_loc[0]
        apple_rect.y = new_apple_loc[1]
        snake_size += 4
    screen.blit(apple_surf, apple_rect)

    death_from_border()

    pygame.display.update()
    screen.fill('Black')
    clock.tick(10)
