import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from scipy.optimize import curve_fit
from unit_plot import *

def My_color(label):
    if label == 0:
        mycolor = '#6A539D'
    if label == 1:
        mycolor ='#E6D7B2'
    if label == 2:
        mycolor = '#99CCCC'
    if label == 3:
        mycolor = '#FFCCCC'
    if label == 4:
        mycolor = '#666633'
    return mycolor

def linear(x,a,b):
    y = a*x + b
    return y

if __name__ == "__main__":
    plot_init(14,13)
    datapath = 'data_experiment/'
    delt_F = 312
    SD = []
    count = 10

    data_y_pred = np.loadtxt(datapath + 'data_y_pred(0920_3).txt')
    data_y_pred_f = data_y_pred * delt_F 
    n = 4
    x = np.array([1,2,3,4])
    pred_f = np.zeros(n)
    SD_array = np.zeros(n)
    data_y_pred_f_mean = np.zeros(n*count)
    for i in range(n):
        pred_f[i] = (data_y_pred_f[i*count:(i+1)*count]).mean()
        data_y_pred_f_mean[i*count:(i+1)*count] = pred_f[i]
        SD_array[i] = (data_y_pred_f[i*count:(i+1)*count]).std()
    SD.append(SD_array)
    y = pred_f
    a,b = curve_fit(linear, x, y)[0]
    y1 = a*x + b
    print('a={},b={}'.format(a,b))
   
    xx = np.arange(40)
    fig,ax = plt.subplots(1,1,figsize=(6,4))
    for i in range(4):
        plt.plot(xx[i*count:(i+1)*count],data_y_pred_f[i*count:(i+1)*count],'o',label='∆BFS with weight {}'.format(i+1))#,color=My_color(i)
        #plt.plot(data_y_pred_f_mean,'-',color='green',label='mean')
    plt.ylabel('∆BFS/MHz)', fontsize=14,labelpad=3,fontweight='bold')
    plot_para()
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)
    #plt.close()
    fig.savefig(datapath + "prediction(0920_3)1.png",dpi=800)

    fig, ax = plt.subplots(1,1,figsize=(6,4))
    plt.plot(x, y, '*', color='red',markersize=8,label='ANN data')
    plt.plot(x, y1,linewidth=2,label='linear fitting')
    plt.xlabel('load', fontsize=14,labelpad=3,fontweight='bold')
    plt.ylabel('∆BFS/MHz', fontsize=14,labelpad=3,fontweight='bold')
    #plt.title('prediction')
    plot_para()
    plt.subplots_adjust(left=0.12, right=0.95, bottom=0.12, top=0.95)
    fig.savefig(datapath + "prediction_mean(0920_3)1.png",dpi=800)

    plt.show()
    



    