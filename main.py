import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = WIDTH
GRAVITY = 0.5
JUMP_STRENGTH = 15
CAMERA_OFFSET_X = WIDTH // 2
CAMERA_OFFSET_Y = HEIGHT // 2
FONT_SIZE = 24
LAVA_DROP_SIZE = 10
LASER_WIDTH = 10
LASER_HEIGHT = 400  # Adjust the height of the lava laser
LASER_SPEED = 7
EARTHQUAKE_INTENSITY = 100
HOUSE_WIDTH = 100
HOUSE_HEIGHT = 150  # Adjust this as needed
HOUSE_COLOR = (100, 100, 100)
LONG_PLATFORM_WIDTH = 300  # Adjust the length as needed
LONG_PLATFORM_HEIGHT = 20
LONG_PLATFORM_COLOR = (0, 128, 128)  # Teal color for the long platform
SECOND_HOUSE_HEIGHT = 250  # Height of the new taller building
SECOND_HOUSE_COLOR = (150, 50, 50)  # Color for the new building

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Player setup
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
player_velocity = 0
on_ground = True

# Platform setup
platforms = [pygame.Rect(0, HEIGHT - PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)]

# Disaster setup
disaster_names = ["Lava Rain", "Earthquake", "Fire", "Thunderstorm"]
current_disaster = None
lava_drops = []
earthquake_offset = 0
earthquake_direction = 1  # Direction of earthquake effect
fire_bricks = []
lava_strikes = []
thunderstorm_start = pygame.time.get_ticks()
# State Variables for Disasters
last_lava_drops = []
last_fire_bricks = []
last_lava_strikes = []

# House setup
house_x = WIDTH // 4
house_y = HEIGHT - PLATFORM_HEIGHT - HOUSE_HEIGHT
house = pygame.Rect(house_x, house_y, HOUSE_WIDTH, HOUSE_HEIGHT)

# Second building setup
second_building_x = WIDTH // 2 + LONG_PLATFORM_WIDTH
second_building_y = HEIGHT - PLATFORM_HEIGHT - SECOND_HOUSE_HEIGHT
second_building = pygame.Rect(second_building_x, second_building_y, HOUSE_WIDTH, SECOND_HOUSE_HEIGHT)

