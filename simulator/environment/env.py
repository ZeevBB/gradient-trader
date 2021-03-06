## to do: add side coin information! 

import os
import pandas as pd 
import numpy as np


available_coins = ["bitcoin_cash", "bitcoin", "bitconnect", "dash_price", "ethereum_classic", "ethereum", "iota", "litecoin", "monero", "nem", "neo", "numeraire", "omisego", "qtum", "ripple", "stratis", "waves"]


class Coin:
    def __init__(self, coin_name="ethereum"):
        if coin_name not in available_coins:
            raise Exception("Bad coin name!")
        self.coin_name = coin_name
        self.series = pd.read_csv("%s/cryptocurrencypricehistory/%s_price.csv" % (os.path.dirname(os.path.abspath(__file__)), self.coin_name), parse_dates=["Date"])
        ## reorder so that date increases
        self.series.index = self.series.sort_values(by=["Date"]).index
        self.series = self.series.sort_index()
        self.length = len(self.series.index)
        self.current_index = 0
        
        # stats
        self.rolling_mean = self.series["Close"].rolling(window=20,center=False).mean()
        self.rolling_std = self.series["Close"].rolling(window=20,center=False).std()
        self.upper_band = self.rolling_mean + 2*self.rolling_std
        self.lower_band = self.rolling_mean - 2*self.rolling_std
        

    def advance(self):
        if self.current_index+1 < self.length:
            self.current_index += 1
            data = self.series.loc[self.current_index]
            return data
        else:
            return None
        
    def advance_n_step(self, step):
        if self.current_index+step < self.length:
            self.current_index += step
            data = self.series.loc[self.current_index]
            return data
        else:
            return None 

    def getCurrentValue(self):
        return self.series.loc[self.current_index]["Close"]

    def getCurrentRollingMean(self):
        return self.rolling_mean[self.current_index]
    
    def getCurrentRollingMean(self):
        return self.rolling_mean[self.current_index]
    
    
    def getCurrentBollingerBand(self):
        return self.upper_band[self.current_index], self.lower_band[self.current_index]

