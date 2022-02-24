import pandas as pd
import numpy as np

gold = pd.read_csv ('data/gold.csv',sep=';')
bc = pd.read_csv ('data/bc_pred.csv')


'''调参区'''
bc_ori = 0.01    #第一次入手时用的现金比例
gold_ori = 0.01
cash_precent = 0.9 #每次最多拿出30%现金来进行交易
gold_precent = 0.9
bc_precent = 0.9
earning_weight = 0.9 #投资因子中的收益权重
risk_weight = 1 - earning_weight #投资因子中的风险惩罚项权重

proper = [1000,0,0]
df_gold = pd.DataFrame(gold)
df_bc = pd.DataFrame(bc)

# temp_gold = df_gold.loc[:10,"Increase"]
# temp_golds = df_gold[df_gold['Increase'] > 0]
# temp_golds = temp_golds.loc[:10,"Increase"]
# print(temp_golds)
#print(temp_gold.quantile())

#is_start = False
# for day in range(len(df_gold)):
#     if(is_start == False):
#         if (df_gold.loc[day, "USD"] < 1300):
#             proper[0] = proper[0] * (1 - 0.3 * 1.01)
#             proper[1] = proper[0] * 0.3 / df_gold.loc[day, "USD"]
#             is_start = True
#         continue
#     if (df_gold.loc[day + 1, "USD"] > 1.01 * df_gold.loc[day, "USD"]):
#         # 买入
#         temp_gold = df_gold[df_gold['Increase'] > 0]
#         temp_gold = temp_gold.loc[:day, "Increase"]
#         real_cash_percent = cash_precent * (df_gold.loc[day + 1, "USD"] - df_gold.loc[day, "USD"]) / (
#                 df_gold.loc[day, "USD"] * temp_gold.max())
#         # print((df_gold.loc[day+1,"USD"] - df_gold.loc[day,"USD"])/df_gold.loc[day,"USD"],temp_gold.max())
#         if (real_cash_percent > 1):
#             real_cash_percent = 0.99
#         print(real_cash_percent)
#         proper[1] = proper[1] + proper[0] * real_cash_percent / df_gold.loc[day, "USD"]
#         proper[0] = proper[0] * (1 - 1.01 * real_cash_percent)
#     elif (df_gold.loc[day + 1, "USD"] < 0.99 * df_gold.loc[day, "USD"]):
#         temp_gold = df_gold[df_gold['Increase'] < 0]
#         temp_gold = temp_gold.loc[:day, "Increase"]
#         real_gold_percent = gold_precent * (df_gold.loc[day + 1, "USD"] - df_gold.loc[day, "USD"]) / (
#                 df_gold.loc[day, "USD"] * temp_gold.min())
#         if (real_gold_percent > 1):
#             real_gold_percent = 0.99
#         proper[0] = proper[0] + 0.99 * proper[1] * real_gold_percent * df_gold.loc[day, "USD"]
#         proper[1] = proper[1] * (1 - real_gold_percent)
#     print(df_gold.loc[day,"Date"],proper[0]+proper[1]*df_gold.loc[day,"USD"])







def buy_gold(day):
    temp_gold = df_gold[df_gold['Increase'] > 0]
    temp_gold = temp_gold.loc[:day, "Increase"]
    # real_cash_percent = cash_precent * (df_gold.loc[day + 1, "USD"] - df_gold.loc[day, "USD"]) / (
    #         df_gold.loc[day, "USD"] * temp_gold.max())
    real_cash_percent = cash_precent
    if (real_cash_percent > 1):
        real_cash_percent = 0.99
    proper[1] = proper[1] + proper[0] * real_cash_percent / df_gold.loc[day, "USD"]
    proper[0] = proper[0] * (1 - 1.01 * real_cash_percent)
