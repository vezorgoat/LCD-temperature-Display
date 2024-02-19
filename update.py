current_datetime = datetime.now()

# Format date and time
formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

# Write date and time to display
display.lcd_display_string(formatted_datetime, 1)

# Write temperature to display
temp_c, temp_f = read_temp()
display.lcd_display_string("Temp: {:.1f}C {:.1f}F".format(temp_c, temp_f), 2)
