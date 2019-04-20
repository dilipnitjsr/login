'''
date: 19-03-2019
WEb based login system 
'''
from django.shortcuts import render
from django.http import HttpResponse
from kiteconnect import KiteConnect
import psycopg2

import telegram
def sendBot(message,token,contact):
    if contact==None:
        print("Bot send contact id is None.")
        return
    try:
            bot = telegram.Bot(token)
            bot.send_message(chat_id=contact, text=message)
            print ("Send : "+ contact)
    except Exception as e:
        print(e)
        print ("Error : "+ contact)

def kConnect(user_id,access_token,api_key="qedv3sswnde4220a",):
        kite = KiteConnect(api_key)
        kite.set_access_token(token)
        return kite
    

def opendb():
    database='xyoqlexl'
    user='xyoqlexl'
    password='t9keRD3SZWQTValdWjDleaSlP4ASLR23'
    host='stampy.db.elephantsql.com'
    port=5432        
    conn=False
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    return conn



def sendsql(kiteuser):

        """
        Open new connection
        """
        conn = 0
        try:

            #print("Sending Token to Database ...")
            
            conn = opendb()
            
            cur = conn.cursor()
            cur.execute("UPDATE userKite SET  token = '%s' WHERE id = '%s';" %(kiteuser["access_token"], kiteuser['user_id'] ))
            #cur.execute("INSERT INTO userKite (id, token) VALUES ('%s', '%s');" %(kiteuser['user_id'], kiteuser["access_token"]))
            conn.commit()
            cur.close()
            print("UPDATED : "+kiteuser["access_token"])
            conn.close()
            return True
        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
                print ('Error : %s' % e)
                #print("Connection closed.")
                conn.close()
            print ('Error : %s' % e)
            return False





# Create your views here.
def index(request):
    if request.method == "GET":
    	#print(request.GET["id"])
    	token=request.GET.get("request_token")
    	print("Hello GET :",token)
    	print("Status :",request.GET.get("status"))
    	if request.GET.get("status") == "success":
                try :
                    kite = KiteConnect("qedv3sswnde4220a")
                    kiteuser = kite.generate_session(request_token=token, api_secret="4k89x63xm6b6p9w6x6k1o4d3n0dworh1")
                    sendsql(kiteuser)
                    print("LOGIN : ",kiteuser['user_id'])
                    sendBot(kiteuser['user_name'] +" : LOGIN : "+ kiteuser['user_id'],token=config.token,contact=config.dodfno)
                    return HttpResponse('<html><body><br><br><h1><center> Welcome to DoD Automation!<hr><br><br> '+kiteuser['user_name']+" : Login Success </center><br></h1><h4><a href='https://kite.trade/connect/login?api_key=qedv3sswnde4220a&v=3'> Another Login </a></h4></body></html>")

                except Exception as e:
                    print("Exception : ", str(e.args))
                    return HttpResponse("<html><body><br><br><h1><center><a href='https://kite.trade/connect/login?api_key=qedv3sswnde4220a&v=3'> Please Re-login </a></center></h1></body></html>")
                #return HttpResponse('DoD Automation! login success')
    #return HttpResponse('Welcome to DoD Automation! https://kite.trade/connect/login?api_key=qedv3sswnde4220a&v=3')
    return render(request, "index.html")


def db(request):
	
	return render(request, "index.html")
	#return HttpResponse('Welcome to DoD Automation!')
