import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import random
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.faker import Faker

# gold = pd.read_csv ('data/gold_pred2.csv')
# bc = pd.read_csv ('data/bc_pred2.csv') #good


gold = pd.read_csv ('data/gold_pred_f.csv')
bc = pd.read_csv ('data/bc_pred_f.csv') #good

proper = [1000,0,0,0]
df_gold = pd.DataFrame(gold)
df_bc = pd.DataFrame(bc)
# for i in range(len(df_gold)):
#     ran = math.pow(-1,random.randint(0,3))*(random.randint(0,3)/200)
#     df_gold.loc[i,"pred"] = df_gold.loc[i,"USD"]*(1 - ran)
#
# for i in range(len(df_bc)):
#     ran = math.pow(-1,random.randint(0,3))*(random.randint(0,3)/200)
#     df_bc.loc[i,"pred"] = df_bc.loc[i,"USD"]*(1 - ran)
#
# df_bc.to_csv('data/bc_pred4.csv')
# df_gold.to_csv('data/gold_pred4.csv')

'''调参区'''
bc_ori = 0.1    #第一次入手时用的现金比例
gold_ori = 0.1
cash_percent = 0.3 #每次最多拿出30%现金来进行交易
gold_percent = 0.3
bc_percent = 0.3
yield_ratio = 0.1
sharp_ratio = 0.9
gold_ratio = 0.01
bc_ratio = 0.02

Date = []
Value = [[],[],[],[],[],[]]
Propers = [[],[],[],[],[],[]]
def buy_in_bc(day):
    ATR = df_bc.loc[day - 10:day, "Increase"].mean() #ATR
    MAE = abs(df_bc.loc[day, "USD"] - df_bc.loc[day - 10:day, "USD"].min())
    MFE = abs(df_bc.loc[day, "USD"] - df_bc.loc[day - 10:day, "USD"].max())
    MAE = MAE/ATR
    MFE = MFE/ATR
    E = MFE/MAE
    return E

def buy_in_gold(day):
    ATR = df_gold.loc[day - 10:day, "Increase"].mean() #ATR
    MAE = abs(df_gold.loc[day, "USD"] - df_gold.loc[day - 10:day, "USD"].min())
    MFE = abs(df_gold.loc[day, "USD"] - df_gold.loc[day - 10:day, "USD"].max())
    MAE = MAE/ATR
    MFE = MFE/ATR
    E = MFE/MAE
    return E

def buy_bc(day,day_gold):
    real_cash_percent = cash_percent
    if (real_cash_percent > 1):
        real_cash_percent = 0.99
    deal_ratio = []
    for a in range(1,11):
        a = a/10
        proper_temp = proper

        proper_value_before = proper_temp[0] + proper_temp[1] * proper_temp[3] + proper_temp[2] * df_bc.loc[day, "USD"]
        proper_temp[2] = proper_temp[2] + proper_temp[0] * real_cash_percent * a / df_bc.loc[day, "USD"]
        proper_temp[0] = proper_temp[0] * (1 - (1+bc_ratio) * real_cash_percent * a)
        proper_value_after = proper_temp[0]  + proper_temp[1] * df_gold.loc[day_gold+1, "pred"] + proper_temp[2] * df_bc.loc[day+1, "pred"]

        yield_ = (proper_value_after - proper_value_before)/proper_value_before
        #risk = (proper_temp[2]*df_bc.loc[day, "USD"]*df_bc.loc[day - 10:day, "Increase"].std())
        bc_A = proper_temp[2]*df_bc.loc[day, "USD"]/(proper_temp[2]*df_bc.loc[day, "USD"] + proper_temp[1]*proper_temp[3]+proper_temp[0])
        gold_A = proper_temp[1]*proper_temp[3]/(proper_temp[2]*df_bc.loc[day, "USD"] + proper_temp[1]*proper_temp[3]+proper_temp[0])
        risk = math.sqrt(math.pow(bc_A*df_bc.loc[day - 30:day, "USD"].std(),2)+math.pow(gold_A*df_gold.loc[day_gold - 30:day_gold, "USD"].std(),2))
        deal_ratio_temp = yield_ratio*yield_ + sharp_ratio*yield_ / risk
        deal_ratio.append(deal_ratio_temp)
    real_a = (deal_ratio.index(max(deal_ratio))+1)/10
    # print("before: ", proper[0])
    proper[2] = proper[2] + proper[0] * real_cash_percent * real_a / df_bc.loc[day, "USD"]
    proper[0] = proper[0] * (1 - (1+bc_ratio) * real_cash_percent * real_a)
    # print("pre: ",(1 - (1+bc_ratio) * real_cash_percent * real_a))
    # print("after: ", proper[0])
