import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import torch
from torch import nn
import numpy as np
import matplotlib.pyplot as plt

class Net1(nn.Module):
    def __init__(self,node,act):
        super().__init__()
        self.node=node #各层神经元数
        self.n=len(node) #神经网络层数
        self.act=act #各层之间激活函数
        self.model=nn.Sequential()
        for i in range(self.n-2):
            self.model.append(nn.Linear(self.node[i],self.node[i+1]))
            self.model.append(self.act[i])
        self.model.append(nn.Linear(self.node[self.n-2],self.node[self.n-1]))

    def forward(self,input):
        output=self.model(input)
        return output.squeeze(-1)

def minmax_normalization(x):
    minx = min(x)
    maxx = max(x)
    xx = (x-minx)/(maxx-minx)
    return xx

def Prediction(x,modelpath):
    x = minmax_normalization(x)
    net = Net1(node=[50,40,30,15,1],act=[nn.ReLU(),nn.ReLU(),nn.ReLU()])#node=[40,30,30,20,1],act=[nn.ReLU(),nn.ReLU(),nn.ReLU()
    net.load_state_dict(torch.load(modelpath))
    net.eval()
    x = torch.from_numpy(np.float32(x))
    pred = net(x)
    y_pred = pred.detach().numpy()
    return y_pred

if __name__ == "__main__":
    delt_F = 312
    data = [53.654552, 53.329945, 53.727508, 54.289699, 54.205179, 54.049730, 54.839492, 55.618763, 55.840969, 57.596326,
        60.376525, 63.955426, 69.642901, 74.456573, 77.660441, 78.216195, 73.815823, 69.066525, 63.968182, 59.993029,
        58.186412, 57.930112, 56.798458, 56.803823, 57.485580, 57.933688, 57.428837, 56.448698, 55.874467, 54.810524,
        54.242492, 54.263592, 54.065824, 53.862095, 54.482341, 53.870559, 54.410577, 54.255009, 54.110646, 54.219484]
    data = np.array(data)
    y_pred = Prediction(data,'(snr)best_model(40-30-20-1_256_001).model')
    plt.figure()
    plt.plot(data)
    print(y_pred)
    #data = np.loadtxt('BGS.txt')
    '''num = data.shape[0]
    y_pred = np.zeros(num)
    for i in range(num):
        y_pred[i] = Prediction(data[i]) * delt_F
    plt.figure()
    plt.plot(y_pred,'o',color='red',label='prediction')
    plt.title('predicted delt_BFS using ANN')
    plt.ylabel('delt_BFS(MHz)')'''
    '''N = 1700
    startpos = 80 #80
    endpos = 1625 #1590 1640
    dis = np.arange(N)*2

    delt_BFS = np.zeros(N)
    for j in range(startpos,endpos):
        delt_BFS[j] = Prediction(data[:,j]) * delt_F
    plt.figure()
    plt.plot(dis[startpos:endpos],delt_BFS[startpos:endpos],'o',color='red',label='prediction')
    plt.title('predicted delt_BFS using ANN')
    plt.xlabel('distance(m)')
    plt.ylabel('delt_BFS(GHz)')

    plt.figure()
    plt.plot(data[:,400])
    plt.plot(data[:,1543])
    plt.plot(data[:,1610])'''
    
    plt.show()