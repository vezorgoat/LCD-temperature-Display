# Import necessary libraries for communication and display use
import drivers
from time import sleep
from datetime import datetime
import os
import glob
import time

#these tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*')[0] #get file path of sensor

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()

def read_temp_raw():
    with open(device_path +'/w1_slave','r') as f:
        valid, temp = f.readlines()
    return valid, temp
 
def read_temp():
    valid, temp = read_temp_raw()

    while 'YES' not in valid:
        time.sleep(0.2)
        valid, temp = read_temp_raw()

    pos = temp.index('t=')
    if pos != -1:
        #read the temperature .
        temp_string = temp[pos+2:]
        temp_c = float(temp_string)/1000.0 
        temp_f = temp_c * (9.0 / 5.0) + 32.0
        return temp_c, temp_f

try:
    print("Writing to display")
    while True:
        # Clear the display
        display.lcd_clear()
        
        # Write temperature to display
        temp_c, temp_f = read_temp()
        display.lcd_display_string("Temp: {:.1f}C {:.1f}F".format(temp_c, temp_f), 1)

        # Write just the time to the display
        display.lcd_display_string(str(datetime.now().time()), 2)
        
        sleep(1)
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
