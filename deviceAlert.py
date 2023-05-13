# -*- coding: utf-8 -*-

from devMap import devMap

class deviceAlert(object):
    def __init__(self, influx, devType, threshold = None):
        self._influx = influx
        self._devQueryMap = devMap[devType]
        self._threshold = threshold

        self.overThr = {k : None
                        for k in devMap[devType]['meas']['instance'].keys()}
        self.devResult = {rK : {k : None 
                                for k in devMap[devType][rK]['instance'].keys()} 
                          for rK in self._devQueryMap.keys()}

    def __del__(self):
        if self._influx is not None:
            self._influx.close()

    def _query(self, queryType, instName):
        database = self._devQueryMap[queryType]['db']
        instance = self._devQueryMap[queryType]['instance'][instName]
        metric = self._devQueryMap[queryType]['metric']
        qtype = self._devQueryMap[queryType]['type']
        selector = self._devQueryMap[queryType]['selector']

        queryStr = (f"SELECT {selector}(\"value\") "
                    f"FROM \"{database}\" "
                    f"WHERE (\"instance\" = '{instance}' "
                    f"AND \"metric\" = '{metric}')")

        queryRes = self._influx.query(queryStr)
        
        if queryRes is not None:
            queryVal = qtype(list(queryRes.get_points())[0][selector])

            self.devResult[queryType][instName] = queryVal

            return queryVal

        return None

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, thr):
        self._threshold = thr

    def queryMeas(self, instName):
        return self._query('meas', instName)
    
    def queryStatus(self, instName):
        return self._query('status', instName)

    def getMeas(self):
        measDict = {k : self.queryMeas(k)
                    for k in self.devResult['meas'].keys()}

        self.devResult['meas'].update(measDict)
        
        return self.devResult['meas']

    def getStatus(self):
        statusDict = {k : self.queryStatus(k)
                      for k in self.devResult['status'].keys()}

        self.devResult['status'].update(statusDict)
        
        return self.devResult['status']

    def getOverThreshold(self):
        meas = None
        status = None

        if 'meas' in self._devQueryMap.keys():
            self.getMeas()
            meas = self.devResult['meas']

        if 'status' in self._devQueryMap.keys():
            self.getStatus()
            status = self.devResult['status']

        if self._threshold is None:
            return None

        for k in self.overThr.keys():
            if (status is not None) and (meas is not None):
                self.overThr[k] = ((status[k] == 1) and 
                                   (meas[k] >= self._threshold))
            elif meas[k] is not None:
                self.overThr[k] = (meas[k] >= self._threshold)

        thrNum = 0
        for i,(k,v) in enumerate(self.overThr.items()):
            thrNum = thrNum | (int(v) << i)

        return thrNum
