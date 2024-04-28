import math
import random
import pygame
import sys

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (0, 0, 128), (128, 0, 128)]  # Red, orange, yellow, green, blue, navy, purple

class Target:
    def __init__(self, speed, lives):
        # Initialize target properties
        self.radius = random.randint(10, 30)  # Randomize the radius of the target
        self.x = random.randint(self.radius, WIDTH - self.radius)  # Randomize the x-coordinate of the target within the screen bounds
        self.y = random.randint(self.radius, HEIGHT - self.radius)  # Randomize the y-coordinate of the target within the screen bounds
        self.speed = speed  # Speed of the target
        self.direction = random.uniform(0, math.pi*2)  # Assign a random direction (in radians)
        self.color = random.choice(COLORS)  # Select a random color for the target
        self.lives = lives  # Number of lives for the target

    def move(self):
        # Move the target
        self.x += self.speed * math.cos(self.direction)  # Update the x-coordinate
        self.y += self.speed * math.sin(self.direction)  # Update the y-coordinate

        # Prevent target from going off the screen
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.direction = math.pi - self.direction
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.direction = -self.direction

        # If difficulty is hard, randomly change direction more often
        if self.lives == 2:
            if random.random() < 0.05:  # 5% chance to change direction
                self.direction = random.uniform(0, math.pi*2)

    def draw(self, screen):
        # Draw the target on the screen
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Sound:
    def __init__(self, sound_file):
        # Initialize sound object
        self.sound = pygame.mixer.Sound(sound_file)

    def play(self):
        # Play the sound
        self.sound.play()

def update_score(score):
    # Update and display the score
    return f"Score: {score}"  # Show only the score by removing the total_targets part

def update_time(game_time, elapsed_time):
    # Update and display the remaining time
    remaining_time = max(0, game_time - elapsed_time)
    return f"Time: {remaining_time:.1f}s"  # Show time with one decimal place

def draw_result_screen(screen, font, score):
    # Display the game over screen with score
    screen.fill(WHITE)
    result_text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
    screen.blit(result_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)

def welcome_screen(screen, font):
    # Display the welcome screen
    screen.fill(WHITE)
    welcome_text = font.render("Welcome to Balloon Burst Game!", True, (0, 0, 0))
    start_text = font.render("Select difficulty: Press 'E' for Easy, 'M' for Medium, 'H' for Hard", True, (0, 0, 0))
    welcome_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(welcome_text, welcome_rect)
    screen.blit(start_text, start_rect)
    pygame.display.flip()

    difficulty = None
    while difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    difficulty = "easy"
                elif event.key == pygame.K_m:
                    difficulty = "medium"
                elif event.key == pygame.K_h:
                    difficulty = "hard"

    return difficulty

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Balloon Burst Game")
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()

    difficulty = welcome_screen(screen, font)

    # Main game loop after the game starts
    targets = []
    lives = 5 if difficulty == "easy" else 3 if difficulty == "medium" else 2
    score = 0
    speed = 1 if difficulty == "easy" else 2 if difficulty == "medium" else 4

    # Game time (in seconds)
    game_time = 30
    start_time = pygame.time.get_ticks()

    game_over = False

    while not game_over:
        screen.fill(WHITE)

        # Add new targets
        if len(targets) < 10:  # Always 10 targets on screen
            targets.append(Target(speed, lives))

        # Move and draw targets
        for target in targets:
            target.move()
            target.draw(screen)

        # Display lives
        lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
        screen.blit(lives_text, (WIDTH - 150, 10))

        # Display score
        score_text = font.render(update_score(score), True, (255, 0, 0))
        screen.blit(score_text, (10, 10))

        # Display remaining time
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert milliseconds to seconds
        time_text = font.render(update_time(game_time, elapsed_time), True, (255, 0, 0))
        screen.blit(time_text, (WIDTH - 300, 10))

        # Update the display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_target = None
                for target in targets[:]:  # Create a copy of the list with slicing [:]
                    distance = math.sqrt((target.x - mouse_x)**2 + (target.y - mouse_y)**2)
                    if distance < target.radius:
                        clicked_target = target
                        targets.remove(target)
                        score += 1
                        game_time += 0.5  # Increase time by half a second
                        break  # Only check one target for clicking
                if clicked_target is None:
                    lives -= 1
                    if lives == 0:
                        # Only display the score and restart or quit the game
                        draw_result_screen(screen, font, score)
                        game_over = True

        # End the game when time runs out or all targets are hit
        if update_time(game_time, elapsed_time) == "Time: 0s":
            # Only display the score and restart or quit the game
            draw_result_screen(screen, font, score)
            game_over = True

        clock.tick(60)  # Set the game speed to 60 frames per second

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()




