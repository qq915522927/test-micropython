# Import necessary libraries
import machine
import ssd1306
import time

# Define pin numbers for I2C communication
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))

# Initialize SSD1306 display with 128x64 resolution
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Define a function to scroll text on the display
def scroll_text(text):
    display.fill(0)  # Clear the display
    text_width = len(text) * 8
    x = 128

    while x > -text_width:
        display.fill(0)  # Clear the display
        display.text(text, x, 0)  # Add text to the display
        display.show()  # Show the display
        x -= 1
        time.sleep_ms(50)

# Call the scroll_text function with your desired text
scroll_text("Hello, world!")
