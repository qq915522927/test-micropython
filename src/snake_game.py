# Import necessary libraries
import machine
import time
import ssd1306

from mpu6050 import accel

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
accelerometer = accel(i2c)


# Initialize SSD1306 display with 128x64 resolution
display = ssd1306.SSD1306_I2C(128, 64, i2c)


# Define the size of the "snake" and the speed of movement
snake_size = 20
speed = 3

# Define the initial position of the snake
snake = [(x, 0) for x in range(snake_size)]

# Define the current direction of movement of the snake
direction = 'right'
deadzone = 5000

# Define a function to move the snake on the display
def move_snake():
    global snake, direction

    # Read the current acceleration values from the MPU6050 sensor
    values = accelerometer.get_values()
    ax = values["AcX"]
    ay = values["AcY"]
    az = values["AcZ"]

    # display.fill(0)  # Clear the display
    # display.text("{} {} {}".format(ax, ay, az), 0, 0)  # Add text to the display
    # display.show()  # Show the display
    # time.sleep_ms(speed)

    # Determine the current direction of movement based on the acceleration values
    if abs(ax) > deadzone or abs(ay) > deadzone:
        if abs(ax) > abs(ay):
            if ax > deadzone:
                direction = 'down'
            elif ax < -deadzone:
                direction = 'up'
        else:
            if ay > deadzone:
                direction = 'right'
            elif ay < -deadzone:
                direction = 'left'
    print("{} {} {}".format(ax, ay, direction))

    # Move the snake one step in the current direction of movement
    head_x, head_y = snake[-1]
    if direction == 'right':
        new_head = (head_x + 1, head_y)
        if new_head[0] > 100:
            new_head = (0, head_y)
    elif direction == 'left':
        new_head = (head_x - 1, head_y)
        if new_head[0] < 0:
            new_head = (100, head_y)
    elif direction == 'up':
        new_head = (head_x, head_y - 1)
        if new_head[1] < 0:
            new_head = (head_x, 60)
    else:
        new_head = (head_x, head_y + 1)
        if new_head[1] > 60:
            new_head = (head_x, 0)
    snake.pop(0)  # Remove the tail of the snake
    snake.append(new_head)  # Add a new head to the snake

    # Clear the display and draw the snake
    display.fill(0)
    for segment in snake:
        display.rect(segment[0], segment[1], 1, 1, 1)
    display.show()

    # Wait for a short time to control the speed of movement
    time.sleep_ms(speed)

# Call the move_snake function repeatedly to start the game
while True:
    move_snake()