# Long platform setup
long_platform = pygame.Rect(WIDTH // 2 - LONG_PLATFORM_WIDTH // 2, HEIGHT // 2, LONG_PLATFORM_WIDTH, LONG_PLATFORM_HEIGHT)

# Font setup
font = pygame.font.Font(None, FONT_SIZE)

# Timer setup
disaster_timer_start = pygame.time.get_ticks()
DISASTER_INTERVAL = 5000  # 5 seconds

# Function to handle player death
def player_death():
    print("Player died!")
    # Reset player position, or implement other death mechanics
    player.x, player.y = WIDTH // 2, HEIGHT // 2

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and on_ground:
                player_velocity = -JUMP_STRENGTH
                on_ground = False

    # Disaster timer
    if pygame.time.get_ticks() - disaster_timer_start > DISASTER_INTERVAL:
        current_disaster = random.choice(disaster_names)
        disaster_timer_start = pygame.time.get_ticks()
        
        # Earthquake
        if current_disaster == "Earthquake":
            earthquake_offset += 2 * earthquake_direction  # Adjust the earthquake effect
            if abs(earthquake_offset) > EARTHQUAKE_INTENSITY:
                earthquake_direction *= -1  # Reverse the direction when intensity limit is reached

    # Lava Rain
    if current_disaster == "Lava Rain":
        if random.randint(0, 20) == 0:  # Random chance to spawn a lava drop
            lava_drops.append(pygame.Rect(random.randint(0, WIDTH), 0, LAVA_DROP_SIZE, LAVA_DROP_SIZE))
        for lava in lava_drops:
            lava.y += 2  # Speed of lava drop
            if lava.y > HEIGHT:
                lava_drops.remove(lava)
            if player.colliderect(lava):  # Check for collision with lava
                player_death()
    # Tsunami
    if current_disaster == "Tsunami":
        tsunami_speed = 5  # Adjust the speed as needed
        tsunami_width = 30  # Adjust the width of the tsunami brick
        tsunami_height = 400  # Adjust the height of the tsunami brick

        # Create the tsunami brick
        tsunami_brick = pygame.Rect(0, HEIGHT - PLATFORM_HEIGHT - tsunami_height, tsunami_width, tsunami_height)

        # Move the tsunami brick left and right
        tsunami_brick.x += tsunami_speed

        # Reverse the direction when the brick reaches the screen edges
        if tsunami_brick.left <= 0 or tsunami_brick.right >= WIDTH:
            tsunami_speed *= -1

    # Check for collision with the player
        if player.colliderect(tsunami_brick):
            player_death()

    # Draw the tsunami brick
        adjusted_tsunami_brick = tsunami_brick.move(camera_offset)
        pygame.draw.rect(screen, (255, 0, 0), adjusted_tsunami_brick)


    # Fire (Randomly Placed Lava Bricks)
    if current_disaster == "Fire":
        if random.randint(0, 30) == 0:  # Random chance to spawn a fire brick
            fire_bricks.append(pygame.Rect(random.randint(0, WIDTH), HEIGHT - PLATFORM_HEIGHT, LAVA_DROP_SIZE, LAVA_DROP_SIZE))

        for fire_brick in fire_bricks:
            fire_brick.inflate_ip(2, 2)  # Increase the size of the fire brick
            fire_brick.y -= 2  # Move the fire brick upward
            if fire_brick.width >= 230:  # Adjust the size limit as needed
                fire_bricks.remove(fire_brick)  # Remove the fire brick when it reaches a certain size
            if player.colliderect(fire_brick):  # Check for collision with fire brick
                player_death()

    # Thunderstorm (Infinitely Tall Lava)
    if current_disaster == "Thunderstorm":
        if pygame.time.get_ticks() - thunderstorm_start > 2000:  # Spawn lava every 2 seconds
            lava_strikes.append(pygame.Rect(random.randint(0, WIDTH), 0, LASER_WIDTH, HEIGHT))
            thunderstorm_start = pygame.time.get_ticks()
        for lava_strike in lava_strikes:
            lava_strike.y += LASER_SPEED  # Speed of lava strike
            if player.colliderect(lava_strike):  # Check for collision with lava strike
                player_death()

    # Earthquake
    if current_disaster == "Earthquake":
        earthquake_offset += 2 * earthquake_direction  # Adjust the earthquake effect
        if abs(earthquake_offset) > EARTHQUAKE_INTENSITY:
            earthquake_direction *= -1  # Reverse the direction when intensity limit is reached

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_d]:
        player.x += 5

    # Camera follows the player and earthquake
    camera_offset = [CAMERA_OFFSET_X - player.x + earthquake_offset, CAMERA_OFFSET_Y - player.y]

    # Draw platforms
    for platform in platforms:
        adjusted_platform = platform.move(camera_offset)
        pygame.draw.rect(screen, (0, 255, 0), adjusted_platform)

    # Draw player
    adjusted_player = player.move(camera_offset)
    pygame.draw.rect(screen, (255, 255, 255), adjusted_player)

    # Draw the house
    adjusted_house = house.move(camera_offset)
    pygame.draw.rect(screen, HOUSE_COLOR, adjusted_house)

    # Draw the second building
    adjusted_second_building = second_building.move(camera_offset)
    pygame.draw.rect(screen, SECOND_HOUSE_COLOR, adjusted_second_building)

    # Draw the long platform
    adjusted_long_platform = long_platform.move(camera_offset)
    pygame.draw.rect(screen, LONG_PLATFORM_COLOR, adjusted_long_platform)

    # Apply gravity
    player_velocity += GRAVITY
    player.y += player_velocity

    # Collision with platform
    on_ground = False
    if player.colliderect(platforms[0]) and player_velocity > 0:
        player.y = platforms[0].y - PLAYER_SIZE
        player_velocity = 0
        on_ground = True

    # Collision with house
    if player.colliderect(house):
        if player_velocity > 0:
            player.y = house.y - PLAYER_SIZE
            player_velocity = 0
            on_ground = True
        else:
            player.y = house.y + HOUSE_HEIGHT

    # Collision with second building
    if player.colliderect(second_building):
        if player_velocity > 0:
            player.y = second_building.y - PLAYER_SIZE
            player_velocity = 0
            on_ground = True
        else:
            player.y = second_building.y + SECOND_HOUSE_HEIGHT

    # Collision with long platform
    if player.colliderect(long_platform) and player_velocity > 0:
        player.y = long_platform.y - PLAYER_SIZE
        player_velocity = 0
        on_ground = True

    # Draw lava rain
    if current_disaster == "Lava Rain":
        for lava in lava_drops:
            adjusted_lava = lava.move(camera_offset)
            pygame.draw.rect(screen, (255, 0, 0), adjusted_lava)

    # Draw fire bricks
    if current_disaster == "Fire":
        for fire_brick in fire_bricks:
            adjusted_fire_brick = fire_brick.move(camera_offset)
            pygame.draw.rect(screen, (255, 0, 0), adjusted_fire_brick)

    # Draw thunderstorm
    if current_disaster == "Thunderstorm":
        for lava_strike in lava_strikes:
            adjusted_lava_strike = lava_strike.move(camera_offset)
            pygame.draw.rect(screen, (255, 0, 0), adjusted_lava_strike)

    # Display disaster text
    if current_disaster:
        disaster_text = font.render(f"Disaster: {current_disaster}", True, (255, 0, 0))
        screen.blit(disaster_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap framerate
    pygame.time.Clock().tick(60)
