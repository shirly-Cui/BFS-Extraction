import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from unit_plot import *

def calc_RMSE_SD_valid(data_y,data_y_pred):
    delt_F = 312#312 273
    data_y_pred_f = data_y_pred * delt_F #转化为频率值(MHz)
    data_y_f = data_y * delt_F
    n = data_y.shape[0]
    index = []
    index_tmp = 0
    for i in range(1,n):
        if(data_y[i] != data_y[i-1]):
            index.append([index_tmp,i-1])
            index_tmp = i
    index.append([index_tmp,n-1])

    num_y = len(index)
    RMSE_array = np.zeros(num_y)
    SD_array = np.zeros(num_y)
    y_f = np.zeros(num_y)
    num_valid = np.zeros(num_y) #每个BFS下 拟合得到的有效的结果个数
    num_f = np.zeros(num_y) #每个BFS下数据的个数
    for i in range(num_y):
        l = index[i][0]
        r = index[i][1]+1
        y_f[i] = data_y_f[l]
        ff = np.zeros(r-l)
        ff_pred = np.zeros(r-l)
        count = 0
        for j in range(l,r):
            if(abs(data_y_pred_f[j] - data_y_f[j]) < 25):
                ff[count] = data_y_f[j]
                ff_pred[count] = data_y_pred_f[j]
                count = count+1
        num_valid[i] = count
        num_f[i] = r-l
        RMSE_array[i] = np.sqrt(((ff_pred[0:count] -ff[0:count]) ** 2).mean())
        SD_array[i] = (ff_pred[0:count]).std()
    return y_f, RMSE_array, SD_array, num_valid, num_f

def calc_RMSE_SD(data_y,data_y_pred):
    delt_F = 312#312 273
    data_y_pred_f = data_y_pred * delt_F #转化为频率值(MHz)
    data_y_f = data_y * delt_F
    n = data_y.shape[0]
    index = []
    index_tmp = 0
    for i in range(1,n):
        if(data_y[i] != data_y[i-1]):
            index.append([index_tmp,i-1])
            index_tmp = i
    index.append([index_tmp,n-1])

    num_y = len(index)
    RMSE_array = np.zeros(num_y)
    SD_array = np.zeros(num_y)
    y_f = np.zeros(num_y)
    for i in range(num_y):
        l = index[i][0]
        r = index[i][1]+1
        y_f[i] = data_y_f[l]
        ff = data_y_f[l:r]
        ff_pred = data_y_pred_f[l:r]
        RMSE_array[i] = np.sqrt(((ff_pred -ff) ** 2).mean())
        SD_array[i] = ff_pred.std()
    return y_f, RMSE_array, SD_array

def plot_para():
    #ymajorLocator = MultipleLocator(2)
    xminorLocator = MultipleLocator(5)
    #ax.yaxis.set_major_locator(ymajorLocator)
    ax.xaxis.set_minor_locator(xminorLocator)
    # 修改刻度属性
    ax.tick_params(which='major', length=3, width=1.5, direction='in', top='on',right="on")
    ax.tick_params(which='minor', length=2, width=1,direction='in', top='on',right="on")
    # 添加网格
    ax.grid(which='major',ls='--',alpha=.8,lw=.8)
    # 添加图例
    ax.legend(fontsize=12,loc='upper right')

if __name__ == "__main__":
    datapath0 = 'data_1114/label1/'
    datapath1 = 'data_1114/pred1_3()/'
    savepath = 'data_1114/pred1_3()/fig1/'
    w = 40
    ##############################################计算RMSE和SD
    RMSE = []
    SD = []
    for snr in range(15,30,10):
        for k in range(5,10):
            data_y = np.loadtxt(datapath0 + '(deltBFS_120_snr={}_{}_{})data_y.txt'.format(snr,w,k))
            data_y_pred = np.loadtxt(datapath1 + '(deltBFS_120_snr={}_{}_{})data_y_pred.txt'.format(snr,w,k))
            y_f,RMSE1,SD1 = calc_RMSE_SD(data_y,data_y_pred)
            RMSE.append(RMSE1)
            SD.append(SD1)

    ################################################绘图
    plot_init(12,12)
    fig = plt.figure(figsize=(12,4)) 
    #ax = plt.subplot(1,1,1)
    for i in range(2):
        snr = 15 + i*10
        ax = plt.subplot(1,2,i+1)
        for j in range(5):
            k = (5-j)/10
            ax.plot(y_f[5:],RMSE[i*5+j][5:],label='k = {:.1f}'.format(k))
        ax.set_xlabel('∆BFS/MHz', fontsize=12,labelpad=3)#,fontweight='bold'
        ax.set_ylabel('RMSE/MHz', fontsize=12,labelpad=3)
        #ax.set_title('SNR={}dB'.format(snr))
        plot_para()
    #plt.subplots_adjust(left=0.08, right=0.95, bottom=0.1, top=0.95, wspace=0.15, hspace=0.4)
    #fig.savefig((datapath1 + "RMSE2(w={}).pdf").format(w),format='pdf',dpi=800)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.95, wspace=0.15)#, hspace=0.2
    fig.savefig((savepath + "RMSE(w={}).pdf").format(w),format='pdf',dpi=800)

    '''#fig = plt.figure(figsize=(12,7)) 
    #ax = plt.subplot(1,1,1)
    for i in range(2):
        snr = 15 + i*10
        ax = plt.subplot(2,2,i+3)
        for j in range(5):
            k = (5-j)/10
            ax.plot(y_f[5:],SD[i*5+j][5:],label='k = {:.1f}'.format(k))
        ax.set_xlabel('∆BFS/MHz', fontsize=18,labelpad=3)
        ax.set_ylabel('SD/MHz', fontsize=18,labelpad=3)
        ax.set_title('SNR={}dB'.format(snr))
        plot_para()
    plt.subplots_adjust(left=0.08, right=0.95, bottom=0.1, top=0.95, wspace=0.18, hspace=0.4)
    fig.savefig((savepath + "RMSE(w={}).pdf").format(w),format='pdf',dpi=800)'''

    fig = plt.figure(figsize=(7,4))
    ax = plt.axes()
    for i in range(2):
        snr = 15 + i*10
        for j in range(5):
            k = (5-j)/10
            if(j==2):
                plt.plot(y_f[5:],RMSE[i*5+j][5:],linewidth=2,label='SNR = {}'.format(snr))
    plt.xlabel('∆BFS/MHz', fontsize=18,labelpad=3,fontweight='bold')
    plt.ylabel('RMSE/MHz', fontsize=18,labelpad=3,fontweight='bold')
    plot_para()
    plt.subplots_adjust(left=0.12, right=0.95, bottom=0.15, top=0.95)
    fig.savefig((datapath1 + "RMSE2(w={},k=0.3).pdf").format(w),format='pdf',dpi=800)

    fig = plt.figure(figsize=(7,4))
    ax = plt.axes()
    for i in range(2):
        snr = 15 + i*10
        for j in range(5):
            k = (5-j)/10
            if(j==2):
                plt.plot(y_f[5:],SD[i*5+j][5:],linewidth=2,label='SNR = {}'.format(snr))
    plt.xlabel('∆BFS/MHz', fontsize=18,labelpad=3,fontweight='bold')
    plt.ylabel('SD/MHz', fontsize=18,labelpad=3,fontweight='bold')
    plot_para()
    plt.subplots_adjust(left=0.12, right=0.95, bottom=0.15, top=0.95)
    fig.savefig((datapath1 + "SD2(w={},k=0.3).pdf").format(w),format='pdf',dpi=800)
    #plt.tight_layout()
    plt.show()
    



    