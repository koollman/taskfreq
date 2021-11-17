#!/usr/bin/env python3

import time
import signal
import sys
import random

# global variable counting iterations
globals={'iter':0,
         'freq':1}


def task_basic(i):
    print("basic runing",i)
    time.sleep(0.05)

def task_random(i):
    print("random runing",i)
    # delay between 0 and twice the frequency expected
    freq=globals['freq']
    delay=random.randint(0,int(2*(1/freq)*1000))
    time.sleep(delay/1000)

def tick():
    globals['iter']+=1
    return globals['iter']

# clock-based
def sched_clock_based(runtask, freq):
    while True:
        t=tick()
        start=time.monotonic()
        runtask(t)
        end=time.monotonic()
        duration=end-start
        wait=1/freq-duration
        if wait > 0 :
            time.sleep(wait)

#naive sched:
def sched_naive(runtask, freq):
    while True:
        t=tick()
        runtask(t)
        time.sleep(1/freq)

def run(sched, task, freq=10, runtime=5):
    def alarm_handler(signum, frame):
        print("Ending")
        iter=globals['iter']
        print("iterations: ", iter)
        real_freq=iter/runtime
        print("frequency (real)  : ", real_freq)
        print("frequency (wanted): ", freq)
        print("difference :", real_freq-freq)
        sys.exit(0)

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(runtime)
    globals['freq']=freq
    sched(task, freq)

def get_funcs(prefix):
    import inspect
    members=inspect.getmembers(sys.modules[__name__])
    prefix_size=len(prefix)
    functions = dict((name[prefix_size:],obj) for name,obj in members if (inspect.isfunction(obj) and name.startswith(prefix)))
    return functions

def parse_args(tasks,scheds):
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('scheduler', choices=scheds.keys())
    parser.add_argument('task', choices=tasks.keys())
    parser.add_argument('-f', '--freq', help='frequency in Hertz', default=10, type=float)
    parser.add_argument('-r', '--runtime', help='runtime in seconds', default=5, type=int)
    args=args = parser.parse_args()
    return args

def main():
    tasks=get_funcs('task_')
    scheds=get_funcs('sched_')
    args=parse_args(tasks,scheds)
    print("scheduler:", args.scheduler, "task:",args.task)
    print("freq (Hz):", args.freq, "runtime(s):",args.runtime)
    scheduler=scheds[args.scheduler]
    task=tasks[args.task]
    run(scheduler, task, args.freq, args.runtime)

if __name__ == '__main__':
    main()
    
    
