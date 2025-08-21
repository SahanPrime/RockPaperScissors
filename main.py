import pygame
import random
import sys
from collections import deque, defaultdict, Counter
import time
import os

# Handle the temporary directory issue with PyInstaller
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock-Paper-Scissors - Enhanced AI")

# Colors
BACKGROUND = (25, 25, 40)
TEXT_COLOR = (240, 240, 255)
HIGHLIGHT = (70, 200, 220)
WIN_COLOR = (100, 230, 100)
LOSE_COLOR = (230, 100, 100)
DRAW_COLOR = (220, 220, 100)
BUTTON_COLOR = (50, 120, 180)
BUTTON_HOVER = (70, 150, 210)
ROUND_COLOR = (180, 120, 220)
TITLE_COLOR = (220, 180, 100)
CREATOR_COLOR = (150, 200, 250)
PATTERN_COLOR = (180, 220, 180)
PREDICTION_COLOR = (255, 180, 100)

# Fonts
try:
    title_font = pygame.font.SysFont('arial', 64, bold=True)
    creator_font = pygame.font.SysFont('arial', 28, italic=True)
    choice_font = pygame.font.SysFont('arial', 36)
    stats_font = pygame.font.SysFont('arial', 24)
    result_font = pygame.font.SysFont('arial', 42, bold=True)
    round_font = pygame.font.SysFont('arial', 30, bold=True)
    small_font = pygame.font.SysFont('arial', 20)
except:
    # Fallback to default fonts if specified fonts aren't available
    title_font = pygame.font.SysFont(None, 64, bold=True)
    creator_font = pygame.font.SysFont(None, 28, italic=True)
    choice_font = pygame.font.SysFont(None, 36)
    stats_font = pygame.font.SysFont(None, 24)
    result_font = pygame.font.SysFont(None, 42, bold=True)
    round_font = pygame.font.SysFont(None, 30, bold=True)
    small_font = pygame.font.SysFont(None, 20)

# Game states
TITLE_SCREEN = 0
GAME_SCREEN = 1
current_state = TITLE_SCREEN
title_display_time = 0
title_duration = 3.0

# Game variables
player_score = 0
ai_score = 0
draws = 0
rounds_played = 0
max_rounds = 25
player_choice = None
ai_choice = None
result = None
game_over = False
last_result_time = 0
result_display_time = 2.0

# Enhanced AI variables
move_history = []  # Store actual move strings
prediction_history = []  # Track AI predictions and their success
current_predictions = {}  # Multiple prediction methods
ai_strategies_success = defaultdict(lambda: {'correct': 0, 'total': 0})
last_ai_prediction = None
last_prediction_method = None

# Game images
choice_images = {
    'rock': pygame.Surface((120, 120)),
    'paper': pygame.Surface((120, 120)),
    'scissors': pygame.Surface((120, 120))
}

# Draw shapes on the choice images
pygame.draw.circle(choice_images['rock'], (180, 180, 200), (60, 60), 50)
pygame.draw.rect(choice_images['paper'], (240, 240, 240), (15, 15, 90, 90))
pygame.draw.line(choice_images['scissors'], (200, 200, 220), (30, 30), (90, 90), 8)
pygame.draw.line(choice_images['scissors'], (200, 200, 220), (30, 90), (90, 30), 8)

