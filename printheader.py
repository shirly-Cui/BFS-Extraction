# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:19:37 2017

@author: pk012
"""
from fileheader import *
from datatype import *

def printHeader(version, header):
    if version == 1807:
          printHeader32bit(header)
    elif version == 1809:
          printHeader16bit(header)
    elif version == DataVersion.V1604.value:
          printHeaderV1604(header)
    elif version == DataVersion.V2012.value:
          printHeader32bit(header)
    else:
          print('未知的产品版本：', header['version'])

def printHeader32bit(header):
    print(u'采集信息:')
    print(u'版本号：', header['version'])
    print('数据头大小: ', header['headerSize'])
    print('开始时间：%02d/%02d/%02d-%02d:%02d:%02d-%d' % \
          (header['sampleTime']['year'], \
          header['sampleTime']['month'], \
          header['sampleTime']['day'], \
          header['sampleTime']['hour'], \
          header['sampleTime']['minute'], \
          header['sampleTime']['second'], \
          header['sampleTime']['msecond']))
    print('产品类型: ',header['productType'])  
    print('数据类型: ',header['dataType'])
    print('线路名：%s,通道名：%d%d' % (header['channelInfo']['channelName'], header['channelInfo']['fpgaChannelNo'], header['channelInfo']['oswChannelNo'] ))

    print('空间采样率：', header['sampleFreqOfZone'])
    print('光纤长度: ', header['fibreLength'])
    print('帧数: ', header['frameCount'])
    print('硬件累加次数: ', header['hardAddtimes'])
    print('ad宽度: ', header['adWidth'])
    print('脉冲宽度: ', header['pulseWidth'])
    print('采样类: ', header['sampleStyle'])
   
    print('采样开始位置：', header['startPos'])
    print('采样结束位置: ', header['endPos'])

    print('掺铒光纤放大器：', header['edfaValue']) 
    print('拉曼放大: ', header['ramanValue']) 
    print('电路放大系数', header['amplifier'])

    print('时间采样率：', header['sampleFreqOfTime'])    
    print('时间采样点数: ', header['sampleCountByTime'])   
    print('空间采样点数: ', header['sampleCountOfZone'])

    print('采样序列号：', header['serailNo'])
    print('扫频起始频率: ', header['startFreq'])   
    print('扫频间隔: ', header['freqGap'])
    print('扫频步数: ', header['sweepCount'])
    print('扫频功率: ', header['power'])

def printHeader16bit(header):
    print('采集信息:')
    print('版本号：', header['version'])
    print('数据头大: ', header['headerSize'])
    print('采集时间: %02d%02d%02d-%02d%02d%02d-%d' % \
      (header['year'], \
       header['month'], \
       header['day'], \
       header['hour'], \
       header['minute'], \
       header['second'], \
       header['millisecond']))
    print('产品类型: ',header['productType'])  
    print('数据类型: ',header['dataType'])  

    print('通道名：%d%d, 线路名：%c%c%c%c' % 
      (header['fpgaChannelNo'], 
       header['oswChannelNo'], 
       header['channelName1'],
       header['channelName2'],
       header['channelName3'],
       header['channelName4']))
 
    print('空间采样率：', header['sampleFreqIntergerPart'] + header['sampleFreqFractionPart'] * 0.0001)    
    print('光纤长度: ', header['fiberLengthLow'] + header['fiberLengthHigh'] * 65536)
    print('帧数: ', header['frameCount'])
    print('硬件累加次数: ', header['hardAddtimes'])
    print('ad宽度: ', header['adWidth'])
    print('脉冲宽度: ', header['pulseWidth']) 
    print('采样类型: ', header['sampleStyle']) 
    print('采样开始位置：', header['startPos'])
    print('采样结束位置: ', header['endPosLow'] + header['endPosHigh'] )       
    print('空间采样点数: ', header['sampleCountOfZoneLow'] + header['sampleCountOfZoneHigh'])

    print('掺铒光纤放大器：', header['edfaValueIntegerPart'] + header['edfaValueFractionPart'] * 0.0001) 
    print('拉曼放大: ', header['ramanValueIntegerPart'] + header['ramanValueFractionPart']) 
    print('电路放大系数', header['amplifierIntegerPart'] + header['amplifierFractionPart'] * 0.0001)
    print('时间采样率：', header['sampleFreqIntegerPartByTime'] + header['sampleFreqFractionPartByTime'] * 0.0001)    
    print('时间采样点数: ', header['sampleCountByTime'])          
    print('采样序列号：', header['serailNo'])

def printHeaderV1604(header):
    print('采集信息:')
    print('版本号：', header['version'])
    print('线路名：%c%c%c' % 
       (header['channelName1'],
        header['channelName2'],
        header['channelName3']))
    print('空间采样率：', header['sampleFreqOfZone'] * 0.01)    
    print('光纤长度: ', header['fiberLength'])
    print('采样开始位置：', header['startPos'])
    print('采样结束位置: ', header['endPos'])   
    print('空间采样点数: ', header['sampleCountOfZone'])
    print('脉冲宽度: ', header['pulseWidth']) 
    print('帧数: ', header['frameCount'])
    print('硬件累加次数: ', header['hardAddtimes'])
    print('软件累加次数: ', header['softwareAddtimes'])
    print('时间采样率：', header['sampleFreqIntegerPartByTime'] + header['sampleFreqFractionPartByTime'] * 0.001)
    print('时间采样点数: ', header['sampleCountByTime'])      
    print('空间分辨: ', header['gapofZone'])
    print('ad宽度: ', header['adWidth'])
    print('电路放大系数:', header['amplifier'] * 0.01)
    print('拉曼放大器，一级：%d,二级: %d' % (header['ramanValue1'], header['ramanValue2']))
    print('掺铒光纤放大, 通讯方式: %d, 一级：%d,二级: %d' % (header['edfaStyle'], header['edfaValue1'], header['edfaValue2']))
    print('采集时间: 02d%02d%02d-%02d%02d%02d-%d' % \
      (header['year'], \
       header['month'], \
       header['day'], \
       header['hour'], \
       header['minute'], \
       header['second'], \
       header['millisecond']))
	   