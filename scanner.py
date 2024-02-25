import smbus
import time
import RPi.GPIO as GPIO

# Define GPIO pins for SDA0 and SCL0
SDA_PIN = 28
SCL_PIN = 29

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SDA_PIN, GPIO.OUT)
GPIO.setup(SCL_PIN, GPIO.OUT)

# Initialize I2C bus
bus = smbus.SMBus(0)  # Use bus 0 for the default I2C interface

def scan_i2c():
    devices = []
    for address in range(128):
        try:
            bus.read_byte(address)
            devices.append(address)
        except Exception as e:
            pass
    return devices

try:
    # Scan for I2C devices
    i2c_devices = scan_i2c()
    if i2c_devices:
        print("I2C devices found:")
        for device in i2c_devices:
            print(f"Address: {hex(device)}")
    else:
        print("No I2C devices found.")

finally:
    # Clean up GPIO
    GPIO.cleanup()
