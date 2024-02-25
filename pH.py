import spidev
import time

# Define SPI bus and device (ADC)
spi = spidev.SpiDev()
spi.open(0, 0)  # Check which SPI device is being used on your Pi (0 or 1) and select the appropriate one

# Function to read SPI data from ADC channel
def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

try:
    while True:
        # Read data from ADC connected to pH module
        adc_value = read_adc(0)  # Replace 0 with the actual channel number your pH module is connected to
        
        # Print ADC value
        print("ADC Value:", adc_value)

        # Adjust the delay based on your sampling requirements
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