def sell_gold(day):
    temp_gold = df_gold[df_gold['Increase'] < 0]
    temp_gold = temp_gold.loc[:day, "Increase"]
    #real_gold_percent = gold_precent * (df_gold.loc[day + 1, "USD"] - df_gold.loc[day, "USD"]) / (df_gold.loc[day, "USD"] * temp_gold.min())
    real_gold_percent = gold_precent
    if (real_gold_percent > 1):
        real_gold_percent = 0.99
    proper[0] = proper[0] + 0.99 * proper[1] * real_gold_percent * df_gold.loc[day, "USD"]
    proper[1] = proper[1] * (1 - real_gold_percent)

def buy_bc(day):
    temp_bc = df_bc[df_bc['Increase'] > 0]
    temp_bc = temp_bc.loc[:day, "Increase"]
    # real_cash_percent = cash_precent * (df_bc.loc[day + 1, "USD"] - df_bc.loc[day, "USD"]) / (
    #         df_bc.loc[day, "USD"] * temp_bc.max())
    real_cash_percent = cash_precent
    if (real_cash_percent > 1):
        real_cash_percent = 0.99
    proper[2] = proper[2] + proper[0] * real_cash_percent / df_bc.loc[day, "USD"]
    proper[0] = proper[0] * (1 - 1.02 * real_cash_percent)

def sell_bc(day):
    temp_bc = df_bc[df_bc['Increase'] < 0]
    temp_bc = temp_bc.loc[:day, "Increase"]
    # real_bc_precent = bc_precent * (df_bc.loc[day + 1, "USD"] - df_bc.loc[day, "USD"]) / (
    #         df_bc.loc[day, "USD"] * temp_bc.min())
    real_bc_precent = bc_precent
    if (real_bc_precent > 1):
        real_bc_precent = 0.99
    proper[0] = proper[0] + 0.98 * proper[2] * real_bc_precent * df_bc.loc[day, "USD"]
    proper[2] = proper[2] * (1 - real_bc_precent)

# is_start = False
# count = 0
# for day in range(len(df_bc)-1):
#     if(is_start == False):
#         proper[0] = proper[0] * (1 - bc_ori * 1.02)
#         proper[2] = proper[0] * bc_ori / df_bc.loc[day, "USD"]
#         is_start = True
#         continue
#     if(df_bc.loc[day + 1, "pred"] > 1.02 * df_bc.loc[day, "USD"]):
#         buy_bc(day)
#         count = count + 1
#     elif(df_bc.loc[day + 1, "pred"] < 0.98 * df_bc.loc[day, "USD"]):
#         sell_bc(day)
#         count = count + 1
# print(df_bc.loc[day+1,"Date"],proper[0]+proper[2]*df_bc.loc[day+1,"USD"])

# is_start = False
# for day in range(len(df_gold)-1):
#     if(is_start == False):
#         if (df_gold.loc[day, "USD"] < 1300):
#             proper[0] = proper[0] * (1 - gold_ori * 1.02)
#             proper[1] = proper[0] * gold_ori / df_gold.loc[day, "USD"]
#             is_start = True
#         continue
#     if(df_gold.loc[day + 1, "USD"] > 1.01 * df_gold.loc[day, "USD"]):
#         buy_gold(day)
#     elif(df_gold.loc[day + 1, "USD"] < 0.99 * df_gold.loc[day, "USD"]):
#         sell_gold(day)
#     #print(proper)
# print(df_gold.loc[day+1,"Date"],proper[0]+proper[1]*df_gold.loc[day+1,"USD"])



