import matplotlib.pyplot as plt

def plot_init(fontsize=18,LegendTitle_fontsize=16):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    # 设置全局图表属性变量
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = fontsize
    plt.rcParams['axes.linewidth'] = 1
    # 设置图例标题大小
    plt.rcParams['legend.title_fontsize'] = LegendTitle_fontsize

def plot_para():
    # 修改刻度属性
    plt.tick_params(which='major', length=3, width=1.5, direction='in', top='on',right="on")
    plt.tick_params(which='minor', length=2, width=1,direction='in', top='on',right="on")
    # 添加网格
    plt.grid(which='major',ls='--',alpha=.8,lw=.8)
    # 添加图例
    plt.legend(fontsize=13,loc='upper left')

