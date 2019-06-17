import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
from matplotlib import rcParams

daily_data_19="190102 19.60 19.56 20.06 19.40 649682nn\
190103 19.59 18.78 19.60 18.72 948600nn\
190104 18.51 19.20 19.27 18.24 771891nn\
190107 19.45 20.02 20.15 19.20 1248492nn\
190108 19.92 19.90 20.26 19.73 830617nn\
190109 19.95 19.92 20.35 19.79 984072nn\
190110 19.90 20.07 20.35 19.78 849049nn\
190111 20.29 20.51 21.27 20.29 1518342nn\
190114 20.20 20.09 20.47 19.90 762049nn\
190115 20.07 20.60 20.80 19.90 975654nn\
190116 20.55 20.31 20.61 20.22 615087nn\
190117 20.24 20.01 20.48 19.90 643691nn\
190118 19.85 19.98 20.08 19.67 708480nn\
190121 20.06 21.04 21.16 20.01 1855824nn\
190122 21.00 20.44 21.09 20.24 1081594nn\
190123 20.36 20.45 20.69 20.08 594125nn\
190124 20.50 20.37 20.72 20.12 665691nn\
190125 20.40 20.32 20.67 20.20 508649nn\
190128 20.35 20.24 20.55 20.12 484500nn\
190129 20.10 19.98 20.20 19.70 569530nn\
190130 19.98 19.71 20.14 19.68 429831nn\
190131 19.76 20.11 20.38 19.76 723098nn\
190201 20.22 20.41 20.53 19.90 705106nn\
190211 20.20 20.87 20.99 20.16 912809nn\
190212 20.93 21.06 21.13 20.60 837727nn\
190213 21.11 22.95 23.17 20.95 2412237nn\
190214 22.70 22.85 23.12 22.55 1311908nn\
190215 22.75 23.00 23.70 22.55 1372753nn\
190218 23.45 24.14 24.15 23.25 1493215nn\
190219 24.46 24.06 24.88 23.62 1341400nn\
190220 24.07 24.00 24.25 23.42 994730nn\
190221 23.96 25.31 26.30 23.85 1821326nn\
190222 25.50 27.84 27.84 25.32 2098379nn\
190225 30.60 30.31 30.60 29.10 3190504nn\
190226 30.18 29.90 32.78 28.60 3239619nn\
190227 29.38 29.45 30.84 28.92 1972814nn\
190228 29.47 29.80 30.22 29.12 1421570nn\
190301 30.03 29.73 30.15 28.80 1235940nn\
190304 30.11 30.31 31.55 29.90 2159491nn\
190305 30.22 31.65 31.70 29.65 1906566nn\
190306 32.43 31.30 32.87 30.55 2140882nn\
190307 30.67 30.40 31.12 30.00 1688287nn\
190308 29.10 29.21 31.01 28.88 1739426nn\
190311 29.80 30.40 30.50 29.30 1370705nn\
190312 30.66 31.09 31.10 30.31 1727617nn\
190313 29.84 28.68 30.15 28.35 2286629nn\
190314 28.50 28.25 28.56 27.49 1242688nn\
190315 28.55 28.38 28.83 28.24 766498nn\
190318 28.38 29.19 29.21 27.77 930481nn\
190319 29.00 29.03 29.62 28.84 798103nn\
190320 28.92 28.98 29.45 28.72 642784nn\
190321 29.17 28.90 29.29 28.88 699078nn\
190322 28.80 28.22 28.84 27.70 1036826nn\
190325 27.51 28.33 28.77 27.40 894689nn\
190326 28.45 27.13 28.58 27.05 832679nn\
190327 27.35 26.67 27.63 26.20 876586nn\
190328 28.30 29.34 29.34 27.91 2530819nn\
190329 28.50 29.20 29.34 27.66 2355035nn\
190401 29.70 30.00 30.55 29.70 1828261nn\
190402 30.01 29.90 30.40 29.49 1280241nn\
190403 29.81 29.85 29.96 29.33 875200nn\
190404 30.17 29.98 30.30 29.50 871282nn\
190408 30.05 29.24 30.25 29.10 855990nn\
190409 29.24 30.20 30.80 29.19 1354219nn\
190410 30.15 31.50 32.25 29.80 1804568nn\
190411 31.00 30.39 31.25 30.10 1072725nn\
190412 30.20 30.26 31.00 30.10 570955nn\
190415 30.82 30.50 31.99 30.35 1048541nn\
190416 30.31 33.55 33.55 30.10 2304204nn\
190417 34.00 34.08 34.75 32.98 2310984nn\
190418 33.50 34.09 35.62 33.30 1792256nn\
190419 33.95 36.49 36.90 33.60 1904800nn\
190422 36.50 36.76 38.50 35.66 2235859nn\
190423 36.31 35.53 37.16 35.20 1601327nn\
190424 35.45 35.02 35.80 33.98 1653636nn\
190425 34.95 33.65 35.36 33.55 1387543nn\
190426 33.01 34.17 35.00 33.01 1251393nn\
190429 34.20 33.85 34.45 32.99 1164960nn\
190430 32.10 32.15 32.44 30.50 1714840nn\
190506 29.30 28.94 30.69 28.94 1507203nn\
190507 29.20 29.01 29.70 27.41 1511928nn\
190508 27.91 28.89 29.77 27.80 1201768nn\
190509 28.54 28.30 29.36 28.18 878925nn\
190510 29.15 30.88 31.00 28.00 1846948nn\
190513 30.02 30.21 30.79 29.85 1078269nn\
190514 29.70 29.95 30.69 29.61 1045375nn\
190515 30.58 30.51 30.72 30.08 1100000nn\
190516 30.00 29.62 30.13 29.00 1285610nn\
190517 29.50 28.50 30.21 28.00 1293069nn\
190520 28.46 27.90 28.63 26.50 1312073nn\
190521 28.00 29.20 29.83 27.65 1530663nn\
190522 29.23 29.48 30.55 28.88 1470854nn\
190523 29.18 28.24 29.18 28.13 1018689nn\
190524 28.05 28.25 28.58 28.00 574920nn\
190527 28.27 29.29 29.59 28.02 1118500nn\
190528 29.50 29.30 29.57 28.95 786025nn\
190529 28.90 29.16 29.58 28.81 619180nn\
190530 28.90 28.38 28.97 27.95 859556nn\
190531 28.41 28.76 29.15 28.29 746412nn\
190603 29.30 30.29 31.19 28.96 1894903nn\
190604 30.70 30.50 31.51 30.05 1701285nn\
190605 31.15 32.09 32.30 30.66 1862005nn\
190606 31.56 29.78 31.56 29.29 1861741nn\
190610 29.78 31.02 31.28 29.78 1383037nn\
190611 31.01 31.62 31.96 30.35 1720584nn\
190612 31.01 31.47 32.10 31.00 1231723nn"



daily_data2 = daily_data_19.split('nn')
daily_data = []
for i in range(len(daily_data2)):
    daily_data.append(('20'+daily_data2[i]).split(" "))
#daily_data = daily_data2.split()
print(daily_data)
exit(0)



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



