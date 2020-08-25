from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD


import boto3
import requests
import random

import dateutil.parser
import pytz
import os, time
from time import sleep


'''
LINE 1 of the display: show a random, non-blank, non-commented line of a file Ivan and Drew control

LINE 2 of the display: show some UV and sunset data 
'''

# LINE 1 
botosess = boto3.Session(
    aws_access_key_id=os.environ['LCD_TEASER_AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['LCD_TEASER_AWS_SECRET_KEY'],
)

s3 = botosess.resource('s3')

obj = s3.Object('geoffriverpi', 'lcdstuff1.txt')
mainfile = obj.get()['Body'].read().decode('utf-8') 

# real lines
realies = [line.strip() for line in mainfile.splitlines() if len(line.strip())>0 and not line.strip().startswith('#')]

# show this one
line1msg = random.choice(realies)


# LINE 2 
## get the other stuff
# drew signed up for this thru his google 
uvr = requests.get('https://api.openuv.io/api/v1/uv?lat=37.300622&lng=-107.868322', headers={'x-access-token':'680a9667af50df2fac5f2e2cec4d31d4'})
uvidx = "%.1f" % round(uvr.json()['result']['uv'],1)

sunsetdt = dateutil.parser.parse(uvr.json()['result']['sun_info']['sun_times']['sunset'])
animastz = pytz.timezone('US/Mountain')

#idk why this was so hard i hate it
sunset = sunsetdt.astimezone(animastz).strftime('%-I:%M %p')

line2msg = 'UV Index: ' + uvidx + ' | Sunset At: ' + sunset


def loop():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):
        lcd.setCursor(0,0)  # set cursor position
        lcd.message(line1msg + '\n' + line2msg)
        sleep(1.3)

        for i in range(max(len(line1msg,line2msg))-16):         
            lcd.DisplayLeft()
            sleep(.55)
        
        sleep(2)
        lcd.clear()
        
        
def destroy():
    lcd.clear()


## COPIED FROM HELPER FILE

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
