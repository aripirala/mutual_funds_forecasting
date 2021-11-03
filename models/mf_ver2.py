# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:30:18 2021

@author: c62004
"""


import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import mutual_fund as mf


def calc_unit_change(in_df: pd.DataFrame, strt_col: int, n_weeks: int) -> pd.DataFrame:
    fund_name = []
    r_sq = []
    intercepts = []
    slopes = []
    unit_increase = []
    cur_nav = []
    m, n = in_df.shape

    for row in range(m):
        p1 = in_df.iloc[row, (strt_col - n_weeks):strt_col]
        # L = len(p1)
        x = np.array(range(n_weeks)).reshape((-1, 1))
        y = np.array(p1.astype(np.float))
        # plt.scatter(range(18), p1.astype(np.float), c='black')
        #
        model = LinearRegression()
        model.fit(x, y)
        rsquare = model.score(x, y)
        #
        fund_name.append(in_df.iloc[row, 0])
        cur_nav.append(p1[n_weeks - 1])
        r_sq.append(rsquare)
        intercepts.append(model.intercept_)
        slopes.append(model.coef_[0])
        value = model.coef_[0] * 100 / model.intercept_
        unit_increase.append(value)
        #
    frame = {'Fund': fund_name, 'NAV': cur_nav, 'R_Squared': r_sq, 'Intercept': intercepts,
             'Slope': slopes, 'Unit_Rise': unit_increase}
    out_df = pd.DataFrame(frame)
    out_df.sort_values(by=['Unit_Rise'], ascending=False, inplace=True)
    return out_df
    # ------------------------------------------------------------------------


def recommend_position(ur1: pd.DataFrame, ur2: pd.DataFrame, ind_fund: str):
    # ur1, ur2 : data frames with unit rise calculation
    # ur1 should be from prior time compared to ur2
    # first calculate index positions
    ind1 = ur1[ur1['Fund'] == ind_fund]
    ind1_change = ind1['Unit_Rise'].iloc[0]

    ind2 = ur2[ur2['Fund'] == ind_fund]
    ind2_change = ind2['Unit_Rise'].iloc[0]

    if ind1_change > 0 and ind2_change > 0:
        if ind2_change > ind1_change:
            print('Index moving from lower rate of increase to higher rate of increase')
        else:
            print('Index moving from higher rate of increase to lower rate of increase')
    # end of if
    if ind1_change > 0 and ind2_change < 0:
        print('Index moving from positive to negative')

    if ind1_change < 0 and ind2_change > 0:
        print('Index moving from negative to positive')

    if ind1_change < 0 and ind2_change < 0:
        if ind2_change > ind1_change:
            print('Index in negative territory, but improving')
        else:
            print('Index worsening: Check debt markets !!')

    funds = []
    strategy = []
    nav = []
    unit_rise = []

    for i, item in enumerate(ur1['Fund']):
        fund_change_1 = ur1['Unit_Rise'].iloc[i]
        fund_ur2 = ur2[ur2['Fund'] == item]
        fund_change_2 = fund_ur2['Unit_Rise'].iloc[0]
        funds.append(item)
        unit_rise.append(fund_change_2)
        nav.append(fund_ur2['NAV'].iloc[0])

        if ind1_change > 0 and ind2_change > 0:

            if ind2_change > ind1_change:
                # Bull market, increasing momentum
                if fund_change_1 > ind1_change and fund_change_2 > ind2_change:
                    if fund_change_2 > fund_change_1:
                        strategy.append('Strong_BUY')
                        continue
                    else:
                        strategy.append('BUY')
                        continue
                #
                if fund_change_1 < ind1_change and fund_change_2 > ind2_change:
                    # Increasing momentum / cross over
                    strategy.append('BUY')
                    continue
                else:
                    strategy.append('Undecided')
                    continue
            else:
                # index is decreasing
                index_drop = ind1_change - ind2_change
                fund_drop = fund_change_1 - fund_change_2
                if fund_change_1 > ind1_change and fund_change_2 > ind2_change:
                    if fund_change_2 > fund_change_1:
                        strategy.append('Strong_BUY')
                        continue
                    if fund_drop < index_drop:
                        strategy.append('BUY')
                        continue
                    strategy.append('Undecided')
                    continue
                #
                if fund_change_1 < ind1_change and fund_change_2 > ind2_change:
                    strategy.append('BUY')
                    continue
                if fund_change_1 > ind1_change and fund_change_2 < ind2_change:
                    strategy.append('SELL')
                    continue
                strategy.append('Undecided')
                continue

        if ind1_change > 0 and ind2_change < 0:
            # Entering bear territory
            if fund_change_1 > ind1_change and fund_change_2 > fund_change_1:
                strategy.append('BUY')
                continue
            if fund_change_1 > ind1_change and fund_change_2 > 0:
                strategy.append('HOLD')
                continue
            if fund_change_2 < ind2_change:
                strategy.append('SELL')
                continue
            strategy.append('Undecided')
            continue

        if ind1_change < 0 and ind2_change > 0:
            if fund_change_1 > 0 and fund_change_2 > ind2_change:
                strategy.append('BUY')
                continue
            if fund_change_2 < fund_change_1:
                strategy.append('SELL')
                continue
            strategy.append('Undecided')
            continue

        if ind1_change < 0 and ind2_change < 0:
            if ind2_change > ind1_change:
                if fund_change_1 > 0 and fund_change_2 > fund_change_1:
                    strategy.append('Strong_BUY')
                    continue
                if fund_change_1 < ind1_change and fund_change_2 > ind2_change:
                    strategy.append('Strong_BUY')
                    continue
                if fund_change_1 > ind1_change and fund_change_2 > ind2_change:
                    strategy.append('BUY')
                    continue
                strategy.append('SELL')
                continue
            if ind2_change < ind1_change:
                # Bear territory
                if fund_change_1 > 0 and fund_change_2 > fund_change_1:
                    strategy.append('Strong_BUY')
                    continue
                if fund_change_1 < ind1_change and fund_change_2 > 0:
                    strategy.append('Strong_BUY')
                    continue
                strategy.append('SELL')
                continue
        # end of if
        strategy.append('Undecided')
    # end of for
    frame = {'Fund': funds, 'Decision': strategy, 'NAV': nav, 'Unit_Rise': unit_rise}
    out_df = pd.DataFrame(frame)
    return out_df
    # ------------------------------------------------------------------------


def add_funds(funds_df: pd.DataFrame, day: int, funds_dict: dict) -> dict:

    for i, fund in enumerate(funds_df['Fund']):

        if fund in funds_dict.keys():
            continue

        if funds_df['Decision'].iloc[i] == 'BUY':
            mf_obj = mf.mutual_fund(fund=fund, day=day, nav=funds_df['NAV'].iloc[i],
                                    invest_amt=1000, recommendation='BUY')
            mf_obj.set_interval(interval=70)
            funds_dict[fund] = mf_obj
            continue

        if funds_df['Decision'].iloc[i] == 'Strong_BUY':
            mf_obj = mf.mutual_fund(fund=fund, day=day, nav=funds_df['NAV'].iloc[i],
                                    invest_amt=1000, recommendation='Strong_BUY')
            mf_obj.set_interval(interval=70)
            funds_dict[fund] = mf_obj
            continue
    # end of for
    return funds_dict


def sell_funds(funds_df: pd.DataFrame, day: int, funds_dict: dict) -> dict:

    for i, fund in enumerate(funds_df['Fund']):
        if fund in funds_dict.keys():
            fund_obj = funds_dict[fund]
            sell_status = fund_obj.sell_fund(nav=funds_df['NAV'].iloc[i], day=day)
            funds_dict[fund] = fund_obj
    # end of for
    return funds_dict


index = 'NIFTY'
df = pd.read_excel('MutualFund_Movement.xlsx', sheet_name=0)
m, n = df.shape
test_strt = 30
interval = 5
iterations = n - test_strt
unit_change_1 = calc_unit_change(in_df=df, strt_col=test_strt, n_weeks=interval)
count = 0
elapsed_days = 0
fund_transactions = {}

for i in range(iterations):
    test_strt += 1
    unit_change_2 = calc_unit_change(in_df=df, strt_col=test_strt, n_weeks=interval)
    test_out = recommend_position(ur1=unit_change_1, ur2=unit_change_2, ind_fund=index)
    buy_funds_1 = test_out[test_out['Decision'] == 'BUY']
    fund_transactions = add_funds(funds_df=buy_funds_1, day=elapsed_days,
                                  funds_dict=fund_transactions)

    buy_funds_2 = test_out[test_out['Decision'] == 'Strong_BUY']
    fund_transactions = add_funds(funds_df=buy_funds_2, day=elapsed_days,
                                  funds_dict=fund_transactions)

    sell_funds_1 = test_out[test_out['Decision'] == 'SELL']
    fund_transactions = sell_funds(funds_df=sell_funds_1, day=elapsed_days,
                                   funds_dict=fund_transactions)
    index_data = test_out[test_out['Fund'] == index]
    elapsed_days += 7
#
count = 0
for key in fund_transactions.keys():
    fund_obj = fund_transactions[key]
    df_tmp = df[df['Fund'] == fund_obj.fund_name]
    if not fund_obj.status:
        out_df = fund_obj.get_sales_profit()
    else:
        out_df = fund_obj.get_value(cur_nav=df_tmp.iloc[0, -1], cur_day=elapsed_days)

    if count == 0:
        final_df = out_df
    else:
        final_df = pd.concat([final_df, out_df], axis=0, ignore_index=True)
    count += 1
#
final_df.to_excel('the_results.xlsx')
