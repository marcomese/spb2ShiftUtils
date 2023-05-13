# -*- coding: utf-8 -*-

from deviceAlert import deviceAlert

BELL = '\a'
FAIL = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

pwrMap = {0 : 'OFF',
          1 : 'ON'}

alStr = "{}{} over thresholds ({})!\033[0m\n"

class emons(deviceAlert):
    def __init__(self, influx, threshold = None, 
                 alertStyles = [], alertStr = alStr):
        super().__init__(influx, 'EMON', threshold)
        
        txtStyle = ''.join(alertStyles)
        
        self._alertStr = alertStr
        self._emonAlertMap = {0 : "",
                              1 : self._alertStr.format(txtStyle,'EMON5',threshold),
                              2 : self._alertStr.format(txtStyle,'EMON6',threshold),
                              3 : self._alertStr.format(txtStyle,'Both EMONs',threshold)}

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
                 alertStyles = [], alertStr = alStr):
        super().__init__(influx, 'PDM', threshold)
        
        txtStyle = ''.join(alertStyles)
        
        self._alertStr = alertStr
        self._pdmsAlertMap = {0 : "",
                              1 : self._alertStr.format(txtStyle,'PDM1',threshold),
                              2 : self._alertStr.format(txtStyle,'PDM2',threshold),
                              3 : self._alertStr.format(txtStyle,'PDM1 and PDM2',threshold),
                              4 : self._alertStr.format(txtStyle,'PDM3',threshold),
                              5 : self._alertStr.format(txtStyle,'PDM1 and PDM3',threshold),
                              6 : self._alertStr.format(txtStyle,'PDM2 and PDM3',threshold),
                              7 : self._alertStr.format(txtStyle,'All PDMs',threshold)}
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

class zynqs(deviceAlert):
    def __init__(self, influx, threshold = None,
                 alertStyles = [], alertStr = alStr):
        super().__init__(influx, 'ZYNQ', threshold)
        
        txtStyle = ''.join(alertStyles)
        
        self._alertStr = alertStr
        self._zynqAlertMap = {0 : "",
                              1 : self._alertStr.format(txtStyle,'ZYNQ1',threshold),
                              2 : self._alertStr.format(txtStyle,'ZYNQ2',threshold),
                              3 : self._alertStr.format(txtStyle,'ZYNQ1 and ZYNQ2',threshold),
                              4 : self._alertStr.format(txtStyle,'ZYNQ3',threshold),
                              5 : self._alertStr.format(txtStyle,'ZYNQ1 and ZYNQ3',threshold),
                              6 : self._alertStr.format(txtStyle,'ZYNQ2 and ZYNQ3',threshold),
                              7 : self._alertStr.format(txtStyle,'All ZYNQs',threshold)}
        self._alert = ""

    @property
    def alert(self):
        thrNum = self.getOverThreshold()
        
        self._alert = f"{self._zynqAlertMap[thrNum]}"
        
        return self._alert
    
    def __str__(self):
        thrNum = self.getOverThreshold()
    
        vStr = []
        for k,v in self.devResult['meas'].items():
            vStr.append(f"{k} T = {v:.2f}°C")
    
        valueStr = ""
        for v in vStr:
            valueStr = valueStr + v + "\n"
    
        self._alert = f"{self._zynqAlertMap[thrNum]}"
    
        return self._alert+valueStr
