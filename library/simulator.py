import pprint as pp
import pandas as pd
from collections import deque

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
        return self.current_price*units
        
    def sell(self, units):
        if self.total_units < units:
            print("We dont have enought units. Can't perform the action")
            return 0
        
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

    def update_fund(self, price):
        self.current_price = price
        self.current_value = self.total_units*self.current_price
    
    def get_current_value(self):
        return self.current_value
        

class Simulator:
    def __init__(self, fund_history, seed_fund=5000, periods=52) -> None:
        self.fund_history = fund_history
        self.portfolio = {}
        self.balance = seed_fund
        self.max_per_fund = 1000
        self.periods = periods
        self.curr_period = 1
            
    def get_recommendations(self, model, period):
        print("Model generating recommendations")
        return True
    
    def analyze_recommendations(self, recommendations):
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

    def get_price(self, symb, period=None):
        if period is None:
            period = self.curr_period
        pass

    def update_portfolio(self):
        for symb, fund in self.portfolio.items():
            price = self.get_price(symb)
            fund.update_fund(price)


    def simulate(self, models):
        for i, model in enumerate(models):
            print("Running the simulation for model - {i+1}")
            for period in range(1,self.periods,1): 
                self.curr_period = period           
                self.print_desirables(period)
                self.update_portfolio(period)
                recommendations = self.get_recommendations(model, period)
                self.analyze_recommendations(recommendations)
                
    

if __name__ == "__main__":
    
    
    models = []
    
    params = {
        'periods': 5,
        'fund_history': pd.DataFrame(),
    }
    sim = Simulator(*params)
    sim.simulate(models)