class EnhancedPatternAI:
    def __init__(self):
        self.move_history = []
        self.strategies = {
            'frequency': {'weight': 1.0, 'success': 0, 'attempts': 0},
            'anti_frequency': {'weight': 1.0, 'success': 0, 'attempts': 0},
            'alternating': {'weight': 1.0, 'success': 0, 'attempts': 0},
            'repeating': {'weight': 1.0, 'success': 0, 'attempts': 0},
            'cycle': {'weight': 1.0, 'success': 0, 'attempts': 0},
            'reactive': {'weight': 1.0, 'success': 0, 'attempts': 0},
            'markov_2': {'weight': 1.0, 'success': 0, 'attempts': 0},
            'markov_3': {'weight': 1.0, 'success': 0, 'attempts': 0},
            'random': {'weight': 0.3, 'success': 0, 'attempts': 0}
        }
        self.last_prediction = None
        self.last_method = None
    
    def add_move(self, move):
        """Add a move to history and update strategy success rates"""
        self.move_history.append(move)
        if len(self.move_history) > 50:  # Keep last 50 moves
            self.move_history = self.move_history[-50:]
        
        # Update success rate for last prediction
        if self.last_prediction and self.last_method:
            if move == self.last_prediction:
                self.strategies[self.last_method]['success'] += 1
            self.strategies[self.last_method]['attempts'] += 1
            
            # Update weights based on success rate
            if self.strategies[self.last_method]['attempts'] >= 3:
                success_rate = self.strategies[self.last_method]['success'] / self.strategies[self.last_method]['attempts']
                self.strategies[self.last_method]['weight'] = max(0.1, success_rate * 2)
    
    def predict_frequency_based(self):
        """Predict based on most frequent move"""
        if len(self.move_history) < 3:
            return None
        
        counter = Counter(self.move_history[-15:])  # Look at last 15 moves
        most_common = counter.most_common(1)[0][0]
        return most_common
    
    def predict_anti_frequency(self):
        """Predict least frequent move (counter to frequency bias)"""
        if len(self.move_history) < 3:
            return None
        
        counter = Counter(self.move_history[-15:])
        least_common = counter.most_common()[-1][0]
        return least_common
    
    def predict_alternating(self):
        """Detect and predict alternating patterns (ABAB, ABCABC, etc.)"""
        if len(self.move_history) < 4:
            return None
        
        # Check for 2-move alternating pattern
        last_4 = self.move_history[-4:]
        if (last_4[0] == last_4[2] and last_4[1] == last_4[3] and 
            last_4[0] != last_4[1]):
            # Continue the alternating pattern
            return last_4[0]  # Next should be the first move in the pattern
        
        # Check for 3-move alternating pattern
        if len(self.move_history) >= 6:
            last_6 = self.move_history[-6:]
            if (last_6[0] == last_6[3] and last_6[1] == last_6[4] and 
                last_6[2] == last_6[5] and len(set(last_6[:3])) >= 2):
                return last_6[0]  # Continue ABC pattern
        
        return None
    
    def predict_repeating(self):
        """Detect repeating patterns"""
        if len(self.move_history) < 2:
            return None
        
        # Check if last 2-3 moves are the same
        if len(self.move_history) >= 3 and all(m == self.move_history[-1] for m in self.move_history[-3:]):
            return self.move_history[-1]  # Continue repeating
        elif len(self.move_history) >= 2 and self.move_history[-1] == self.move_history[-2]:
            return self.move_history[-1]  # Start of repeat
        
        return None
    
    def predict_cycle(self):
        """Detect cycle patterns like RPS-RPS-RPS"""
        if len(self.move_history) < 6:
            return None
        
        # Check for 3-move cycles
        for cycle_length in [3, 4, 5]:
            if len(self.move_history) >= cycle_length * 2:
                recent = self.move_history[-cycle_length * 2:]
                first_cycle = recent[:cycle_length]
                second_cycle = recent[cycle_length:]
                
                if first_cycle == second_cycle:
                    # Found a cycle, predict next move in cycle
                    position_in_cycle = len(self.move_history) % cycle_length
                    if position_in_cycle < len(first_cycle):
                        return first_cycle[position_in_cycle]
        
        return None
    
    def predict_reactive(self):
        """Predict based on reaction to AI's last move"""
        if len(self.move_history) < 2:
            return None
        
        # This would need AI's move history to work properly
        # For now, assume player might copy their own last move
        return self.move_history[-1]
    
    def predict_markov_2(self):
        """2nd order Markov chain: predict based on last 2 moves"""
        if len(self.move_history) < 3:
            return None
        
        # Find all occurrences of the last 2 moves
        pattern = tuple(self.move_history[-2:])
        next_moves = []
        
        for i in range(len(self.move_history) - 2):
            if tuple(self.move_history[i:i+2]) == pattern:
                if i + 2 < len(self.move_history):
                    next_moves.append(self.move_history[i + 2])
        
        if next_moves:
            return Counter(next_moves).most_common(1)[0][0]
        return None
    
    def predict_markov_3(self):
        """3rd order Markov chain: predict based on last 3 moves"""
        if len(self.move_history) < 4:
            return None
        
        pattern = tuple(self.move_history[-3:])
        next_moves = []
        
        for i in range(len(self.move_history) - 3):
            if tuple(self.move_history[i:i+3]) == pattern:
                if i + 3 < len(self.move_history):
                    next_moves.append(self.move_history[i + 3])
        
        if next_moves:
            return Counter(next_moves).most_common(1)[0][0]
        return None
    
    def get_weighted_prediction(self):
        """Get prediction using weighted ensemble of all strategies"""
        if len(self.move_history) < 2:
            return random.choice(['rock', 'paper', 'scissors']), 'random'
        
        predictions = {}
        
        # Get predictions from all strategies
        predictions['frequency'] = self.predict_frequency_based()
        predictions['anti_frequency'] = self.predict_anti_frequency()
        predictions['alternating'] = self.predict_alternating()
        predictions['repeating'] = self.predict_repeating()
        predictions['cycle'] = self.predict_cycle()
        predictions['reactive'] = self.predict_reactive()
        predictions['markov_2'] = self.predict_markov_2()
        predictions['markov_3'] = self.predict_markov_3()
        predictions['random'] = random.choice(['rock', 'paper', 'scissors'])
        
        # Weight predictions by strategy success
        weighted_votes = defaultdict(float)
        method_contributions = defaultdict(list)
        
        for method, prediction in predictions.items():
            if prediction:
                weight = self.strategies[method]['weight']
                weighted_votes[prediction] += weight
                method_contributions[prediction].append(method)
        
        if not weighted_votes:
            return random.choice(['rock', 'paper', 'scissors']), 'random'
        
        # Choose prediction with highest weight
        best_prediction = max(weighted_votes.items(), key=lambda x: x[1])
        predicted_move = best_prediction[0]
        contributing_methods = method_contributions[predicted_move]
        
        # Store for success tracking
        self.last_prediction = predicted_move
        self.last_method = contributing_methods[0] if contributing_methods else 'random'
        
        return predicted_move, self.last_method
    
    def get_counter_move(self, predicted_player_move):
        """Get the move that beats the predicted player move"""
        counters = {
            'rock': 'paper',
            'paper': 'scissors',
            'scissors': 'rock'
        }
        return counters.get(predicted_player_move, random.choice(['rock', 'paper', 'scissors']))
    
    def get_ai_choice(self):
        """Main AI decision function"""
        if len(self.move_history) < 2:
            return random.choice(['rock', 'paper', 'scissors'])
        
        # Use weighted prediction 85% of the time
        if random.random() < 0.85:
            predicted_move, method = self.get_weighted_prediction()
            return self.get_counter_move(predicted_move)
        else:
            # Random move 15% of the time to stay unpredictable
            return random.choice(['rock', 'paper', 'scissors'])

