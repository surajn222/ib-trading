# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 18:55:58 2021

@author: surajn222
"""
import sys
import time
from threading import Timer

from ibwrapper import ibwrapper
from loggingInitializer import *

logging = initialize_logger("log")

def main():
    extender = 750
    # combo_list = [["RELIANCE", "ADANIENT"]]
    #list_scrips = [["EUR", "CHF"]]
    list_scrips = [["EUR"]]

    #create an object
    obj_ibwrapper = ibwrapper(extender, list_scrips)

    # Establish conenctions
    obj_ibwrapper.connect()

    # Initialize
    obj_ibwrapper.initialise()

    # Sleep - wait for the historical data to be fetched

    print("Waiting for historical data")
    time.sleep(5)

    # Compute indicators
    obj_ibwrapper.start()


    # Algo Start
    #Timer(120, obj_ibwrapper.local_app.disconnect).start()
    print("Starting")
    sys.exit()
    obj_ibwrapper.local_app.run()




try:
    main()
except Exception as e:
    print(str(e))
