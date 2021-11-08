import pprint as pp
import pandas as pd
import numpy as np
from collections import deque
from datetime import datetime, timedelta
    

class Block:
    def __init__(self, units, purchase_price, period):
        self.units =  units
        self.purchase_price=purchase_price
        self.period =  period
    
    def get_block_value(self):
        return self.units*self.purchase_price
    
    def calc_block_incremental_value(self, current_price):
        return self.units*(current_price - self.purchase_price)

class Fund:
    def __init__(self, symb, type='mutual') -> None:
        self.symb = symb
        self.total_units = 0
        self.type = type
        self.latest_purchase_period=None
        self.latest_purchase_units = None
        self.current_price = None
        self.current_value = self.total_units*self.current_price
        self.blocks = deque()        

    def buy(self, units, purchase_period):
        self.blocks.appendleft(Block(units, self.current_price, purchase_period))
        self.total_units += units
        self.latest_purchase_period = purchase_period
        self.latest_purchase_units = units
        self.update_fund() #update current value
        return self.current_price*units
        
    def sell(self, units=None, sell_value=None):
        if sell_value:
            units = sell_value/self.current_price
        if self.total_units < units:
            print("We dont have enought units. Can't perform the action")
            return 0
        if sell_value is None:
            sell_value = self.current_price*units
        
        while(units>0):
            sell_block = self.blocks.pop()
            if sell_block.units > units:                
                sell_block.units -= units
                self.total_units -= units
                units = 0
                self.blocks.append(sell_block)
                return sell_value
            units -= sell_block.units 
            self.total_units -= sell_block.units
        return sell_value

    def update_fund(self, price=None):
        if price:
            self.current_price = price
        self.current_value = self.total_units*self.current_price
    
    def get_current_value(self):
        return self.current_value
        

class Simulator:
    def __init__(self, fund_history, seed_fund=5000, periods=52, start_period='2020-10-19', max_per_fund=1000) -> None:
        self.fund_history = fund_history
        # print(periods)
        # print("Printing fund history")
        # print(type(fund_history))
        # print(fund_history)
        # print(self.fund_history.head())
        self.portfolio = {}
        self.balance = seed_fund
        self.max_per_fund = max_per_fund
        self.start_period = start_period
        self.periods = periods
        self.periods_dt = self.generate_periods()
        self.curr_period = 1        
        self.current_fund_price_df = pd.DataFrame()
    
    def generate_periods(self):
        print("Generating periods")
        start_dt = datetime.strptime(self.start_period, '%Y-%m-%d')
        periods_list = [start_dt + timedelta(days=7*per) for per in range(self.periods)]
        return periods_list

    def get_recommendations(self, model, period):
        print("Model generating recommendations")        
        unit_rise_df = pd.DataFrame(self.fund_history.loc[:self.periods_dt[period]]
                                    .apply(model, axis=0), # apply mean to each column 
                                    columns=['unit_rise']).sort_values('unit_rise', ascending=False)
        return unit_rise_df
    
    def analyze_recommendations(self, recommendations):
        """[summary]
        TODO: 
        1. Get current portfolio value
        2. Sell some units if any fund is greater than max_per_fund threshold -  1/10 and passed minimum holding period (2months)
        3. Identify 3 stocks to buy and 3 stocks to sell 
        4. Each buy can be at most for 1/20th current wealth
        5. Each sell can be at most 1/20th current wealth (account for selling fee 1%)

        Args:
            recommendations ([type]): [description]
        """
        print("comparing the performance of recommendations with current portfolio")

    def print_desirables(self, period=None):
        print(f"In Period - {period}")
        print(f"current portfolio - ")
        pp.pprint(self.portfolio)
    
    def buy_fund(self, symb, units, purchase_price):
        
        if self.balance < units*purchase_price:
            print("Insufficient Funds")
            return
        
        if symb in self.portfolio.keys():
            symb_fund = self.portfolio[symb]
        else:
            symb_fund = Fund(symb)
            symb_fund.update_fund(purchase_price)
            self.portfolio[symb] = symb_fund

        purchase_value = symb_fund.buy(units, self.curr_period)
        self.balance -= purchase_value
        
    def sell_fund(self, symb, units):
        if symb not in self.portfolio.keys():
            print(f"Selling couldnt be completed as you dont have {symb} in your portfolio")
            return 0
        
        symb_fund = self.portfolio[symb]
        sell_value = symb_fund.sell(units)
        if sell_value == 0:
            print("Sale couldnt happen")
        else:
            self.balance += sell_value

    def update_current_price(self):
        self.current_fund_price_df = pd.DataFrame(self.fund_history.loc[self.periods_dt[self.curr_period]])

    def get_price(self, symb):        
        return self.current_fund_price_df.loc[symb].values[0]
        
    def update_portfolio(self):
        for symb, fund in self.portfolio.items():
            price = self.get_price(symb)
            fund.update_fund(price)

    def simulate(self, models):
        for i, model in enumerate(models):
            print("Running the simulation for model - {i+1}")
            for period in range(4,52,1): 
                self.curr_period = period
                self.update_current_price()           
                self.print_desirables(period)
                self.update_portfolio()
                recommendations = self.get_recommendations(model, period)
                # print(recommendations.head())
                self.analyze_recommendations(recommendations)
                    
                    
if __name__ == "__main__":
    # from models
    
    models = []
    
    params = {
        'periods': 52,
        'fund_history': pd.DataFrame(),
    }
    sim = Simulator(*params)
    sim.simulate(models)

