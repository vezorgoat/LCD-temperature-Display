import time
import Adafruit_ADS1x15

# Initialize ADC
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# Function to read analog voltage from pH sensor
def read_voltage(channel):
    value = adc.read_adc(channel, gain=GAIN)
    voltage = value / 32767.0 * 6.144  # Assuming a gain of 1, and 6.144V range
    return voltage

try:
    while True:
        # Read analog voltage from pH sensor
        analog_voltage = read_voltage(0)  # Assuming pH sensor is connected to channel 0

        # Print analog voltage
        print("Analog Voltage:", analog_voltage)

        # Adjust the delay based on your sampling requirements
        time.sleep(1)

except KeyboardInterrupt:
    pass
