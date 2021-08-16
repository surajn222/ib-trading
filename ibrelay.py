import os
import sys
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Timer
import pandas as pd
import time as t
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

def epoch_to_datetime(epoch_seconds):
    return dt.datetime.fromtimestamp(epoch_seconds).strftime('%Y-%m-%d %H:%M:%S')

def epoch_to_datetime_second(epoch_seconds):
    return dt.datetime.fromtimestamp(epoch_seconds).strftime('%S')

time_of_tick_data_prev = 0



class ibrelay(EClient, EWrapper):

    def __init__(self, extender, df):
        EClient.__init__(self, self)
        self.df = df
        self.tick_df = pd.DataFrame(index=[0],
                                    columns=["datetime", "systemtime", 'reqid', "bidprice", "askprice", "bidSize",
                                             "askSize"])
        self.tck_df = pd.DataFrame()
        self.dict_scrip = {}
        self.extender = extender
        self.time_of_tick_data_prev = 0

    def historicalData(self, reqId, bar):
        dictionary = {'Time': bar.date, 'Open': bar.open, 'High': bar.high, 'Low': bar.low, 'Close': bar.close}
        self.df = self.df.append(dictionary, ignore_index=True)
        print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')

    # Display a message once historical data is retreived
    def historicalDataEnd(self, reqId, start, end):
        print('\nHistorical Data Retrieved\n')
        print(self.df.head())

        self.df["Time"] = pd.to_datetime(self.df["Time"])
        self.df['E_Time'] = (((self.df["Time"] - dt.datetime(1970, 1, 1)).dt.total_seconds()) / 60).astype(int)
        self.dict_scrip[reqId] = self.df[["Time", "E_Time", "Close"]].to_records()
        self.dict_scrip[reqId].resize((self.extender, 1))
        self.df = pd.DataFrame()

    def tickByTickBidAsk(self, reqId, time, bidPrice, askPrice,
                         bidSize, askSize, tickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
                                 askSize, tickAttribBidAsk)
        print("BidAsk. ReqId:", reqId, "Time:", time,
              "BidPrice:", bidPrice, "AskPrice:", askPrice, "BidSize:", bidSize,
              "AskSize:", askSize, "BidPastLow:", tickAttribBidAsk.bidPastLow, "AskPastHigh:",
              tickAttribBidAsk.askPastHigh)

        print(bidPrice)

        #Based on the value of the data in the global_dict,
        #global_dict[reqId] = bidPrice


        # if (self.dict_scrip[reqId - 2]["Time"].iloc[-1] != self.current_time):
        #     self.dict_scrip[reqId - 2] = self.dict_scrip[reqId - 2].append(
        #         {'E_Time': self.current_time, 'Close': round((bidPrice + askPrice) / 2, 5)}, ignore_index=True)

        '''
        self.tick_df.datetime =  datetime.datetime.fromtimestamp(time).strftime("%Y/%m/%d %H:%M:%S.%f")
        self.tick_df.systemtime =  datetime.datetime.now()
        self.tick_df.reqid = reqId
        self.tick_df['bidprice'] = bidPrice
        self.tick_df['askprice'] = askPrice
        self.tick_df['bidSize'] = bidSize
        self.tick_df['askSize'] = askSize
        self.tck_df = self.tck_df.append(self.tick_df)
        '''
