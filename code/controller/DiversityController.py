#Dash Processing & Analysis
#@100rabh.nigam
#@CoreyWarren
#Team Basketball

#This program is VC layer using Dash components & cleansed data

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from pandas_datareader import data as web
from datetime import datetime as dt
from RecordKeeper import RecordKeeper

import plotly.graph_objs as go #pip install plotly
import plotly.express as px 


#Constants
RACE_WHITE      = 1 
RACE_BLACK      = 2
RACE_ASIAN      = 3
RACE_HISPANIC   = 4
GENDER_MALE     = 1
GENDER_FEMALE   = 2

#Preparing UI...
app = dash.Dash('How diverse is your position?')
df = pd.read_csv("./dataset_original.csv")
print(df)




#HTML LAYOUT FOR DASH APP...
app.layout = html.Div([

    #Header
    html.H4(children='Diversity in Jobs based on Gender, Race'),
    #Take user occupation
    dcc.Dropdown(id='job-dropdown', options=[
        {'label': row['Occupation'], 'value': row['SN']} for index, row in df.iterrows()
    ], placeholder='Your Occupation'),    
    #User's gender
    dcc.Dropdown(id='gender-dropdown', options=[
        {'label': 'Male', 'value': GENDER_MALE},
        {'label': 'Female', 'value': GENDER_FEMALE} 
    ], placeholder='Gender'), 
    #User's race
    dcc.Dropdown(id='race-dropdown', options=[
        {'label': 'White', 'value': RACE_WHITE},
        {'label': 'Black or African American', 'value': RACE_BLACK},
        {'label': 'Asian', 'value': RACE_ASIAN},
        {'label': 'Hispanic', 'value': RACE_HISPANIC}
    ], placeholder='Your Race'),
    #Submit Action button
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state'),
    #Graph
    dcc.Graph(
        id='my-graph'
        ),

    #Reporting Dropdown
    dcc.Dropdown(id='dropdown', options=[
        {'label': row['Occupation'], 'value': row['SN']} for index, row in df.iterrows()
    ], multi=True, placeholder='Filter by Occupation'),
    #Reporting Table view
    html.Div(id='table-container')
#], style={'width': '500'})
],  style={'width': '75%', 'margin': 'auto'})



def generate_table(dataframe, max_rows=10):
    """
    Draws a table based on df
    """
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



#USER SUBMISSION BUTTON CALLBACK...

@app.callback(Output('submit-button', 'children'),
            [Input('submit-button', 'n_clicks'),
            Input('job-dropdown', 'value'),
            Input('gender-dropdown', 'value'),
            Input('race-dropdown', 'value')])
            
def update_output(n_clicks, job_dropdown_value, gender_dropdown_value,race_dropdown_value):
    """
    Callback for handling submit action
    """
    # add this record to df 
    #propogate data to parent
    #Store csv
    RecordKeeper.addRecord(df,gender_dropdown_value,race_dropdown_value,job_dropdown_value)
    print ( job_dropdown_value+gender_dropdown_value+race_dropdown_value)
    return True



#TABLE UPDATING CALLBACK...

@app.callback(
    Output('table-container', 'children'),
    [Input('dropdown', 'value')])
def display_table(dropdown_value):
    """
    Callback to display filtered table
    """
    if dropdown_value is None:
        return generate_table(df, 1000)
    
    dff = df.where(df.SN.isin(dropdown_value))
    return generate_table(dff,1000)



#BAR GRAPH UPDATING CALLBACK...

@app.callback(Output('my-graph', 'figure'), [Input('dropdown', 'value')])
def update_graph(dropdown_value):
    """
    Callback to update graph
    """
    #Devise mechanism to grade based on 
    #Grades back to df
    if dropdown_value is None:
        dff=df
    else:
        dff=df.where(df.SN.isin(dropdown_value))

    return {
        'data': [
            go.Bar(x=dff.Occupation, y=dff[('Women')], name='Women'),
            go.Bar(x=dff.Occupation, y=dff[('White')], name='White'),
            go.Bar(x=dff.Occupation, y=dff[('Black or African American')], name='Black or African American'),
            go.Bar(x=dff.Occupation, y=dff[('Asian')], name='Asian'),
            go.Bar(x=dff.Occupation, y=dff[('Hispanic or Latino')], name='Hispanic or Latino')
            ],
        
        'layout': go.Layout(
            title='Job Demographics by Percentage',
            barmode='stack'#,
            #barnorm="percent"
            )
        }
        
        

#CSS
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})


#MAIN FUNCTION
if __name__ == '__main__':
    print("Starting")
    app.run_server()
    print("Completed")
