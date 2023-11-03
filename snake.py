import pygame
import random
pygame.init()
pygame.display.set_caption("snek")

# Creates Display
arena_size = 800
arena_center = arena_size/2
grid_size = 40
game_size = arena_size+grid_size*2
screen = pygame.display.set_mode((game_size, game_size))

# Variables for running game
clock = pygame.time.Clock()
running = True
fps = 10

# Scores Shtuff
font = pygame.font.Font('./Pixelify_Sans/PixelifySans-VariableFont_wght.ttf', grid_size)
high_score = 0
current_score = 0

def random_apple_location(tail_locations, head_rect):
    apple_x = generate_random_location()
    apple_y = generate_random_location()
    for loc in tail_locations:
        in_tail = apple_x == loc[0] and apple_y == loc[1]
        in_head = apple_x == head_rect.x and apple_y == head_rect.y
        in_border = apple_x == grid_size or apple_y == grid_size
        if in_tail or in_head or in_border:
            apple_x = generate_random_location()
            apple_y = generate_random_location()
    return (apple_x, apple_y)

generate_random_location = lambda : random.randrange(1,((arena_size+grid_size)/grid_size).__int__())*grid_size

def determine_movement_direction(x_toggle, y_toggle):
    key = pygame.key.get_pressed()

    if y_toggle != 0:
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            y_toggle = 0
            x_toggle = -1
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            y_toggle = 0
            x_toggle = 1
    elif x_toggle != 0:
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            y_toggle = 1 
            x_toggle = 0
        if key[pygame.K_w] or key[pygame.K_UP]:
            y_toggle = -1 
            x_toggle = 0
    elif y_toggle == 0 and x_toggle == 0:
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            y_toggle = 1 
            x_toggle = 0
        if key[pygame.K_w] or key[pygame.K_UP]:
            y_toggle = -1 
            x_toggle = 0
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            y_toggle = 0
            x_toggle = -1
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            y_toggle = 0
            x_toggle = 1

    return (x_toggle, y_toggle)

def allow_for_quiting():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()

def render_background(arena_surf, arena_rect):
    screen.fill('Grey10')
    screen.blit(arena_surf, arena_rect)

def render_scores(tail_length):
    score_color = (100, 100, 100)
    score_surf = font.render((tail_length+1).__str__(), False, score_color)
    score_rect = score_surf.get_rect(topleft = (arena_center+grid_size*2,-5))
    screen.blit(score_surf, score_rect)

    high_score_color = (255,255,255)
    high_score_surf = font.render(high_score.__str__(), False, high_score_color)
    high_score_rect = high_score_surf.get_rect(topright = (arena_center-grid_size,-5))
    screen.blit(high_score_surf, high_score_rect)

def game():
    tail_locations = []
    tail_length = 0

    head_y_toggle = 0
    head_x_toggle = 0

    # Creates all game objects
    arena_surf = pygame.Surface((arena_size, arena_size)).convert_alpha()
    arena_surf.fill('Black')
    arena_rect = arena_surf.get_rect(topleft = (grid_size,grid_size))

    head_surf = pygame.Surface((grid_size-1, grid_size-1)).convert_alpha()
    head_surf.fill('Purple')
    head_rect = head_surf.get_rect(topleft = (arena_center,arena_center))

    apple_surf = pygame.Surface((grid_size-1, grid_size-1))
    apple_surf.fill('Green')
    apple_rect = apple_surf.get_rect(topleft = random_apple_location(tail_locations, head_rect))

    while running:
        render_background(arena_surf, arena_rect)

        # Stores locations for tail
        prev_head_location = (head_rect.x, head_rect.y)
        tail_locations.append(prev_head_location)
        too_many_stored_tail_locs = len(tail_locations) > tail_length
        if too_many_stored_tail_locs:
            tail_locations.pop(0)

        # Renders player movement
        head_direction = determine_movement_direction(head_x_toggle, head_y_toggle)
        (head_x_toggle, head_y_toggle) = (head_direction[0], head_direction[1])
        head_rect.x += head_direction[0]*grid_size
        head_rect.y += head_direction[1]*grid_size
        screen.blit(head_surf, head_rect)

        # Renders new tail locations
        for loc in tail_locations:
            tail_rect = head_surf.get_rect(topleft = loc)
            screen.blit(head_surf, tail_rect)
            if head_rect.colliderect(tail_rect):
                return tail_length+1

        # Renders random location for apple 
        # Adds length to tail
        player_eats_apple = head_rect.colliderect(apple_rect)
        if player_eats_apple:
            new_apple_location = random_apple_location(tail_locations, head_rect)
            (apple_rect.x, apple_rect.y) = (new_apple_location[0], new_apple_location[1])
            tail_length += 4
        screen.blit(apple_surf, apple_rect)

        render_scores(tail_length)

        # Death for player if exists arena
        player_leaving_arena = not head_rect.colliderect(arena_rect)
        if player_leaving_arena:
            return tail_length+1

        # Updates frames
        pygame.display.update()
        clock.tick(fps)
        allow_for_quiting()

# Runs game continuously
while running:
    current_score = game()
    if current_score > high_score:
        high_score = current_score
