import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Assuming SPI device 0, chip select 0

# Function to read data from pH sensor
def read_pH():
    # Read raw data from sensor
    # Replace this with your actual code to read data from the pH sensor
    raw_data = spi.xfer([0x00])  # Example SPI read, replace with your implementation
    return raw_data

try:
    while True:
        # Read data from pH sensor
        sensor_data = read_pH()

        # Print raw sensor data
        print("Raw pH Sensor Data:", sensor_data)

        # Adjust the delay based on your sampling requirements
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
