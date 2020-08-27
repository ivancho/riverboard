from gpiozero import Servo
from time import sleep
import math
import requests

URL_API = 'https://waterservices.usgs.gov/nwis/iv/'
DURANGO_SITE = '09361500'
VARS = '00060,00010'

'''
Drew chose to interpret this in a crazy way due to the users manual, which we won't get into
but these pins are, very simply:::!!!!

GPIO12 and GPIO 13
Nothing complicated about that.
'''
PIN1 = 12
PIN2 = 13

ADJ = 0.45
MIN_W = (1.0 - ADJ)/1000
MAX_W = (2.0 + ADJ)/1000


def get_servo(pin):
    return Servo(pin, min_pulse_width=MIN_W, max_pulse_width=MAX_W, initial_value=None)


TEMP_SERVO = get_servo(PIN1)
FLOW_SERVO = get_servo(PIN2)


def setTemp(val_c):
    """Map Celsius [0,26] ([32F, 79F]) linearly to [-1, 1]"""
    TEMP_SERVO.value = val_c/13.0 - 1


def setFlow(val_cfs):
    """
    Map flow logarithmically to [-1, 1] so 100 corresponds to 1, 1000 to -0.5 and 10K to -1
    This is the left (flipped) servo, so -1 corresponds to top.
    """
    ld = math.log10(val_cfs)
    FLOW_SERVO.value = 0.5 * ld**2 - 4 * ld + 7


def get_temp_and_flow():
    r = requests.get(
        '{}/?site={}&format=json&indent=on&variables={}'.format(URL_API, DURANGO_SITE, VARS))
    j = r.json()
    results = []
    for s in j['value']['timeSeries']:
        current = s['values'][0]['value'][0]
        results.append({
            'variable': s['variable']['variableDescription'],
            'value': float(current['value']),
            'timestamp': current['dateTime']
        })

    return results


def set_from_api():
    vals = get_temp_and_flow()
    print(vals)
    for v in vals:
        if v['variable'].startswith('Temperature'):
            print('Setting temp to {}'.format(v['value']))
            setTemp(v['value'])
        elif v['variable'].startswith('Discharge'):
            print('Setting flow to {}'.format(v['value']))
            setFlow(v['value'])
        else:
            raise Exception('Unknown variable from API {}'.format(v))


def show_servo_values():
    print('Temp @ {}, Flow @ {}'.format(TEMP_SERVO.value, FLOW_SERVO.value))


if __name__ == '__main__':
    while True:
        set_from_api()
        sleep(900)
