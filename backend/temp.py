

import bar_chart_race as bcr
import pandas as pd
import matplotlib as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df=pd.read_csv('electric_cars2.csv',index_col=["year"])
bcr.bar_chart_race(df, 'electric_cars2.gif', n_bars=13,
                   fixed_order=['比亚迪e2', '宝马iX3', '宋MAX新能源', '逸动新能源',
                                '广汽丰田iA5','唐新能源','小鹏P7','小鹏G3','菱智M5EV',
                                'Model Y','欧拉好猫','荣威Ei5','凌宝BOX'],
                   steps_per_period=50, period_length=200,
                   fixed_max=True,bar_kwargs={'alpha': .2, 'ec': 'black', 'lw': 3})




