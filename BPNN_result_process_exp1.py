import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from scipy.optimize import curve_fit
from unit_plot import *

def linear(x,a,b):
    y = a*x + b
    return y

if __name__ == "__main__":
    plot_init(12,12)
    datapath = 'data_experiment/'
    savepath= 'data_experiment/fig/'
    average_times = [512,2048,4096]
    pos = [1080,1081,1082,1083]
    delt_F = 312
    SD = []
    count = 100
    #i_average = 1
    i_pos = 2
    n = 4
    colors = ['#EA5506', '#27630D', '#223F73', '#D7003A']#E5190B
    number = [20,30,45,70]
    for i_average in range(3):
        data_y_pred = np.loadtxt(datapath + 'data_y_pred(1116_{}_{}).txt'.format(average_times[i_average], pos[i_pos]))
        data_y_pred_f = data_y_pred * delt_F 
        if (i_average == 2):
            x = [1,2,3,4]
        else:
            x = [2,3,4,5]
      
        pred_f = np.zeros(n)
        SD_array = np.zeros(n)
        data_y_pred_f_mean = np.zeros(n*count)
        y = np.zeros(n*count)
        index = 0
        for i in x:
            pred_f[index] = (data_y_pred_f[i*count:(i+1)*count]).mean()
            y[index*count:(index+1)*count] = data_y_pred_f[i*count:(i+1)*count]
            data_y_pred_f_mean[index*count:(index+1)*count] = pred_f[index]
            SD_array[index] = (data_y_pred_f[i*count:(i+1)*count]).std()
            index = index + 1
        SD.append(SD_array)
        '''y = pred_f
        a,b = curve_fit(linear, x, y)[0]
        y1 = a*x + b
        print('{}:a={},b={}'.format(pos[i_pos],a,b))'''
   
        fig = plt.figure(figsize=(6,4))
        axes = plt.subplot()
        #ax = plt.subplot(2,1,1)
        for i in range(n):
            plt.scatter(range(i*count,(i+1)*count),y[i*count:(i+1)*count], facecolors='none', edgecolors=colors[i],label='{} steel balls'.format(number[i]))
        #plt.plot(data_y_pred_f_mean,'-',color='green',label='mean')
        plt.plot([50,150,250,350], pred_f, '^', markersize=10, color='#000000', markerfacecolor='none', label='mean ∆BFS')#
        plt.xticks([50,150,250,350], ['20', '30', '45', '70'])

        #axes.minorticks_on()
        axes.tick_params(axis="y", which="major", direction="in", width=1, length=5)
        #axes.tick_params(axis="y", which="minor", direction="in", width=1, length=3)
        axes.tick_params(axis="x", which="major", direction="out", width=1, length=5)
        #axes.tick_params(axis="x", which="minor", direction="in", width=1, length=3)
        axes.xaxis.set_major_locator(MultipleLocator(100))
        #axes.xaxis.set_minor_locator(MultipleLocator(50))
        plt.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
        #plt.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
        plt.xlabel('four weight classes', fontsize=14,labelpad=3)
        plt.ylabel('extracted ∆BFS/MHz)', fontsize=14,labelpad=3)
        #plt.title('prediction')
        
        plt.legend(fontsize=13,loc='upper left')
        #plot_para()
        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.95)
        #plt.close()
        fig.savefig(savepath + "prediction1(1116_{}_{}).pdf".format(average_times[i_average], pos[i_pos]),format='pdf',dpi=800)

        '''ax = plt.subplot(2,1,2)
        plt.plot(pred_f, 'o', color='b',markersize=8,label='mean data')
        #plt.plot(x, y1,linewidth=2,label='linear fitting')
        plt.xticks([0,1,2,3], ['load1', 'load2', 'load3', 'load4'])
        #plt.xlabel('strain/με', fontsize=14,labelpad=3,fontweight='bold')
        plt.ylabel('mean ∆BFS/MHz', fontsize=12,labelpad=3)
        #plt.title('prediction')
        plot_para()
        plt.subplots_adjust(left=0.12, right=0.95, bottom=0.05, top=0.95, hspace=0.1)
        fig.savefig(savepath + "prediction_mean(1116_{}_{}).pdf".format(average_times[i_average], pos[i_pos]),format='pdf',dpi=800)
        '''
    fig = plt.figure(figsize=(6,4)) 
    markers = ['x','o','v']
    for i_average in range(3):
        '''if (i_average == 2):
            n = 7
            x = np.array([0,500,1000,1250,1500,1750,2000])
            i_scatter = np.array([0,1,2,4,6])
        else:
            n = 8
            x = np.array([0,500,750,1000,1250,1500,1750,2000])
            i_scatter = np.array([0,1,3,5,7])
        plt.scatter(x[i_scatter],SD[i_average][i_scatter],marker=markers[i_average])'''
        plt.plot(SD[i_average],label='average times = {}'.format(average_times[i_average]),marker=markers[i_average])#markevery=(10,1)
        #plt.plot(x,SD[i_pos],label='position = {}'.format(pos[i_pos]))
    plt.xlabel('number of steel balls', fontsize=14,labelpad=3)
    plt.xticks([0,1,2,3], ['20', '30', '45', '70'])
    plt.ylabel('SD/MHz', fontsize=12,labelpad=3)
    plot_para()
    plt.legend(fontsize=13,loc='upper right')
    plt.subplots_adjust(left=0.12, right=0.95, bottom=0.12, top=0.95)
    #fig.savefig(savepath + "SD(1116_pos={}).pdf".format(pos[i_pos]),format='pdf', dpi=800)
    #fig.savefig(datapath + "SD(1116_average_times={}).png".format(average_times[i_average]))
    #plt.tight_layout()
    plt.show()
    



    