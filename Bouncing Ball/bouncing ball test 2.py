import turtle
import time
import random
import math
import pygame

time.sleep(5)

# Initialize pygame for sound
pygame.init()

# Load the sound files into a list
collision_sounds = [pygame.mixer.Sound(f"sound{i}.wav") for i in range(1, 13)]

# Variable to track the current sound index
current_sound_index = 0

# Function to play the next sound in the list
def play_next_sound():
    global current_sound_index
    pygame.mixer.Sound.play(collision_sounds[current_sound_index])
    current_sound_index = (current_sound_index + 1) % len(collision_sounds)

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("#0E133D")
wn.title("Bouncing Ball")
wn.tracer(0)  # Turn off automatic screen updates

# Draw the circular boundary
boundary = turtle.Turtle()
boundary.hideturtle()
boundary.penup()
boundary.goto(0, -200)  # Adjust the starting point of the circle and the radius
boundary.pendown()
boundary.color("pink")
boundary.width(5)
boundary.circle(200)  # Adjust the radius of the circle

colors = ["red", "blue", "orange", "green", "yellow", "white", "purple", "pink","cyan","darksalmon", "black","magenta"]


# Function to create balls
def create_balls(num_balls):
    balls = []
    ball_radius = 10  # Initial radius of the ball

    for _ in range(num_balls):
        ball = turtle.Turtle()
        ball.shape("circle")
        ball.color(random.choice(colors))
        ball.penup()
        ball.speed(0)
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        ball.goto(x, y)
        ball.dy = random.uniform(-1, 1)
        ball.dx = random.uniform(-1, 1)
        ball.da = random.randint(-5, 5)
        ball.radius = ball_radius  # Assign initial radius to the ball
        ball.speed_factor = 1  # Initial speed factor
        balls.append(ball)
    
    return balls

# Function to increase the size of the ball
def increase_ball_size(ball):
    ball_radius = ball.radius
    ball_radius += 0  # Increase the radius by 5 units
    ball.shapesize(ball_radius / 10)  # Adjust the size of the ball shape
    ball.radius = ball_radius  # Update the radius of the ball

# Function to change the speed of the ball
def change_ball_speed(ball):
    ball.speed_factor *= 0.2

# Number of balls to spawn
num_balls = 1  # Change this number to adjust the number of balls spawned
balls = create_balls(num_balls)


gravity = 0.2
fps = 60
delay = 1 / fps  # Delay between frames

while True:
    for ball in balls:
        ball.dy -= gravity * ball.speed_factor  # Adjust speed based on speed factor
        ball.sety(ball.ycor() + ball.dy)
        ball.setx(ball.xcor() + ball.dx)

        # Check for collision with the circular boundary
        dist_from_center = math.sqrt(ball.xcor()**2 + ball.ycor()**2)
        ball_radius = ball.radius  # Get current radius of the ball
        if dist_from_center > (200 - ball_radius):  # Adjust the collision radius
            # Calculate the angle of incidence
            angle = math.atan2(ball.ycor(), ball.xcor())
            
            # Reflect the ball's velocity
            normal = (math.cos(angle), math.sin(angle))
            dot_product = ball.dx * normal[0] + ball.dy * normal[1]
            ball.dx -= 2 * dot_product * normal[0]
            ball.dy -= 2 * dot_product * normal[1]

            # Ensure the ball is inside the circle
            overlap = dist_from_center - (200 - ball_radius)
            ball.setx(ball.xcor() - overlap * normal[0])
            ball.sety(ball.ycor() - overlap * normal[1])

            # Increase the size of the ball upon collision
            increase_ball_size(ball)

            # Change the color of the ball to a new color (excluding its current color)
            #new_color = random.choice([color for color in colors if color != ball.color()])
            #ball.color(new_color)

            # Change the speed of the ball
            change_ball_speed(ball)

            # Play the next collision sound
            play_next_sound()

    # Check for collisions between balls
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if balls[i].distance(balls[j]) < 2 * balls[i].radius:  # Assuming ball diameter is 20
                # Calculate the distance and overlap between the balls
                distance = balls[i].distance(balls[j])
                overlap = 2 * balls[i].radius - distance
                
                # Calculate the direction from ball[i] to ball[j]
                dx = balls[j].xcor() - balls[i].xcor()
                dy = balls[j].ycor() - balls[i].ycor()
                angle = math.atan2(dy, dx)
                
                # Move each ball away from each other by half the overlap distance
                move_x = math.cos(angle) * overlap / 2
                move_y = math.sin(angle) * overlap / 2
                
                balls[i].setx(balls[i].xcor() - move_x)
                balls[i].sety(balls[i].ycor() - move_y)
                balls[j].setx(balls[j].xcor() + move_x)
                balls[j].sety(balls[j].ycor() + move_y)

    # Update the screen
    wn.update()

    # Delay to control the frame rate
    time.sleep(delay)

# Keep the window open
wn.mainloop()
