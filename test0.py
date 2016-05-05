#!/usr/bin/python

from RPi import GPIO

GPIO.setup(18, GPIO.OUT)
GPIO.output(18, False)
print('Hello!');