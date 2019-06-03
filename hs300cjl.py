import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
from matplotlib import rcParams
data=get_price(['000300.SH'], None, '20171110', '1d', ['volume'], True, None,200, is_panel=0)['000300.SH']
data['volma5']=pd.rolling_mean(data['volume'],5)
data['volma10']=pd.rolling_mean(data['volume'],10)
volma5=list(data['volma5'])
volma10=list(data['volma10'])
data['goldordie']=(data['volma5']-data['volma10'])
time=data.index
t=[]
for x in time:
    x=str(x).split()
    x=x[0]
    t.append(x)
#画图数据
time=t
x=list(data['volume'])
y=len(x)
z=range(0,y,1)
fig,ax = plt.subplots(figsize = (48,8),facecolor='pink')
ticks = ax.set_xticks(range(1,200,40))
rects =plt.bar(left = z,height = x,width = 0.4,color=('r','g'),align="center",yerr=0.1)
plt.title('VOL')
# plt.xticks(z,t)
# 蓝线：五日量能
plt.plot(volma5,'b',label="五日量能")
# 蓝线：十日量能
plt.plot(volma10,'y',label="十日量能")
plt.title("沪深300成交量")  
print("沪深300成交量")
jc=[]
sc=[]
for x in range(0,200,1):
    z=x-1
    y2=data['goldordie'].iloc[x]
    y1=data['goldordie'].iloc[z]
    if y1<0 and y2>0:
        jc.append(x)
    elif y1>0 and y2<0:
        sc.append(x)
for x in jc:
    if x== jc[-1]:
        vol=data['volma5'].iloc[x]
        plt.plot(x, vol, 'r*', markersize = 40.0,label='金叉')
    else:
        vol=data['volma5'].iloc[x]
        plt.plot(x, vol, 'r*', markersize = 40.0)
for x in sc:
    if x==sc[-1]:
        vol=data['volma5'].iloc[x]
        plt.plot(x, vol, 'g*', markersize = 40.0,label='死叉')
    else:
        vol=data['volma5'].iloc[x]
        plt.plot(x, vol, 'g*', markersize = 40.0)
plt.legend()
plt.show()

沪深300成交量

