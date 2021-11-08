import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression


def calc_unit_change(col):
    """
    """    
    window=4
    fund_history = col.values[-window:]

    sum_col = np.sum(fund_history)
    
    if np.isnan(sum_col):
        # there is a nan in the window
        return -100
    
    x = np.array(range(window)).reshape((-1, 1))
    
    model = LinearRegression()
    model.fit(x, fund_history)
    unit_rise = model.coef_[0] * 100 / model.intercept_
    return unit_rise