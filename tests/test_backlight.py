import unittest
import time

from backlight import backlight


class TestCase(unittest.TestCase):
    """
    a simple test case for the backlight client. notice specific devices
    or use cases can not be tested as they are likely to fail on different
    machines, for instance im using a gmux_backlight while someone might be
    using the intel_backlight or aspci_video0
    """
    def setUp(self):
        self.monitor = backlight.Monitor()
        self.monitor_start = self.monitor.brightness
        self.keyboard = backlight.Keyboard()
        self.keyboard_start = self.keyboard.brightness

    def tearDown(self):
        self.monitor.brightness = self.monitor_start
        self.keyboard.brightness = self.keyboard_start

    def test_monitor_increase(self):
        increase = self.monitor.increase()
        self.assertGreater(increase, self.monitor_start)

    def test_monitor_decrease(self):
        decrease = self.monitor.decrease()
        self.assertLess(decrease, self.monitor_start)

    def test_keyboard_increase(self):
        increase = self.keyboard.increase()
        self.assertGreater(increase, self.keyboard_start)

    def test_keyboard_decrease(self):
        decrease = self.keyboard.decrease()
        self.assertLess(decrease, self.keyboard_start)

    def test_monitor_maximum(self):
        value = self.monitor.max_brightness + 10
        self.monitor.brightness = value
        self.assertNotEqual(value, self.monitor.brightness)
        self.assertEqual(self.monitor.brightness, self.monitor.max_brightness)

    def test_keyboard_maximum(self):
        value = self.keyboard.max_brightness + 10
        self.keyboard.brightness = value
        self.assertNotEqual(value, self.keyboard.brightness)
        self.assertEqual(self.keyboard.brightness, self.keyboard.max_brightness)

    def test_monitor_sweep_up(self):
        self.monitor.brightness = 0
        last_val = self.monitor.brightness
        while self.monitor.brightness < self.monitor.max_brightness:
            cur_val = self.monitor.increase()
            time.sleep(0.1)
            self.assertGreater(cur_val, last_val)

    def test_monitor_sweep_down(self):
        self.monitor.brightness = self.monitor.max_brightness
        last_val = self.monitor.brightness
        while self.monitor.brightness > 0:
            cur_val = self.monitor.decrease()
            time.sleep(0.1)
            self.assertLess(cur_val, last_val)

    def test_keyboard_sweep_up(self):
        self.keyboard.brightness = 0
        last_val = self.keyboard.brightness
        while self.keyboard.brightness < self.keyboard.max_brightness:
            cur_val = self.keyboard.increase()
            time.sleep(0.1)
            self.assertGreater(cur_val, last_val)

    def test_keyboard_sweep_down(self):
        self.keyboard.brightness = self.keyboard.max_brightness
        last_val = self.keyboard.brightness
        while self.keyboard.brightness < self.keyboard.max_brightness:
            cur_val = self.keyboard.increase()
            time.sleep(0.1)
            self.assertLess(cur_val, last_val)

