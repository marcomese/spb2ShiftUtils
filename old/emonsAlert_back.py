# -*- coding: utf-8 -*-

class emons(object):
    def __init__(self, influx, threshold = None):
        self._emonStatusInst = {'EMON5' : 8,
                                'EMON6' : 0}
        self._alertStr = "\a\033[31m{} over thresholds!\033[37m\n"
        self._emonAlertMap = {0 : "",
                              1 : self._alertStr.format('EMON5'),
                              2 : self._alertStr.format('EMON6'),
                              3 : self._alertStr.format('Both EMONs')}
        self._emonPwrMap = {0 : 'OFF',
                            1 : 'ON'}
        self._threshold = threshold if threshold is not None else 270
        self._influx = influx

        self.overThr = {'EMON5' : False,
                        'EMON6' : False}
        self.phdPower = {'EMON5' : 0.0,
                         'EMON6' : 0.0}
        self.status = {'EMON5' : 'OFF',
                       'EMON6' : 'OFF'}
        self.alert = ""

    def __str__(self):
        v = ("EMON5: {} P = {}pW\nEMON6: {} P = {}pW")

        return self.checkThreshold()+v.format(self.status['EMON5'],
                                              self.phdPower['EMON5'],
                                              self.status['EMON6'],
                                              self.phdPower['EMON6'])

    def emonPhdQuery(self, emonN):
        queryStr = (f"SELECT last(\"value\") FROM \"EMON\" WHERE "
                    f"(\"instance\" = '{emonN}' AND "
                    f"\"metric\" = 'phd_power')")
        
        queryRes = self._influx.query(queryStr)
        
        if queryRes is not None:
            return float(list(queryRes.get_points())[0]['last'])
        
        return None

    def emonStatusQuery(self, emonN):
        queryStr = (f"SELECT last(\"value\") FROM \"SSPC\" WHERE "
                    f"(\"instance\" = '{self._emonStatusInst[emonN]}' AND "
                    "\"metric\" = 'power')")
        
        queryRes = self._influx.query(queryStr)
        
        if queryRes is not None:
            return int(list(queryRes.get_points())[0]['last'])
        
        return None

    def getPhdPower(self):
        emonP = {'EMON5' : self.emonPhdQuery(5),
                 'EMON6' : self.emonPhdQuery(6)}

        self.phdPower.update(emonP)
        
        return emonP

    def getStatus(self):
        emonS = {'EMON5' : self._emonPwrMap[self.emonStatusQuery('EMON5')],
                 'EMON6' : self._emonPwrMap[self.emonStatusQuery('EMON6')]}
        
        self.status.update(emonS)
        
        return emonS

    def checkThreshold(self):
        self.getPhdPower()
        self.getStatus()

        for k in self.phdPower.keys():
            if self.phdPower[k] is not None:
                self.overThr[k] = ((self.status[k] == 'ON') and 
                                   (self.phdPower[k] >= self._threshold))

        emonNum = ((int(self.overThr['EMON6']) << 1) | 
                    int(self.overThr['EMON5']))

        self.alert = f"{self._emonAlertMap[emonNum]}"

        return self.alert

if __name__ == '__main__':
    import sys
    from time import sleep
    from influxdb import InfluxDBClient
    from influxdb.exceptions import InfluxDBClientError

    timeInterval = 5
    threshold = None

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

        emon = emons(influx, threshold)

        while(1):
            print(emon)

            sleep(timeInterval)

    except InfluxDBClientError as err:
        sys.exit(f"{err}")
        influx.close()

    except KeyboardInterrupt:
        sys.exit("Exiting...")
        influx.close()
