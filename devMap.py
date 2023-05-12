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
                    'type'     : float},
        'status' : {'db'       : 'SSPC',
                    'instance' : {'PDM1' : 7,
                                  'PDM2' : 15,
                                  'PDM3' : 6},
                    'metric'     : 'power', 
                    'type'     : int}
    },
    'EMON' : {
        'meas'   : {'db'       : 'EMON',
                    'instance' : {'EMON5' : '5',
                                  'EMON6' : '6'},
                    'metric'   : 'phd_power',
                    'type'     : float},
        'status' : {'db'       : 'SSPC',
                    'instance' : {'EMON5' : 8,
                                  'EMON6' : 0},
                    'metric'   : 'power', 
                    'type'     : int}
    }
}