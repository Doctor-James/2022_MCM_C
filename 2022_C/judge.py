# import pandas as pd
# import numpy as np
# import math
# import matplotlib.pyplot as plt
# import random
#
# data = pd.read_csv('data2.csv')
# df = pd.DataFrame(data)
#
# gain = []
# gain.append((df.loc[99,'Value'] - 1000)/1000)
# gain.append((df.loc[213,'Value'] - df.loc[99,'Value'])/df.loc[99,'Value'])
# gain.append((df.loc[327,'Value'] - df.loc[213,'Value'])/df.loc[213,'Value'])
# gain.append((df.loc[442,'Value'] - df.loc[327,'Value'])/df.loc[327,'Value'])
# gain.append((df.loc[555,'Value'] - df.loc[442,'Value'])/df.loc[442,'Value'])
# print('gain: ',gain)
#
# sharpe = []
# sharpe.append(gain[0]/math.sqrt(df.loc[:99,'Value'].std())*20)
# sharpe.append(gain[1]/math.sqrt(df.loc[99:213,'Value'].std())*30)
# sharpe.append(gain[2]/math.sqrt(df.loc[213:327,'Value'].std())*70)
# sharpe.append(gain[3]/math.sqrt(df.loc[327:442,'Value'].std())*100)
# sharpe.append(gain[4]/math.sqrt(df.loc[442:555,'Value'].std())*80)
# print('sharpe: ',sharpe)
#
#
#
# drawdown = []
# for i in range(int(len(df)/10)):
#     index = i*10
#     drawdown.append((df.loc[index,'Value'] - df.loc[index+10,'Value'])/df.loc[index,'Value'])
# print('drawdown10: ',min(drawdown))
#
# drawdown30 = []
# for i in range(int(len(df)/30)):
#     index = i*30
#     drawdown30.append((df.loc[index,'Value'] - df.loc[index+30,'Value'])/df.loc[index,'Value'])
# print('drawdown30: ',min(drawdown30))


import pandas as pd

suffix = 'csv'
path = r'ratio_change_new/{}.{}'
bc_df = pd.read_csv(path.format('bc_change', suffix))
gold_df = pd.read_csv(path.format('gold_change', suffix))
bc_gold_df = pd.read_csv(path.format('gold_bc_change', suffix))

print(bc_df.columns)
print(gold_df.columns)
print(bc_gold_df.columns)

STRATEGY_NUM = 5

def make_dataset(df):
    data_list = [[] for i in range(len(df)*STRATEGY_NUM)]
    for i in range(len(df)):
        line = df.iloc[i, 1:]
        for j in range(STRATEGY_NUM):
            data = line[j]
            data_list[i*STRATEGY_NUM+j] = [df.columns[j+1], line[-1], data]
    return data_list

bc_list = make_dataset(bc_df)
gold_list = make_dataset(gold_df)
bc_gold_list = make_dataset(bc_gold_df)

# print(bc_list, gold_list, bc_gold_list)
# bc_list.extend(gold_list)
# bc_list.extend(bc_gold_list)
bc_data = pd.DataFrame(bc_list)
# print(bc_data)
bc_data.columns = ["strategy", "year", "profit"]

import seaborn as sns
import matplotlib.pyplot as plt

print(len(bc_data))
data = bc_data[:]

sns.set_theme(style="darkgrid")

# Plot each year's time series in its own facet
g = sns.relplot(
    data=data,
    x="year", y="profit",
    col="strategy",
    hue="strategy",
    kind="line", palette="bright", linewidth=2, zorder=5,
    col_wrap=1, height=2, aspect=3,
)

# Iterate over each subplot to customize further
for year, ax in g.axes_dict.items():

    # Add the title as an annotation within the plot
    ax.text(.8, .85, year, transform=ax.transAxes, fontweight="bold")

    # Plot every year's time series in the background
    sns.lineplot(
        data=data,
        x="year", y="profit", units="strategy",
        estimator=None, color=".7", linewidth=1, ax=ax,
    )

# Reduce the frequency of the x axis ticks
ax.set_xticks([])
# Tweak the supporting aspects of the plot
g.set_titles("")
g.set_axis_labels("Date", "Dollar")
g.tight_layout()
# plt.xlabel()
plt.savefig('./bc.png')
plt.show()