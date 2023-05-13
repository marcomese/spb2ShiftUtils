#!/usr/bin/python3

import sys
from time import sleep
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from spb2Devices import emons, pdms, zynqs, BELL, FAIL, UNDERLINE
import argparse as ap

alertStyle = [BELL,FAIL,UNDERLINE]
    

if __name__ == '__main__':
    parser = ap.ArgumentParser(description = 'Produce sound alerts when a device exceed threshold')

    parser.add_argument('-t','--time-interval', type=int,
                        help = "set the time interval between measurements",
                        default = 5)
    parser.add_argument('-e','--emons-threshold', type=int,
                        help = "set the threshold for EMONs",
                        default = 250)
    parser.add_argument('-p','--pdms-threshold', type=int,
                        help = "set the threshold for PDMs temperature",
                        default = 30)
    parser.add_argument('-z','--zynqs-threshold', type=int,
                        help = "set the threshold for ZYNQs temperature",
                        default = 80)

    args = parser.parse_args()

    timeInterval = args.time_interval
    emonsThr = args.emons_threshold
    pdmsThr = args.pdms_threshold
    zynqsThr = args.zynqs_threshold

    try:
        influx = InfluxDBClient(host='calibano.ba.infn.it',
                                port=8086,
                                database='spbmonitor')
    
        emon = emons(influx, emonsThr, alertStyle)
    
        pdm = pdms(influx, pdmsThr, alertStyle)
        
        zynq = zynqs(influx, zynqsThr, alertStyle)
    
        while(1):
            print(emon)
            print(pdm)
            print(zynq)
    
            sleep(timeInterval)
    
    except InfluxDBClientError as err:
        sys.exit(f"{err}")
        influx.close()
    
    except KeyboardInterrupt:
        sys.exit("\nExiting...")
        influx.close()