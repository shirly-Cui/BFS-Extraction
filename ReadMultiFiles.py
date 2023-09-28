import os
import matplotlib.pyplot as plt
from calculationentrance import *

def listdir(path, subfolder, list_name): #subfolder表示是否读取子文件夹
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if (os.path.isdir(file_path)): 
            if subfolder: 
                listdir(file_path, subfolder, list_name)  
        elif os.path.splitext(file_path)[1]=='.dat':  
            list_name.append(file_path)  

def ReadRawFiles(filePath):#读取原始数据
    print('开始BOTDR原始数据提取') 
    rawDataPaths = []
    listdir(filePath, 0, rawDataPaths)
    Datalist = []
    calcTool = calculationentrance()
    for rawDataPath in rawDataPaths:
        if 'raw.dat' in rawDataPath:
            print('路径', rawDataPath)
            rawData = calcTool.getBOTDRRawData(rawDataPath)
            rawData = rawData[:,12:] #去掉前12个数据
            Datalist.append(rawData)
    filenum = len(Datalist)
    frameSize = calcTool.frameSize-12
    sampleFreq = calcTool.sampleFreq
    startFreq = calcTool.startFreq 
    freqGap = calcTool.freqGap
    sweepCount = calcTool.sweepCount
    para = [frameSize, sampleFreq, startFreq, freqGap, sweepCount]
    print('BOTDR原始数据提取完成')
    print('读取文件个数为：', filenum)
    return para, Datalist

def ReadFreqFiles(filePath):#读取频率数据
    print('开始BOTDR频率数据提取')
    FreqPaths = []
    listdir(filePath, 0, FreqPaths)
    Freqlist = []
    calcTool = calculationentrance()
    for FreqPath in FreqPaths:
        print('路径', FreqPath)
        [sampleFreqOfZone, freqData] = calcTool.getBOTDRFreqData(FreqPath)
        freqData = freqData[:,12:] #去掉前12个数据
        Freqlist.append(freqData)
    return Freqlist

def ReadPowFiles(filePath):#读取功率数据
    print('开始BOTDR功率数据提取')
    PowerPaths = []
    listdir(filePath, 0, PowerPaths)
    Powerlist = []
    calcTool = calculationentrance()
    for PowerPath in PowerPaths:
        #print('路径', PowerPath)
        powData = calcTool.getBOTDRPowerData(PowerPath)
        powData = powData[:,12:]
        Powerlist.append(powData)
    return Powerlist

if __name__ == '__main__':
    filePath = "F:/BOTDR/freqdata/"
    Freqlist = ReadFreqFiles(filePath)
    filenum = len(Freqlist)
    for i in range(filenum):
        freqdata1 = Freqlist[i][1]
        plt.figure()
        plt.plot(freqdata1[0:1600])
        plt.title('num = %d' %i)
    
    plt.show()