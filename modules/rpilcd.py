from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8, charmap='A02', auto_linebreaks=True, backlight_enabled=False)

lcd.clear()
