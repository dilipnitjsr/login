# -*- coding: utf-8 -*-
"""
Created on 05-08-2018

@author: Dilip Kumar
"""
print("............Config............")
#import threading
import dodlib
#from dodlib import state
#import psycopg2
import sqlalchemy as sq
import datetime

engine = sq.create_engine("postgres://totzyadr:clJeh9EzbYi72MehEv5FXOSjQqkoAAsI@elmer.db.elephantsql.com:5432/totzyadr")

token ="471420613:AAEAePKy3Zz1cLw9gXHLCZupuvfS3xtzJq8" #BOT Dodtradebot Mr Dod Automation
#bot_token='471420613:AAEAePKy3Zz1cLw9gXHLCZupuvfS3xtzJq8' #BOT D002bot FnO
#botlog=None
dodfno =  '529908821' # DoD DoDFnO private
contact = -1001383361020 # channel : DoD FnO Automation
#fno ='-1001189501567' #  None  group
#https://api.telegram.org/bot471420613:AAEAePKy3Zz1cLw9gXHLCZupuvfS3xtzJq8/getMe
#https://api.telegram.org/bot557409809:AAHPToVJD9IxVnVVbGIwfenNchoC7XR5P2Q/getUpdates



state={}
reg={}
#margin={"NIFTY 50":100000,"NIFTY BANK":70000,"ICICIBANK":200000}
#target = {"4Min":0.0002*4,"5Min":0.0002*5,"6Min":0.0002*6,"10Min":0.0002*10,"15minute":0.00015*15,"15Min":0.00015*15,"30Min":0.00015*30,
#			"1H":0.00015*60,"hour":0.00015*60,"2H":0.00015*120,"4H":0.00015*240}


#print(state)
date=datetime.datetime.now()
wait=5
waitIn=1

#atrN=7
#atrFact=3.5
#df=None
#dft={}
#master={}

#strongtrade={}

#samplingList = ['5min', '15min', '30min',  '1H', '2H', '4H','1D', '2D']

#interval="hour"

#trade=["BUY","SELL","AUTO"]

#timeFrame=["minute","3minute","5minute","10minute","15minute","hour"]


#debug = False
debug = True

#SLD= 0.0
#SLU=float('inf')

#TRENDSL=None
#TREND=None
#position=False


#Lock = threading.Lock()
#################
#m2mShow=False
#m2mInterval=30 #minutes

#dodlib.sendBot("hello",token,contact)



api_key = "qedv3sswnde4220a"


nisha={'name':"Nisha",'user_id' : 'LR8172' , 'api_key' : api_key,
                    'capital':20000,'risk':None,"DayTarget":None,
                    'active':True,"day_range":"*",
					'kite':dodlib.kiteSqlConnect("LR8172",api_key),
                    }

nisha['kite']=dodlib.kiteSqlConnect(nisha['user_id'],nisha['api_key'])

dilip={'name':"Dilip Kumar",'user_id' : 'DD0131' , 'api_key' : api_key,
                    'capital':100000,'risk':None,"DayTarget":None,
                    'active':True,
                    "kite":dodlib.kiteSqlConnect("DD0131",api_key),
                    "day_range":"*",
                    }

siva={'name':"Siva",'user_id' : 'SS0960' , 'api_key' : api_key,
                    'capital':1000000,'risk':None,"DayTarget":None,"day_range":"*",'active':True,
                    "kite":dodlib.kiteSqlConnect("SS0960",api_key),
                    }

vathana={'name':'Vathana','user_id' : 'XK1191' , 'api_key' : api_key,
                    'capital':190000,'risk':None,"DayTarget":None,
                    'active':True,"day_range":"*",
					'kite':dodlib.kiteSqlConnect("XK1191",api_key),
                    }

user_name="KSL Master"

kitehist=dilip['kite']
print("config ....End:",user_name)
