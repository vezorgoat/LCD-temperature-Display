import os
import glob
import time
import smbus
import drivers
from time import sleep
from datetime import datetime

# Mount the temperature sensor device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Define I2C address and register addresses for the TDS sensor
TDS_ADDRESS = 0x48  # I2C address of the TDS sensor
TDS_CMD_READ = 0x00  # Command to read data from the sensor

# Create an instance of the smbus for I2C communication
bus = smbus.SMBus(1)  # Use bus 1 for Raspberry Pi 3, use 0 for older models

# Set up the path to the temperature sensor
base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*')[0]  # Get file path of sensor

# Initialize the LCD display
display = drivers.Lcd()

def read_temp_raw():
    with open(device_path + '/w1_slave', 'r') as f:
        valid, temp = f.readlines()
    return valid, temp

def read_temp():
    valid, temp = read_temp_raw()

    while 'YES' not in valid:
        time.sleep(0.2)
        valid, temp = read_temp_raw()

    pos = temp.index('t=')
    if pos != -1:
        # Read the temperature.
        temp_string = temp[pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * (9.0 / 5.0) + 32.0
        return temp_c, temp_f

def read_tds_value():
    # Send command to request TDS data
    bus.write_byte(TDS_ADDRESS, TDS_CMD_READ)
    # Wait for a short time to allow the sensor to process the request
    time.sleep(0.5)
    # Read 2 bytes of TDS data from the sensor
    data = bus.read_i2c_block_data(TDS_ADDRESS, 0x00, 2)
    # Combine the two bytes into a single integer value
    tds_value = (data[0] << 8) | data[1]
    return tds_value

try:
    while True:
        # Clear the display
        display.lcd_clear()

        # Get current temperature and determine status
        temp_c, temp_f = read_temp()
        if 0 <= temp_c <= 30:
            temp_status = "Mid"
        elif 30 < temp_c <= 70:
            temp_status = "Good"
        elif 80 <= temp_c <= 120:
            temp_status = "Bad"
        else:
            temp_status = "Unknown"

        # Read TDS value from the sensor
        tds = read_tds_value()

        # Get current time
        current_time = datetime.now().strftime("%I:%M %p")

        # Write time to display
        display.lcd_display_string("Time: " + current_time, 1)

        # Write temperature and status to display
        display.lcd_display_string("Temp: {:.1f}C {:.1f}F".format(temp_c, temp_f), 2)
        display.lcd_display_string("Status: " + temp_status, 3)

        # Write TDS value to display
        display.lcd_display_string("TDS: {}".format(tds), 4)

        sleep(2)

except KeyboardInterrupt:
    # If there is a KeyboardInterrupt, exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
