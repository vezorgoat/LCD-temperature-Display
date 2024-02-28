
import time
import smbus
import drivers
from datetime import datetime
from time import sleep
from CQRobot_ADS1115 import ADS1115

# Define I2C address and register addresses for the TDS sensor
TDS_ADDRESS = 0x48  # I2C address of the TDS sensor
TDS_CMD_READ = 0x00  # Command to read data from the sensor

# Create an instance of the smbus for I2C communication
bus = smbus.SMBus(1)  # Use bus 1 for Raspberry Pi 3, use 0 for older models

# Initialize ADS1115 ADC for pH sensor
ads1115 = ADS1115()
ads1115.setAddr_ADS1115(0x48)  # Set the I2C address of the ADC
ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)  # Set the gain to 6.144V
calibration_value = 7.0  # Calibration value obtained from your calibration process

# Load the driver and set it to "display"
display = drivers.Lcd()

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

def read_ph_value():
    # Read analog voltage from pH sensor
    analog_voltage = ads1115.readVoltage(0)['r']  # Assuming pH sensor is connected to channel 0

    # Calculate pH value using the calibration value
    ph_value = 14.0 - (analog_voltage + calibration_value) / 1000.0  # Adjust this formula as needed
    return ph_value

try:
    while True:
        # Clear the display
        display.lcd_clear()

        # Get current time
        current_time = datetime.now().strftime("%I:%M %p")

        # Get TDS value
        tds_value = read_tds_value()

        # Get pH value
        ph_value = read_ph_value()

        # Determine TDS status
        if 0 <= tds_value <= 30:
            tds_status = "Mid"
        elif 30 < tds_value <= 70:
            tds_status = "Good"
        elif 80 <= tds_value <= 120:
            tds_status = "Bad"
        else:
            tds_status = "Unknown"

        # Determine pH status
        if ph_value < 7:
            ph_status = "Acidic"
        elif ph_value > 7:
            ph_status = "Alkaline"
        else:
            ph_status = "Neutral"

        # Write time to display
        display.lcd_display_string("Time: " + current_time, 1)

        # Write TDS and pH values to display
        display.lcd_display_string("TDS: {}   pH: {:.2f}".format(tds_status, ph_value), 2)
        display.lcd_display_string("pH Status: " + ph_status, 3)

        sleep(1)

except KeyboardInterrupt:
    # If there is a KeyboardInterrupt, exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
