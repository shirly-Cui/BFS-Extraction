#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import numpy as np

# 单字节
ChannelInfo = np.dtype({
    'names': ['fpgaChannelNo', 'oswChannelNo', 'channelName'],
    'formats': [np.uint16, np.uint16, 'S4']},
    align=True)

# 共2字节
DataTime = np.dtype({
    'names': ['year', 'month', 'day',  'hour', 'minute', 'second', 'msecond'],
    'formats': [np.uint8, np.uint8, np.uint8, np.uint8, np.uint8, np.uint8, np.uint16]}, align=True)

# 共256字节
# FileHeader32bit = np.dtype({
#     'names': ['version', 'channelInfo', 'sampleTime', 'dataType',
#               'sampleFreqOfZone', 'fibreLength', 'frameCount', 'hardAddtimes',
#               'adWidth', 'pulseWidth', 'startPos', 'endPos',
#               'sampleFreqOfTime', 'sampleCountOfZone', 'sampleCountOfTime', 'cutoffFreq',
#               'edfa', 'raman', 'amplifier', 'serialNo',
#               'reserved'],  # 数据解析用
#     'formats': [np.uint16,  ChannelInfo, DataTime, np.uint32,
#                 np.float32, np.uint32, np.uint32, np.uint32,
#                 np.uint32, np.uint32, np.uint32, np.uint32,
#                 np.float32, np.uint32, np.uint32,  np.float32,
#                 np.float32, np.float32, np.float32,  np.uint32,
#                 'S172'],
#     'itemsize': 256})

FileHeader32bit = np.dtype({
    'names': ['version', 'headerSize', 'sampleTime', 'productType', 'dataType', 'channelInfo',
              'sampleFreqOfZone', 'fibreLength', 'frameCount', 'hardAddtimes',
              'adWidth', 'pulseWidth', 'sampleStyle', 'startPos', 'endPos',
              'edfaValue', 'ramanValue', 'amplifier',
              'sampleFreqOfTime', 'sampleCountOfZone', 'sampleCountByTime', 
              'serailNo', 'startFreq', 'freqGap', 'sweepCount', 'power',
              'reserved'],  # 数据解析用
    'formats': [np.uint16, np.uint16, DataTime, np.uint16, np.uint16, ChannelInfo,
                np.float32, np.uint32, np.uint32, np.uint32,
                np.uint32, np.uint32, np.uint32, np.uint32, np.uint32,
                np.float32, np.float32, np.float32,
                np.float32, np.uint32, np.uint32, 
                np.uint32, np.float32, np.float32, np.uint32, np.float32,
                'S152'],
    'itemsize': 256})

# 16bit数据头说明
SynchronousTime = np.dtype({
    'names': ['second', 'nanoSecond'],
    'formats': [np.uint32, np.uint32]})

FileHeader16bit = np.dtype({
    'names': ['version', 'headerSize', 'year', 'month', 'day',
              'hour', 'minute', 'second', 'millisecond', 'productType',
              'dataType', 'fpgaChannelNo', 'oswChannelNo', 'channelName1', 'channelName2',
              'channelName3', 'channelName4', 'sampleFreqIntergerPart', 'sampleFreqFractionPart', 'fiberLengthLow',
              'fiberLengthHigh', 'frameCount', 'hardAddtimes', 'adWidth', 'pulseWidth',
              'sampleStyle', 'startPos', 'endPosLow', 'endPosHigh', 'sampleCountOfZoneLow',
              'sampleCountOfZoneHigh', 'edfaValueIntegerPart', 'edfaValueFractionPart', 'ramanValueIntegerPart', 'ramanValueFractionPart',
              'amplifierIntegerPart', 'amplifierFractionPart', 'sampleFreqIntegerPartByTime', 'sampleFreqFractionPartByTime', 'sampleCountByTime',
              # syncTime:占用4个uint16大小
              'serailNo', 'syncTime', 'lowSampleFreqIntergerPart', 'lowSampleFreqFractionPart',
              'reserved'],  # 数据解析用
    'formats': [np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, SynchronousTime, np.uint16, np.uint16, 'S162'],
    'itemsize': 256})

FileHeaderV1604 = np.dtype({
    'names': ['version',  'channelName1', 'channelName2', 'channelName3', 'sampleFreqOfZone',
              'fiberLength', 'startPos', 'endPos', 'sampleCountOfZone', 'pulseWidth',
              'frameCount', 'hardAddtimes', 'softwareAddtimes', 'sampleFreqIntegerPartByTime', 'sampleFreqFractionPartByTime', 
              'sampleCountByTime', 'gapofZone', 'adWidth', 'amplifier', 'ramanValue1', 
              'ramanValue2', 'edfaStyle', 'edfaValue1', 'edfaValue2', 'year',
              'month', 'day', 'hour', 'minute', 'second', 
              'millisecond', 'reserved'],
    'formats': [np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, np.uint16, np.uint16, np.uint16, np.uint16,
                np.uint16, 'S66'],
    'itemsize': 128})
