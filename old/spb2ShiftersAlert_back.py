# -*- coding: utf-8 -*-

import sys
from time import sleep
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

emon5StatusInst = 8
emon6StatusInst = 0

emon5StatusQuery = (f"SELECT last(\"value\") FROM \"SSPC\" WHERE "
                    f"(\"instance\" = '{emon5StatusInst}' AND "
                    "\"metric\" = 'power')")

emon6StatusQuery = (f"SELECT last(\"value\") FROM \"SSPC\" WHERE "
                    f"(\"instance\" = '{emon6StatusInst}' AND "
                    "\"metric\" = 'power')")

emon5pWQuery = ("SELECT last(\"value\") FROM \"EMON\" WHERE "
                "(\"instance\" = '5' AND "
                "\"metric\" = 'phd_power')")

emon6pWQuery = ("SELECT last(\"value\") FROM \"EMON\" WHERE "
                "(\"instance\" = '6' AND "
                "\"metric\" = 'phd_power')")

defaultThreshold = 270
defaultTimeInterval = 5

emonThrMap = {0 : 'None',
              1 : 'EMON5',
              2 : 'EMON6',
              3 : 'Both EMONs'}

emonPwrMap = {0 : 'OFF',
              1 : 'ON'}

if __name__ == '__main__':
    timeInterval = defaultTimeInterval
    threshold = defaultThreshold

    try:
        influx = InfluxDBClient(host='calibano.ba.infn.it', port=8086, database='spbmonitor')
    
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
    
        while(1):
            emon5pW = float(list(influx.query(emon5pWQuery).get_points())[0]['last'])
            emon6pW = float(list(influx.query(emon6pWQuery).get_points())[0]['last'])
            emon5Status = int(list(influx.query(emon5StatusQuery).get_points())[0]['last'])
            emon6Status = int(list(influx.query(emon6StatusQuery).get_points())[0]['last'])

            emon5OverThr = ((emon5Status == 1) and 
                            (emon5pW >= threshold))
            emon6OverThr = ((emon6Status == 1) and 
                            (emon6pW >= threshold))

            emonNum = (int(emon6OverThr) << 1) | int(emon5OverThr)

            whichEmon = emonThrMap[emonNum]

            if emonNum > 0:
                print(f"\a\033[31m{whichEmon} over thresholds!\033[37m")

            print(f"EMON5: {emonPwrMap[emon5Status]} P = {emon5pW}pW\n"
                  f"EMON6: {emonPwrMap[emon6Status]} P = {emon6pW}pW")

            sleep(timeInterval)

    except InfluxDBClientError as err:
        sys.exit(f"{err}")
        influx.close()

    except KeyboardInterrupt:
        sys.exit("Exiting...")
        influx.close()