def make_deal_gain():
    day_gold = 0
    is_bc_start = False
    is_gold_start = False
    for day in range(len(df_bc)-1):
        #判断是不是黄金交易日
        for i in range(day_gold, len(df_gold)):
            if(df_bc.loc[day,"Date"] == df_gold.loc[i,"Date"]):
                day_gold = i
                if (is_bc_start == False):
                    #if (df_bc.loc[day, "USD"] < 600):
                    proper[0] = proper[0] * (1 - bc_ori * 1.02)
                    proper[2] = proper[0] * bc_ori / df_bc.loc[day, "USD"]
                    is_bc_start = True
                if(is_gold_start == False):
                    #if (df_gold.loc[day_gold, "USD"] < 1200):
                    proper[0] = proper[0] * (1 - gold_ori * 1.01)
                    proper[1] = proper[0] * gold_ori / df_gold.loc[day, "USD"]
                    is_gold_start = True
                #比特币亏损，先卖比特币，再考虑黄金涨跌
                if(df_bc.loc[day + 1, "USD"] < 0.98 * df_bc.loc[day, "USD"]):
                    sell_bc(day)
                    # if(df_gold.loc[day_gold + 1, "USD"] > 1.01 * df_gold.loc[day_gold, "USD"]):
                    #     buy_gold(day_gold)
                    if (df_gold.loc[day_gold + 1, "USD"] < 0.99 * df_gold.loc[day_gold, "USD"]):
                        sell_gold(day_gold)
                #比特币涨，但黄金亏损，先卖黄金，再买比特币
                elif(df_bc.loc[day + 1, "USD"] > 1.02 * df_bc.loc[day, "USD"]):
                    if(df_gold.loc[day_gold + 1, "USD"] < 0.99 * df_gold.loc[day_gold, "USD"]):
                        sell_gold(day_gold)
                        buy_bc(day)
                    #两个都涨，考虑投资因子A
                    elif(df_gold.loc[day_gold + 1, "USD"] > 1.01 * df_gold.loc[day_gold, "USD"]):
                        if(day)>60:
                            if(day_gold>60):
                                # print("df_gold:", df_gold.loc[day_gold-60:day_gold, "USD"].std(), "df_bc:",
                                #       df_bc.loc[day - 60:day, "USD"].std())
                                bc_A = earning_weight*(df_bc.loc[day + 1, "USD"] - df_bc.loc[day, "USD"])-risk_weight*df_bc.loc[day-60:day, "USD"].std()
                                gold_A = earning_weight * (df_gold.loc[day_gold + 1, "USD"] - df_gold.loc[day_gold, "USD"]) - risk_weight * df_gold.loc[day_gold - 60:day_gold,"USD"].std()
                            elif (day_gold <= 60):
                                # print("df_gold:", df_gold.loc[:day_gold, "USD"].std(), "df_bc:",
                                #       df_bc.loc[day - 60:day, "USD"].std())
                                bc_A = earning_weight*(df_bc.loc[day + 1, "USD"] - df_bc.loc[day, "USD"])-risk_weight*df_bc.loc[day-60:day, "USD"].std()
                                gold_A = earning_weight * (df_gold.loc[day_gold + 1, "USD"] - df_gold.loc[day_gold, "USD"]) - risk_weight * df_gold.loc[:day_gold,"USD"].std()
                        elif(day)<=60:
                            if(day_gold>60):
                                # print("df_gold:", df_gold.loc[day_gold-60:day_gold, "USD"].std(), "df_bc:",
                                #       df_bc.loc[:day, "USD"].std())
                                bc_A = earning_weight*(df_bc.loc[day + 1, "USD"] - df_bc.loc[day, "USD"])-risk_weight*df_bc.loc[:day, "USD"].std()
                                gold_A = earning_weight * (df_gold.loc[day_gold + 1, "USD"] - df_gold.loc[day_gold, "USD"]) - risk_weight * df_gold.loc[day_gold - 60:day_gold,"USD"].std()
                            elif (day_gold <= 60):
                                # print("df_gold:", df_gold.loc[:day_gold, "USD"].std(), "df_bc:",
                                #       df_bc.loc[:day, "USD"].std())
                                bc_A = earning_weight*(df_bc.loc[day + 1, "USD"] - df_bc.loc[day, "USD"])-risk_weight*df_bc.loc[:day, "USD"].std()
                                gold_A = earning_weight * (df_gold.loc[day_gold + 1, "USD"] - df_gold.loc[day_gold, "USD"]) - risk_weight * df_gold.loc[:day_gold,"USD"].std()
                        if(gold_A < 0):
                            gold_A = 0
                        if(bc_A < 0):
                            bc_A = 0
                        bc_buy_precent = bc_A*cash_precent/(bc_A+gold_A)
                        gold_buy_precent = gold_A *cash_precent/ (bc_A + gold_A)
                        proper[2] = proper[2] + proper[0] * bc_buy_precent / df_bc.loc[day, "USD"]
                        proper[1] = proper[1] + proper[0] * gold_buy_precent / df_gold.loc[day_gold, "USD"]
                        proper[0] = proper[0]*(1-1.02*bc_buy_precent-1.01*gold_buy_precent)
                break
        if(is_bc_start == False):
            #if (df_bc.loc[day, "USD"] < 600):
            proper[0] = proper[0] * (1 - bc_ori * 1.02)
            proper[2] = proper[0] * bc_ori / df_bc.loc[day, "USD"]
            is_bc_start = True
            continue
        if (df_bc.loc[day + 1, "USD"] > 1.02 * df_bc.loc[day, "USD"]):
            buy_bc(day)
        elif (df_bc.loc[day + 1, "USD"] < 0.98 * df_bc.loc[day, "USD"]):
            sell_bc(day)
    print(df_bc.loc[day+1,"Date"],proper[0]+proper[1]*df_gold.loc[day_gold+1,"USD"]+proper[2]*df_bc.loc[day+1,"USD"])


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


