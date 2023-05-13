# -*- coding: utf-8 -*-
"""
Created on Tue May  9 11:13:31 2023

@author: limadou
"""

devMap = {
    'PDM' : {
        'meas'   : {'db'       : 'HKB',
                    'instance' : {'PDM1' : 4,
                                  'PDM2' : 5,
                                  'PDM3' : 7},
                    'metric'     : 'temperature', 
                    'type'     : float,
                    'selector' : 'last'},
        'status' : {'db'       : 'SSPC',
                    'instance' : {'PDM1' : 7,
                                  'PDM2' : 15,
                                  'PDM3' : 6},
                    'metric'     : 'power', 
                    'type'     : int,
                    'selector' : 'last'}
    },
    'EMON' : {
        'meas'   : {'db'       : 'EMON',
                    'instance' : {'EMON5' : 5,
                                  'EMON6' : 6},
                    'metric'   : 'phd_power',
                    'type'     : float,
                    'selector' : 'last'},
        'status' : {'db'       : 'SSPC',
                    'instance' : {'EMON5' : 8,
                                  'EMON6' : 0},
                    'metric'   : 'power', 
                    'type'     : int,
                    'selector' : 'last'}
    },
    'ZYNQ' : {
        'meas'   : {'db'       : 'Zynq-Board',
                    'instance' : {'ZYNQ1' : 1,
                                  'ZYNQ2' : 2,
                                  'ZYNQ3' : 3},
                    'metric'   : 'temperature',
                    'type'     : float,
                    'selector' : 'mean'}
    }
}