# Initialize AI
ai_brain = EnhancedPatternAI()

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, HIGHLIGHT, self.rect, 3, border_radius=10)
        
        text_surf = choice_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                self.action()
                return True
        return False

# Create buttons
rock_button = Button(150, 450, 120, 50, "Rock", lambda: set_player_choice('rock'))
paper_button = Button(340, 450, 120, 50, "Paper", lambda: set_player_choice('paper'))
scissors_button = Button(530, 450, 120, 50, "Scissors", lambda: set_player_choice('scissors'))

def set_player_choice(choice):
    global player_choice, ai_choice, result, player_score, ai_score, draws, rounds_played, game_over, last_result_time
    
    if game_over or result:  # Prevent multiple clicks
        return
    
    player_choice = choice
    
    # AI makes its choice BEFORE seeing player's choice (prediction happens here)
    ai_choice = ai_brain.get_ai_choice()
    
    # Add player's move to AI's learning history
    ai_brain.add_move(choice)
    
    # Determine winner
    if player_choice == ai_choice:
        result = "draw"
        draws += 1
    elif (player_choice == 'rock' and ai_choice == 'scissors') or \
         (player_choice == 'paper' and ai_choice == 'rock') or \
         (player_choice == 'scissors' and ai_choice == 'paper'):
        result = "win"
        player_score += 1
    else:
        result = "lose"
        ai_score += 1
    
    rounds_played += 1  # Count all rounds including draws
    last_result_time = time.time()
    
    # Check if game is over
    if rounds_played >= max_rounds:
        game_over = True

def reset_round():
    global player_choice, ai_choice, result
    player_choice = None
    ai_choice = None
    result = None

def reset_game():
    global player_score, ai_score, draws, rounds_played, player_choice, ai_choice, result, game_over, ai_brain
    player_score = 0
    ai_score = 0
    draws = 0
    rounds_played = 0
    player_choice = None
    ai_choice = None
    result = None
    game_over = False
    ai_brain = EnhancedPatternAI()  # Reset AI learning

# Main game loop
clock = pygame.time.Clock()
running = True

