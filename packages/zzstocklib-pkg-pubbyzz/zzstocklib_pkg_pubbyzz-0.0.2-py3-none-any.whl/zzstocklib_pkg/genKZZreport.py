import pandas as pd
import struct
import datetime
import os

#only deal with tongxinda shanghai&shenzhen stock lday data
def stock_csv(code):
    file_object_path = 'C:/workspace/stock/stockdata/lday/' + code +'.csv'
    filepath ='C:/new_jyplug/vipdoc/sz/lday/sz' + code +'.day'
    
    if not os.path.exists(filepath):
       filepath = 'C:/new_jyplug/vipdoc/sh/lday/sh' + code +'.day'

    
    if not os.path.exists(filepath):                        
       filepath = 'C:/new_jyplug/vipdoc/sh/lday/sh' + code +'.day'
       #如果当前上海和深圳市场都没有文件，则在本地新建一个空文件退出
       file_object = open(file_object_path, 'w+')
       file_object.close()
       return
    
    data = []

    with open(filepath, 'rb') as f:
        
        file_object = open(file_object_path, 'w+')
        while True:
            stock_date = f.read(4)
            stock_open = f.read(4)
            stock_high = f.read(4)
            stock_low= f.read(4)
            stock_close = f.read(4)
            stock_amount = f.read(4)
            stock_vol = f.read(4)
            stock_reservation = f.read(4)

            # date,open,high,low,close,amount,vol,reservation

            if not stock_date:
                break
            stock_date = struct.unpack("l", stock_date)     # 4字节 如20091229
            stock_open = struct.unpack("l", stock_open)     #开盘价*1000
            stock_high = struct.unpack("l", stock_high)     #最高价*1000
            stock_low= struct.unpack("l", stock_low)        #最低价*1000
            stock_close = struct.unpack("l", stock_close)   #收盘价*1000
            stock_amount = struct.unpack("f", stock_amount) #成交额
            stock_vol = struct.unpack("l", stock_vol)       #成交量
            stock_reservation = struct.unpack("l", stock_reservation) #保留值

            date_format = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d') #格式化日期
            list= date_format.strftime('%Y-%M-%d')+","+str(stock_open[0]/1000)+","+str(stock_high[0]/1000.0)+","+str(stock_low[0]/1000.0)+","+str(stock_close[0]/1000.0)+","+str(stock_amount[0])+","+str(stock_vol[0])+"\r\n"
            file_object.writelines(list)
        file_object.close()

def load_stock(code):
    file_url = 'C:/workspace/stock/stockdata/lday/' + code +'.csv'
    #if not os.path.exists(file_url):
    #   stock_csv(code)
    # 每次都装载最新
    stock_csv(code) 
    df = pd.read_csv(file_url, names=['date','open','high','low','close','amount','vol'])
    return df

kzz_df = pd.read_excel('C:\\workspace\\stock\\stockdata\\dict\\KZZ.xlsx',dtype={'债券代码':str})
# 对于每一行，通过列名name访问对应的元素
kzz_df['历史最低价'] = 0.0
kzz_df['历史最高价'] = 0.0
kzz_df['当前价'] = 0.0
kzz_df['剩余年限'] = 0.0
kzz_df['到期价值'] = 0.0
kzz_df['到期收益率'] = 0.0
kzz_df['到期年化收益率'] = 0.0
kzz_df['年化%5收益率'] = 0.0
for index, row in kzz_df.iterrows():
    temp_df = load_stock(row['债券代码'])
    if len(temp_df) > 0:
        row['历史最低价'] = temp_df['close'].min()
        row['历史最高价'] = temp_df['close'].max()
        row['当前价'] = temp_df.iloc[-1]['close']
        #print(row['债券代码'] + ' ' + str(row['历史最低价']))
    
        kzz_df.iloc[index] = row

kzz_df.to_excel('C:\workspace\stock\stockdata\dict\kzz_updated.xlsx',index=False)
