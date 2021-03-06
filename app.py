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
from covid import scrape_1,scrape_2,scrape_3,Active_sort,Line_plot1,Line_plot2


external_stylesheets = [dbc.themes.COSMO]

colors={
    'area':'lightgrey'
}




#fig6 = px.bar(df6, x="Date", y="Tests", title='<b>Number of Tests Performed Since March</b>')


# fig = go.Figure([go.Bar(name="Total confirmed Cases",
#                         x=df2['State'][0:15],
#                         y=df2['Total_confirmed_cases'],
#                         marker_color='indianred'),
#                 go.Bar(name="Cured/Discharged",
#                         x=df2['State'][0:15], 
#                         y=df2["Cured_Discharged_Migrated"],
#                     marker_color='lightsalmon'),
#                 go.Bar(name="Deaths",
#                         x=df2['State'][0:15], 
#                         y=df2["Deaths"],
#                     marker_color='red')
#                 ])

# fig.update_layout(barmode='group')


#fig2 = px.line(df5, x="Date", y="Cases", title='<b>Number of Cases Since February</b>')




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



# card_content1 = [
#     dbc.CardBody(
#         [
            
            

#             html.H5("Total Cases", className="card-title"),
            
#                 df2["Total_confirmed_cases"].sum()

#         ]
#     ),
# ]

# card_content2 = [
   
#     dbc.CardBody(
#         [
            
#             html.H5("Total Recovered", className="card-title"),
            
#                 df2["Cured_Discharged_Migrated"].sum()

#         ]
#     ),
# ]


# card_content3 = [
   
#     dbc.CardBody(
#         [
           
#             html.H5("Total Deaths", className="card-title"),
            
#                 df2["Deaths"].sum()

#         ]
#     ),
# ]

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
# fig9 = go.Figure(data=[go.Table(header=dict(values=['State','Total Cases', 'Deaths', 'Active Cases'],
# fill_color='lightgrey',font_size=20,height=50),
#                  cells=dict(values=[df2["State"],df2["Total_confirmed_cases"],df2["Cured_Discharged_Migrated"],df2["Active_cases"]],height=50,font_size=18))
#                     ,'min_height':400])