try:
    while running:
        mouse_pos = pygame.mouse.get_pos()
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle button events
            if current_state == GAME_SCREEN and not game_over and not result:
                rock_button.handle_event(event)
                paper_button.handle_event(event)
                scissors_button.handle_event(event)
            elif current_state == GAME_SCREEN and game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    reset_game()
        
        # Update button hover states
        if current_state == GAME_SCREEN and not game_over and not result:
            rock_button.check_hover(mouse_pos)
            paper_button.check_hover(mouse_pos)
            scissors_button.check_hover(mouse_pos)
        
        # Auto-reset after result display time
        if current_state == GAME_SCREEN and result and current_time - last_result_time > result_display_time and not game_over:
            reset_round()
        
        # Check if we should transition from title screen to game screen
        if current_state == TITLE_SCREEN:
            if title_display_time == 0:
                title_display_time = current_time
            elif current_time - title_display_time > title_duration:
                current_state = GAME_SCREEN
        
        # Draw everything
        screen.fill(BACKGROUND)
        
        if current_state == TITLE_SCREEN:
            # Draw title screen
            title_text = title_font.render("Enhanced Rock Paper Scissors", True, TITLE_COLOR)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
            
            creator_text = creator_font.render("Created by Sahan Rashmika", True, CREATOR_COLOR)
            screen.blit(creator_text, (WIDTH//2 - creator_text.get_width()//2, HEIGHT//2))
            
        elif current_state == GAME_SCREEN:
            # Draw round counter
            round_text = round_font.render(f"Round: {rounds_played}/{max_rounds}", True, ROUND_COLOR)
            screen.blit(round_text, (WIDTH//2 - round_text.get_width()//2, 30))
            
            # Draw scores and AI win rate
            win_rate = (ai_score / rounds_played * 100) if rounds_played > 0 else 0
            score_text = stats_font.render(f"Player: {player_score}  AI: {ai_score}  Draws: {draws}  AI Win Rate: {win_rate:.1f}%", True, TEXT_COLOR)
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 70))
            
            if game_over:
                # Draw game over message
                if player_score > ai_score:
                    result_text = result_font.render("You Win the Game!", True, WIN_COLOR)
                elif ai_score > player_score:
                    result_text = result_font.render("AI Wins the Game!", True, LOSE_COLOR)
                else:
                    result_text = result_font.render("It's a Tie Game!", True, DRAW_COLOR)
                
                screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 220))
                
                # Draw final score
                final_text = choice_font.render(f"Final Score - Player: {player_score}, AI: {ai_score}, Draws: {draws}", True, TEXT_COLOR)
                screen.blit(final_text, (WIDTH//2 - final_text.get_width()//2, 270))
                
                # Draw instruction to click to play again
                instruction_text = stats_font.render("Click anywhere to play again", True, HIGHLIGHT)
                screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, 320))
            
            # Draw choices and results if not game over
            elif result:
                # Draw player choice
                screen.blit(choice_images[player_choice], (WIDTH//4 - 60, 180))
                player_text = choice_font.render("Your Choice", True, TEXT_COLOR)
                screen.blit(player_text, (WIDTH//4 - player_text.get_width()//2, 310))
                
                # Draw AI choice
                screen.blit(choice_images[ai_choice], (3*WIDTH//4 - 60, 180))
                ai_text = choice_font.render("AI Choice", True, TEXT_COLOR)
                screen.blit(ai_text, (3*WIDTH//4 - ai_text.get_width()//2, 310))
                
                # Draw result
                if result == "win":
                    result_text = result_font.render("You Win!", True, WIN_COLOR)
                elif result == "lose":
                    result_text = result_font.render("AI Wins!", True, LOSE_COLOR)
                else:
                    result_text = result_font.render("Draw!", True, DRAW_COLOR)
                
                screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 360))
                
                # Draw countdown for auto-reset
                time_left = result_display_time - (current_time - last_result_time)
                countdown_text = stats_font.render(f"Next round in: {time_left:.1f}s", True, HIGHLIGHT)
                screen.blit(countdown_text, (WIDTH//2 - countdown_text.get_width()//2, 400))
            
            elif not game_over:
                # Draw instruction
                instruction_text = choice_font.render("Choose your weapon:", True, TEXT_COLOR)
                screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, 210))
                
                # Draw choice buttons with images
                screen.blit(choice_images['rock'], (150, 250))
                screen.blit(choice_images['paper'], (340, 250))
                screen.blit(choice_images['scissors'], (530, 250))
                
                rock_button.draw(screen)
                paper_button.draw(screen)
                scissors_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

except Exception as e:
    # Log any errors to a file for debugging
    with open("error_log.txt", "w") as f:
        f.write(str(e))
    raise e

finally:
    pygame.quit()
    sys.exit()
