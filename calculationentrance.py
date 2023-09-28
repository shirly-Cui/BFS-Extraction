#!/usr/bin/python
#-*- coding:UTF-8 -*-

#使用说明
#1、请修改文件路径；filePath
#2、请修改开始和结束坐标

from fileheader import *
from printheader import *
from datatype import *
from filereader import *

import numpy as np

class calculationentrance:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frameSize = 1024
        self.frameCount = 1
        self.sampleFreq = 1   
        self.startFreq = 10.0 
        self.freqGap = 0.05
        self.sweepCount = 50           

    def getDataContinueInfo(self, filePath):        
        fileReader = FileReader() 
        fileList = fileReader.getFileList(filePath)
        fileCount = len(fileList) 

        if fileCount > 0: 
            fileReader.readAndPrintHeader(fileList[0])
            self.frameCount = fileReader.frameCount
            self.frameSize = fileReader.frameSize        
    
        allTimeFlag = np.zeros((1,self.frameCount * fileCount)) 
        fileIndex = 0

        for fileName in fileList: 
            print('读取第%d个数据，共%d个' % (fileIndex + 1, len(fileList)))
            header = fileReader.readDataHeader(fileName)
            allTimeFlag[0, fileIndex * self.frameCount : (fileIndex + 1) * self.frameCount] = header
            fileIndex = fileIndex + 1
        
        return allTimeFlag

    def getOriginData(self, fileName):        
        fileReader = FileReader()         
        fileReader.readAndPrintHeader(fileName)
        self.frameCount = fileReader.frameCount
        self.frameSize = fileReader.frameSize
        self.sampleFreqByZone = fileReader.sampleFreqByZone
        self.sampleFreqByTime = fileReader.sampleFreqByTime          
        originData = fileReader.readDataBody(fileName)        
        return originData

    def getFFTData(self, fileName, startPos, endPos):        
        origindData = self.getOriginData(fileName) 
        
        calclData = origindData[:,startPos:endPos]
        N = self.frameCount
        dotNum = len(calclData[0])
        xf = np.linspace(0, 1, N) * self.sampleFreqByTime
        xf = xf - self.sampleFreqByTime/2

        shiftFreq = np.zeros((dotNum, N))
        shifted = []
        #按列计算    
        for i in range(dotNum - 1):
            array = calclData[:,i] - np.mean(calclData[:,i])
            transformed = np.fft.fft(array) * 2/N 
            transformed = abs(transformed)
            shifted = np.fft.fftshift(transformed) #使用fftshift函数进行移频操作。
            shiftFreq[i] = shifted

        shifted = np.transpose(shifted)
        return xf, shiftFreq    
    
    def getDataStabilityInfo(self, filePath, startPos, endPos):
        fileReader = FileReader() 
        fileList = fileReader.getFileList(filePath)
        fileCount = len(fileList) 

        if fileCount > 0: 
            fileReader.readAndPrintHeader(fileList[0])
            self.frameCount = fileReader.frameCount
            self.frameSize = fileReader.frameSize        
    
        voltageMin = np.zeros((1, fileCount)) 
        voltageMax = np.zeros((1, fileCount)) 
        fileIndex = 0
        dotCount = int(endPos - startPos) #计算的点数

        for fileName in fileList: 
            print('读取第%d个数据，共%d个' % (fileIndex + 1, len(fileList)))
            #获取原始数据
            originData = fileReader.readDataBody(fileName) 
            Y0 = []
            for index in range(len(originData[:, 1])): #按行计算               
                #data = [1,3,2,4]
                #Y1 = sorted(data, reverse = True)
                Y1 = sorted(originData[index, startPos:endPos], reverse = True)
                Y2 = Y1[0:int(dotCount/2)]
                Y0.append(sum(Y2)/int(dotCount/2))
 
            voltageMin[0, fileIndex] = min(Y0)
            voltageMax[0, fileIndex] = max(Y0)
            fileIndex = fileIndex + 1

        return voltageMax, voltageMin 

    def getBOTDRRawData(self, fileName):
        fileReader = FileReader()               
        fileReader.readAndPrintHeader(fileName)
        
        self.frameCount = fileReader.frameCount
        self.frameSize = fileReader.frameSize
        self.sampleFreq = fileReader.sampleFreqOfZone 
        self.startFreq = fileReader.startFreq 
        self.freqGap = fileReader.freqGap
        self.sweepCount = fileReader.sweepCount             
        originData = fileReader.readBOTDRDataBody(fileName)        
        return originData

    def getBOTDRPowerData(self, fileName):  
        fileReader = FileReader()                 
        fileReader.readAndPrintHeader(fileName)           
        originData = fileReader.readBOTDRDataBody(fileName)  

        #须判断是否包含功率数据
        resData = np.zeros((2, fileReader.frameSize))
        self.dataType = fileReader.dataType
        if self.dataType & 0x04:
            #for index in np.arange(0, self.frameSize, 1):  
            resData[0, :] = originData[0, :]
            resData[1, :] = originData[1, :]
        else:
            print("无功率数据")
        return resData

    def getBOTDRFreqData(self, fileName):
        fileReader = FileReader()       
        fileReader.readAndPrintHeader(fileName) 
        sampleFreqOfZone = fileReader.sampleFreqOfZone                      
        originData = fileReader.readBOTDRDataBody(fileName)  

        #须判断是否包含频率数据
        resData = np.zeros((2, fileReader.frameSize))
        self.dataType = fileReader.dataType
        if self.dataType & 0x08: 
            resData[0, :] = originData[0, :]
            freqIndex = 1
            if self.dataType & 0x04: #有功率数据，则频率数据位于下一行
                freqIndex = freqIndex + 1  
            resData[1, :] = originData[freqIndex, :]

        else:
            print("无频率数据")

        return [sampleFreqOfZone, resData]

    def getBOTDRTemperatureData(self, fileName):
        fileReader = FileReader()        
        fileReader.readAndPrintHeader(fileName)                 
        originData = fileReader.readBOTDRDataBody(fileName)  

        resData = np.zeros((2, fileReader.frameSize))
        self.dataType = fileReader.dataType
        if self.dataType & 0x10:
            resData[0, :] = originData[0, :]
            freqIndex = 1

            if self.dataType & 0x04 :
                freqIndex = freqIndex + 1

            if self.dataType & 0x08 :
                freqIndex = freqIndex + 1   
            resData[1, :] = originData[freqIndex, :]
        else:
            print("无温度数据")    
        return resData

    def getBOTDRStrainData(self, fileName):
        fileReader = FileReader()        
        fileReader.readAndPrintHeader(fileName)                 
        originData = fileReader.readBOTDRDataBody(fileName)
      
        resData = np.zeros((2, fileReader.frameSize))
        self.dataType = fileReader.dataType
        if self.dataType & 0x20:
            resData[0, :] = originData[0, :]

            freqIndex = 1        
            if self.dataType & 0x04:
                freqIndex = freqIndex + 1

            if self.dataType & 0x08:
                freqIndex = freqIndex + 1

            if self.dataType & 0x10:
                freqIndex = freqIndex + 1

            resData[1, :] = originData[freqIndex, :]
        else:
            print("无应变数据")
        return resData

if __name__ == '__main__':
    calcTool = calculationentrance()
    filePath = 'D:\\设备维护\\pyqt测试数据集\\156'
    #calcTool.getDataContinueInfo(filePath)   #计算连续性用

    # fileName = 'D:\\ktdata\\ch00/ch00_181210_191718_558.dat'
    # originData = calcTool.getOriginData(fileName)    
    # calcTool.getFFTData(fileName, 1, 5)    #计算频率用

    calcTool.getDataStabilityInfo(filePath,500,1000)
