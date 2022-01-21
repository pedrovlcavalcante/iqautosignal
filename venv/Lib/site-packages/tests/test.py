from ejtraderIQ import IQOption
import time
import numpy as np
import pandas as pd
print("login...")

api=IQOption("emerson@ejtrader.com","Olatikas@123","DEMO")

symbol="EURUSD"
timeframe="M1"

 
while True:
    data = api.history(symbol,timeframe,1)
    print(data)
# api.start_price_stream(symbol,timeframe)   
# payout = api.payout(symbol)
# print(payout)
# id =  api.sell(100,symbol,timeframe) 




# win=api.checkwin(id)
# print(win)

# while True:
#    data = api.realtime_data()
#    print(data)
   
        
        
# api.stop_price_stream(symbol,timeframe)
        
        


    
# from iqoptionapi.stable_api import IQ_Option
# import time
# import logging
# #logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
# I_want_money=IQ_Option("emerson@ejtrader.com","Olatikas@123")
# I_want_money.connect()#connect to iqoption
# ACTIVES="EURUSD"
# duration=1#minute 1 or 5
# I_want_money.subscribe_strike_list(ACTIVES,duration)
# while True:
#     data=I_want_money.get_digital_current_profit(ACTIVES, duration)
#     if data > 81: print("maior")#from first print it may be get false,just wait a second you can get the profit
#     time.sleep(1)
# I_want_money.unsubscribe_strike_list(ACTIVES,duration)

