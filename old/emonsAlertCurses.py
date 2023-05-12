#!/usr/bin/python3

import sys
import curses
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from spb2Devices import emons
from queue import Queue, Empty
from threading import Thread
from time import sleep
import re

dataQueue = Queue()
logQueue = Queue()

UPPERWIN_WIDTH    = 0.5
UPPERWIN_HEIGHT   = 0.8
LOWERWIN_WIDTH    = 1
LOWERWIN_HEIGHT   = 1-UPPERWIN_HEIGHT
LATERALWIN_WIDTH  = 1-UPPERWIN_WIDTH
LATERALWIN_HEIGHT = 1-LOWERWIN_HEIGHT

LOG = 1
ERR = 2

def exitLoop(*args):
    pass

def setThr(emon, thr):
    if thr != "":
        emon.threshold = int(thr)

execCmd = {'exit'          : exitLoop,
           'set threshold' : setThr}

commands = '|'.join(execCmd.keys())

cmdRegex = f"({commands})\s*(.*)?"
cmdParser = re.compile(cmdRegex)

def logThread(logWin):
    i = 0
    while True:
        logWin.erase()

        try:
            inp = logQueue.get(timeout=0.1)
            if inp == 'exit':
                return
            else:
                logWin.addstr(i, 1, inp)
                i = i + 1
  
        except Empty:
            pass

        logWin.box()

        logWin.noutrefresh()

        curses.doupdate()

def dataThread(mainWin, emon, timeInterval):
    while True:
        mainWin.erase()
       
        alert = emon.alert

        color = curses.color_pair(LOG)
        
        alertStr = ""
        if alert != "":
            alertStr = f"{alert} over threshold!"
            color = curses.color_pair(ERR)
            curses.beep()

        mainWin.addstr(1, 1, f"EMON THR = {emon.threshold}", color)            
        mainWin.addstr(2, 1, alertStr, color)

        mainWin.box()

        try:
            inp = dataQueue.get(timeout=0.1)
            if inp == 'exit':
                return
        except Empty:
            pass

        mainWin.noutrefresh()
        
        sleep(timeInterval)

def cmdThread(cmdWin, emon):
    while True:
        args = None
        cmdWin.erase()

        cmdWin.addstr(1, 1, "Enter a command:")
        cmdWin.addstr(2, 1, ">")

        cmdWin.box()

        cmd = cmdWin.getstr().decode('utf-8')

        parsedCmd = cmdParser.findall(cmd)
        if parsedCmd != []:
            cmd, args = parsedCmd[0]

        dataQueue.put(cmd)
        logQueue.put(cmd)

        if cmd not in execCmd.keys():
            cmdWin.addstr(2, 1, "Bad command!")
        elif cmd in execCmd.keys() and cmd != "exit":
            execCmd[cmd](emon, args)
        else:
            return

        cmdWin.noutrefresh()

def main():
    timeInterval = 5
    threshold = 150
    
    argc = len(sys.argv)
    argv = sys.argv

    if argc == 1:
        pass
    elif argc == 2:
        timeInterval = int(argv[1])
    elif argc == 3:
        timeInterval = int(argv[1])
        threshold = int(argv[2])
    else:
        sys.exit(f"Use: {argv[0]} [time interval in seconds] [threshold]")           
    
    try:
        stdscr = curses.initscr()
        stdscr.keypad(True)
        curses.curs_set(False)
        curses.start_color()
        curses.init_pair(LOG, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(ERR, curses.COLOR_RED, curses.COLOR_BLACK)

        UPPERWIN_COLS    = int(UPPERWIN_WIDTH*curses.COLS)
        UPPERWIN_LINES   = int(UPPERWIN_HEIGHT*curses.LINES)
        LOWERWIN_COLS    = int(LOWERWIN_WIDTH*curses.COLS)
        LOWERWIN_LINES   = int(LOWERWIN_HEIGHT*curses.LINES)
        LATERALWIN_COLS  = int(LATERALWIN_WIDTH*curses.COLS)
        LATERALWIN_LINES = int(LATERALWIN_HEIGHT*curses.LINES)
    
        upperwin = stdscr.subwin(UPPERWIN_LINES, UPPERWIN_COLS,
                                 0, 0)
        
        lowerwin = stdscr.subwin(LOWERWIN_LINES, LOWERWIN_COLS-1,
                                 UPPERWIN_LINES,0)
        
        lateralwin = stdscr.subwin(LATERALWIN_LINES, LATERALWIN_COLS, 
                                   0, UPPERWIN_COLS)
    
        influx = InfluxDBClient(host='calibano.ba.infn.it',
                                port=8086,
                                database='spbmonitor')
    
        emon = emons(influx, threshold)

        dataThr = Thread(target=dataThread, args=(upperwin, emon, timeInterval))
        cmdThr = Thread(target=cmdThread, args=(lowerwin, emon))
        logThr = Thread(target=logThread, args=(lateralwin,))

        dataThr.start()
        cmdThr.start()
        logThr.start()
    
    except InfluxDBClientError as err:
        sys.exit(f"{err}")
        influx.close()

    except KeyboardInterrupt:
        sys.exit("\nExiting...")
        influx.close()

    finally:
        dataThr.join()
        cmdThr.join()
        logThr.join()
        stdscr.keypad(False)
        curses.endwin()

if __name__ == '__main__':
    main()
