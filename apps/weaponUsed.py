# -*- coding: utf-8 -*-
  
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import webbrowser
from threading import Timer

pd.options.mode.chained_assignment = None


def open_browser():
      webbrowser.open_new('http://127.0.0.1:8050/')


app = dash.Dash(__name__)
df=pd.read_csv("apps/data/global_terror_2.csv",encoding='latin-1')

app.layout = html.Div(
        html.Div([
        html.Div(children=[
        
        html.Div([dcc.Dropdown(id='region', className='dropdown',
                               placeholder='Select Region',
                               multi=True,
                               options=[{'label': c , 'value': c} for c in sorted(df['region_txt'].unique())],
                               value=[''])],
        style={
            'width':'40%',
            'padding':40,
            'justify-content': 'center',
            'margin-left':220
        }
    ),
        html.Div([dcc.Dropdown(id='country', className='dropdown',
                               multi=True,
                               placeholder='Select Country',
                               options=[{'label': c , 'value': c} for c in sorted(df['country_txt'].unique())],
                               value=[''])],
        style={
            'width':'40%',
            'padding':40,
            'justify-content': 'center',
            'margin-left':220
        }
    ),
    

    dcc.Graph(id = 'pie-chart'),
    
     
]),
    
])
)
@app.callback(Output('pie-chart','figure'),
              [Input('region','value'),
               Input('country','value')
              ]
              )

def update_fig(region_val,country_val):
    data= df
    #data[(data.region_txt.isin([region_val]))&(data.country_txt.isin([country_val]))]
    #data = df.iloc[[index for index,row in df.iterrows() if row['region_txt'] == region_val and row['country_txt'] == country_txt]]
    
    
    #data = df[(df.region_txt == region_val) & (df.country_txt == country_val)]
    
    
    
    # print(region_val,country_val)
    
    piechart=px.pie(
            data_frame=data,
            names=data['weaptype1_txt'],
            hole=.3,
            )
    piechart.update_traces(textposition='inside')
    piechart.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return (piechart)

if __name__=='__main__':
    Timer(1, open_browser).start();
    app.run_server()