import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Escape Room: The Quantum Paradox")

# Colors
WHITE = (255, 255, 255)
BROWN = (139,69,19)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 139)
DARK_GREEN = (0, 100, 0)
DARK_BROWN = (101, 67, 33)

class PixelRenderer:
    @staticmethod
    def draw_pixelated_rect(surface, color, rect, pixel_size=10):
        """Draw a pixelated rectangle"""
        for x in range(rect.left, rect.right, pixel_size):
            for y in range(rect.top, rect.bottom, pixel_size):
                pygame.draw.rect(surface, color, 
                    pygame.Rect(x, y, pixel_size, pixel_size))

    @staticmethod
    def draw_pixelated_door(surface, rect):
        """Draw a detailed pixelated door"""
        # Door base
        PixelRenderer.draw_pixelated_rect(surface, DARK_BROWN, rect)
        
        # Door handle
        handle_rect = pygame.Rect(
            rect.right - 30, 
            rect.centery - 10, 
            20, 
            20
        )
        PixelRenderer.draw_pixelated_rect(surface, GRAY, handle_rect, pixel_size=5)
        
        # Wood grain effect
        for i in range(rect.top, rect.bottom, 20):
            pygame.draw.line(surface, BROWN, 
                (rect.left, i), 
                (rect.right, i), 
                2
            )

    @staticmethod
    def draw_pixelated_box(surface, rect):
        """Draw a detailed pixelated box"""
        # Box base
        PixelRenderer.draw_pixelated_rect(surface, DARK_BLUE, rect)
        
        # Highlight and shadow
        lighter_blue = (100, 100, 255)
        darker_blue = (0, 0, 100)
        
        # Top highlight
        for x in range(rect.left, rect.right, 10):
            for y in range(rect.top, rect.top + 20, 10):
                pygame.draw.rect(surface, lighter_blue, 
                    pygame.Rect(x, y, 10, 10))
        
        # Bottom shadow
        for x in range(rect.left, rect.right, 10):
            for y in range(rect.bottom - 20, rect.bottom, 10):
                pygame.draw.rect(surface, darker_blue, 
                    pygame.Rect(x, y, 10, 10))

    @staticmethod
    def draw_pixelated_painting(surface, rect):
        """Draw a detailed pixelated painting"""
        # Painting frame
        frame_rect = pygame.Rect(rect.left - 10, rect.top - 10, 
                                 rect.width + 20, rect.height + 20)
        PixelRenderer.draw_pixelated_rect(surface, DARK_BROWN, frame_rect, pixel_size=8)
        
        # Painting content
        PixelRenderer.draw_pixelated_rect(surface, DARK_GREEN, rect)
        
        # Abstract pixel art elements
        colors = [GREEN, BLUE, RED]
        for _ in range(10):
            x = rect.left + random.randint(0, rect.width)
            y = rect.top + random.randint(0, rect.height)
            color = random.choice(colors)
            pygame.draw.rect(surface, color, 
                pygame.Rect(x, y, 20, 20))

    @staticmethod
    def draw_color_blocks(surface, blocks):
        """Draw pixelated color blocks"""
        colors = [RED, GREEN, BLUE]
        for block, color in zip(blocks, colors):
            # Base color
            PixelRenderer.draw_pixelated_rect(surface, color, block, pixel_size=5)
            
            # Add some random pixel noise
            for _ in range(10):
                noise_x = block.left + random.randint(0, block.width)
                noise_y = block.top + random.randint(0, block.height)
                noise_color = (
                    max(0, min(255, color[0] + random.randint(-50, 50))),
                    max(0, min(255, color[1] + random.randint(-50, 50))),
                    max(0, min(255, color[2] + random.randint(-50, 50)))
                )
                pygame.draw.rect(surface, noise_color, 
                    pygame.Rect(noise_x, noise_y, 5, 5))

