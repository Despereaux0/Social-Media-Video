import turtle
import time
import random
import math

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Bouncing Ball")
wn.tracer(0)  # Turn off automatic screen updates

# Draw the circular boundary
boundary = turtle.Turtle()
boundary.hideturtle()
boundary.penup()
boundary.goto(0, -230)  # Adjust the starting point of the circle
boundary.pendown()
boundary.color("white")
boundary.circle(230)  # Adjust the radius of the circle

# Function to create balls
def create_balls(num_balls):
    balls = []
    colors = ["red", "blue", "orange", "green", "yellow", "white", "purple", "pink"]
    ball_radius = 10  # Initial radius of the ball

    for _ in range(num_balls):
        ball = turtle.Turtle()
        ball.shape("circle")
        ball.color(random.choice(colors))
        ball.penup()
        ball.speed(0)
        y = random.randint(-160, 160)
        ball.goto(y, 90)  # Start at the center
        ball.dy = random.uniform(0, 0)
        ball.dx = random.uniform(0, 0)
        ball.da = random.randint(-5, 5)
        ball.radius = ball_radius  # Assign initial radius to the ball
        balls.append(ball)
    
    return balls

# Number of balls to spawn
num_balls = 1  # Change this number to adjust the number of balls spawned
balls = create_balls(num_balls)

gravity = 0.1
fps = 60
delay = 1 / fps  # Delay between frames

while True:
    for ball in balls:
        ball.dy -= gravity
        ball.sety(ball.ycor() + ball.dy)
        ball.setx(ball.xcor() + ball.dx)

        # Check for collision with the circular boundary
        dist_from_center = math.sqrt(ball.xcor()**2 + ball.ycor()**2)
        ball_radius = ball.radius  # Get current radius of the ball
        if dist_from_center > (230 - ball_radius):  # Adjust the collision radius
            # Calculate the angle of incidence
            angle = math.atan2(ball.ycor(), ball.xcor())
            
            # Reflect the ball's velocity
            normal = (math.cos(angle), math.sin(angle))
            dot_product = ball.dx * normal[0] + ball.dy * normal[1]
            ball.dx -= 2 * dot_product * normal[0]
            ball.dy -= 2 * dot_product * normal[1]

            # Adjust the speed (optional)
            ball.dx *= 1.01  # Adjust the horizontal velocity
            ball.dy *= 1.01  # Adjust the vertical velocity

            # Increase the size of the ball
            ball.radius += 1.2
            
            # Ensure the ball is inside the circle
            overlap = dist_from_center - (230 - ball_radius)
            ball.setx(ball.xcor() - overlap * normal[0])
            ball.sety(ball.ycor() - overlap * normal[1])

            # Update the ball's size
            ball.shapesize(ball.radius / 10)  # Scale the size based on radius

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


