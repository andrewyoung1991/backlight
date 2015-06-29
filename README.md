# backlight

backlight is a simple python module for changing the keyboard or monitor backlight brightness. it ships with a command line utility for changing the brightness from your terminal.

```bash
$ backlight-ctl --decrease monitor
$ backlight-ctl --increase keyboard
$ baclkight-ctl --help
usage: backlight-cli [-h] [-i] [-d] [-g] {keyboard,monitor}

changes the backlight brightness

positional arguments:
  {keyboard,monitor}

optional arguments:
  -h, --help          show this help message and exit
  -i, --increase
  -d, --decrease
  -g, --get_current

```

## installing

clone the repo and run:
- `python setup.py test`
- `python setup.py install`

if the tests do not pass, there is most likely a permission error addressed later in this readme.

## creating backlight objects

the backlight interface is very simple and all backlights can inherit from the `Backlight` class by providing the path to your backlight hardware (on arch linux this is `/sys/class/backlight` or `/sys/class/led` for keyboards), and optionally the name of the device (the default behavior is to attempt to autodiscover a device).


## allowing non-root users to change the backlight value

by default (in the linux environment) the values of a backlight are only changable by the root user. enabling users to control the backlight on Arch Linux using systemctl requires a service similar to the following

```ini
# /usr/lib/systemd/system/gmux-monitor-backlight.service
# systemctl enable gmux-monitor-backlight.service

[Unit]
Description=Gmux Monitor Backlight
Wants=systemd-backlight@backlight:gmux_monitor.service
After=systemd-backlight@backlight:gmux_monitor.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/chmod 666 /sys/class/backlight/gmux_backlight/brightness

[Install]
WantedBy=multi-user.target
```

on other platforms `/bin/chmod 666 /sys/class/backlight/gmux_backlight/brightness` should do the trick
