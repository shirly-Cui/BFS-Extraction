import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import fftpack
from scipy.fftpack import fft

def minmax_normalization(x):
    minx = min(x)
    maxx = max(x)
    xx = (x-minx)/(maxx-minx)
    return xx

def wgn(x, snr):
    len_x = x.shape[0]
    Ps = np.sum(np.power(x, 2)) / len_x
    Pn = Ps / (np.power(10, snr / 10))
    
    noise = np.random.randn(len_x) * np.sqrt(Pn)
    return x + noise

def test_wgn():
    x = np.zeros(20) + 0.5
    y = wgn(x,20)
    noise = y-x
    n = x.shape[0]
    Ps = np.sum(x*x)/n
    Pn = np.sum(noise*noise)/n
    snr = 10*math.log(Ps/Pn,10)
    print('snr = {}'.format(snr))
    plt.figure()
    plt.plot(x)
    plt.plot(y)
    plt.ylim(0,1)
    plt.show()


def smooth(x,num):#滑动平均
    if num // 2 == 0: # 偶数转奇数
        num -= 1
    length = len(x)
    y = np.zeros(length)
    N = (num - 1) / 2
    for i in range(0, length):
        cont_0 = i
        cont_end = length - i - 1
        if cont_0 in range(0,int(N)) or cont_end in range(0,int(N)):
            cont = min(cont_0,cont_end)
            y[i] = np.mean(x[i - cont : i + cont + 1])
        else:
            y[i] = np.mean(x[i - int(N) : i + int(N) + 1])
    return y

def FFT(Fs, data):
    """
    对输入信号进行FFT
    :param Fs:  采样频率
    :param data:待FFT的序列
    :return:
    """
    L = len(data)  # 信号长度
    N = np.power(2, np.ceil(np.log2(L)))  # 下一个最近二次幂，也即N个点的FFT
    result = np.abs(fft(x=data, n=int(N))) / L * 2  # N点FFT
    axisFreq = np.arange(int(N / 2)) * Fs / N  # 频率坐标
    result = result[range(int(N / 2))]  # 因为图形对称，所以取一半

    return axisFreq, result

def FFT_shift(axisFreq,fftdata):
    tmp = (-1) * axisFreq[-1:]


def cxcorr(a,v):#互相关
    nom = np.linalg.norm(a[:])*np.linalg.norm(v[:])
    return fftpack.irfft(fftpack.rfft(a)*fftpack.rfft(v[::-1]))/nom

if __name__ == '__main__':
    '''fs = 300
    t = np.linspace(0,3,3*fs)
    s = np.sin(2*np.pi*100*t)+np.cos(2*np.pi*40*t)
    axisF, F1 = FFT(fs,s)
    plt.figure()
    plt.subplot(211)
    plt.plot(t,s)
    plt.subplot(212)
    plt.plot(axisF,F1)
    plt.show()'''
    a = np.array([ [[1,2]], [[3,4]] ])
    print(a.shape)
    a = np.squeeze(a,axis=1)
    print(a.shape)