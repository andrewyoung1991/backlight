#!/usr/bin/env python

from __future__ import print_function

import os
import re
import configparser


keyboard_dir = re.compile(r"^.+::kbd_backlight$")
monitor_dir = re.compile(r"^.+_(backlight|video0)$")


class Backlight(object):
    path = None
    is_keyboard = False

    def __init__(self):
        self.device = self.get_device()
        self.brightness_path = os.path.join(self.path, self.device, "brightness")
        self.max_brightness_path = \
            os.path.join(self.path, self.device, "max_brightness")
        self._max_brightness = None

    def get_device(self):
        matcher = keyboard_dir if self.is_keyboard else monitor_dir
        devices = [device for device in os.listdir(self.path) if
            matcher.match(device)]
        return devices[0]

    @property
    def increment_value(self):
        return self.max_brightness // 10

    @property
    def max_brightness(self):
        if not self._max_brightness:
            with open(self.max_brightness_path) as _file:
                self._max_brightness = int(_file.read())
        return self._max_brightness

    def _get_brightness(self):
        with open(self.brightness_path) as _file:
            brightness = int(_file.read())
        return brightness

    def _set_brightness(self, value):
        with open(self.brightness_path, "w") as _file:
            value = str(min(value, self.max_brightness))
            _file.write(value)
        return value

    brightness = property(_get_brightness, _set_brightness)

    def increase(self):
        if self.brightness < self.max_brightness:
            self.brightness = \
                min(self.brightness + self.increment_value, self.max_brightness)
        return self.brightness

    def decrease(self):
        if self.brightness > 0:
            self.brightness = max(self.brightness - self.increment_value, 0)
        return self.brightness


class Keyboard(Backlight):
    path = "/sys/class/leds/"
    is_keyboard = True


class Monitor(Backlight):
    path = "/sys/class/backlight/"


def run():
    import argparse
    parser = argparse.ArgumentParser(description="changes the backlight brightness")
    parser.add_argument(
        "-i", "--increase",
        action="store_true",
        help="increase backlight brightness"
    )
    parser.add_argument(
        "-d", "--decrease",
        action="store_true",
        help="decrease backlight brightness"
    )
    parser.add_argument(
        "-g", "--get_current",
        action="store_true",
        help="get current brightness value"
    )
    parser.add_argument(
        "device",
        choices=("keyboard", "monitor"),
        help="device backlight to adjust"
    )
    args = parser.parse_args()

    if args.device == "keyboard":
        backlight = Keyboard()
    elif args.device == "monitor":
        backlight = Monitor()

    if args.get_current:
        print("{0} brightness is {1}".format(args.device, backlight.brightness))
        return

    try:
        if args.increase:
            value = backlight.increase()
        elif args.decrease:
            value = backlight.decrease()
    except PermissionError as err:
        print("Could not change {0} brightness: \n{1}\ntry rerunning as sudo,"
            " or ask for read/write privleges on {2}".format(args.device, err,
            backlight.brightness_path))
    else:
        print("{0} brightness has been set to {1}".format(args.device, value))

