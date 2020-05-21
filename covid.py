from dash import Dash
#from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import flask
from werkzeug.serving import run_simple
import dash_html_components as html
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import dash_table
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc




Dates=[]
Cases=[]
df5=pd.DataFrame()

url="https://www.mohfw.gov.in/"
response=requests.get(url)




def scrape_1():

    url="https://www.mohfw.gov.in/"
    response=requests.get(url)
    soup=BeautifulSoup(response.content,"html.parser")
    tables=soup.find_all("table")
    table0=tables[0]
    state=[]
    total_confirmed_cases=[]
    cured_discharged_migrated=[]
    deaths=[]

    rows=table0.find_all("tr")
    rows
    for row in rows:
        col=row.find_all("td")
        try:
            
            state.append(col[1].text.strip())
            total_confirmed_cases.append(int(col[2].text.strip()))
            cured_discharged_migrated.append(int(col[3].text.strip()))
            deaths.append((col[4].text.strip()))
        except:
            print("")

    

    df=pd.DataFrame(list(zip(state,total_confirmed_cases,cured_discharged_migrated,deaths)),columns=["State",
"Total_confirmed_cases",
"Cured_Discharged_Migrated",
"Deaths"])
    df=df.iloc[0:33]
    df.replace('0#','0',regex=True,inplace=True)
    df["Deaths"] = df["Deaths"].astype(str).astype(int)
    #New column for active cases in the States 
    df["Active_cases"]=df["Total_confirmed_cases"]-df["Cured_Discharged_Migrated"]-df["Deaths"]
    
    df2=df.sort_values("Total_confirmed_cases",ascending=False)
    return df2

def scrape_2():
    response1=requests.get("https://api.covid19api.com/dayone/country/india/status/confirmed/live").json()

    for data in response1:
        Dates.append(data['Date'][0:10])
        Cases.append(data['Cases'])
        

    df5=pd.DataFrame(Dates,columns=["Date"])
    df5["Cases"]=pd.DataFrame(Cases)
    return df5

def scrape_3():

    response3=requests.get("https://api.rootnet.in/covid19-in/stats/testing/history").json()


    Dates=[]
    Tests=[]
    df6=pd.DataFrame()
    for data1 in response3['data']:
        Dates.append(data1['day'])
        Tests.append(data1['totalSamplesTested'])
        #print(Dates,Cases)

    df6=pd.DataFrame(Dates,columns=["Date"])
    df6["Tests"]=pd.DataFrame(Tests)
    df6.dropna(axis=0,inplace=True)
    return df6

def Active_sort():
    df=scrape_1()
    df2=df.sort_values("Active_cases",ascending=False)
    return df2
        
