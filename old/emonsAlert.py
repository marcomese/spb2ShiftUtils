#!/usr/bin/python3

import sys
from time import sleep
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from spb2Devices import emons, BELL, FAIL, UNDERLINE

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
    influx = InfluxDBClient(host='calibano.ba.infn.it',
                            port=8086,
                            database='spbmonitor')

    emon = emons(influx, threshold, [BELL,FAIL,UNDERLINE])

    while(1):
        print(emon)

        sleep(timeInterval)

except InfluxDBClientError as err:
    sys.exit(f"{err}")
    influx.close()

except KeyboardInterrupt:
    sys.exit("\nExiting...")
    influx.close()