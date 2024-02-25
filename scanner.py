import smbus

# Define the I2C bus number (usually 1 on Raspberry Pi)
bus_number = 1

# Create an instance of the I2C bus
bus = smbus.SMBus(bus_number)

# Define the range of I2C addresses to scan
address_range = range(0x03, 0x78)  # Addresses from 0x03 to 0x77 (inclusive)

def scan_i2c():
    devices = []
    for address in address_range:
        try:
            bus.read_byte(address)
            devices.append(hex(address))
        except Exception as e:
            pass
    return devices

if __name__ == "__main__":
    print("Scanning for I2C devices...")
    i2c_devices = scan_i2c()
    if i2c_devices:
        print("Found the following devices:")
        for device in i2c_devices:
            print(device)
    else:
        print("No I2C devices found.")
