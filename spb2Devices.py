# -*- coding: utf-8 -*-

from deviceAlert import deviceAlert

BELL = '\a'
FAIL = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

pwrMap = {0 : 'OFF',
          1 : 'ON'}

class emons(deviceAlert):
    def __init__(self, influx, threshold = None,
                 alertStyles = []):
        super().__init__(influx, 'EMON', threshold)
        
        txtStyle = ''.join(alertStyles)
        
        self._alertStr = "{}{} over thresholds!\033[0m\n"
        self._emonAlertMap = {0 : "",
                              1 : self._alertStr.format(txtStyle,'EMON5'),
                              2 : self._alertStr.format(txtStyle,'EMON6'),
                              3 : self._alertStr.format(txtStyle,'Both EMONs')}

        self._alert = ""

    @property
    def alert(self):
        thrNum = self.getOverThreshold()
        
        self._alert = f"{self._emonAlertMap[thrNum]}"
        
        return self._alert

    def __str__(self):
        thrNum = self.getOverThreshold()

        sStr = []
        for k,v in self.devResult['status'].items():
            sStr.append(f"{k}: {pwrMap[v]} ")

        vStr = []
        for v in self.devResult['meas'].values():
            vStr.append(f"P = {v}pW")

        valueStr = ""
        for s,v in zip(sStr,vStr):
            valueStr = valueStr + s + v + "\n"

        self._alert = f"{self._emonAlertMap[thrNum]}"

        return self._alert+valueStr

class pdms(deviceAlert):
    def __init__(self, influx, threshold = None,
             alertStyles = []):
        super().__init__(influx, 'PDM', threshold)
        
        txtStyle = ''.join(alertStyles)
        
        self._alertStr = "{}{} over thresholds!\033[0m\n"
        self._pdmsAlertMap = {0 : "",
                              1 : self._alertStr.format(txtStyle,'PDM1'),
                              2 : self._alertStr.format(txtStyle,'PDM2'),
                              3 : self._alertStr.format(txtStyle,'PDM1 and PDM2'),
                              4 : self._alertStr.format(txtStyle,'PDM3'),
                              5 : self._alertStr.format(txtStyle,'PDM1 and PDM3'),
                              6 : self._alertStr.format(txtStyle,'PDM2 and PDM3'),
                              7 : self._alertStr.format(txtStyle,'All PDMs')}
        self._alert = ""

    @property
    def alert(self):
        thrNum = self.getOverThreshold()
        
        self._alert = f"{self._emonAlertMap[thrNum]}"
        
        return self._alert
    
    def __str__(self):
        thrNum = self.getOverThreshold()
    
        sStr = []
        for k,v in self.devResult['status'].items():
            sStr.append(f"{k}: {pwrMap[v]} ")

        vStr = []
        for v in self.devResult['meas'].values():
            vStr.append(f"T = {v}°C")
    
        valueStr = ""
        for s,v in zip(sStr,vStr):
            valueStr = valueStr + s + v + "\n"
    
        self._alert = f"{self._pdmsAlertMap[thrNum]}"
    
        return self._alert+valueStr