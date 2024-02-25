import time
import sys
from CQRobot_ADS1115 import ADS1115

# Define ADC gain settings
ADS1115_REG_CONFIG_PGA_6_144V = 0x00

# Initialize ADS1115 ADC
ads1115 = ADS1115()
ads1115.setAddr_ADS1115(0x48)  # Set the I2C address of the ADC
ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)  # Set the gain to 6.144V

# Calibration value obtained from your calibration process
calibration_value = 21.34 - 0.7  # Replace this with your actual calibration value

# Main loop
while True:
    # Read analog voltage from pH sensor
    analog_voltage = ads1115.readVoltage(0)['r']  # Assuming pH sensor is connected to channel 0

    # Calculate pH value using the calibration value
    ph_value = -5.70 * analog_voltage + calibration_value

    # Print pH value
    print("pH Value:", ph_value)

    time.sleep(1)  # Delay for stability (adjust as needed)