server = flask.Flask(__name__)
dash_app1 = Dash(__name__, server = server, url_base_pathname='/dashboard/',external_stylesheets=external_stylesheets )
dash_app2 = Dash(__name__, server = server, url_base_pathname='/reports/')
dash_app1.layout = html.Div([
        html.H1(children=html.Strong("India Covid-19 Updates"),
           style={
               'textAlign':'center',
               'color':'black',
               'font-family':'Comic Sans MS',
               'fontsize':'20px',
               'backgroundColor':colors['area'],
               'text-decoration':'underline'

           }),

           html.Br(style={'backgroundColor':colors['area']}),
           html.Br(),
    html.Div([
       
    dbc.Row(
    [
        dbc.Col(dbc.Card([
    dbc.CardBody(
        [
            
            

            html.H5("Total Cases", className="card-title"),
            
                scrape_1()["Total_confirmed_cases"].sum()

        ]
    ),
],
        
        
        
        
        
         outline=True,style={'backgroundColor':"lightblue","border":"2px black solid",'color':'black','fontWeight':'bold','font-size':'26px'})),
        dbc.Col(dbc.Card([
   
    dbc.CardBody(
        [
            
            html.H5("Total Recovered", className="card-title"),
            
                scrape_1()["Cured_Discharged_Migrated"].sum()

        ]
    ),
], 
        
        
        
        
        color="blue", outline=True,style={'backgroundColor':"lightgreen","border":"2px black solid",'color':'black','fontWeight':'bold','font-size':'26px'})),
        dbc.Col(dbc.Card([
   
    dbc.CardBody(
        [
           
            html.H5("Total Deaths", className="card-title"),
            
                scrape_1()["Deaths"].sum()

        ]
    ),
], 
        
        
        
        
        
        color="info", outline=True,style={'backgroundColor':"lightsalmon","border":"2px black solid",'color':'black','fontWeight':'bold','font-size':'26px'})),
    ],className="mb-4", style={
               'textAlign':'center',
               'color':'grey',
                'font' : 'bold',
                'backgroundColor':colors['area']
           }),
    ]),

    html.Div([
        html.P("Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered covid19 which is widespread all over the world. "+
"Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without "+
"requiring special treatment.  Older people, and those with underlying medical "+ 
"problems like cardiovascular disease, diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness.")
    ],style={'color':'black','font-size':'26px'}),
    #   html.Div(
    #      generate_table(df2)),
    html.Br(),
    html.Br(),
    html.Div([
        
    dash_table.DataTable(
    data=scrape_1().to_dict('records'),
    columns=[{'id': c, 'name': c} for c in scrape_1().columns],
    fixed_rows={'headers': True},
    style_table={'height': 800},
     style_cell={
        'textAlign':'center','maxWidth':50,'maxHeight':100,'font_size':'20px',
    },
    style_header={'backgroundColor':'lightblue','fontWeight':'bold'}
)
    
    ],style={"border":"2px black solid",
    'backgroundColor':colors['area'],
                     }),

    html.Br(),
    html.Br(),

    html.Div([
        html.P("Top 15 States with Highest Cases in India")
    ],style={
               'textAlign':'center',
               'color':'black',
                'fontWeight' : 'bold',
                'text-decoration':'underline',
                'backgroundColor':colors['area'],
                'font-size':'20px'
                }
                ),

    
    
    html.Div([
    # dcc.Graph(figure=fig)
    dcc.Graph(id='Total Cases',
                 figure={
                     'data': [
                go.Bar(name="Total confirmed Cases",
                        x=scrape_1()['State'][0:15],
                        y=scrape_1()['Total_confirmed_cases'],
                        marker_color='indianred'),
                go.Bar(name="Cured/Discharged",
                        x=scrape_1()['State'][0:15], 
                        y=scrape_1()["Cured_Discharged_Migrated"],
                    marker_color='lightsalmon'),
                go.Bar(name="Deaths",
                        x=scrape_1()['State'][0:15], 
                        y=scrape_1()["Deaths"],
                    marker_color='red')
                ],
                'layout': go.Layout(title="<b>Total Cases in India</b>",autosize=True)
                 })
    
    ],style={"border":"2px black solid",
    'backgroundColor':colors['area']}),
    html.Br(),
    html.Br(),

   html.Div([
       html.P(scrape_1()['State'][0]+" is the state having the highest number of confirmed cases amongst all the states in India."+
       " A majority of the coronavirus (COVID-19) cases in India affected people between ages 19.5 and 49.5. Of these, the age "+
       "group between 20 and 29 years old were most affected . This trend was significantly lower when compared to findings from other countries. However, compared to many western countries,"+
       " India also had a younger population directly affecting the proportion of COVID-19 cases.")
   ],style={'color':'black','font-size':'26px'}),
    html.Br(),

    html.Div([
        html.P("Datewise Growth in Cases since 2nd Feb")
    ],style={
               'textAlign':'center',
               'color':'black',
                'fontWeight' : 'bold',
                'text-decoration':'underline',
                'backgroundColor':colors['area'],
                'font-size':'20px'
                }),
    html.Div([
    dcc.Graph(figure=Line_plot1())
    
    
    ],style={"border":"2px black solid",
    'backgroundColor':colors['area']},className="six columns"),
    html.Br(),
    

   html.Div([
       html.P("The first case of Corona virus in India was observed to be on 30th January 2020. Since then there has been an "+
       "additive growth in cases all accross the country.")
   ],style={'color':'black','font-size':'26px'}),
    html.Br(),

    html.Div([
        html.P("Datewise Tests Performed in India since March ")
    ],style={
               'textAlign':'center',
               'color':'black',
                'fontWeight' : 'bold',
                'text-decoration':'underline',
                'backgroundColor':colors['area'],
                'font-size':'20px'
                }),
    html.Div([
    dcc.Graph(figure=Line_plot2())
    ],style={"border":"2px black solid",
    'backgroundColor':colors['area']},className="six columns"),

    html.Br(),
    

   html.Div([
       html.P("Testing for Covid-19 has increased in the country gradually. On an average, around 15 lakh samples are being tested."+
       " Covid-19 is diagnosed using Reverse Transcription Polymerase Chain Reaction (RT-PCR) assay, "+
       "which is the only diagnostic test for Covid-19 approved by the World Health Organization. ")
   ],style={'color':'black','font-size':'26px'}),
    html.Br(),
    

    html.Div([
        html.P("Top 10 States with Lowest Active Cases")
    ],style={
               'textAlign':'center',
               'color':'black',
                'fontWeight' : 'bold',
                'text-decoration':'underline',
                'backgroundColor':colors['area'],
                'font-size':'20px'
                }),
     html.Div([
        dcc.Graph(id='Active Cases',
                 figure={
                     'data': [
                         go.Bar(x=Active_sort()['State'][5:15],
                               y=Active_sort()["Active_cases"][5:15],
                               marker_color='lightsalmon')
                     ],
                     'layout': go.Layout(title="<b>Lowest Active Cases</b>",autosize=True)
                 })
        
    ],style={
        'backgroundColor':colors['area'],"border":"2px black solid"
        
    }),

    html.Br(),
    

   html.Div([
       html.P(Active_sort()['State'][0]+", "+Active_sort()['State'][1]+"and " +Active_sort()['State'][2]+" are some of the states in Green Zone. The effect of Covid-19 is observed to be very less in these States.")
   ],style={'color':'black','font-size':'26px'}),
    html.Br(),

#     #  html.Div([
#     # dbc.Row(
#     # [
#     #     dbc.Col(dbc.Card(card_content4, outline=False,style={'height':'30vh','width':'40vh','backgroundColor':"lightblue"}))
        
#     # ],className="mb-4", style={
#     #            'textAlign':'center',
#     #            'color':'black',
#     #             'font' : 'bold',
#     #             'backgroundColor':'lavender'
#     #        }),
#     # ]),




    
    
    # html.Div([
    #     dcc.Graph(id='g1',
    #              figure={
    #                  'data': [
    #                      go.Pie(values=df2['Total_confirmed_cases'][0:7],
    #                            labels=df2['State'][0:7])
    #                  ],
    #                  'layout': go.Layout(title="<b>Total Cases</b>",autosize=True)
    #              }),
    # ],className="six columns", style={
    #     'backgroundColor':colors['area'],'margin':'15px',"border":"2px black solid"
    # }),

    html.Br(),
    

    html.Div([
        html.P("Percentage of Deaths observed for top 20 States in India")
    ],style={
               'textAlign':'center',
               'color':'black',
                'fontWeight' : 'bold',
                'fontUnderline':True,
                'text-decoration':'underline',
                'backgroundColor':colors['area'],
                'font-size':'20px'
                }),
        
        html.Div([
        
         dcc.Graph(id='g2',
                 figure={
                     'data': [
                         go.Pie(values=scrape_1()["Deaths"][0:20],
                               labels=scrape_1()['State'][0:20])
                     ],
                     'layout': go.Layout(title="<b>Deaths</b>",autosize=True)
                 }),
        ],className="six columns",style={
        'backgroundColor':colors['area'],'border':'2px',"border":"2px black solid",
    }),
    html.Br(),
     html.Div([
         html.P("Maximum number of deaths have been observed in "+scrape_1()['State'][0]+". The worst affected cities here are Mumbai and Pune."+
         " A lot of arrangements for beds have to be made in order to occupy the new cases emerging.")
        ],style={
            'color':'black','font-size':'26px'
        }),
 

    
   
   
    
    
    

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

# run_simple('127.0.0.1', 5000, app, use_reloader=True, use_debugger=True,)