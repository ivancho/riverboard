from gpiozero import Servo
from time import sleep

adj = 0.45
min_w = (1.0 - adj)/1000
max_w = (2.0 + adj)/1000


def get_servo(pin):
    return Servo(pin, min_pulse_width=min_w, max_pulse_width=max_w)


def test_range():
    # GPIO12 and 13
    s1 = get_servo(12)
    s2 = get_servo(13)

    s1.value = -1
    s2.value = 1

    sleep(0.5)
    for i in range(-100, 101):
        s1.value = i/100.0
        s2.value = -i/100.0
        sleep(0.2)


test_range()
