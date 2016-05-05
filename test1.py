#!/usr/bin/python

import time
import signal
import sys
import RPi.GPIO as GPIO

def signal_handler(signalnum, frame):
    GPIO.cleanup()
    SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) \
        for n in dir(signal) if n.startswith('SIG') and '_' not in n )
    print('Caught signal %s, exiting.' % SIGNALS_TO_NAMES_DICT[signalnum])
    sys.exit(0)

for signal_to_catch in [signal.SIGINT, signal.SIGTERM]:
    signal.signal(signal_to_catch, signal_handler)

RED_LED_PIN=11
YEL_LED_PIN=13
BLU_LED_PIN=15

SW0_PIN=16
SW1_PIN=18

GPIO.setmode(GPIO.BOARD)

GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(YEL_LED_PIN, GPIO.OUT)
GPIO.setup(BLU_LED_PIN, GPIO.OUT)
GPIO.setup(SW0_PIN, GPIO.IN)
GPIO.setup(SW1_PIN, GPIO.IN)

while True:
    GPIO.output(RED_LED_PIN, True)

    print('SW0: %s  SW1: %s' %(GPIO.input(SW0_PIN), GPIO.input(SW1_PIN)))
    GPIO.output(YEL_LED_PIN, GPIO.input(SW0_PIN))
    GPIO.output(BLU_LED_PIN, GPIO.input(SW1_PIN))

    GPIO.output(RED_LED_PIN, False)
    time.sleep(0.1)

