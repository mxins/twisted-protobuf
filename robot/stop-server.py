#! /usr/bin/env python
#-*-coding:utf-8-*-

from twisted.python import log, failure
import os, signal

def shutdown():
    try:
        pid = int(file('twistd.pid', mode='r').readline())
        os.kill(pid, signal.SIGUSR1)
        os.kill(pid, signal.SIGTERM)
    except IOError, e:
        log.msg( 'UnExpected: No such PID file: twistd.pid in current dir.')
        log.msg( '\tDetail:', str(e))

if __name__ == '__main__':
    shutdown()