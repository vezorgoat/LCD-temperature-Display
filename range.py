# Clear the display
display.lcd_clear()

# Get current temperature
temp_c, temp_f = read_temp()

# Determine the temperature range and corresponding message
if 0 <= temp_c <= 30:
    message = "Mid"
elif 30 < temp_c <= 70:
    message = "Good"
elif 80 <= temp_c <= 120:
    message = "Bad"
else:
    message = "Unknown"

# Get current time
current_time = datetime.now().strftime("%I:%M %p")

# Write time to display
display.lcd_display_string("Time: " + current_time, 1)

# Write temperature and message to display
display.lcd_display_string("Temp: {:.1f}C {:.1f}F".format(temp_c, temp_f), 2)
display.lcd_display_string("Status: " + message, 3)
