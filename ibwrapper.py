# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 18:49:44 2021

@author: micke
"""
import time
from threading import Thread

# import matplotlib.pyplot as plt
from ibrelay import *
from loggingInitializer import *

logging = initialize_logger("log")

df = pd.DataFrame()
global_bidPrice = 0
dict_size = {}
dict_scrip = {}

class ibwrapper(object):
    def __init__(self, extender, list_scrips):
        self.df_hist = pd.DataFrame()
        global df
        self.local_app = ibrelay(extender)
        self.dict_scrip = {}
        self.reqid = self.get_req_id()
        self.list_scrips = list_scrips



    def get_req_id(self):
        file_reqid = "reqId"
        f = open(file_reqid, "r")
        int_req_id = f.read()

        f = open(file_reqid, "w")
        f.write(str(int(int_req_id)+1))
        f.close()

        return int_req_id


    def fetch_historical_data(self, inst, reqid, duration='1 D', barsize='1 min'):
        logging.info("fetch_historical_data")
        self.local_app.reqHistoricalData(reqId=reqid,
                                         contract=inst,
                                         endDateTime='',
                                         durationStr=duration,
                                         barSizeSetting=barsize,
                                         whatToShow='MIDPOINT',
                                         useRTH=0,
                                         formatDate=1,
                                         keepUpToDate=False,
                                         chartOptions=[])

    global_dict = {1: 0, 2: 0}

    def fetch_tick_data(self, inst, reqid):
        #Create a thread with a target function()
        #threading.Thread(target = inserter(),args = "")

        logging.info("Fetching Bid Ask Tick data ")
        self.local_app.reqTickByTickData(reqId=reqid,
                                         contract=inst,
                                         tickType='BidAsk',
                                         numberOfTicks=100,
                                         ignoreSize=True)

    def make_contract(self, symbol, currency="USD", secType="CASH", exchange="IDEALPRO"):
        self.instrument = Contract()
        self.instrument.symbol = symbol
        self.instrument.currency = currency
        self.instrument.secType = secType
        self.instrument.exchange = exchange
        return self.instrument

    def connect(self, host='127.0.0.1', port=7496, clientId=3):
        logging.info("Trying to connect")
        try:
            self.local_app.connect(host=host, port=port, clientId=clientId)
        except Exception as e:
            logging.info(str(e))
        logging.info("Connected")

    def initialise(self):
        for combo in self.list_scrips:
            for instrument in combo:
                logging.info("Historical data fetch")
                self.cont = self.make_contract(instrument)
                self.reqid = self.get_req_id()
                self.fetch_historical_data(self.cont, self.reqid)
                time.sleep(1)

    def check_if_current_time_is_minute_end(self, time_range):
        # for i in range(time):
        global df
        global dict_scrip
        global dict_size

        while True:
            time_now = epoch_to_datetime_second(int(t.time()))
            # time_of_tick_data = epoch_to_datetime_second(time_now)

            if str(time_now) == "00":
                logging.info("Current time is a minute " + str(time_now) + " - time to alter the data frame")
                logging.info("Time now: " + str(time_now))
                logging.info("Current state of the Historical dataframe: ")
                logging.info(str(df.tail()))
                logging.info("Size of the above dataframe" + str(len(df.index)))
                logging.info("\n")

                logging.info("Adding Global Bid Price=" + str(global_bidPrice))
                dictionary = {'Time': '12:00:00', 'Open': '22222', 'High': '22222', 'Low': '22222', 'Close': '2222'}
                df = df.append(dictionary, ignore_index=True)
                logging.info("Post changes of the Historical dataframe: ")
                logging.info(str(df.tail()))
                logging.info("Size of the above dataframe" + str(len(df.index)))
                logging.info("\n\n\n")
                time.sleep(1)

                #Update Counter
                logging.info("Printing Dict Size in check_if_current_time_is_minute_end ---")
                logging.info(dict_size)

                for k,v in dict_size.items():
                    reqid_temp = k
                    size_of_numpy_array = v

                logging.info("Req Id" + str(reqid_temp))
                logging.info("size_of_numpy_array" + str(size_of_numpy_array))
                #insert new values in record
                #Print Record first
                logging.info("Dict Scrip -----------------------------")

                for k,v in dict_scrip.items():
                    logging.info(type(k))
                    logging.info(type(v))

                #Add a static value next
                logging.info(type(dict_scrip.get(reqid_temp)))

                logging.info(dict_scrip.get(reqid_temp))

                #dicr_scrip = {REQID: NUMPY_ARRAY, REQID2: NUMPY_ARRY2}



                dict_scrip.get(reqid_temp)["Close"][0] = 9999
                dict_scrip.get(reqid_temp)["Close"][1] = 9999
                dict_scrip.get(reqid_temp)["Close"][2] = 9999
                dict_scrip.get(reqid_temp)["Close"][3] = 9999

                logging.info(dict_scrip.get(reqid_temp)["Close"][0:4])


                logging.info("Data Insertion -----------------------------------------------------")
                dict_scrip.get(reqid_temp)["Close"][size_of_numpy_array] = (global_bidPrice + global_askPrice) / 2
                logging.info(dict_scrip.get(reqid_temp)["Close"][size_of_numpy_array])

                logging.info("Printing Numpy Array")
                logging.info(dict_scrip.get(reqid_temp)[1000:1020])



            else:
                logging.info("Current time is not a minute " + str(time_now))
                time.sleep(1)




    def fetch_data(self):
        """
        Fetch historical data and then tick data
        :return:
        """
        for combo in self.list_scrips:
            logging.info("Thread2: For loop execution start")
            for instrument in combo:
                self.cont = self.make_contract(instrument)
                self.reqid = self.get_req_id()
                self.fetch_tick_data(self.cont, self.reqid)
                t.sleep(10)

    def run_app(self):
        self.local_app.run()

    def start(self):
        """
        :param combo_list: scrips to fetch data for
        this function will start two threads, one to check the minute, and the other to fetch tick data
        :return: void
        """
        thread1 = Thread(target=self.check_if_current_time_is_minute_end, args=(30,))
        thread1.start()
        logging.info("thread1 initialized")

        thread2 = Thread(target=self.fetch_data)
        thread2.start()
        logging.info("thread2 initialized")

        thread3 = Thread(target=self.run_app)
        thread3.start()
        logging.info("thread3 initialized")

        thread1.join()
        thread2.join()
        thread3.join()
























def epoch_to_datetime(epoch_seconds):
    return dt.datetime.fromtimestamp(epoch_seconds).strftime('%Y-%m-%d %H:%M:%S')

def epoch_to_datetime_second(epoch_seconds):
    return dt.datetime.fromtimestamp(epoch_seconds).strftime('%S')

time_of_tick_data_prev = 0

class ibrelay(EClient, EWrapper):

    def __init__(self, extender):
        EClient.__init__(self, self)
        global df
        self.tick_df = pd.DataFrame(index=[0],
                                    columns=["datetime", "systemtime", 'reqid', "bidprice", "askprice", "bidSize",
                                             "askSize"])
        self.tck_df = pd.DataFrame()
        self.extender = extender
        self.time_of_tick_data_prev = 0

    def historicalData(self, reqId, bar):
        global df
        global size
        dictionary = {'Time': bar.date, 'Open': bar.open, 'High': bar.high, 'Low': bar.low, 'Close': bar.close}
        df = df.append(dictionary, ignore_index=True)

        #logging.info(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')

    # Display a message once historical data is retreived
    def historicalDataEnd(self, reqId, start, end):
        logging.info('\nHistorical Data Retrieved\n')

        global df
        global size
        global dict_scrip

        logging.info(str(df.head()))

        df["Time"] = pd.to_datetime(df["Time"])
        df['E_Time'] = (((df["Time"] - dt.datetime(1970, 1, 1)).dt.total_seconds()) / 60).astype(int)

        dict_scrip[reqId] = df[["Time", "E_Time", "Close"]].to_records()
        dict_scrip[reqId].resize((self.extender, 1))

        size = len(df.index)
        dict_size[reqId] = size
        logging.info("Dictionary size from historical data end -----------------------------------------")
        logging.info(dict_size)

        #df = pd.DataFrame()

    def tickByTickBidAsk(self, reqId, time, bidPrice, askPrice,
                         bidSize, askSize, tickAttribBidAsk):
        super().tickByTickBidAsk(reqId, time, bidPrice, askPrice, bidSize,
                                 askSize, tickAttribBidAsk)
        global global_bidPrice
        global global_askPrice
        logging.info("BidAsk. ReqId:" + str(reqId) + "Time:"+ str(time) +
              "BidPrice:" + str(bidPrice) + "AskPrice:" + str(askPrice) + "BidSize:" + str(bidSize) +
              "AskSize:" + str(askSize) + "BidPastLow:" + str(tickAttribBidAsk.bidPastLow) + "AskPastHigh:" +
              str(tickAttribBidAsk.askPastHigh))

        global_bidPrice = bidPrice
        global_askPrice = askPrice

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
