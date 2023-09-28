# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 11:51:20 2017

@author: pk012
"""

from enum import Enum

#@unique
class DataType(Enum):
    RawData = 0x01
    BlockData = 0x04
    LowFreqData = 0x0f
    PhiOTDRData = 0x1f
    MultiSystem_V03 = 0x1003

#@unique
class DataVersion(Enum):
    V1807 = 1807
    V1809 = 1809
    V1604 = 1604
    V2012 = 2012