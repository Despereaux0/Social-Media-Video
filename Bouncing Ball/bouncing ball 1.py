import turtle
import random
import math

# Set key parameters
gravity = -0.01  # pixels/(time of iteration)^2
y_velocity = 0.0625  # pixels/(time of iteration)
x_velocity = 0.0625  # pixels/(time of iteration)
energy_loss = 0.5
width = 450
height = 800
circle_radius = 150  # Radius of the circle
circle_center = (0, 0)  # Center of the circle

# Set window and ball
window = turtle.Screen()
window.setup(width, height)
window.bgcolor("black")  # Set background color to black
window.tracer(0)

# Draw the circle
circle = turtle.Turtle()
circle.penup()
circle.color("white")  # Set circle color to white for visibility
circle.goto(0, -circle_radius)
circle.pendown()
circle.circle(circle_radius)
circle.hideturtle()

# Set up the ball inside the circle
ball = turtle.Turtle()
ball.penup()
ball.color("blue")
ball.shape("circle")

# Randomly place the ball within the circle
angle = random.uniform(0, 360)
radius = random.uniform(0, circle_radius)
x_start = radius * math.cos(math.radians(angle))
y_start = radius * math.sin(math.radians(angle))
ball.goto(x_start, y_start)

def reflect_velocity(x_vel, y_vel, normal_x, normal_y):
    # Reflect the velocity vector around the normal vector
    dot_product = x_vel * normal_x + y_vel * normal_y
    reflected_x = x_vel - 2 * dot_product * normal_x
    reflected_y = y_vel - 2 * dot_product * normal_y
    return reflected_x, reflected_y

# Main loop
while True:
    # Move ball
    ball.sety(ball.ycor() + y_velocity)
    ball.setx(ball.xcor() + x_velocity)
    
    # Acceleration due to gravity
    y_velocity += gravity

    # Check collision with circle boundary
    dist_to_center = math.sqrt((ball.xcor() - circle_center[0])**2 + (ball.ycor() - circle_center[1])**2)
    if dist_to_center > circle_radius:
        # Calculate normal vector at the point of collision
        normal_x = (ball.xcor() - circle_center[0]) / dist_to_center
        normal_y = (ball.ycor() - circle_center[1]) / dist_to_center
        
        # Reflect the velocity
        x_velocity, y_velocity = reflect_velocity(x_velocity, y_velocity, normal_x, normal_y)
        
        # Adjust position to be on the circle boundary
        ball.setx(circle_center[0] + circle_radius * normal_x)
        ball.sety(circle_center[1] + circle_radius * normal_y)

    window.update()