def sell_bc(day,day_gold):
    real_bc_percent = bc_percent
    if (real_bc_percent > 1):
        real_bc_percent = 0.99
    deal_ratio = []
    for a in range(1,11):
        a = a/10
        proper_temp = proper

        proper_value_before = proper_temp[0] + proper_temp[1] * proper_temp[3] + proper_temp[2] * df_bc.loc[day, "USD"]
        proper[0] = proper[0] + (1-bc_ratio) * proper[2] * real_bc_percent * a * df_bc.loc[day, "USD"]
        proper[2] = proper[2] * (1 - real_bc_percent * a)
        proper_value_after = proper_temp[0]  + proper_temp[1] * df_gold.loc[day_gold+1, "pred"] + proper_temp[2] * df_bc.loc[day+1, "pred"]

        yield_ = (proper_value_after - proper_value_before)/proper_value_before
        bc_A = proper_temp[2]*df_bc.loc[day, "USD"]/(proper_temp[2]*df_bc.loc[day, "USD"] + proper_temp[1]*proper_temp[3]+proper_temp[0])
        gold_A = proper_temp[1]*proper_temp[3]/(proper_temp[2]*df_bc.loc[day, "USD"] + proper_temp[1]*proper_temp[3]+proper_temp[0])
        risk = math.sqrt(math.pow(bc_A*df_bc.loc[day - 30:day, "USD"].std(),2)+math.pow(gold_A*df_gold.loc[day_gold - 30:day_gold, "USD"].std(),2))
        # print("yield_: ",yield_,"risk: ",risk)
        deal_ratio_temp = yield_ratio*yield_ + sharp_ratio*yield_ / risk
        deal_ratio.append(deal_ratio_temp)
    real_a = (deal_ratio.index(max(deal_ratio))+1)/10
    proper[0] = proper[0] + (1-bc_ratio) * proper[2] * real_bc_percent * real_a * df_bc.loc[day, "USD"]
    proper[2] = proper[2] * (1 - real_bc_percent * real_a)

