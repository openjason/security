# -*- coding: utf-8 -*- 
import pandas as pd
#获取地址数据


def get_adress_data(adress=0):
	data=pd.read_csv(adress,parse_dates=False,header=None,names=['dateL','openL','highL','lowL','closeL','volL'])
	data['dateL']=pd.to_datetime(data.dateL)
	return data
#获取macd 
def get_macd_data(data,short=0,long1=0,mid=0):
	if short==0:
		short=12
	if long1==0:
		long1=26
	if mid==0:
		mid=9
	data['sema']=pd.ewma(data['closeL'],span=short)
	data['lema']=pd.ewma(data['closeL'],span=long1)
	data.fillna(0,inplace=True)
	data['data_dif']=data['sema']-data['lema']
	data['data_dea']=pd.ewma(data['data_dif'],span=mid)
	data['data_macd']=2*(data['data_dif']-data['data_dea'])
	data.fillna(0,inplace=True)
	return data[['data_dif','data_dea','data_macd']]

def get_kdj_data(data,N=0,M=0):
	if N==0:
	N=9
	if M==0:
	M=2
	low_list=pd.rolling_min(data['lowL'],N)
	low_list.fillna(value=pd.expanding_min(data['lowL']), inplace=True)
	high_list= pd.rolling_max(data['highL'],N)
	high_list.fillna(value=pd.expanding_max(data['highL']), inplace=True)
	rsv=(data['closeL']-low_list)/(high_list-low_list)*100
	data['KDJ_K'] = pd.ewma(rsv,com=M)
	data['KDJ_D']=pd.ewma(data['KDJ_K'],com=M)
	data['KDJ_J'] = 3 * data['KDJ_K'] - 2 * data['KDJ_D']
	data.fillna(0,inplace=True) 
	return data[['KDJ_K','KDJ_D','KDJ_J']] 

def get_ma_data(data,N=0): 
if N==0: 
N=5 
data['ma']=pd.rolling_mean(data['closeL'],N) 
data.fillna(0,inplace=True) 
return data[['ma']] 

def get_rsi_data(data,N=0): 
if N==0: 
N=24 
data['value']=data['closeL']-data['closeL'].shift(1) 
data.fillna(0,inplace=True) 
data['value1']=data['value'] 
data['value1'][data['value1']<0]=0 
data['value2']=data['value'] 
data['value2'][data['value2']>0]=0 
data['plus']=pd.rolling_sum(data['value1'],N) 
