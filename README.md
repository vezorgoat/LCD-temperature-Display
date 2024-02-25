pip install smbus2
sudo i2cdetect -y 1


current_datetime = datetime.now()

# Format date and time
formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

# Write date and time to display
display.lcd_display_string(formatted_datetime, 1)

# Write temperature to display
temp_c, temp_f = read_temp()
display.lcd_display_string("Temp: {:.1f}C {:.1f}F".format(temp_c, temp_f), 2)


pip install adafruit-blinka

pip install adafruit-circuitpython-charlcd


sudo pip install spidev
