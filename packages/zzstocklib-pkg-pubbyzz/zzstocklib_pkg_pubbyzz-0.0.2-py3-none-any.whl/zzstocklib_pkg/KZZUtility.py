import pandas as pd
import requests
from lxml import etree
import time
import json
from pandas.io.json import json_normalize
import os
import re

def get_KZZInfo_from_JSL():
    now_time = time.time()
    url = 'https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=' + str(now_time)
    # 发送请求并解析HTML对象
    response = requests.get(url)
    jsonObj = response.json()

    df = pd.DataFrame.from_dict(json_normalize(jsonObj['rows']), orient='columns')

    #print(df)
    #bond_code, bond_price, bond_increase_rate,bond_stock_price,bond_stock_increase_rate

    jslbond_df = df[['cell.bond_id','cell.price','cell.increase_rt','cell.sprice','cell.sincrease_rt']]
    jslbond_df.columns = ['bond_code','bond_price','bond_increase_rate','bond_stock_price','bond_stock_increase_rate']
    return jslbond_df

    #Assume the kzz_df is a dataframe
def merge_KZZlist_withJSLprice(kzz_df):
    #kzz_df['债券现价'] = 0.0
    kzz_df['债券振幅'] = 0.0
    #kzz_df['股票现价'] = 0.0
    kzz_df['正股振幅'] = 0.0
    
    current_bondprice_df = get_KZZInfo_from_JSL()
    for index, row in current_bondprice_df.iterrows():
        try:
            temp_row = kzz_df.loc[kzz_df['债券代码'] == row['bond_code']]
            temp_row['当前价'] = row['bond_price']
            temp_row['债券振幅'] = row['bond_increase_rate']
            temp_row['正股股价'] = row['bond_stock_price']
            temp_row['正股振幅'] = row['bond_stock_increase_rate']
            kzz_df.loc[kzz_df['债券代码'] == row['bond_code']] = temp_row
        except KeyError:
            print('code {} is not in KZZ list. It need to be updated.'.format(row['bond_code']))
         
    return kzz_df

def gen_KZZDetaillist_with_RPAData(rpa_data_file_path):
    #path = "/Users/zhangzhi/temp/zz/" #文件夹目录
    path = rpa_data_file_path
    files= os.listdir(path) #得到文件夹下的所有文件名称
    data = pd.DataFrame(columns=('债券代码','债券名称','正股代码','正股名称','正股股价','市净率','每股净资产','转股价','信用级别'
                            ,'转股开始日','转股结束日','回售触发价','回售执行日','强赎触发价','赎回登记日','上市日','到期日'
                            ,'发行规模','利率1','利率2','利率3','利率4','利率5','利率6','赎回利率','回售条款','赎回条款'))

    for file in files:
        if file.find("bak") == -1:
            print(file)
            df = pd.read_csv(path  + file,header=None)
            df2 = pd.read_csv(path + df[2][0] + 'bak.csv',header=None)
    
            code = re.findall(r'年(.+?%)', df[2][27])
            lastcode = re.findall(r'([0-9]+%)', df2[2][1])
            if len(code) == 6:
                row={'债券代码':df[2][0],'债券名称':df[4][0],'正股代码':df[2][4],'正股名称':df[4][4],'正股股价':df[2][10],'市净率':df[4][10],
                '每股净资产':0,'转股价':df[4][11],'信用级别':df[2][23]
                                ,'转股开始日':df[2][14],'转股结束日':df[4][14],'回售触发价':df[2][13],'回售执行日':df[2][18],
                '强赎触发价':df[4][13],'赎回登记日':df[2][16],'上市日':df[2][24],'到期日':df[2][26]
                            ,'发行规模':df[4][21],'利率1':code[0],'利率2':code[1],'利率3':code[2],'利率4':code[3],
                '利率5':code[4],'利率6':code[5],'赎回利率':lastcode[0],'回售条款':df2[2][0],'赎回条款':df2[2][1]}
            else:
                row={'债券代码':df[2][0],'债券名称':df[4][0],'正股代码':df[2][4],'正股名称':df[4][4],'正股股价':df[2][10],'市净率':df[4][10],
                '每股净资产':0,'转股价':df[4][11],'信用级别':df[2][23]
                                ,'转股开始日':df[2][14],'转股结束日':df[4][14],'回售触发价':df[2][13],'回售执行日':df[2][18],
                '强赎触发价':df[4][13],'赎回登记日':df[2][16],'上市日':df[2][24],'到期日':df[2][26]
                            ,'发行规模':df[4][21],'利率1':code[0],'利率2':code[1],'利率3':code[2],'利率4':code[3],
                '利率5':code[4],'赎回利率':lastcode[0],'回售条款':df2[2][0],'赎回条款':df2[2][1]}
            data = data.append(row,ignore_index=True)
    return data

def check_KZZ_with_Rules(kzz_df):
    notification_dict = {}
    for index, row in kzz_df.iterrows():
        #rule 1:当某只可转债跌破历史最低价
        if row['当前价'] <= row['历史最低价']:
            key = '债券:{} code:{} 当前价格低于历史最低价{}'.format(row['债券名称'],row['债券代码'],row['历史最低价'])
            if (key not in notification_dict.keys()):
                notification_dict[key] = 'waitting'
        #rule 2:当某只可转债跌到历史最低价+5%左右，且年化收益在5%以上
        if  row['当前价'] <= row['历史最低价']*1.05 and row['当前价'] <= row['年化%5收益率']:
            key = '债券:{} code:{} 当前价格历史最低价{}+5%及年化收益5%空间'.format(row['债券名称'],row['债券代码'],row['历史最低价'])
            if (key not in notification_dict.keys()):
                notification_dict[key] = 'waitting'
    return notification_dict

pd = gen_KZZDetaillist_with_RPAData("C:\\zz\\")
pd.to_excel("C:\ss.xlsx")