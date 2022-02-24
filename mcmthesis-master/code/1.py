    ATR = df_gold.loc[day - 10:day, "Increase"].mean() #ATR
    MAE = abs(df_gold.loc[day, "USD"] - df_gold.loc[day - 10:day, "USD"].min())
    MFE = abs(df_gold.loc[day, "USD"] - df_gold.loc[day - 10:day, "USD"].max())
    MAE = MAE/ATR
    MFE = MFE/ATR
    E = MFE/MAE

def buy_bc(day,day_gold):
    real_cash_percent = cash_percent
    if (real_cash_percent > 1):
        real_cash_percent = 0.99
    deal_ratio = []
    for a in range(1,11):
        a = a/10
        proper_temp = proper.copy()
        proper_value_before = proper_temp[0] + \
            proper_temp[1] * proper_temp[3] + proper_temp[2] * df_bc.loc[day, "USD"]
        proper_temp[2] = proper_temp[2] + \
            proper_temp[0] * real_cash_percent * a / df_bc.loc[day, "USD"]
        proper_temp[0] = proper_temp[0] * \
            (1 - (1+bc_ratio) * real_cash_percent * a)
        proper_value_after = proper_temp[0]  + \
            proper_temp[1] * df_gold.loc[day_gold+1, "pred"] + \
                proper_temp[2] * df_bc.loc[day+1, "pred"]
        yield_ = (proper_value_after - proper_value_before)\
            /proper_value_before
        bc_A = proper_temp[2]*df_bc.loc[day, "USD"]/(proper_temp[2]*df_bc.loc[day, "USD"] \
            + proper_temp[1]*proper_temp[3]+proper_temp[0])
        gold_A = proper_temp[1]*proper_temp[3]/(proper_temp[2]*df_bc.loc[day, "USD"] \
            + proper_temp[1]*proper_temp[3]+proper_temp[0])
        risk = math.sqrt(math.pow(bc_A*df_bc.loc[day - 30:day, "USD"].std(),2)\
            +math.pow(gold_A*df_gold.loc[day_gold - 30:day_gold, "USD"].std(),2))
        deal_ratio_temp = yield_ratio*yield_ + sharp_ratio*yield_ / risk
        deal_ratio.append(deal_ratio_temp)
    real_a = (deal_ratio.index(max(deal_ratio))+1)/10
    proper[2] = proper[2] + proper[0] * real_cash_percent * real_a / df_bc.loc[day, "USD"]
    proper[0] = proper[0] * (1 - (1+bc_ratio) * real_cash_percent * real_a)