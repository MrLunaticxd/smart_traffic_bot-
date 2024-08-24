import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1080, 720
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load the vehicle images
try:
    vehicle_image_vertical = pygame.image.load('assets/vertical_car.png')
    vehicle_image_vertical = pygame.transform.scale(vehicle_image_vertical, (20, 40))
    vehicle_image_horizontal = pygame.image.load('assets/horizontal_car.png')
    vehicle_image_horizontal = pygame.transform.scale(vehicle_image_horizontal, (40, 20))
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

# TrafficLight will control traffic light behavior 
# [N.B: Bypass here reffers to the when the bot will change the light without the 
# time quota being fulfilled for a lane]
class TrafficLight:
    def __init__(self, x, y, linked_lane):
        self.x = x
        self.y = y
        self.color = RED
        self.timer = 0
        self.linked_lane = linked_lane
        self.bypassed = False
        self.bypass_start_time = 0  # Timestamp when bypass occurred

    def update(self, vehicle_count):
        self.timer += clock.get_time()

        if vehicle_count > 10:
            self.color = GREEN
            self.bypassed = True
            self.bypass_start_time = time.time()  # Record the time bypass starts
        else:
            if self.color == RED and self.timer >= 30000:  # Change to green after 30 seconds
                self.color = GREEN
                self.bypassed = False
                self.timer = 0
            elif self.color == GREEN and self.timer >= 30000:  # Change to red after 30 seconds
                self.color = RED
                self.timer = 0

#Traffic lights have been drawn
    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x, self.y, 50, 150))
        if self.color == RED:
            pygame.draw.circle(window, RED, (self.x + 25, self.y + 25), 20)
        elif self.color == GREEN:
            pygame.draw.circle(window, GREEN, (self.x + 25, self.y + 125), 20)

        # Optionally, draw "Bypass" text
        if self.bypassed:
            # Check if 2 seconds have passed since the bypass started
            if time.time() - self.bypass_start_time < 2:
                font = pygame.font.SysFont(None, 36)
                text = font.render("Bypass", True, GREEN)
                window.blit(text, (self.x - 10, self.y + 160))
            else:
                self.bypassed = False  # Reset bypass flag after 2 seconds

# Vehicle class controls vehecle behavior
class Vehicle:
    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # "up" or "left"
        self.stopped = False  # To track if the vehicle is stopped at a red light

    def update(self, traffic_light_vertical, traffic_light_horizontal):
        if self.direction == "up":
            # Stop at the red light
            if self.y < traffic_light_vertical.y + 150 and self.y > traffic_light_vertical.y and traffic_light_vertical.color == RED:
                self.stopped = True
            elif self.stopped and traffic_light_vertical.color == GREEN:
                self.stopped = False
            if not self.stopped:
                self.y -= self.speed
            # Remove vehicle if it has passed the screen
            if self.y < 0:
                return True
        elif self.direction == "left":
            # Stop at the red light
            if self.x < traffic_light_horizontal.x + 50 and self.x > traffic_light_horizontal.x and traffic_light_horizontal.color == RED:
                self.stopped = True
            elif self.stopped and traffic_light_horizontal.color == GREEN:
                self.stopped = False
            if not self.stopped:
                self.x -= self.speed
            # Remove vehicle if it has passed the screen
            if self.x < 0:
                return True
        return False

    def draw(self, window):
        if self.direction == "up":
            window.blit(vehicle_image_vertical, (self.x, self.y))
        else:
            window.blit(vehicle_image_horizontal, (self.x, self.y))

def draw_vehicle_count(window, vehicle_count_vertical, vehicle_count_horizontal):
    font = pygame.font.SysFont(None, 36)
    vertical_text = font.render(f'Vehicles (Vertical): {vehicle_count_vertical}', True, WHITE)
    horizontal_text = font.render(f'Vehicles (Horizontal): {vehicle_count_horizontal}', True, WHITE)
    window.blit(vertical_text, (10, 10))
    window.blit(horizontal_text, (10, 50))

def main():
    vehicles_vertical = []  
    vehicles_horizontal = []

    traffic_light_vertical = TrafficLight(width//2 - 25, height//2 - 75, vehicles_vertical)
    traffic_light_horizontal = TrafficLight(width//2 + 75, height//2 - 25, vehicles_horizontal)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update vehicle counts
        vehicle_count_vertical = len(vehicles_vertical)
        vehicle_count_horizontal = len(vehicles_horizontal)

        # Update traffic lights based on vehicle count
        traffic_light_vertical.update(vehicle_count_vertical)
        traffic_light_horizontal.update(vehicle_count_horizontal)

        # Switch the light colors based on the vertical light
        if traffic_light_vertical.color == GREEN:
            traffic_light_horizontal.color = RED
        else:
            traffic_light_horizontal.color = GREEN

        # Update vehicles
        for vehicle in vehicles_vertical[:]:
            if vehicle.update(traffic_light_vertical, traffic_light_horizontal):
                vehicles_vertical.remove(vehicle)
        for vehicle in vehicles_horizontal[:]:
            if vehicle.update(traffic_light_vertical, traffic_light_horizontal):
                vehicles_horizontal.remove(vehicle)

        # Add new vehicles
        if random.randint(0, 400) < 5:
            vehicles_vertical.append(Vehicle(width//2 - 10, height, random.randint(1, 3), "up"))
        if random.randint(0, 400) < 5:
            vehicles_horizontal.append(Vehicle(width, height//2 - 10, random.randint(1, 3), "left"))

        # Draw everything
        window.fill(BLACK)

        traffic_light_vertical.draw(window)
        traffic_light_horizontal.draw(window)

        for vehicle in vehicles_vertical:
            vehicle.draw(window)
        for vehicle in vehicles_horizontal:
            vehicle.draw(window)

        # Draw vehicle counts
        draw_vehicle_count(window, vehicle_count_vertical, vehicle_count_horizontal)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
