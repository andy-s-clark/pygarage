#!/usr/bin/python

import time
import signal
import sys
import RPi.GPIO as GPIO


def signal_handler(signalnum, frame):
    GPIO.cleanup()
    SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n)
                                 for n in dir(signal)
                                 if n.startswith('SIG') and '_' not in n)
    print('Caught signal %s, exiting.' % SIGNALS_TO_NAMES_DICT[signalnum])
    sys.exit(0)


for signal_to_catch in [signal.SIGINT, signal.SIGTERM]:
    signal.signal(signal_to_catch, signal_handler)

IN_CHANNELS = [8, 7]
OUT_CHANNELS = [27, 22, 23, 24, 10, 9, 25, 11]

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN_CHANNELS, GPIO.IN)
GPIO.setup(OUT_CHANNELS, GPIO.OUT)


