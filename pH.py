import spidev
import time
import logging
import RPi.GPIO as GPIO

# Setup GPIO for LED
LED_PIN = 18  # Example pin, choose one available on your Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Setup logging
logging.basicConfig(filename='pH_data.log', level=logging.INFO)

# Define SPI bus and device (ADC)
spi = spidev.SpiDev()
spi.open(0, 0)  # Check which SPI device is being used on your Pi (0 or 1) and select the appropriate one

# Function to read SPI data from ADC channel
def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Main function
def main():
    try:
        while True:
            # Read data from ADC connected to pH module
            adc_value = read_adc(0)  # Replace 0 with the actual channel number your pH module is connected to

            # Convert ADC value to pH value (you'll need to calibrate this based on your pH module)
            pH_value = convert_to_pH(adc_value)  # You need to implement this function

            # Print and log pH value
            logging.info("pH Value: %f", pH_value)

            # Toggle LED
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(LED_PIN, GPIO.LOW)

            # Adjust the delay based on your sampling requirements
            time.sleep(1)

    except KeyboardInterrupt:
        spi.close()
        GPIO.cleanup()

# Function to convert ADC value to pH value (you'll need to implement this based on your pH module's calibration)
def convert_to_pH(adc_value):
    # Implement your conversion logic here
    # This is just a placeholder
    pH_value = adc_value * 0.1  # Example conversion, replace with your actual conversion formula
    return pH_value

if __name__ == "__main__":
    main()