class EscapeRoom:
    def __init__(self):
        # Game State
        self.current_room = 1
        self.key_found = False
        self.door_unlocked = False
        self.escaped = False
        self.notification_message = ""
        self.color_sequence = [RED, GREEN, BLUE]
        self.color_sequence_input = []
        self.riddle_solved = False
        self.keypad_solved = False
        self.input_active = False
        self.user_input = ""
        
        # Plot Twist Key
        self.key_is_hologram = False
        self.hologram_reveal_timer = 0

        # Lion Head Interaction
        self.lion_head_appeared = False
        self.lion_warning_timer = 0

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Room 1 Objects
        self.room1_objects = {
            'door': pygame.Rect(700, 250, 150, 300),
            'box': pygame.Rect(150, 450, 150, 100),
            'painting': pygame.Rect(350, 100, 200, 150),
            'color_blocks': [
                pygame.Rect(360, 120, 30, 30),  # Red
                pygame.Rect(400, 140, 30, 30),  # Green
                pygame.Rect(440, 160, 30, 30)   # Blue
            ]
        }

        # Room 2 Objects
        self.room2_objects = {
            'door': pygame.Rect(700, 250, 150, 300),
            'key_item': pygame.Rect(300, 400, 100, 100),
            'puzzle_device': pygame.Rect(200, 200, 200, 150)
        }

        # Room 3 Objects
        self.room3_objects = {
            'final_door': pygame.Rect(400, 300, 200, 400)
        }

        # Notification Area
        self.notification_box = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)

    def draw_pixelated_lion_head(self, surface):
        """Draw a pixelated lion head with a warning message"""
        # Lion head base color
        lion_color = (200, 150, 100)  # Brownish color
        lion_rect = pygame.Rect(300, 250, 200, 200)
        
        # Draw pixelated lion head
        for x in range(lion_rect.left, lion_rect.right, 10):
            for y in range(lion_rect.top, lion_rect.bottom, 10):
                pygame.draw.rect(surface, lion_color, 
                    pygame.Rect(x, y, 10, 10))
        
        # Add some mane details with darker color
        mane_color = (150, 100, 50)
        for x in range(lion_rect.left, lion_rect.right, 20):
            for y in range(lion_rect.top, lion_rect.top + 50, 10):
                pygame.draw.rect(surface, mane_color, 
                    pygame.Rect(x, y, 20, 10))
        
        # Eyes
        eye_color = (0, 0, 0)
        pygame.draw.rect(surface, eye_color, 
            pygame.Rect(lion_rect.left + 50, lion_rect.top + 80, 20, 20))
        pygame.draw.rect(surface, eye_color, 
            pygame.Rect(lion_rect.right - 70, lion_rect.top + 80, 20, 20))
        
        # Warning text
        warning_text = ["BEWARE OF KEYS", "THEY ARE NOT", "WHAT THEY SEEM"]
        for i, line in enumerate(warning_text):
            text_surface = pygame.font.Font(None, 24).render(line, True, RED)
            text_rect = text_surface.get_rect(
                center=(lion_rect.centerx, lion_rect.bottom + 30 + i * 30)
            )
            surface.blit(text_surface, text_rect)

    def dramatic_escape_sequence(self):
        """Create a more twisted narrative revelation."""
        screen.fill(BLACK)
        
        # More complex, layered narrative
        text_lines = [
            "QUANTUM PARADOX: REALITY UNRAVELED",
            "",
            "As the holographic key flickers,",
            "reality begins to deconstruct.",
            "",
            "YOU ARE NOT JUST THE ARCHITECT...",
            "",
            "You are a quantum experiment.",
            "Multiple versions of yourself",
            "exist simultaneously in this room.",
            "",
            "EACH PUZZLE YOU SOLVED",
            "WAS A MEMORY FRAGMENT",
            "FROM ALTERNATE TIMELINES.",
            "",
            "The room is your mind.",
            "The key is your consciousness.",
            "",
            "REVELATION: You never truly 'escaped'.",
            "YOU ARE TRAPPED IN AN INFINITE LOOP",
            "OF YOUR OWN CREATION.",
            "",
            "QUANTUM STATE: OBSERVED AND OBSERVER",
            "ARE THE SAME ENTITY.",
            "",
            "WAKE UP... OR CONTINUE PLAYING?"
        ]

        # Enhanced visual effect with flickering and distortion
        clock = pygame.time.Clock()
        text_y = HEIGHT
        distortion_intensity = 0
        fade_out = False

        while text_y > -800:  # Extended scroll
            screen.fill(BLACK)
            
            # Add visual distortion effect
            distortion_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            distortion_surface.fill((0, 0, 0, min(distortion_intensity, 200)))
            screen.blit(distortion_surface, (0, 0))
            
            for i, line in enumerate(text_lines):
                # Random color shifts and glitching
                color = (
                    min(255, 100 + random.randint(0, 155)), 
                    min(255, 100 + random.randint(0, 155)), 
                    min(255, 100 + random.randint(0, 155))
                )
                
                text = self.font.render(line, True, color)
                text_rect = text.get_rect(center=(
                    WIDTH//2 + random.randint(-distortion_intensity//2, distortion_intensity//2), 
                    text_y + i * 50 + random.randint(-distortion_intensity//4, distortion_intensity//4)
                ))
                screen.blit(text, text_rect)
            
            text_y -= 3  # Slower scroll
            
            # Increase distortion over time
            if not fade_out:
                distortion_intensity += 2
                if distortion_intensity > 100:
                    fade_out = True
            else:
                distortion_intensity -= 1
                if distortion_intensity < 0:
                    distortion_intensity = 0
            
            pygame.display.flip()
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # Final glitch effect
        for _ in range(20):
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            pygame.display.flip()
            pygame.time.delay(50)

        pygame.quit()
        sys.exit()

    def show_notification(self, message):
        """Displays a notification message at the bottom of the screen."""
        pygame.draw.rect(screen, BLACK, self.notification_box)
        text = self.small_font.render(message, True, WHITE)
        text_rect = text.get_rect(center=self.notification_box.center)
        screen.blit(text, text_rect)

    def show_input_box(self):
        """Displays an input box for the user."""
        input_box = pygame.Rect(20, HEIGHT - 200, WIDTH - 40, 40)
        pygame.draw.rect(screen, WHITE, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        text_surface = self.small_font.render(self.user_input, True, BLACK)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

    def draw_room1(self):
        """Draws the first room with pixelated background and interactions."""
        # Pixelated background
        for x in range(0, WIDTH, 20):
            for y in range(0, HEIGHT, 20):
                color = (
                    max(0, BLACK[0] + random.randint(-20, 20)),
                    max(0, BLACK[1] + random.randint(-20, 20)),
                    max(0, BLACK[2] + random.randint(-20, 20))
                )
                pygame.draw.rect(screen, color, pygame.Rect(x, y, 20, 20))

        # Draw pixelated objects
        PixelRenderer.draw_pixelated_door(screen, self.room1_objects['door'])
        PixelRenderer.draw_pixelated_box(screen, self.room1_objects['box'])
        PixelRenderer.draw_pixelated_painting(screen, self.room1_objects['painting'])
        
        # Draw color blocks
        PixelRenderer.draw_color_blocks(screen, self.room1_objects['color_blocks'])

        # Object labels
        labels = ['Door', 'Box', 'Painting']
        rects = [self.room1_objects['door'], self.room1_objects['box'], self.room1_objects['painting']]
        
        for label, rect in zip(labels, rects):
            label_text = self.small_font.render(label, True, WHITE)
            screen.blit(label_text, (rect.x + 20, rect.y - 30))

    def draw_room2(self):
        """Draws the second room with pixelated background."""
        # Pixelated background with variation
        for x in range(0, WIDTH, 20):
            for y in range(0, HEIGHT, 20):
                color = (
                    max(0, BLACK[0] + random.randint(-30, 30)),
                    max(0, BLACK[1] + random.randint(-30, 30)),
                    max(0, BLACK[2] + random.randint(-30, 30))
                )
                pygame.draw.rect(screen, color, pygame.Rect(x, y, 20, 20))

        # Draw pixelated door
        PixelRenderer.draw_pixelated_door(screen, self.room2_objects['door'])
        
        # Puzzle device
        PixelRenderer.draw_pixelated_rect(screen, RED, self.room2_objects['puzzle_device'], pixel_size=12)

        # Lion head interaction
        if self.lion_head_appeared:
            self.draw_pixelated_lion_head(screen)

        # Object labels
        labels = ['Exit Door', 'Puzzle Device']
        rects = [self.room2_objects['door'], self.room2_objects['puzzle_device']]
        
        for label, rect in zip(labels, rects):
            label_text = self.small_font.render(label, True, WHITE)
            screen.blit(label_text, (rect.x + 20, rect.y - 30))

    def draw_room3(self):
        """Draws the third room with the key item and hologram reveal"""
        # Pixelated background with variation
        for x in range(0, WIDTH, 20):
            for y in range(0, HEIGHT, 20):
                color = (
                    max(0, BLACK[0] + random.randint(-30, 30)),
                    max(0, BLACK[1] + random.randint(-30, 30)),
                    max(0, BLACK[2] + random.randint(-30, 30))
                )
                pygame.draw.rect(screen, color, pygame.Rect(x, y, 20, 20))

        # Pixelated key with glitch effect
        key_rect = self.room2_objects['key_item']
        PixelRenderer.draw_pixelated_rect(screen, YELLOW, key_rect, pixel_size=8)
        
        # Glitch effect on key
        for _ in range(10):
            glitch_x = key_rect.left + random.randint(0, key_rect.width)
            glitch_y = key_rect.top + random.randint(0, key_rect.height)
            glitch_color = (
                random.randint(200, 255),
                random.randint(200, 255),
                random.randint(200, 255)
            )
            pygame.draw.rect(screen, glitch_color, 
                pygame.Rect(glitch_x, glitch_y, 10, 10))

    def game_loop(self):
        clock = pygame.time.Clock()
        while not self.escaped:
            # Draw current room
            if self.current_room == 1:
                self.draw_room1()
            elif self.current_room == 2:
                self.draw_room2()
            else:
                self.draw_room3()

                # Key item interaction with hologram plot twist
                mouse_pos = pygame.mouse.get_pos()
                if self.room2_objects['key_item'].collidepoint(mouse_pos):
                    self.key_is_hologram = True
                    self.hologram_reveal_timer = pygame.time.get_ticks()
                    self.notification_message = "The key... it's changing! Is this real?"

                # Plot twist reveal
                if self.key_is_hologram and pygame.time.get_ticks() - self.hologram_reveal_timer > 2000:
                    self.dramatic_escape_sequence()

            # Show notification
            self.show_notification(self.notification_message)

            # Show input box if active
            if self.input_active:
                self.show_input_box()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.current_room == 1:
                        # Box interaction
                        if self.room1_objects['box'].collidepoint(mouse_pos):
                            if not self.riddle_solved:
                                self.notification_message = "Riddle:'Another one?? Fine...my hardest one.... only asked 23 times 'What speaks without a mouth?' "
                                self.input_active = True
                            else:
                                self.notification_message = "The box is empty now."

                        # Painting interaction
                        elif self.room1_objects['painting'].collidepoint(mouse_pos):
                            self.notification_message = "There's a note attached...It says 'Start with 1'"

                        # Color block interactions
                        for block in self.room1_objects['color_blocks']:
                            if block.collidepoint(mouse_pos):
                                self.color_sequence_input.append(
                                    RED if block == self.room1_objects['color_blocks'][0] else
                                    GREEN if block == self.room1_objects['color_blocks'][1] else
                                    BLUE
                                )

                        # Color sequence check
                        if self.color_sequence_input == self.color_sequence:
                            self.notification_message = "You solved the painting puzzle! Found a clue!"
                        elif len(self.color_sequence_input) > len(self.color_sequence):
                            self.notification_message = "Incorrect sequence. Try again!"
                            self.color_sequence_input = []

                        # Door interaction
                        if self.room1_objects['door'].collidepoint(mouse_pos):
                            if not self.keypad_solved:
                                self.notification_message = "Enter the 4-digit code."
                                self.input_active = True
                            else:
                                self.current_room = 2
                                self.notification_message = "Entering Room 2..."

                    elif self.current_room == 2:
                        # Puzzle device interaction
                        if self.room2_objects['puzzle_device'].collidepoint(mouse_pos):
                            self.lion_head_appeared = True
                            self.notification_message = "You see a strange device...You touch it...Your head appears!"
                            self.lion_warning_timer = pygame.time.get_ticks()

                        # Door interaction
                        if self.room2_objects['door'].collidepoint(mouse_pos):
                            self.current_room = 3
                            self.notification_message = "Final Room... something feels different..."

                    # Plot twist in Room 3
                    elif self.current_room == 3:
                        if self.room2_objects['door'].collidepoint(mouse_pos):
                            self.escaped = True

                # Input handling
                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                        if "Riddle" in self.notification_message:
                            if self.user_input.lower() == "echo":
                                self.riddle_solved = True
                                self.key_found = True
                                self.notification_message = "Correct! You found a key and a note....'End with 4'"
                            else:
                                self.notification_message = "Incorrect! Try again."
                        elif "code" in self.notification_message.lower():
                            if self.user_input == "1234":
                                self.keypad_solved = True
                                self.door_unlocked = True
                                self.notification_message = "Correct! The door is unlocked!"
                            else:
                                self.notification_message = "Wrong code. Try again."
                        self.user_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        self.user_input += event.unicode

            pygame.display.flip()
            clock.tick(60)

        # Victory screen
        screen.fill(BLACK)
        victory_text = self.font.render("YOU LOSE.....aint that easy", True, WHITE)
        text_rect = victory_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(victory_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

def main():
    game = EscapeRoom()
    game.game_loop()

if __name__ == "__main__":
    main()