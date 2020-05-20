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
from covid import scrape_1,scrape_2,scrape_3,Active_sort


external_stylesheets = [dbc.themes.SKETCHY]

colors={
    'area':'#c3cfc2'
}

df2=scrape_1()
df5=scrape_2()
df6=scrape_3()



fig6 = px.bar(df6, x="Date", y="Tests", title='<b>Number of Tests Performed Since March</b>')


fig = go.Figure([go.Bar(name="Total confirmed Cases",
                        x=df2['State'][0:14],
                        y=df2['Total_confirmed_cases'],
                        marker_color='indianred'),
                go.Bar(name="Cured/Discharged",
                        x=df2['State'][0:14], 
                        y=df2["Cured_Discharged_Migrated"],
                    marker_color='lightsalmon'),
                go.Bar(name="Deaths",
                        x=df2['State'][0:14], 
                        y=df2["Deaths"],
                    marker_color='red')
                ])

fig.update_layout(barmode='group')


fig2 = px.line(df5, x="Date", y="Cases", title='<b>Number of Cases Since February</b>')




def generate_table(dataframe, max_rows=30):
    return html.Table(className="responsive-table",
                      children=[
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    
    ])



card_content1 = [
    dbc.CardBody(
        [
            html.H5("Total Cases", className="card-title"),
            
                df2["Total_confirmed_cases"].sum()

        ]
    ),
]

card_content2 = [
   
    dbc.CardBody(
        [
            html.H5("Total Recovered", className="card-title"),
            
                df2["Cured_Discharged_Migrated"].sum()

        ]
    ),
]


card_content3 = [
   
    dbc.CardBody(
        [
            html.H5("Total Deaths", className="card-title"),
            
                df2["Deaths"].sum()

        ]
    ),
]

# card_content4 = [
   
#     dbc.CardBody(
#         [
#             html.H5("Green Zone States", className="card-title"),
            
#                 html.Link(rel='stylesheet',href="/static/dash-dashtable.css"),
#     dash_table.DataTable(id='table1',
#                         columns=[{"id": i,"States" : i} for i in df4.columns],
#                         data=df4.to_dict('records'),
#                         css=[{'selector': '.dash-cell div.dash-cell-value', 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
#               style_table={'maxWidth': '230px','backgroundColor':'black','tableAlign':'center'},
#         selected_rows=[0],
#         style_cell = {"fontFamily": "Arial", "size": 10, 'textAlign': 'center','fill_color':'lavender'})
#             #dcc.Graph(figure=fig5)

#         ]
#     ),
# ]







server = flask.Flask(__name__)
dash_app1 = Dash(__name__, server = server, url_base_pathname='/dashboard/',external_stylesheets=external_stylesheets )
dash_app2 = Dash(__name__, server = server, url_base_pathname='/reports/')
dash_app1.layout = html.Div([
        html.H1(children='Statewise Distribution of Covid-19 in India',
           style={
               'textAlign':'center',
               'color':'black',
               'font':'bold',
               'fontsize':'10px',
               'backgroundColor':colors['area']

           }),

           html.Br(style={'backgroundColor':colors['area']}),
           html.Br(),
    html.Div([
    dbc.Row(
    [
        dbc.Col(dbc.Card(card_content1,  outline=True,style={'backgroundColor':"lightblue"})),
        dbc.Col(dbc.Card(card_content2, color="blue", outline=True,style={'backgroundColor':"lightgreen"})),
        dbc.Col(dbc.Card(card_content3, color="info", outline=True,style={'backgroundColor':"lightsalmon"})),
    ],className="mb-4", style={
               'textAlign':'center',
               'color':'grey',
                'font' : 'bold',
                'backgroundColor':colors['area']
           }),
    ]),
    #   html.Div(
    #      generate_table(df2)),

    html.Div([
        html.P("Real time Updates in the States")
    ],style={
               'textAlign':'center',
               'color':'black',
                'font' : 'bold',
                'backgroundColor':colors['area'],
                'font-size':'30px'
                }
                ),
    
    html.Div([
    dcc.Graph(figure=fig)
    
    ],style={"border":"2px black solid",
    'backgroundColor':colors['area']}),

   


    html.Div([
    html.Div([
    dcc.Graph(figure=fig2)
    
    ],style={"border":"2px black solid",'margin':'15px',
    'backgroundColor':colors['area']},className="six columns"),

    html.Div([
    dcc.Graph(figure=fig6)
    
    ],style={"border":"2px black solid",'margin':'15px',
    'backgroundColor':colors['area']},className="six columns"),

    ],className="row",),


     html.Div([
        dcc.Graph(id='Active Cases',
                 figure={
                     'data': [
                         go.Bar(x=df2['State'][0:29],
                               y=df2["Active_cases"][0:29],
                               marker_color='lightsalmon')
                     ],
                     'layout': go.Layout(title="<b>Active Cases in the States</b>",autosize=True)
                 })
        
    ],style={
        'backgroundColor':colors['area'],"border":"2px black solid"
        
    }),

    #  html.Div([
    # dbc.Row(
    # [
    #     dbc.Col(dbc.Card(card_content4, outline=False,style={'height':'30vh','width':'40vh','backgroundColor':"lightblue"}))
        
    # ],className="mb-4", style={
    #            'textAlign':'center',
    #            'color':'black',
    #             'font' : 'bold',
    #             'backgroundColor':'lavender'
    #        }),
    # ]),




    
    html.Div([
    html.Div([
        dcc.Graph(id='g1',
                 figure={
                     'data': [
                         go.Pie(values=df2['Total_confirmed_cases'][0:7],
                               labels=df2['State'][0:7])
                     ],
                     'layout': go.Layout(title="<b>Total Cases</b>",autosize=True)
                 }),
    ],className="six columns", style={
        'backgroundColor':colors['area'],'margin':'15px',"border":"2px black solid"
    }),
        
        html.Div([
        
         dcc.Graph(id='g2',
                 figure={
                     'data': [
                         go.Pie(values=df2["Deaths"][0:7],
                               labels=df2['State'][0:7])
                     ],
                     'layout': go.Layout(title="<b>Deaths</b>",autosize=True)
                 }),
        ],className="six columns",style={
        'backgroundColor':colors['area'],'margin':'15px','border':'2px',"border":"2px black solid",
    }),
    ],className="row"),

    html.Br(),
    html.Br(),

     html.Div([
        ]),
 

    
   
   
    
    
    

],style={
        'backgroundColor':colors['area']
    })

dash_app2.layout = html.Div([html.H1('Hi there, I am app2 for reports')])







@server.route('/')
@server.route('/hello')
def hello():
    return flask.redirect('/dashboard')

@server.route('/dashboard')
def render_dashboard():
    return flask.redirect('/dash1')


@server.route('/reports')
def render_reports():
    return flask.redirect('/dash2')

app = DispatcherMiddleware(server, {
    '/dash1': dash_app1.server,
     '/dash2': dash_app2.server
    
})

if __name__ == '__main__':
    app.run_server()

#run_simple('127.0.0.1', 5000, app, use_reloader=True, use_debugger=True,)