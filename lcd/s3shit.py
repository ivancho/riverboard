from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD


import boto3
import requests
import random
import math
import dateutil.parser
import pytz
import os
import time
from time import sleep
from datetime import datetime
from dataclasses import dataclass


'''
LINE 1 of the display: show a random, non-blank, non-commented line of a file Ivan and Drew control

LINE 2 of the display: show some UV and sunset data
'''

# LINE 1


@dataclass
class APIResponses:
    sunrisetimestamp: float
    sunsettimestamp: float
    lastcalledtimestamp: float
    teasermsg: str
    uvstringmsg: str

    def full_lcd_msg(self) -> str:
        return self.teasermsg + '\n' + self.uvstringmsg

    def max_line_len(self) -> int:
        return max(len(self.teasermsg), len(self.uvstringmsg))

    def call_interval_seconds(self) -> int:
        # give us some headroom over the 50 free api calls
        apicallsperday = 50-5
        # call more in the day than the night... as the UV stuff just doesn't update that much
        daycalls = math.ceil(.75 * apicallsperday)
        nightcalls = apicallsperday-daycalls
        daylen = self.sunsettimestamp-self.sunrisetimestamp
        nightlen = 24*60*60-daylen
        #print(apicallsperday, daycalls, nightcalls)

        now = time.time()
        if now > self.sunrisetimestamp and now < self.sunsettimestamp:
            return math.ceil(daylen/daycalls)

        return math.ceil(nightlen/nightcalls)

    def time_for_next_call(self) -> bool:
        return time.time() > (self.lastcalledtimestamp+self.call_interval_seconds())


def remote_calls() -> APIResponses:
    botosess = boto3.Session(
        aws_access_key_id=os.environ['LCD_TEASER_AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['LCD_TEASER_AWS_SECRET_ACCESS_KEY'],
    )

    s3 = botosess.resource('s3')

    obj = s3.Object('geoffriverpi', 'lcdstuff1.txt')
    mainfile = obj.get()['Body'].read().decode('utf-8')

    # real lines
    realies = [line.strip() for line in mainfile.splitlines() if len(
        line.strip()) > 0 and not line.strip().startswith('#')]

    # show this one
    teasermsg = random.choice(realies)

    # LINE 2
    # get the other stuff
    # drew signed up for this thru his google
    geofflat = 37.300622
    geofflong = -107.868322
    # wanna get fancy use this https://stackoverflow.com/a/39457871
    animastz = pytz.timezone('US/Mountain')

    uvr = requests.get('https://api.openuv.io/api/v1/uv?lat=%f&lng=%f' % (geofflat, geofflong),
                       headers={'x-access-token': os.environ['LCD_OPEN_UV_API_KEY']})
    uvidx = "%.1f" % round(uvr.json()['result']['uv'], 1)

    sunsetdt = dateutil.parser.parse(
        uvr.json()['result']['sun_info']['sun_times']['sunset'])
    sunrisedt = dateutil.parser.parse(
        uvr.json()['result']['sun_info']['sun_times']['sunrise'])

    # idk why this was so hard i hate it
    sunset = sunsetdt.astimezone(animastz).strftime('%-I:%M %p')

    line2msg = 'UV Index: ' + uvidx + ' | Sunset At: ' + sunset

    return APIResponses(sunrisetimestamp=sunrisedt.timestamp(), sunsettimestamp=sunsetdt.timestamp(), lastcalledtimestamp=time.time(), teasermsg=teasermsg, uvstringmsg=line2msg)


def loop():
    mcp.output(3, 1)     # turn on LCD backlight
    lcd.begin(16, 2)     # set number of LCD lines and columns
    resp = None
    while(True):
        if resp is None or resp.time_for_next_call():
            resp = remote_calls()
            print(resp)

        lcd.setCursor(0, 0)  # set cursor position
        lcd.message(resp.full_lcd_msg())
        sleep(1.3)

        for i in range(resp.max_line_len()-16):
            lcd.DisplayLeft()
            sleep(.55)

        sleep(2)
        lcd.clear()


def destroy():
    lcd.clear()


# COPIED FROM HELPER FILE

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)

if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
