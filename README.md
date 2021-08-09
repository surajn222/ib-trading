# ib-trading
ib-trading  

#Fetch historical data and append tick data  

To clone:  
&nbsp;git clone https://github.com/surajn222/ib-trading.git  
&nbsp;Right click on Project Folder > Open in Pycharm

This code does the below in order:
1. Fetch Historical data from ib api and add to df
2. Create new thread to fetch and save tick data   
3. Create new thread to identify if the current time is minute. If it is, append new data to the historical data
4. Create a new thread to tigger the ib-api to execute all of the above  

To run the code:
1. Everytime IB Workstation is started, clear the "reqId" file, and add a "0" to it (representing the first reqId)  
2. Run the main.py  

Big fixes:  
1. Works with IB Workstation, provided connection is established. RedId issue is resolved. IB Gateway is not required  

Todo:  
1. Currently, dummy tick data is being added to the historical dataframe. Work on adding the right data to the dataframe.   
2. requirements.txt contains a lot of unnecessary libraries. To be cleaned.  
3. Tested with only one scrip - EURUSD. Pending testing with multiple scrips.     
