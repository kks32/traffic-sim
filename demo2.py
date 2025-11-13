import pygame
import sys
from PIL import Image

# Initialize pygame
pygame.init()

def load_png_with_pil(filepath):
    """Load PNG using PIL and convert to pygame surface"""
    pil_image = Image.open(filepath)
    pil_image = pil_image.convert('RGB')
    size = pil_image.size
    data = pil_image.tobytes()
    return pygame.image.fromstring(data, size, 'RGB')

# Load intersection background
intersection_img = load_png_with_pil('images/intersection.png')
WIDTH, HEIGHT = intersection_img.get_size()

# Screen settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulation - Step 2")

# Load traffic signal images
red_signal = load_png_with_pil('images/signals/red.png')
green_signal = load_png_with_pil('images/signals/green.png')

# Simple Vehicle class
class Vehicle:
    def __init__(self, x, y, image, speed):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.stopped = False
        self.width = image.get_rect().width

    def move(self, stop_x, vehicles):
        """Move vehicle, stop at stop line if signal is red or if there's a vehicle ahead"""
        # Check if there's a vehicle ahead in the same lane
        vehicle_ahead = None
        min_distance = float('inf')

        for other in vehicles:
            if other != self and other.y == self.y:  # Same lane
                if other.x > self.x:  # Ahead of this vehicle
                    distance = other.x - self.x
                    if distance < min_distance:
                        min_distance = distance
                        vehicle_ahead = other

        # Calculate safe following distance for vehicle ahead
        gap = 15
        if vehicle_ahead:
            safe_distance = vehicle_ahead.x - self.width - gap
        else:
            safe_distance = float('inf')

        # If signal is green
        if signal_state == 'green':
            # Move but don't hit vehicle ahead
            if self.x + self.speed < safe_distance:
                self.x += self.speed
            self.stopped = False
        # If signal is red
        elif signal_state == 'red':
            # Determine stopping position (stop line or behind vehicle ahead, whichever is closer)
            if vehicle_ahead:
                target_stop = min(stop_x, safe_distance)
            else:
                target_stop = stop_x

            # If haven't reached stopping position yet, keep moving
            if self.x + self.speed < target_stop:
                self.x += self.speed
            else:
                # Stop at the position
                self.stopped = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Load car images
car_img = load_png_with_pil('images/right/car.png')
car_img = pygame.transform.scale(car_img, (54, 22))

bus_img = load_png_with_pil('images/right/bus.png')
bus_img = pygame.transform.scale(bus_img, (80, 22))

truck_img = load_png_with_pil('images/right/truck.png')
truck_img = pygame.transform.scale(truck_img, (80, 22))

# Define lane y-positions (2 lanes going right)
lanes = {
    'car': 370,    # Car lane
    'truck': 398   # Truck lane
}

# Create vehicles in different lanes
vehicles = []
vehicles.append(Vehicle(50, lanes['car'], car_img, 2))         # Car in car lane
vehicles.append(Vehicle(-100, lanes['truck'], truck_img, 1.5)) # Truck in truck lane
vehicles.append(Vehicle(-300, lanes['car'], car_img, 2.2))     # Another car in car lane
vehicles.append(Vehicle(-500, lanes['truck'], truck_img, 1.6)) # Another truck in truck lane

# Traffic signal state
signal_state = 'red'
signal_timer = 0
signal_x = 500  # Stop line x-coordinate
signal_y = 230  # Signal display position

# Clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update signal timing (red for 4 seconds, then green)
    signal_timer += 1
    if signal_state == 'red' and signal_timer > 480:  # 4 seconds at 60 FPS
        signal_state = 'green'

    # Update vehicles
    for vehicle in vehicles:
        vehicle.move(signal_x, vehicles)
        # Reset vehicle if it goes off screen
        if vehicle.x > WIDTH:
            vehicle.x = -100
            vehicle.stopped = False

    # Draw everything
    screen.blit(intersection_img, (0, 0))

    # Draw signal
    if signal_state == 'red':
        screen.blit(red_signal, (signal_x - 10, signal_y))
    else:
        screen.blit(green_signal, (signal_x - 10, signal_y))

    # Draw vehicles
    for vehicle in vehicles:
        vehicle.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
