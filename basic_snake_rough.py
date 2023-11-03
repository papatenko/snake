import pygame
import random
pygame.init()

# Creates Display
screen_dimension = 800
screen_center = screen_dimension/2
screen = pygame.display.set_mode((screen_dimension, screen_dimension))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
running = True

# Movement Variables  
grid_size = 50
y_direction = 0
x_direction = 0

# Creates Player
player_surf = pygame.Surface((grid_size-1, grid_size-1)).convert_alpha()
player_surf.fill('Red')
player_rect = player_surf.get_rect(topleft = (screen_center, screen_center))

# Creates Snake
previous_locations = []
snake_size = 0

# Creates Apple 
apple_surf = pygame.Surface((grid_size-1, grid_size-1))
apple_surf.fill('Blue')
apple_x = random.randrange(0,(screen_dimension/grid_size).__int__())*grid_size
apple_y = random.randrange(0,(screen_dimension/grid_size).__int__())*grid_size
apple_rect = apple_surf.get_rect(topleft = (apple_x,apple_y))

while running:

    # Rest of the code doesn't work without this for loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    previous_locations.append((player_rect.x, player_rect.y))
    if len(previous_locations) >= snake_size:
        previous_locations.pop(0)

    # Snake Movement System
    key = pygame.key.get_pressed()

    if y_direction != 0:
        if key[pygame.K_a]:
            y_direction = 0
            x_direction = -1
        if key[pygame.K_d]:
            y_direction = 0
            x_direction = 1
    elif x_direction != 0:
        if key[pygame.K_s]:
            y_direction = 1 
            x_direction = 0
        if key[pygame.K_w]:
            y_direction = -1 
            x_direction = 0
    if y_direction == 0 and x_direction == 0:
        if key[pygame.K_s]:
            y_direction = 1 
            x_direction = 0
        if key[pygame.K_w]:
            y_direction = -1 
            x_direction = 0
        if key[pygame.K_a]:
            y_direction = 0
            x_direction = -1
        if key[pygame.K_d]:
            y_direction = 0
            x_direction = 1

    player_rect.x += (x_direction*grid_size)
    player_rect.y += y_direction*grid_size
    screen.blit(player_surf, player_rect)

    # Snake extension movement 

    for value in previous_locations:
        snake_rect = player_surf.get_rect(topleft = value)
        screen.blit(player_surf, snake_rect)
        if player_rect.colliderect(snake_rect):
            player_rect.x = screen_center.__int__()
            player_rect.y = screen_center.__int__()
            screen.blit(player_surf, player_rect)
            y_direction = 0
            x_direction = 0
            snake_size = 0
            previous_locations = []

    # Collider Shtuff
    if player_rect.colliderect(apple_rect):
        apple_rect.x = random.randrange(0,(screen_dimension/grid_size).__int__())*grid_size
        apple_rect.y = random.randrange(0,(screen_dimension/grid_size).__int__())*grid_size
        for value in previous_locations:
            if apple_rect.x == value[0] and apple_rect.y == value[1]:
                apple_rect.x = random.randrange(0,(screen_dimension/grid_size).__int__())*grid_size
                apple_rect.y = random.randrange(0,(screen_dimension/grid_size).__int__())*grid_size
                pass
            pass
        snake_size += 3
        pass
    screen.blit(apple_surf, apple_rect)

    # Death
    if player_rect.x <= -grid_size or player_rect.x >= screen_dimension or player_rect.x >= screen_dimension or player_rect.y <= -grid_size or  player_rect.y >= screen_dimension:
        player_rect.x = screen_center
        player_rect.y = screen_center
        screen.blit(player_surf, player_rect)
        y_direction = 0
        x_direction = 0
        snake_size = 0
        previous_locations = []

    pygame.display.update()
    screen.fill('Black')
    clock.tick(10)

