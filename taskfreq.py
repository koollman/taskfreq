#!/usr/bin/env python3

import time
import signal
import sys

freq=10 #Hz
total_runtime=5 #s

x=[0]

def alarm_handler(signum, frame):
    print("Ending")
    print("iterations: ", x[0])
    real_freq=x[0]/total_runtime
    print("frequency (real)  : ", real_freq)
    print("frequency (wanted): ", freq)
    print("difference :", real_freq-freq)
    sys.exit(0)

signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(total_runtime)

def runtask(i):
    print("runing",i)
    time.sleep(0.05)

# clock-based
while True:
    x[0]+=1
    start=time.monotonic()
    runtask(x[0])
    end=time.monotonic()
    duration=end-start
    time.sleep(1/freq-duration)

## naive sched:
# while True:
#     x[0]+=1
#     runtask(x[0])
#     time.sleep(1/freq)


