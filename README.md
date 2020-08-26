### Calibrate the direction of the arms

```
$ cd /home/pi/riverboard
$ GPIOZERO_PIN_FACTORY=pigpio python
>>> from riverboard import *
>>> setFlow(100) # and then 200, 300, 400, 500, 1000 and 10000
# and write on the cardboard where the toothpick is pointing.
# Then to move the other servo
>>> setTemp(0) # and then e.g. 5, 10, 15, 20, 25 - setTemp takes in Celsius, you can pick instead Fahrenheit values like 40F, 50F, 60F etc and convert them into 4.444C, 10C, 15.555C etc if you want to make non-metric labels
```

### Setting up services

    # set environment variables
    # edit /home/pi/env

    # link it up
    ln -s /home/pi/riverboard/riverboard_lcd.service ~/.config/systemd/user/
    # reload the daemons
    systemctl daemon-reload --user
    # see if it's there
    systemctl --user list-unit-files | grep riverboard
    # see if there's issues
    systemd-analyze verify riverboard_lcd.service
    #start it
    systemctl start riverboard_lcd --user
    # see status
    systemctl status --user riverboard_lcd
    # see messages this boot
    journalctl -u riverboard_lcd.service -b
