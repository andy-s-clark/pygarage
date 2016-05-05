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
GPIO.setup(IN_CHANNELS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(OUT_CHANNELS, GPIO.OUT)

last0 = 0
last1 = 0
while True:
    in0 = GPIO.input(IN_CHANNELS[0])
    in1 = GPIO.input(IN_CHANNELS[1])
    GPIO.output(OUT_CHANNELS[0], in0)
    GPIO.output(OUT_CHANNELS[1], in1)
    if in0 != last0:
      print('In0 changed from %i to %i' % (last0, in0))
      print('SW0: %s  SW1: %s' % (in0, in1))
    if in1 != last1:
      print('In1 changed from %i to %i' % (last1, in1))
      print('SW0: %s  SW1: %s' % (in0, in1))
    last0 = in0
    last1 = in1

