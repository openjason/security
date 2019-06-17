#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

df = pd.DataFrame(getKline('1day','30','0'))
df.columns = ['date', 'open', 'high', 'low', 'close', 'amount']

def calc_EMA(df, N): 
    for i in range(len(df)):
        if i==0:
            df.ix[i,'ema']=df.ix[i,'close']
        if i>0:
            df.ix[i,'ema']=((N-1)*df.ix[i-1,'ema']+2*df.ix[i,'close'])/(N+1)
    ema=list(df['ema'])
    return ema

def calc_MACD(df, short=12, long=26, M=9):
    emas = calc_EMA(df, short)
    emaq = calc_EMA(df, long)
    df['diff'] = pd.Series(emas) - pd.Series(emaq)
    for i in range(len(df)):
        if i==0:
            df.ix[i,'dea'] = df.ix[i,'diff']  
        if i>0:  
            df.ix[i,'dea'] = ((M-1)*df.ix[i-1,'dea'] + 2*df.ix[i,'diff'])/(M+1)  
    df['macd'] = 2*(df['diff'] - df['dea'])
    return df

calc_MACD(df, 12, 26, 9)