import time
import sys
from CQRobot_ADS1115 import ADS1115

# Define ADC gain settings
ADS1115_REG_CONFIG_PGA_6_144V = 0x00

# Initialize ADS1115 ADC
ads1115 = ADS1115()
ads1115.setAddr_ADS1115(0x48)  # Set the I2C address of the ADC
ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)  # Set the gain to 6.144V

# Constants
VREF = 5.0
analogBuffer = [0] * 30
analogBufferIndex = 0

# Function to calculate median value
def getMedianNum(arr):
    arr.sort()
    n = len(arr)
    if n % 2 == 0:
        return (arr[n//2 - 1] + arr[n//2]) / 2
    else:
        return arr[n//2]

while True:
    # Read analog voltage from pH sensor
    for i in range(30):
        analogBuffer[i] = ads1115.readVoltage(0)['r']  # Assuming pH sensor is connected to channel 0
        time.sleep(0.04)

    # Calculate pH value
    median_voltage = getMedianNum(analogBuffer)
    average_voltage = median_voltage * (VREF / 1024.0)
    # Adjust the pH calculation formula based on your sensor's characteristics
    ph_value = calculate_ph(average_voltage)

    # Print pH value
    print("pH Value:", ph_value)

    # Reset analog buffer
    analogBuffer = [0] * 30
