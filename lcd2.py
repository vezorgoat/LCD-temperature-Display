import time
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# Define LCD properties
lcd_columns = 16
lcd_rows = 2

# Define GPIO pins for SCL and SDA
scl_pin = 28  # GPIO 28 (SCL)
sda_pin = 27  # GPIO 27 (SDA)

# Initialize I2C bus with specified pins
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize LCD class
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, address=0x27)  # Adjust the address if necessary

# Turn on backlight
lcd.backlight = True

# Display message
lcd.message = "Hello, World!\nWelcome to\nRaspberry Pi!"

# Wait for 5 seconds
time.sleep(5)

# Clear display
lcd.clear()