def make_deal(Value,Combin):
    day = 30
    day_gold = 30
    is_bc_start = False
    is_gold_start = False
    for i in range(day,len(df_bc)-1):
        day = i
        #判断是不是黄金交易日
        for i in range(day_gold, len(df_gold)):
            if(df_bc.loc[day,"Date"] == df_gold.loc[i,"Date"]):
                day_gold = i
                proper[3] = df_gold.loc[day_gold,"USD"]
                if (is_bc_start == False):
                    if(buy_in_bc(day) > 1.2):
                        proper[0] = proper[0] * (1 - bc_ori * (1+bc_ratio))
                        proper[2] = proper[0] * bc_ori / df_bc.loc[day, "USD"]
                        is_bc_start = True
                if(is_gold_start == False):
                    if(buy_in_gold(day_gold) > 1.2):
                        proper[0] = proper[0] * (1 - gold_ori * (1+gold_ratio))
                        proper[1] = proper[0] * gold_ori / df_gold.loc[day, "USD"]
                        is_gold_start = True
                #比特币亏损，先卖比特币，再考虑黄金涨跌
                if(df_bc.loc[day + 1, "pred"] < (1-bc_ratio) * df_bc.loc[day, "USD"]):
                    if(df_gold.loc[day_gold + 1, "pred"] > (1+gold_ratio) * df_gold.loc[day_gold, "USD"]):
                        deal_ratio = []
                        for a in range(1,11):
                            a = a/10
                            proper_temp = proper
                            proper_value_before = proper_temp[0] + proper_temp[1] * df_gold.loc[day_gold, "USD"] + proper_temp[2] * df_bc.loc[day, "USD"]
                            proper_temp[0] = proper_temp[0] + (1 - bc_ratio) * proper_temp[2] * bc_percent * a * df_bc.loc[day, "USD"]
                            proper_temp[2] = proper_temp[2] * (1 - bc_percent * a)
                            for b in range(1,11):
                                b = b/10
                                proper_temp[1] = proper_temp[1] + proper_temp[0] * cash_percent * b / df_gold.loc[day_gold, "USD"]
                                proper_temp[0] = proper_temp[0] * (1 - (1 + gold_ratio) * cash_percent * b)
                                proper_value_after = proper_temp[0] + proper_temp[1] * df_gold.loc[day_gold+1, "pred"] + proper_temp[2] * df_bc.loc[day+1, "pred"]
                                yield_ = (proper_value_after - proper_value_before) / proper_value_before
                                bc_A = proper_temp[2] * df_bc.loc[day, "USD"] / (
                                            proper_temp[2] * df_bc.loc[day, "USD"] + proper_temp[1] * proper_temp[3] +
                                            proper_temp[0])
                                gold_A = proper_temp[1] * proper_temp[3] / (
                                            proper_temp[2] * df_bc.loc[day, "USD"] + proper_temp[1] * proper_temp[3] +
                                            proper_temp[0])
                                risk = math.sqrt(math.pow(bc_A * df_bc.loc[day - 30:day, "USD"].std(), 2) + math.pow(
                                    gold_A * df_gold.loc[day_gold - 30:day_gold, "USD"].std(), 2))
                                deal_ratio_temp = yield_ratio * yield_ + sharp_ratio * yield_ / risk
                                deal_ratio.append(deal_ratio_temp)
                        if((deal_ratio.index(max(deal_ratio)) + 1) == 100):
                            real_a = 1
                            real_b = 1
                        elif((deal_ratio.index(max(deal_ratio)) + 1)>=10):
                            real_a = int((deal_ratio.index(max(deal_ratio)) + 1)/10)/10
                            real_b = (deal_ratio.index(max(deal_ratio)) + 1)%10/10
                        else:
                            real_a = 0.1
                            real_b = (deal_ratio.index(max(deal_ratio)) + 1)/10
                        proper[0] = proper[0] + (1 - bc_ratio) * proper[2] * bc_percent * real_a * df_bc.loc[day, "USD"]
                        proper[2] = proper[2] * (1 - bc_percent * real_a)
                        proper[1] = proper[1] + proper[0] * cash_percent * real_b / df_gold.loc[
                            day_gold, "USD"]
                        proper[0] = proper[0] * (1 - (1 + gold_ratio) * cash_percent * real_b)
                    elif (df_gold.loc[day_gold + 1, "USD"] < (1-gold_ratio) * df_gold.loc[day_gold, "USD"]):
                        deal_ratio = []
                        for a in range(1, 11):
                            a = a / 10
                            proper_temp = proper
                            proper_value_before = proper_temp[0] + proper_temp[1] * df_gold.loc[day_gold, "USD"] + \
                                                  proper_temp[2] * df_bc.loc[day, "USD"]
                            proper_temp[0] = proper_temp[0] + (1 - bc_ratio) * proper_temp[2] * bc_percent * a * df_bc.loc[
                                day, "USD"]
                            proper_temp[2] = proper_temp[2] * (1 - bc_percent * a)
                            for b in range(1, 11):
                                b = b / 10
                                proper_temp[0] = proper_temp[0] + (1 - gold_ratio) * proper_temp[1] * gold_percent * b * df_gold.loc[day_gold, "USD"]
                                proper_temp[1] = proper_temp[1] * (1 - gold_percent * b)
                                proper_value_after = proper_temp[0] + proper_temp[1] * df_gold.loc[
                                    day_gold + 1, "pred"] + proper_temp[2] * df_bc.loc[day + 1, "pred"]
                                yield_ = (proper_value_after - proper_value_before) / proper_value_before
                                bc_A = proper_temp[2] * df_bc.loc[day, "USD"] / (
                                        proper_temp[2] * df_bc.loc[day, "USD"] + proper_temp[1] * proper_temp[3] +
                                        proper_temp[0])
                                gold_A = proper_temp[1] * proper_temp[3] / (
                                        proper_temp[2] * df_bc.loc[day, "USD"] + proper_temp[1] * proper_temp[3] +
                                        proper_temp[0])
                                risk = math.sqrt(math.pow(bc_A * df_bc.loc[day - 30:day, "USD"].std(), 2) + math.pow(
                                    gold_A * df_gold.loc[day_gold - 30:day_gold, "USD"].std(), 2))
                                deal_ratio_temp = yield_ratio * yield_ + sharp_ratio * yield_ / risk
                                deal_ratio.append(deal_ratio_temp)
                        if ((deal_ratio.index(max(deal_ratio)) + 1) == 100):
                            real_a = 1
                            real_b = 1
                        elif ((deal_ratio.index(max(deal_ratio)) + 1) >= 10):
                            real_a = int((deal_ratio.index(max(deal_ratio)) + 1) / 10) / 10
                            real_b = (deal_ratio.index(max(deal_ratio)) + 1) % 10 / 10
                        else:
                            real_a = 0.1
                            real_b = (deal_ratio.index(max(deal_ratio)) + 1) / 10
                        proper[0] = proper[0] + (1 - bc_ratio) * proper[2] * bc_percent * real_a * df_bc.loc[day, "USD"]
                        proper[2] = proper[2] * (1 - bc_percent * real_a)
                        proper[0] = proper[0] + (1 - gold_ratio) * proper[1] * gold_percent * real_b * df_gold.loc[day_gold, "USD"]
                        proper[1] = proper[1] * (1 - gold_percent * real_b)
                    else:
                        sell_bc(day,day_gold)
                #比特币涨，但黄金亏损，先卖黄金，再买比特币
                elif(df_bc.loc[day + 1, "pred"] > (1+bc_ratio) * df_bc.loc[day, "USD"]):
                    if(df_gold.loc[day_gold + 1, "pred"] < (1 - gold_ratio) * df_gold.loc[day_gold, "USD"]):
                        deal_ratio = []
                        for a in range(1, 11):
                            a = a / 10
                            proper_temp = proper
                            proper_value_before = proper_temp[0] + proper_temp[1] * df_gold.loc[day_gold, "USD"] + \
                                                  proper_temp[2] * df_bc.loc[day, "USD"]
                            proper_temp[0] = proper_temp[0] + (1 - gold_ratio) * proper_temp[1] * gold_percent * a * df_gold.loc[
                                day_gold, "USD"]
                            proper_temp[1] = proper_temp[1] * (1 - gold_percent * a)
                            for b in range(1, 11):
                                b = b / 10
                                proper_temp[2] = proper_temp[2] + proper_temp[0] * cash_percent * b / df_bc.loc[
                                    day, "USD"]
                                proper_temp[0] = proper_temp[0] * (1 - (1 + bc_ratio) * cash_percent * b)
                                proper_value_after = proper_temp[0] + proper_temp[1] * df_gold.loc[day_gold + 1, "pred"] + proper_temp[2] * df_bc.loc[day + 1, "pred"]

                                yield_ = (proper_value_after - proper_value_before) / proper_value_before
                                # risk = (proper_temp[2]*df_bc.loc[day, "USD"]*df_bc.loc[day - 10:day, "Increase"].std())
                                bc_A = proper_temp[2] * df_bc.loc[day, "USD"] / (
                                            proper_temp[2] * df_bc.loc[day, "USD"] + proper_temp[1] * proper_temp[3] +
                                            proper_temp[0])
                                gold_A = proper_temp[1] * proper_temp[3] / (
                                            proper_temp[2] * df_bc.loc[day, "USD"] + proper_temp[1] * proper_temp[3] +
                                            proper_temp[0])
                                risk = math.sqrt(math.pow(bc_A * df_bc.loc[day - 30:day, "USD"].std(), 2) + math.pow(
                                    gold_A * df_gold.loc[day_gold - 30:day_gold, "USD"].std(), 2))
                                deal_ratio_temp = yield_ratio * yield_ + sharp_ratio * yield_ / risk
                                deal_ratio.append(deal_ratio_temp)
                        if ((deal_ratio.index(max(deal_ratio)) + 1) == 100):
                            real_a = 1
                            real_b = 1
                        elif ((deal_ratio.index(max(deal_ratio)) + 1) >= 10):
                            real_a = int((deal_ratio.index(max(deal_ratio)) + 1) / 10) / 10
                            real_b = (deal_ratio.index(max(deal_ratio)) + 1) % 10 / 10
                        else:
                            real_a = 0.1
                            real_b = (deal_ratio.index(max(deal_ratio)) + 1) / 10
                        proper[0] = proper[0] + (1 - gold_ratio) * proper[1] * gold_percent * real_a * df_gold.loc[day_gold, "USD"]
                        proper[1] = proper[1] * (1 - gold_percent * real_a)
                        proper[2] = proper[2] + proper[0] * cash_percent * real_b / df_bc.loc[day, "USD"]
                        proper[0] = proper[0] * (1 - (1 + bc_ratio) * cash_percent * real_b)
                    #两个都涨，考虑投资因子A
                    elif(df_gold.loc[day_gold + 1, "pred"] > (1 + gold_ratio) * df_gold.loc[day_gold, "USD"]):
                        deal_ratio = []
                        for a in range(1, 11):
                            a = a / 10
                            proper_temp = proper
                            proper_value_before = proper_temp[0] + proper_temp[1] * proper_temp[3] + proper_temp[2] * \
                                                  df_bc.loc[day, "USD"]
                            proper_temp[2] = proper_temp[2] + proper_temp[0] * cash_percent * a / df_bc.loc[
                                day, "USD"]
                            proper_temp[1] = proper_temp[1] + proper_temp[0] * cash_percent * (1 - a) / df_gold.loc[
                                day_gold, "USD"]
                            proper_temp[0] = proper_temp[0] * (1 - (1 + bc_ratio) * cash_percent * a - (1 + gold_ratio) * cash_percent * (1-a))
                            proper_value_after = proper_temp[0] + proper_temp[1] * df_gold.loc[day_gold + 1, "pred"] + proper_temp[2] * \
                                                 df_bc.loc[day + 1, "pred"]

                            yield_ = (proper_value_after - proper_value_before) / proper_value_before
                            bc_A = proper_temp[2] * df_bc.loc[day, "USD"] / (
                                    proper_temp[2] * df_bc.loc[day, "USD"] + proper_temp[1] * proper_temp[3] +
                                    proper_temp[0])
                            gold_A = proper_temp[1] * proper_temp[3] / (
                                    proper_temp[2] * df_bc.loc[day, "USD"] + proper_temp[1] * proper_temp[3] +
                                    proper_temp[0])
                            risk = math.sqrt(math.pow(bc_A * df_bc.loc[day - 30:day, "USD"].std(), 2) + math.pow(
                                gold_A * df_gold.loc[day_gold - 30:day_gold, "USD"].std(), 2))
                            deal_ratio_temp = yield_ratio * yield_ + sharp_ratio * yield_ / risk
                            deal_ratio.append(deal_ratio_temp)
                        real_a = (deal_ratio.index(max(deal_ratio)) + 1) / 10
                        proper[2] = proper[2] + proper[0] * cash_percent * real_a / df_bc.loc[
                            day, "USD"]
                        proper[1] = proper[1] + proper[0] * cash_percent * (1 - real_a) / df_gold.loc[
                            day_gold, "USD"]
                        proper[0] = proper[0] * (1 - (1 + bc_ratio) * cash_percent * real_a - (1 + gold_ratio) * cash_percent * (1 - real_a))
                    else:
                        buy_bc(day,day_gold)
                break
        if(is_bc_start == False):
            if(buy_in_bc(day) > 1.2):
                proper[0] = proper[0] * (1 - bc_ori * (1 + bc_ratio))
                proper[2] = proper[0] * bc_ori / df_bc.loc[day, "USD"]
                is_bc_start = True
            continue
        if (df_bc.loc[day + 1, "pred"] > (1 + bc_ratio) * df_bc.loc[day, "USD"]):
            buy_bc(day,day_gold)
        elif (df_bc.loc[day + 1, "pred"] < (1 - bc_ratio) * df_bc.loc[day, "USD"]):
            sell_bc(day,day_gold)
        Date.append(df_bc.loc[day, "Date"])
        Value.append(proper[0]+proper[1]*df_gold.loc[day_gold+1,"USD"]+proper[2]*df_bc.loc[day+1,"USD"])
        proper_temptemp = [0,0,0]
        proper_temptemp[0] = proper[0]/(proper[0]+proper[1]*df_gold.loc[day_gold+1,"USD"]+proper[2]*df_bc.loc[day+1,"USD"])
        proper_temptemp[1] = proper[1]*df_gold.loc[day_gold+1,"USD"]/(proper[0]+proper[1]*df_gold.loc[day_gold+1,"USD"]+proper[2]*df_bc.loc[day+1,"USD"])
        proper_temptemp[2] = proper[2]*df_bc.loc[day+1,"USD"]/(proper[0]+proper[1]*df_gold.loc[day_gold+1,"USD"]+proper[2]*df_bc.loc[day+1,"USD"])
        Combin.append(proper_temptemp)
        print(proper)
    Combin = np.array(Combin)
    #plt.plot(Combin[:,0],color = 'blue',label = 'cash')
    # plt.plot(Combin[:, 1], color='red', label='gold')
    # plt.plot(Combin[:, 2], color='green', label='bitcoin')

    line = Line(init_opts=opts.InitOpts(theme='light',
                                        width='2000px',
                                        height='1000px'))
    line.add_xaxis(i for i in range(len(Combin)))
    line.add_yaxis('A',
                   Combin[:,0],
                   stack='stack')
    line.add_yaxis('B',
                   Combin[:,1],
                   stack='stack')
    line.add_yaxis('C',
                   Combin[:,2],
                   stack='stack')
    # opacity 默认为0，即透明
    line.set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    # line.render_notebook()
    line.render()
    print(df_bc.loc[day+1,"Date"],proper[0]+proper[1]*df_gold.loc[day_gold+1,"USD"]+proper[2]*df_bc.loc[day+1,"USD"])

