# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 15:52:34 2017

@author: pk012
"""

from fileheader import *
from printheader import *
from datatype import *

import numpy as np
import os
import re

class FileReader:
    binit = False
    frameCount = 1
    frameSize = 1
    sampleFreqByZone = 100
    sampleFreqByTime = 3000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = 0
        self.frameCount = 1
        self.frameSize = 1
        self.sampleFreqByZone = 100
        self.sampleFreqByTime = 3000
        self.sampleFreqOfZone = 40
        self.startFreq = 10.2
        self.freqGap = 0.1
        self.sweepCount = 50
        
    #获取数据头部并打印
    def readAndPrintHeader(self, fileName):
        
        binaryData = np.fromfile(fileName, np.uint16)
        self.version = binaryData[0]

        header = []
        if self.version == DataVersion.V1807.value:
            str = np.fromfile(fileName, dtype = FileHeader32bit)
            header=str[0]
            self.frameCount = header['sampleCountOfTime']
            self.frameSize = header['sampleCountOfZone']
            self.sampleFreqByZone = header['sampleFreqOfZone']
            self.sampleFreqByTime = header['sampleFreqOfTime']
            self.adWidth = header['adWidth']
            self.hardAddtimes = header['hardAddtimes']
            self.startFreq = header['startFreq']
            self.freqGap = header['freqGap']
            self.sweepCount = header['sweepCount']
        elif self.version == DataVersion.V1809.value:
            str = np.fromfile(fileName, dtype = FileHeader16bit) 
            header=str[0]
            self.frameCount = header['sampleCountByTime']
            self.frameSize = header['sampleCountOfZoneLow'] + 65536 * header['sampleCountOfZoneHigh']
            self.sampleFreqByZone = header['sampleFreqIntergerPart'] + header['sampleFreqFractionPart']*0.0001
            self.sampleFreqByTime = header['sampleFreqIntegerPartByTime'] + header['sampleFreqFractionPartByTime']*0.0001
            self.adWidth = header['adWidth']
            self.hardAddtimes = header['hardAddtimes']
        elif self.version == DataVersion.V1604.value:
            str = np.fromfile(fileName, dtype = FileHeaderV1604) 
            header=str[0]
            self.frameCount = header['sampleCountByTime']
            self.frameSize =  header['sampleCountOfZone']
            self.sampleFreqByZone = header['sampleFreqOfZone'] * 0.01
            self.sampleFreqByTime = header['sampleFreqIntegerPartByTime'] + header['sampleFreqFractionPartByTime'] * 0.001
            self.adWidth = header['adWidth']
            self.hardAddtimes = header['hardAddtimes']
        elif self.version == DataVersion.V2012.value:
            str = np.fromfile(fileName, dtype = FileHeader32bit)
            header=str[0]
            self.frameCount = header['frameCount']
            #self.frameCount = header['sampleCountByTime'] #数据种类的个数
            self.frameSize =  header['sampleCountOfZone'] #
            self.adWidth = header['adWidth']
            self.hardAddtimes = header['hardAddtimes']
            self.flag = 0   
            self.dataType = header['dataType']
            self.sampleFreqOfZone = header['sampleFreqOfZone'] 
            self.startFreq = header['startFreq']
            self.freqGap = header['freqGap']
            self.sweepCount = header['sweepCount']
        else:
            print("版本号位置")

        #打印文件头        
        if self.binit == False:
            printHeader(self.version, header)
            self.binit = True

    #获取数据体
    def readDataBody(self, fileName):   
        rawData = np.fromfile(fileName, dtype = np.uint16)
        if self.version == DataVersion.V1604.value:
            rawData = rawData[64:]   
        elif (self.version == DataVersion.V1807.value) or (self.version == DataVersion.V1809.value):
            rawData = rawData[128:]   
        else:
            print('unkonwn verion:', self.version)            

        originData = rawData.reshape(self.frameCount, self.frameSize)  
        base = 500.0 / pow(2.0, self.adWidth) / self.hardAddtimes
        originData = originData * base  
        return originData

    def readBOTDRDataBody(self, fileName): 
        originData = []
        if (self.version == DataVersion.V2012.value):
            if self.dataType == 0x01:
                rawData = np.fromfile(fileName, dtype = np.uint32)
                rawData = rawData[64: ]
                originData = rawData.reshape(self.frameCount, self.frameSize) 
                base = 500.0 / pow(2.0, self.adWidth) / self.hardAddtimes
                originData = originData * base  
            else:                
                originData = np.fromfile(fileName, dtype = np.float32) 
                originData = originData[64:]                
                originData = originData.reshape(self.frameSize, self.frameCount) 
                originData = originData.T
        return originData

    def readDataHeader(self, fileName):   
        rawData = np.fromfile(fileName, dtype = np.uint16)
        if self.version == DataVersion.V1604.value:
            rawData = rawData[64:]   
        else:
            rawData = rawData[128:]     
        originData = rawData.reshape(self.frameCount, self.frameSize) 
        timeFlag = []
        if self.version == DataVersion.V1807.value:
            timeFlag = originData[:,3] + originData[:,4] * 65535
        elif self.version == DataVersion.V1809.value:
            timeFlag = originData[:,1] + originData[:,2] * 65536
        elif self.version == DataVersion.V1604.value:
            timeFlag = originData[:,3] + originData[:,4] * 65535
        return timeFlag

    def compare(self, x, y):  
        stat_x = os.stat(x)  
        stat_y = os.stat(y)  
        if stat_x.st_ctime > stat_y.st_ctime:  
            return -1  
        elif stat_x.st_ctime < stat_y.st_ctime:  
            return 1  
        else:  
            return 0   

    def getFileList(self, filePath):  
        fullFileNameList = []
        if os.path.exists(filePath):
            fileList = os.listdir(filePath)
            for item in fileList: 
                if item.strip():
                    fullFileNameList.append(filePath + '/' + item)

            fullFileNameList.sort()         
        return fullFileNameList     