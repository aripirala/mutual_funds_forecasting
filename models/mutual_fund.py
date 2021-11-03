# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 22:42:31 2021

@author: c62004
"""
import pandas as pd


class mutual_fund(object):

    def __init__(self, fund: str, day: int, nav: float,
                 invest_amt: float, recommendation: str):
        self.fund_name = fund
        self.day_bought = day
        self.nav = nav
        self.amount = invest_amt
        self.recommendation = recommendation
        self.units = invest_amt / nav
        self.interval = 0
        self.status = True

        self.sell_nav = 0
        self.profit = 0
        self.holding_days = 0
        self.abs_percent = 0
        self.annual_percent = 0

    # ----------------------------------------------------

    def sell_fund(self, nav: float, day: int):

        if (day - self.day_bought) > self.interval:
            self.sell_nav = nav
            self.holding_days = day - self.day_bought
            self.profit = (self.sell_nav - self.nav) * self.units
            self.abs_percent = self.profit * 100 / self.amount
            self.annual_percent = (365 * self.abs_percent) / self.holding_days
            self.status = False
            return True
        return False
    # ----------------------------------------------------

    def set_interval(self, interval: int):
        if interval > 0:
            self.interval = interval
    # ----------------------------------------------------

    def calc_value(self, cur_nav: float, day: int):

        self.holding_days = day - self.day_bought
        self.profit = (cur_nav - self.nav) * self.units
        self.abs_percent = self.profit * 100 / self.amount
        self.annual_percent = (365 * self.abs_percent) / self.holding_days
        return
    # ----------------------------------------------------

    def get_sales_profit(self) -> pd.DataFrame:

        frame = {'Fund': self.fund_name, 'NAV_bought': self.nav,
                 'NAV_sold': self.sell_nav, 'Hold_days': self.holding_days,
                 'PL': self.profit, 'Percent_abs': self.abs_percent,
                 'Percent_annual': self.annual_percent,
                 'Recommendation': self.recommendation, 'Status': self.status}
        return pd.DataFrame(frame, index=[0])
    # ----------------------------------------------------

    def get_value(self, cur_nav: float, cur_day: int) -> pd.DataFrame:

        self.calc_value(cur_nav=cur_nav, day=cur_day)
        frame = {'Fund': self.fund_name, 'NAV_bought': self.nav,
                 'NAV_sold': cur_nav, 'Hold_days': self.holding_days,
                 'PL': self.profit, 'Percent_abs': self.abs_percent,
                 'Percent_annual': self.annual_percent,
                 'Recommendation': self.recommendation, 'Status': self.status}
        return pd.DataFrame(frame, index=[0])
    # ----------------------------------------------------