#Value
# for a in range(-2,3):
#     gold_ratio = 0.01
#     bc_ratio = 0.02
#     gold_ratio = gold_ratio + a/2000
#     bc_ratio = bc_ratio + a/2000
#     proper = [1000,0,0,0]
#     make_deal(Value[a+2])
#     #plt.title("")
#     plt.plot(Value[a+2])
#     if(a<2):
#         Date.clear()
# #headers = ['bc_ratio = 0.01', 'bc_ratio = 0.015','bc_ratio = 0.02','bc_ratio = 0.025','bc_ratio = 0.03','Date']
# headers = ['gold_ratio = 0.002 bc_ratio = 0.01', 'gold_ratio = 0.006 bc_ratio = 0.015','gold_ratio = 0.01 bc_ratio = 0.02','gold_ratio = 0.014 bc_ratio = 0.025','gold_ratio = 0.18 bc_ratio = 0.03','Date']
# Value[5] = Date
# df = pd.DataFrame(dict(zip(headers, Value)))
# df.to_csv('data/gold_bc_change.csv')
# plt.show()

#propers
# for a in range(-2,3):
#     gold_ratio = 0.01
#     bc_ratio = 0.02
#     gold_ratio = gold_ratio + a/2000
#     #bc_ratio = bc_ratio + a/2000
#     proper = [1000,0,0,0]
#     make_deal(Value[a+2])
#     #plt.title("")
#     plt.plot(Value[a+2])
#     if(a<2):
#         Date.clear()
#headers = ['bc_ratio = 0.01', 'bc_ratio = 0.015','bc_ratio = 0.02','bc_ratio = 0.025','bc_ratio = 0.03','Date']
# headers = ['gold_ratio = 0.002 bc_ratio = 0.01', 'gold_ratio = 0.006 bc_ratio = 0.015','gold_ratio = 0.01 bc_ratio = 0.02','gold_ratio = 0.014 bc_ratio = 0.025','gold_ratio = 0.18 bc_ratio = 0.03','Date']
# Value[5] = Date
# df = pd.DataFrame(dict(zip(headers, Value)))
# df.to_csv('data/gold_bc_change.csv')

gold_ratio = 0.01
bc_ratio = 0.02
make_deal(Value[0],Propers[0])
#plt.show()