def buy_bc_sharpe(day):
    temp_bc = df_bc.loc[:day, "Increase"]
    # real_cash_percent = cash_precent * (df_bc.loc[day + 1, "USD"] - df_bc.loc[day, "USD"]) / (
    #         df_bc.loc[day, "USD"] * temp_bc.max())
    real_cash_percent = cash_precent
    if (real_cash_percent > 1):
        real_cash_percent = 0.99
    SharpeRatio = []
    for a in range(1,11):
        a = a/10
        proper_temp = proper
        proper_value_before = proper_temp[0] + proper_temp[2] * df_bc.loc[day, "USD"]
        proper_temp[2] = proper_temp[2] + proper_temp[0] * real_cash_percent * a / df_bc.loc[day, "USD"]
        proper_temp[0] = proper_temp[0] * (1 - 1.02 * real_cash_percent * a)
        proper_value_after = proper_temp[0] + proper_temp[2] * df_bc.loc[day, "USD"]
        SharpeRatio_temp = (proper_value_after - proper_value_before)/(proper_value_before * df_bc.loc[day - 10:day, "Increase"].std())
        SharpeRatio.append(SharpeRatio_temp)
    real_a = (SharpeRatio.index(max(SharpeRatio))+1)/10
    proper[2] = proper[2] + proper[0] * real_cash_percent * real_a / df_bc.loc[day, "USD"]
    proper[0] = proper[0] * (1 - 1.02 * real_cash_percent * real_a)

is_start = False
def make_deal_sharpe():
    for day in range(10,len(df_bc)-1):
        if(is_start == False):
            if(buy_in_bc(day) > 1.2):
                proper[0] = proper[0] * (1 - bc_ori * 1.02)
                proper[2] = proper[0] * bc_ori / df_bc.loc[day, "USD"]
                is_start = True
            continue
        if(df_bc.loc[day + 1, "pred"] > 1.02 * df_bc.loc[day, "USD"]):
            buy_bc(day)
            count = count + 1
        elif(df_bc.loc[day + 1, "pred"] < 0.98 * df_bc.loc[day, "USD"]):
            sell_bc(day)
            count = count + 1
    print(df_bc.loc[day+1,"Date"],proper[0]+proper[2]*df_bc.loc[day+1,"USD"])


# for i in range(1,10):
#     proper = [1000,0,0]
#make_deal()

buy_bc_sharpe(60)