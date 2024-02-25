import time
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# Define LCD properties
lcd_columns = 16
lcd_rows = 2

# Define GPIO pins for SCL and SDA
scl_pin = board.D4  # Pin 7 (GPIO 4) for SCL
sda_pin = board.D17  # Pin 11 (GPIO 17) for SDA

# Initialize I2C bus with specified pins
i2c = busio.I2C(scl_pin, sda_pin)

# Initialize LCD class
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Turn on backlight
lcd.backlight = True

# Display message
lcd.message = "Hello, World!"

# Wait for 5 seconds
time.sleep(5)

# Clear display
lcd.clear()
