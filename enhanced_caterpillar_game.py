import random
import turtle as t
import time
from pygame import mixer

class CaterpillarGame:
    def __init__(self):
        # Set up the screen
        self.screen = t.Screen()
        self.screen.setup(700, 700)
        self.screen.bgcolor('black')
        self.screen.title('Caterpillar Game')
        self.screen.tracer(0)  # Turn off automatic animation
        
        # Game state variables
        self.game_started = False
        self.game_paused = False
        self.score = 0
        self.high_score = 0
        self.caterpillar_speed = 2
        self.caterpillar_length = 3
        self.difficulty = 'Normal'
        
        # Create game elements
        self._create_caterpillar()
        self._create_leaf()
        self._create_text_turtles()
        
        # Set up key bindings
        self._setup_keys()
        
        # Update the screen
        self.screen.update()
    
    def _create_caterpillar(self):
        """Create the caterpillar turtle."""
       
        self.caterpillar = t.Turtle()
        self.caterpillar.shape('square')
        self.caterpillar.color('chocolate4', 'chocolate')
        self.caterpillar.speed(0)
        self.caterpillar.penup()
        self.caterpillar.hideturtle()
        
        # Create caterpillar segments
        self.segments = []
        self.segment_colors = ['chocolate', 'chocolate3', 'chocolate2', 'chocolate1']
    
    def _create_leaf(self):
        """Create the leaf turtle."""

        self.leaf = t.Turtle()
        leaf_shape = ((0, 0), (14, 2), (18, 6), (20, 20), (6, 18), (2, 14))
        t.register_shape('leaf', leaf_shape)
        self.leaf.shape('leaf')
        self.leaf.color('green3')
        self.leaf.penup()
        self.leaf.hideturtle()
        self.leaf.speed(0)
    
    def _create_text_turtles(self):
        """Create turtles for displaying text."""
        # Main text turtle
        self.text_turtle = t.Turtle()
        self.text_turtle.hideturtle()
        self.text_turtle.penup()
        self.text_turtle.color('white')
        
        # Score turtle
        self.score_turtle = t.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.color('white')
        self.score_turtle.speed(0)
        
        # Instructions turtle
        self.instructions = t.Turtle()
        self.instructions.hideturtle()
        self.instructions.penup()
        self.instructions.color('white')
    
    def start_game(self):
        """Start or restart the game."""
        if self.game_started:
            return
        
        # Clear any existing text
        self.text_turtle.clear()
        self.instructions.clear()
        
        # Reset game state
        self.game_started = True
        self.score = 0
        
        # Reset and show caterpillar
        self.caterpillar.goto(0, 0)
        self.caterpillar.setheading(0)
        self.caterpillar.showturtle()
        
        # Clear old segments and create initial ones
        for segment in self.segments:
            segment.hideturtle()
        self.segments.clear()
        
        for _ in range(2):  # Create 2 initial segments (plus head = 3 total)
            self.grow_caterpillar()
        
        # Place leaf and update score display
        self.place_leaf()
        self.display_score()
        
        # Start game loop
        self.game_loop()
    
    def _setup_keys(self):
        """Set up key bindings."""
        self.screen.listen()
        self.screen.onkey(self.start_game, 'space')
        self.screen.onkey(self.move_up, 'Up')
        self.screen.onkey(self.move_down, 'Down')
        self.screen.onkey(self.move_left, 'Left')
        self.screen.onkey(self.move_right, 'Right')
        self.screen.onkey(self.toggle_pause, 'p')
        self.screen.onkey(self.set_easy_difficulty, '1')
        self.screen.onkey(self.set_normal_difficulty, '2')
        self.screen.onkey(self.set_hard_difficulty, '3')
    
    def show_welcome_screen(self):
        """Display the welcome screen with instructions."""
        self.text_turtle.clear()
        self.text_turtle.goto(0, 100)
        self.text_turtle.write('CATERPILLAR GAME', align='center', 
                              font=('Arial', 36, 'bold'))
        
        self.instructions.clear()
        self.instructions.goto(0, 20)
        instructions_text = [
            "Press SPACE to start",
            "Arrow keys to move",
            "P to pause",
            "Difficulty: 1-Easy, 2-Normal, 3-Hard",
            f"Current difficulty: {self.difficulty}"
        ]
        for i, line in enumerate(instructions_text):
            self.instructions.goto(0, 20 - i * 30)
            self.instructions.write(line, align='center', font=('Arial', 16)) # type: ignore
    
    def set_easy_difficulty(self):
        """Set game difficulty to easy."""
        if not self.game_started:
            self.difficulty = 'Easy'
            self.caterpillar_speed = 1.5
            self.show_welcome_screen()
    
    def set_normal_difficulty(self):
        """Set game difficulty to normal."""
        if not self.game_started:
            self.difficulty = 'Normal'
            self.caterpillar_speed = 2
            self.show_welcome_screen()
    
    def set_hard_difficulty(self):
        """Set game difficulty to hard."""
        if not self.game_started:
            self.difficulty = 'Hard'
            self.caterpillar_speed = 3
            self.show_welcome_screen()
    
    def toggle_pause(self):
        """Pause or unpause the game."""
        if self.game_started:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.text_turtle.clear()
                self.text_turtle.goto(0, 0)
                self.text_turtle.write('PAUSED', align='center', font=('Arial', 30, 'bold'))
            else:
                self.text_turtle.clear()
                self.game_loop()
    
    def is_outside_window(self):
        """Check if the caterpillar is outside the window."""
        left_wall = -self.screen.window_width() / 2 + 20
        right_wall = self.screen.window_width() / 2 - 20
        top_wall = self.screen.window_height() / 2 - 20
        bottom_wall = -self.screen.window_height() / 2 + 20
        
        x, y = self.caterpillar.position()
        return (x < left_wall or x > right_wall or 
                y < bottom_wall or y > top_wall)
    
    def display_score(self):
        """Display the current score and high score."""
        self.score_turtle.clear()
        
        # Display current score
        self.score_turtle.goto(-self.screen.window_width() / 2 + 50, 
                              self.screen.window_height() / 2 - 40)
        self.score_turtle.write(f"Score: {self.score}", align='left', 
                               font=('Arial', 16, 'bold'))
        
        # Display high score
        self.score_turtle.goto(self.screen.window_width() / 2 - 50, 
                              self.screen.window_height() / 2 - 40)
        self.score_turtle.write(f"High Score: {self.high_score}", align='right', 
                               font=('Arial', 16, 'bold'))
        
        # Display difficulty
        self.score_turtle.goto(0, self.screen.window_height() / 2 - 40)
        self.score_turtle.write(f"Difficulty: {self.difficulty}", align='center', 
                               font=('Arial', 16, 'bold'))
    
    def place_leaf(self):
        try:
            mixer.init()
            sound = mixer.Sound('/Users/premg/Library/CloudStorage/OneDrive-Personal/711127__xiko__retro-collection-1.wav')
            sound.play()
        except Exception:
            # Silently handle sound errors to avoid interrupting gameplay
            pass
            
        self.leaf.hideturtle()
        margin = 200  # Keep away from edges
        max_x = int(self.screen.window_width() / 2) - margin
        max_y = int(self.screen.window_height() / 2) - margin
            
        self.leaf.setx(random.randint(-max_x, max_x))
        self.leaf.sety(random.randint(-max_y, max_y))
        self.leaf.showturtle()

    def grow_caterpillar(self):
        """Add a new segment to the caterpillar."""
        # Create a new segment
        new_segment = t.Turtle()
        new_segment.shape('square')
        new_segment.color(random.choice(self.segment_colors))
        new_segment.penup()
        new_segment.speed(0)
        
        # Position it behind the last segment or behind the head
        if self.segments:
            new_segment.setposition(self.segments[-1].position())
        else:
            # Get the position behind the head based on heading
            head_x, head_y = self.caterpillar.position()
            heading = self.caterpillar.heading()
            
            if heading == 0:  # Right
                new_segment.setposition(head_x - 20, head_y)
            elif heading == 90:  # Up
                new_segment.setposition(head_x, head_y - 20)
            elif heading == 180:  # Left
                new_segment.setposition(head_x + 20, head_y)
            elif heading == 270:  # Down
                new_segment.setposition(head_x, head_y + 20)
        
        self.segments.append(new_segment)
    
    def move_caterpillar(self):
        """Move the caterpillar and its segments."""
        # Move each segment to the position of the segment in front of it
        for i in range(len(self.segments) - 1, 0, -1):
            x, y = self.segments[i-1].position()
            self.segments[i].goto(x, y)
        
        # Move the first segment to the head's position
        if self.segments:
            x, y = self.caterpillar.position()
            self.segments[0].goto(x, y)
        
        # Move the head
        self.caterpillar.forward(self.caterpillar_speed * 10)
    
    def reset_game(self):
        """Reset the game to its initial state."""
        # Clear segments
        for segment in self.segments:
            segment.hideturtle()
        self.segments.clear()
        
        # Reset caterpillar position and appearance
        self.caterpillar.hideturtle()
        self.caterpillar.goto(0, 0)
        self.caterpillar.setheading(0)
        
        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
        
        # Reset game state
        self.score = 0
        self.caterpillar_length = 3
        self.caterpillar_speed = 2
        if self.difficulty == 'Easy':
            self.caterpillar_speed = 1.5
        elif self.difficulty == 'Hard':
            self.caterpillar_speed = 3
        
        self.game_started = False
        self.game_paused = False
        
        # Show welcome screen
        self.show_welcome_screen()
    
    def game_over(self):
        """Handle game over state."""
        self.text_turtle.clear()
        self.text_turtle.goto(0, 50)
        self.text_turtle.write('GAME OVER', align='center', font=('Arial', 40, 'bold'))
        
        if self.score > self.high_score:
            self.high_score = self.score
            self.text_turtle.goto(0, 0)
            self.text_turtle.write(f'NEW HIGH SCORE: {self.high_score}!', 
                                  align='center', font=('Arial', 20, 'bold'))
        
        self.text_turtle.goto(0, -50)
        self.text_turtle.write('Press SPACE to restart', align='center', 
                              font=('Arial', 20)) # type: ignore
        
        self.display_score()
        self.reset_game()
    
    def game_loop(self):
        """Main game loop."""
        if not self.game_started or self.game_paused:
            return
        
        # Move the caterpillar
        self.move_caterpillar()
        
        # Check for collision with leaf
        if self.caterpillar.distance(self.leaf) < 20:
            self.place_leaf()
            self.grow_caterpillar()
            self.score += 1
            
            # Increase speed slightly with each leaf eaten
            speed_increment = 0.1
            if self.difficulty == 'Hard':
                speed_increment = 0.2
            elif self.difficulty == 'Easy':
                speed_increment = 0.05
            
            self.caterpillar_speed += speed_increment
            self.display_score()
        
        # Check for collision with wall
        if self.is_outside_window():
            self.game_over()
            return
        
        # Check for collision with self
        for segment in self.segments:
            if self.caterpillar.distance(segment) < 10:
                self.game_over()
                return
        
        # Update screen and schedule next frame
        self.screen.update()
        self.screen.ontimer(self.game_loop, 100)  # Smoother animation
    
    def move_up(self):
        """Change direction to up."""
        if self.game_started and not self.game_paused:
            if self.caterpillar.heading() != 270:  # Not going down
                self.caterpillar.setheading(90)
    
    def move_down(self):
        """Change direction to down."""
        if self.game_started and not self.game_paused:
            if self.caterpillar.heading() != 90:  # Not going up
                self.caterpillar.setheading(270)
    
    def move_left(self):
        """Change direction to left."""
        if self.game_started and not self.game_paused:
            if self.caterpillar.heading() != 0:  # Not going right
                self.caterpillar.setheading(180)
    
    def move_right(self):
        """Change direction to right."""
        if self.game_started and not self.game_paused:
            if self.caterpillar.heading() != 180:  # Not going left
                self.caterpillar.setheading(0)
    # start game
    def run(self):
        """Start the game."""
        self.show_welcome_screen()
        self.screen.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = CaterpillarGame()
    game.run()