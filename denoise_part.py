import numpy as np
import pywt

def calc_RMSE(data, data_denoise): #计算均方根误差
    RMSE = np.sqrt(((data - data_denoise) ** 2).mean())
    return RMSE

def calc_R(data, data_denoise): #计算平滑度指标
    N = len(data)
    sum1 = 0
    sum2 = 0
    for i in range(N-1):
        sum1 = sum1 + (data[i+1] - data[i])**2
        sum2 = sum2 + (data_denoise[i+1] - data_denoise[i])**2
    r = sum2/sum1
    return r

def calc_corr(data, data_denoise): #计算互相关系数
    corr = np.corrcoef(data, data_denoise)
    return corr[0,1]

#计算三个评价指标
def calc_eval(data, data_denoise):
    m = data.shape[0]
    RMSE = np.zeros(m)
    R = np.zeros(m)
    corr = np.zeros(m)
    for i in range(m):
        RMSE[i] = calc_RMSE(data[i], data_denoise[i])#对每行数据（即每个频率下对应数据）求RMSE
        R[i] = calc_R(data[i], data_denoise[i])
        corr[i] = calc_corr(data[i], data_denoise[i])
    print('评价指标：')
    print('RMSE: ', RMSE.mean())
    print('R: ', R.mean())
    print('corr: ', corr.mean())

#小波分解重构
def wavedecrec_single(data, w, l, threshold):
    coffs=pywt.wavedec(data, w, level=l) #将信号进行小波分解
    for i in range(1,len(coffs)):
        coffs[i]=pywt.threshold(coffs[i], threshold*max(coffs[i]))
    datarec=pywt.waverec(coffs, w)#将信号进行小波重构
    return datarec

def wavedecrec(data, w, l, threshold):
    [M,N] = data.shape
    if (N % 2)==0:
        NN = N
    else:
        NN = N+1
    Datarec = np.zeros((M,NN))
    for i in range(M):
        Datarec[i] = wavedecrec_single(data[i,:], w, l, threshold)
    calc_eval(data[:,0:N], Datarec[:,0:N])
    return Datarec[:,0:N]