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

    # pigpiod must be running -- it should be installed
    sudo systemctl status pigpiod.service
    # it is a system service and cannot be depended on by user services like our python stuff

    # user needs to run when no one is logged in
    sudo loginctl enable-linger pi

    # edit sensitive environment variables
    # edit /home/pi/.riverboard_lcd.env (there are already some values that are needed in there)

    # link it up
    ln -s /home/pi/riverboard/riverboard_lcd.service ~/.config/systemd/user/
    ln -s /home/pi/riverboard/riverboard_servos.service ~/.config/systemd/user/
    # reload the daemons
    systemctl --user daemon-reload
    # see if it's there
    systemctl --user list-unit-files | grep riverboard
    # see if there's issues
    systemd-analyze verify riverboard_lcd.service
    systemd-analyze verify riverboard_servos.service
    #start it
    systemctl --user start riverboard_lcd
    systemctl --user start riverboard_servos
    # see status
    systemctl status --user riverboard_lcd
    systemctl status --user riverboard_servos

    # enable it (& start it) to survive restarts
    systemctl --user enable riverboard_lcd
    systemctl --user start riverboard_lcd
    systemctl --user status riverboard_lcd

    systemctl --user enable riverboard_servos
    systemctl --user start riverboard_servos
    systemctl --user status riverboard_servos

    # see messages
    journalctl --user-unit riverboard_lcd.service
    journalctl --user-unit riverboard_servos.service
