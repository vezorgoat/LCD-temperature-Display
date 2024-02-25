import time
import smbus
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from threading import Timer

calibration_value = 21.34 - 0.7
phval = 0
avgval = 0
buffer_arr = [0] * 10
temp = 0
ph_act = 0.0

# Define display constants
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
RESET_PIN = None
I2C_ADDRESS = 0x3C
i2c = smbus.SMBus(1)

# Initialize display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RESET_PIN, i2c_bus=i2c)
disp.begin()
disp.clear()
disp.display()

# Define timer interval
TIMER_INTERVAL = 0.5

def display_pHValue():
    global ph_act
    # Display pH value on OLED
    disp.clear()
    disp.setTextSize(2)
    disp.setCursor(0, 0)
    disp.print("pH:")
    disp.print(ph_act)
    disp.display()

def read_adc(channel):
    bus = smbus.SMBus(1)
    data = bus.read_i2c_block_data(0x48, 0x01)
    # Convert data to ADC value
    adc_value = data[0] * 256 + data[1]
    return adc_value

def loop():
    global ph_act
    while True:
        for i in range(10):
            buffer_arr[i] = read_adc(0)
            time.sleep(0.03)
        
        for i in range(9):
            for j in range(i+1, 10):
                if buffer_arr[i] > buffer_arr[j]:
                    temp = buffer_arr[i]
                    buffer_arr[i] = buffer_arr[j]
                    buffer_arr[j] = temp
        
        avgval = sum(buffer_arr[2:8])
        volt = float(avgval) * 5.0 / 1024.0 / 6.0
        ph_act = -5.70 * volt + calibration_value

        # Print pH value
        print("pH Val:", ph_act)
        time.sleep(1)

# Initialize timer
timer = Timer(TIMER_INTERVAL, display_pHValue)
timer.start()

if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        timer.cancel()
        disp.clear()
        disp.display()
