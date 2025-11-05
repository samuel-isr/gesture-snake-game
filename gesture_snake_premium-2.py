import cv2
import mediapipe as mp
import pygame
import numpy as np
import random
import math
from collections import deque
import time

# Initialize Pygame
pygame.init()

# Game Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
GRID_SIZE = 25
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - 120) // GRID_SIZE

# Premium Modern Color Palette
BG_DARK = (18, 18, 24)
BG_GRID = (28, 28, 38)
SNAKE_GRADIENT_START = (46, 213, 115)  # Emerald green
SNAKE_GRADIENT_END = (29, 131, 72)     # Deep green
SNAKE_GLOW = (46, 213, 115)
FOOD_PRIMARY = (255, 71, 87)           # Coral red
FOOD_GLOW = (255, 107, 107)
ACCENT_GOLD = (255, 193, 7)            # Gold
ACCENT_BLUE = (66, 165, 245)           # Sky blue
TEXT_PRIMARY = (245, 245, 245)
TEXT_SECONDARY = (158, 158, 158)
PANEL_BG = (24, 24, 32)
SHADOW_COLOR = (0, 0, 0, 100)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

class Snake:
    def __init__(self):
        self.length = 3
        start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.positions = [start_pos, (start_pos[0]-1, start_pos[1]), (start_pos[0]-2, start_pos[1])]
        self.direction = RIGHT
        self.score = 0
        self.move_delay = 0
        self.move_speed = 2.5  # FASTER! Good balance
        self.alive = True
        self.death_time = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        if not self.alive:
            return False
            
        self.move_delay += 1
        if self.move_delay < self.move_speed:
            return False
        
        self.move_delay = 0
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + x) % GRID_WIDTH), (cur[1] + y) % GRID_HEIGHT)
        
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.alive = False
            self.death_time = time.time()
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True
    
    def reset(self):
        self.length = 3
        start_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.positions = [start_pos, (start_pos[0]-1, start_pos[1]), (start_pos[0]-2, start_pos[1])]
        self.direction = RIGHT
        self.score = 0
        self.alive = True
        self.death_time = 0
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            x = p[0] * GRID_SIZE
            y = p[1] * GRID_SIZE
            
            # Calculate gradient color
            ratio = i / max(len(self.positions) - 1, 1)
            color = tuple(int(SNAKE_GRADIENT_START[j] + (SNAKE_GRADIENT_END[j] - SNAKE_GRADIENT_START[j]) * ratio) 
                        for j in range(3))
            
            if i == 0:
                # Head with glow
                glow_surf = pygame.Surface((GRID_SIZE + 16, GRID_SIZE + 16), pygame.SRCALPHA)
                for radius in range(8, 0, -1):
                    alpha = int(30 * (radius / 8))
                    pygame.draw.circle(glow_surf, (*SNAKE_GLOW, alpha), 
                                     (GRID_SIZE // 2 + 8, GRID_SIZE // 2 + 8), 
                                     GRID_SIZE // 2 + radius)
                surface.blit(glow_surf, (x - 8, y - 8))
                
                # Head shape
                rect = pygame.Rect(x + 3, y + 3, GRID_SIZE - 6, GRID_SIZE - 6)
                pygame.draw.rect(surface, color, rect, border_radius=10)
                
                # Sleek eyes
                eye_size = 5
                eye_color = (30, 30, 40)
                if self.direction == RIGHT:
                    pygame.draw.circle(surface, eye_color, (x + GRID_SIZE - 8, y + 7), eye_size)
                    pygame.draw.circle(surface, eye_color, (x + GRID_SIZE - 8, y + GRID_SIZE - 7), eye_size)
                elif self.direction == LEFT:
                    pygame.draw.circle(surface, eye_color, (x + 8, y + 7), eye_size)
                    pygame.draw.circle(surface, eye_color, (x + 8, y + GRID_SIZE - 7), eye_size)
                elif self.direction == UP:
                    pygame.draw.circle(surface, eye_color, (x + 7, y + 8), eye_size)
                    pygame.draw.circle(surface, eye_color, (x + GRID_SIZE - 7, y + 8), eye_size)
                else:
                    pygame.draw.circle(surface, eye_color, (x + 7, y + GRID_SIZE - 8), eye_size)
                    pygame.draw.circle(surface, eye_color, (x + GRID_SIZE - 7, y + GRID_SIZE - 8), eye_size)
                
                # Highlight
                highlight = pygame.Rect(x + 6, y + 6, GRID_SIZE - 12, (GRID_SIZE - 12) // 3)
                pygame.draw.rect(surface, tuple(min(c + 50, 255) for c in color), 
                               highlight, border_radius=8)
            else:
                # Body segments
                rect = pygame.Rect(x + 4, y + 4, GRID_SIZE - 8, GRID_SIZE - 8)
                pygame.draw.rect(surface, color, rect, border_radius=8)
    
    def handle_keys(self, direction):
        if not self.alive:
            return
        if direction == 'UP':
            self.turn(UP)
        elif direction == 'DOWN':
            self.turn(DOWN)
        elif direction == 'LEFT':
            self.turn(LEFT)
        elif direction == 'RIGHT':
            self.turn(RIGHT)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.pulse = 0
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        
        self.pulse += 0.08
        scale = 1 + 0.15 * math.sin(self.pulse)
        
        # Glow effect
        glow_radius = int((GRID_SIZE // 2 + 6) * scale)
        glow_surf = pygame.Surface((glow_radius * 2 + 20, glow_radius * 2 + 20), pygame.SRCALPHA)
        for r in range(glow_radius, 0, -2):
            alpha = int(40 * (r / glow_radius))
            pygame.draw.circle(glow_surf, (*FOOD_GLOW, alpha), 
                             (glow_radius + 10, glow_radius + 10), r)
        surface.blit(glow_surf, (x + GRID_SIZE // 2 - glow_radius - 10, 
                                 y + GRID_SIZE // 2 - glow_radius - 10))
        
        # Food circle
        radius = int((GRID_SIZE // 2 - 4) * scale)
        center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
        pygame.draw.circle(surface, FOOD_PRIMARY, center, radius)
        
        # Highlight
        highlight_pos = (center[0] - radius // 3, center[1] - radius // 3)
        pygame.draw.circle(surface, (255, 150, 150), highlight_pos, radius // 3)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def detect_gesture(hand_landmarks, frame_width, frame_height):
    if not hand_landmarks:
        return None
    
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    
    dx = index_tip.x - index_mcp.x
    dy = index_tip.y - index_mcp.y
    
    threshold = 0.05
    
    if abs(dx) > abs(dy):
        if dx > threshold:
            return 'RIGHT'
        elif dx < -threshold:
            return 'LEFT'
    else:
        if dy > threshold:
            return 'DOWN'
        elif dy < -threshold:
            return 'UP'
    
    return None

def draw_text(surface, text, size, x, y, color=TEXT_PRIMARY, bold=False, shadow=True):
    font = pygame.font.Font(None, size)
    if bold:
        font.set_bold(True)
    
    if shadow:
        shadow_surf = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(x + 2, y + 2))
        surface.blit(shadow_surf, shadow_rect)
    
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)

def draw_stat_box(surface, x, y, width, height, label, value, value_color):
    """Draw a premium stat display box"""
    # Outer container
    box = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (35, 35, 48), box, border_radius=12)
    pygame.draw.rect(surface, (50, 50, 68), box, 2, border_radius=12)
    
    # Label
    draw_text(surface, label, 22, x + width // 2, y + 18, TEXT_SECONDARY, shadow=False)
    
    # Value
    draw_text(surface, str(value), 48, x + width // 2, y + 50, value_color, bold=True)

def draw_ui_panel(surface, snake, current_gesture, high_score):
    """Premium UI panel"""
    panel_rect = pygame.Rect(0, WINDOW_HEIGHT - 120, WINDOW_WIDTH, 120)
    pygame.draw.rect(surface, PANEL_BG, panel_rect)
    pygame.draw.line(surface, ACCENT_BLUE, (0, WINDOW_HEIGHT - 120), 
                    (WINDOW_WIDTH, WINDOW_HEIGHT - 120), 3)
    
    # Score box
    draw_stat_box(surface, 40, WINDOW_HEIGHT - 100, 200, 80, "SCORE", snake.score, ACCENT_GOLD)
    
    # High score box
    draw_stat_box(surface, 280, WINDOW_HEIGHT - 100, 200, 80, "HIGH SCORE", high_score, ACCENT_BLUE)
    
    # Length box
    draw_stat_box(surface, 520, WINDOW_HEIGHT - 100, 180, 80, "LENGTH", snake.length, SNAKE_GLOW)
    
    # Direction indicator
    direction_box = pygame.Rect(740, WINDOW_HEIGHT - 100, 220, 80)
    pygame.draw.rect(surface, (35, 35, 48), direction_box, border_radius=12)
    pygame.draw.rect(surface, (50, 50, 68), direction_box, 2, border_radius=12)
    
    draw_text(surface, "DIRECTION", 22, 850, WINDOW_HEIGHT - 82, TEXT_SECONDARY, shadow=False)
    
    if current_gesture:
        # Draw arrow
        arrow_map = {
            'UP': '↑',
            'DOWN': '↓',
            'LEFT': '←',
            'RIGHT': '→'
        }
        draw_text(surface, arrow_map.get(current_gesture, '•'), 52, 850, WINDOW_HEIGHT - 45, 
                 ACCENT_GOLD, bold=True)
    else:
        draw_text(surface, '•', 52, 850, WINDOW_HEIGHT - 45, TEXT_SECONDARY)

def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, BG_GRID, (x, 0), (x, WINDOW_HEIGHT - 120), 1)
    for y in range(0, WINDOW_HEIGHT - 120, GRID_SIZE):
        pygame.draw.line(surface, BG_GRID, (0, y), (WINDOW_WIDTH, y), 1)

def draw_start_screen(surface):
    surface.fill(BG_DARK)
    
    # Modern title
    draw_text(surface, "SNAKE", 140, WINDOW_WIDTH // 2, 180, SNAKE_GLOW, bold=True)
    draw_text(surface, "Gesture Control Edition", 36, WINDOW_WIDTH // 2, 260, TEXT_SECONDARY)
    
    # Instructions container
    container = pygame.Rect(WINDOW_WIDTH // 2 - 280, 340, 560, 240)
    pygame.draw.rect(surface, (28, 28, 38), container, border_radius=16)
    pygame.draw.rect(surface, ACCENT_BLUE, container, 2, border_radius=16)
    
    instructions = [
        ("Point your finger to control the snake", 28),
        ("Eat food to grow and score points", 28),
        ("Don't crash into yourself!", 28),
    ]
    
    y = 380
    for text, size in instructions:
        draw_text(surface, text, size, WINDOW_WIDTH // 2, y, TEXT_PRIMARY)
        y += 50
    
    # Start prompt
    if int(time.time() * 2.5) % 2 == 0:
        draw_text(surface, "SHOW YOUR HAND TO START", 42, WINDOW_WIDTH // 2, 
                 WINDOW_HEIGHT - 80, ACCENT_GOLD, bold=True)

def draw_game_over_screen(surface, final_score, high_score):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(220)
    overlay.fill(BG_DARK)
    surface.blit(overlay, (0, 0))
    
    # Game Over
    draw_text(surface, "GAME OVER", 120, WINDOW_WIDTH // 2, 200, FOOD_PRIMARY, bold=True)
    
    # Score display
    score_container = pygame.Rect(WINDOW_WIDTH // 2 - 200, 300, 400, 180)
    pygame.draw.rect(surface, (28, 28, 38), score_container, border_radius=16)
    pygame.draw.rect(surface, ACCENT_GOLD, score_container, 3, border_radius=16)
    
    draw_text(surface, "FINAL SCORE", 32, WINDOW_WIDTH // 2, 340, TEXT_SECONDARY)
    draw_text(surface, str(final_score), 90, WINDOW_WIDTH // 2, 410, ACCENT_GOLD, bold=True)
    
    # High score
    if final_score >= high_score:
        draw_text(surface, "★ NEW HIGH SCORE! ★", 38, WINDOW_WIDTH // 2, 520, ACCENT_BLUE, bold=True)
    else:
        draw_text(surface, f"High Score: {high_score}", 32, WINDOW_WIDTH // 2, 520, TEXT_SECONDARY)
    
    # Restart
    if int(time.time() * 2.5) % 2 == 0:
        draw_text(surface, "Press R to Restart", 36, WINDOW_WIDTH // 2, 600, TEXT_PRIMARY)

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake - Gesture Control")
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    cap = cv2.VideoCapture(0)
    
    running = True
    game_state = "START"
    gesture_buffer = deque(maxlen=5)
    current_gesture = None
    high_score = 0
    
    print("🎮 Snake Game - Starting...")
    
    while running:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        hand_detected = False
        if results.multi_hand_landmarks:
            hand_detected = True
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2)
                )
                
                detected = detect_gesture(hand_landmarks, frame.shape[1], frame.shape[0])
                if detected:
                    gesture_buffer.append(detected)
        
        if len(gesture_buffer) > 0:
            most_common = max(set(gesture_buffer), key=gesture_buffer.count)
            if gesture_buffer.count(most_common) >= 3:
                current_gesture = most_common
                snake.handle_keys(current_gesture)
        
        # CLEAN WEBCAM DISPLAY
        cv2.putText(frame, f"Direction: {current_gesture if current_gesture else 'None'}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Score: {snake.score}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Hand Tracking', frame)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    snake.reset()
                    food.randomize_position()
                    game_state = "PLAYING"
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
        
        if game_state == "START":
            draw_start_screen(screen)
            if hand_detected:
                game_state = "PLAYING"
                snake.reset()
        
        elif game_state == "PLAYING":
            moved = snake.move()
            
            if not snake.alive:
                game_state = "GAME_OVER"
            
            if moved and snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 10
                high_score = max(high_score, snake.score)
                food.randomize_position()
                while food.position in snake.positions:
                    food.randomize_position()
            
            screen.fill(BG_DARK)
            draw_grid(screen)
            food.draw(screen)
            snake.draw(screen)
            draw_ui_panel(screen, snake, current_gesture, high_score)
        
        elif game_state == "GAME_OVER":
            screen.fill(BG_DARK)
            draw_grid(screen)
            food.draw(screen)
            snake.draw(screen)
            draw_ui_panel(screen, snake, current_gesture, high_score)
            draw_game_over_screen(screen, snake.score, high_score)
        
        pygame.display.flip()
        clock.tick(60)
    
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    print(f"\n Final Score: {snake.score} | High Score: {high_score}")

if __name__ == "__main__":
    main()
