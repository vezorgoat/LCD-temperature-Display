import time
import sys
sys.path.append('../')
from CQRobot_ADS1115 import ADS1115

# ADS1115 configuration
ads1115 = ADS1115()
ads1115.setAddr_ADS1115(0x48)
ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)

# Constants
VREF = 5.0
analogBuffer = [0] * 30
analogBufferTemp = [0] * 30
analogBufferIndex = 0
copyIndex = 0
averageVoltage = 0
phValue = 0
temperature = 25  # Temperature in Celsius

# Function to calculate median value
def getMedianNum(iFilterLen):
    analogBufferTemp.sort()
    if iFilterLen & 1 > 0:
        median_value = analogBufferTemp[(iFilterLen - 1) // 2]
    else:
        median_value = (analogBufferTemp[iFilterLen // 2] + analogBufferTemp[iFilterLen // 2 - 1]) / 2
    return median_value

analogSampleTimepoint = time.time()
printTimepoint = time.time()

while True:
    # Read analog voltage from pH sensor
    if time.time() - analogSampleTimepoint > 0.04:
        analogSampleTimepoint = time.time()
        analogBuffer[analogBufferIndex] = ads1115.readVoltage(0)['r']  # Assuming pH sensor is connected to channel 0
        analogBufferIndex += 1
        if analogBufferIndex == 30:
            analogBufferIndex = 0

    # Calculate pH value
    if time.time() - printTimepoint > 0.8:
        printTimepoint = time.time()
        for copyIndex in range(30):
            analogBufferTemp[copyIndex] = analogBuffer[copyIndex]
        print("Voltage (mV):", getMedianNum(30))
        averageVoltage = getMedianNum(30) * (VREF / 1024.0)
        # Adjust the pH calculation formula based on your sensor's characteristics
        phValue = calculate_ph(averageVoltage)
        print("pH Value:", phValue)

        # Reset analog buffer
        analogBuffer = [0] * 30

    time.sleep(0.1)
