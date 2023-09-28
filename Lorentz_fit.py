from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

'''def Lorentz(x,y0,A,xc,w):#40,6,xc1,0.1
    y = y0 + (2*A/np.pi)*(w/(4*(x-xc)**2 + w**2))
    return y'''

def Lorentz(x,y0,A,xc,w):#40,50,xc,0.05
    y = y0 + A/(1+4*((x-xc)/w)**2)
    return y

def Lorentz_fit(x, y):
    maxindex = y.argmax()
    xc = x[maxindex]
    miny = min(y)
    maxy = max(y)
    y0 = miny
    A = maxy-miny
    w = 0.05
    try:
        p,c = curve_fit(Lorentz, x, y,p0=[y0,A,xc,w], absolute_sigma=True)#absolute_sigma=True
    except RuntimeError: #若无法拟合，则直接使用原始数据
        #print("curve_fit failed")
        yfit = y
    else:     
        y0,A,xc,w=p
        yfit = Lorentz(x,y0,A,xc,w)
    
    '''print('y0,A,xc,w:')
    print(y0,A,xc,w)
    print('y0,A,xc,w: standard error')
    print(np.sqrt(np.diag(c)))'''

    return yfit, xc

def Lorentz_fit1(x, y, xl):
    maxindex = y.argmax()
    xc = x[maxindex]
    l = max([0,maxindex-xl])
    r = min([maxindex+xl+1,x.shape[0]])
    xx = x[l:r]
    yy = y[l:r]
    miny = min(yy)
    maxy = max(yy)
    y0 = miny
    A = maxy-miny
    w = 0.04
    try:
        p,c = curve_fit(Lorentz, xx, yy,p0=[y0,A,xc,w], absolute_sigma=True)#absolute_sigma=True
    except RuntimeError: #若无法拟合，则直接使用原始数据
        #print("curve_fit failed")
        yfit = yy
    else:     
        y0,A,xc,w=p
        yfit = Lorentz(xx,y0,A,xc,w)
    
    '''print('y0,A,xc,w:')
    print(y0,A,xc,w)
    print('y0,A,xc,w: standard error')
    print(np.sqrt(np.diag(c)))'''

    return yfit, xc, l, r

def BGS_fit_single(x,y,xl):
    maxindex = y.argmax()
    xc = x[maxindex]
    w = 0.04
    l = max([0,maxindex-xl])
    r = min([maxindex+xl+1,x.shape[0]])
    xx = x[l:r]
    yy = y[l:r]
    miny = min(yy)
    maxy = max(yy)
    y0 = miny
    A = maxy-miny

    try:
        p,c = curve_fit(Lorentz, xx, yy,p0=[y0,A,xc,w], absolute_sigma=True)#absolute_sigma=True
    except RuntimeError: #若无法拟合，则直接使用原始数据
        print("curve_fit failed")
    else:     
        y0,A,xc,w=p

    return y0,A,xc,w

def BGS_fit_doub1(x, y):#分别拟合单个峰
    maxindex = y.argmax()
    
    n = min([maxindex*2+1, y.shape[0]])
    x1 = x[0:n]
    y1 = np.zeros(n)
    delt = 2
    y1[0:maxindex+delt] = y[0:maxindex+delt]
    for i in range(maxindex+delt, n):
        y1[i] = y[maxindex*2-i]

    xl=30
    y0,A,xc,w = BGS_fit_single(x1,y1,xl)
    xc1 = xc
    yfit1 = Lorentz(x,y0,A,xc,w)
    
    y2 = y - yfit1
    xl = 10
    y0,A,xc,w = BGS_fit_single(x,y2,xl)
    xc2 = xc
    yfit2 = Lorentz(x,y0,A,xc,w)

    '''plt.figure()
    plt.plot(x, y, label='y')
    plt.plot(x1,y1, label='y1')
    plt.plot(x,yfit1, label='yfit1_all')
    
    plt.plot(x,y2, label='y2')
    plt.plot(x,yfit2, label='yfit2_all')
    plt.legend()'''


    return yfit1, yfit2, xc1, xc2



def Lorentz_doub(x,A1,A2,xc1,xc2,w1,w2):
    y = A1/(1+4*((x-xc1)/w1)**2)+A2/(1+4*((x-xc2)/w2)**2)
    return y

def BGS_fit_doub(x, y):#直接拟合两个峰
    A1 = max(y)
    A2 = A1
    maxindex = y.argmax()
    xc1 = x[maxindex]
    xc2 = min(xc1+0.02, x[-1])
    w1 = 0.04
    w2 = w1
    try:
        p,c = curve_fit(Lorentz_doub, x, y,p0=[A1,A2,xc1,xc2,w1,w2], absolute_sigma=True,maxfev=10000)#absolute_sigma=True
    except RuntimeError: #若无法拟合，则直接使用原始数据
        #print("curve_fit failed")
        yfit = y
    else:     
        A1,A2,xc1,xc2,w1,w2=p
        yfit = Lorentz_doub(x,A1,A2,xc1,xc2,w1,w2)
    
    '''print('y0,A,xc,w:')
    print(y0,A,xc,w)
    print('y0,A,xc,w: standard error')
    print(np.sqrt(np.diag(c)))'''

    return yfit, xc1, xc2

