import pygame
import sys
from PIL import Image
import io

# Initialize pygame
pygame.init()

def load_png_with_pil(filepath):
    """Load PNG using PIL and convert to pygame surface"""
    pil_image = Image.open(filepath)
    # Convert RGBA to RGB for better compatibility
    pil_image = pil_image.convert('RGB')

    # Convert PIL image to pygame surface directly
    size = pil_image.size
    data = pil_image.tobytes()

    return pygame.image.fromstring(data, size, 'RGB')

# Load intersection background and get dimensions
intersection_img = load_png_with_pil('images/intersection.png')
WIDTH, HEIGHT = intersection_img.get_size()

# Screen settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Car Simulation")

# Load car image
car_img = load_png_with_pil('images/right/car.png')
# Scale car to appropriate size for the intersection
car_img = pygame.transform.scale(car_img, (54, 22))

# Car properties
car_x = 50
car_y = HEIGHT // 2
speed = 2
moving = True

# Clock
clock = pygame.time.Clock()
timer = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update car position
    if moving:
        car_x += speed

    # Stop and go logic
    timer += 1
    if timer == 245:  # Stop after 150 frames
        moving = False
    elif timer == 300:  # Go again after 300 frames
        moving = True

    # Reset car if it goes off screen
    if car_x > WIDTH:
        car_x = -60
        timer = 0

    # Draw
    screen.blit(intersection_img, (0, 0))
    screen.blit(car_img, (car_x, car_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
