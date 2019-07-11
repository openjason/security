import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
from matplotlib import rcParams
data=get_price(['000300.SH'], None, '20171110', '1d', ['close'], True, None,233, is_panel=0)['000300.SH']
data['ma12']=pd.ewma(data['close'],12)
data['ma26']=pd.ewma(data['close'],26)
data['diff']=data['ma12']-data['ma26']
data['dea']=pd.ewma(data['diff'],9)
data['macd']=data['diff']-data['dea']
data=data[33:]
diff=list(data['diff'])
dea=list(data['dea'])
fig,ax=plt.subplots(figsize=(16,4),facecolor='pink')
plt.plot(diff,'b',label='diff')
plt.plot(dea,'y',label='dea')
macd=list(data['macd'])
x=len(list(data['macd']))
x=range(0,x,1)
rects =plt.bar(left = x,height = macd,width = 0.4,color=('g','r'),align="center",yerr=0.1)
plt.title('MACD指标')
jc=[]
sc=[]
data['goldordie']=data['diff']-data['dea']
for x in range(0,200,1):
    z=x-1
    y2=data['goldordie'].iloc[x]
    y1=data['goldordie'].iloc[z]
    if y1<0 and y2>0:
        jc.append(x)
    elif y1>0 and y2<0:
        sc.append(x)
for x in jc:
    if x==jc[-1]:
        diff=data['diff'].iloc[x]
        if diff>0:
            plt.plot(x, diff, 'r*', markersize = 20.0,label='金叉')
            plt.annotate(r'多方金叉顺势买入', xy=(x, diff),
                xycoords='data', xytext=(-20, -20),
                textcoords='offset points', fontsize=12,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        else:
            plt.plot(x, diff, 'r*', markersize = 20.0,label='金叉')
            plt.annotate(r'空方金叉猥琐买入', xy=(x, diff),
                xycoords='data', xytext=(-20, -20),
                textcoords='offset points', fontsize=12,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    else:
        diff=data['diff'].iloc[x]
        if diff>0:
            plt.plot(x, diff, 'r*', markersize = 20.0)
            plt.annotate(r'多方金叉顺势买入', xy=(x, diff),
                xycoords='data', xytext=(-20, -20),
                textcoords='offset points', fontsize=12,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        else:
            plt.plot(x, diff, 'r*', markersize = 20.0)
            plt.annotate(r'空方金叉猥琐买入', xy=(x, diff),
                xycoords='data', xytext=(-20, -20),
                textcoords='offset points', fontsize=12,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
for x in sc:
    if x==sc[-1]:
        diff=data['diff'].iloc[x]
        if diff >0:
            plt.plot(x, diff, 'g*', markersize = 20.0,label='死叉')
            plt.annotate(r'多方死叉猥琐卖出', xy=(x, diff),
                xycoords='data', xytext=(20, 20),
                textcoords='offset points', fontsize=12,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        if diff <0:
            plt.plot(x, diff, 'g*', markersize = 20.0,label='死叉')
            plt.annotate(r'空方死叉顺势卖出', xy=(x, diff),
                xycoords='data', xytext=(20, 20),
                textcoords='offset points', fontsize=12,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    else:
        diff=data['diff'].iloc[x]
        if diff>0:
            plt.plot(x, diff, 'g*', markersize = 20.0)
            plt.annotate(r'多方死叉猥琐卖出', xy=(x, diff),
                xycoords='data', xytext=(10, 20),
                textcoords='offset points', fontsize=12,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        else:
            plt.plot(x, diff, 'g*', markersize = 20.0)
            plt.annotate(r'空方死叉顺势卖出', xy=(x, diff),
                xycoords='data', xytext=(10, 20),
                textcoords='offset points', fontsize=12,
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
plt.legend()

<matplotlib.legend.Legend at 0x7feaec9832b0>

