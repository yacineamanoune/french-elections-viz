

from dash import Dash, dcc, Output, Input  
import dash_bootstrap_components as dbc    
import plotly.express as px
import pandas as pd                        
import json
import numpy as np

df = pd.read_excel("data/departements_2ndturn_results.xlsx")
print(df.head())

f = open('data/departements.geojson')
departements = json.load(f)


app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=['Départements'],
                        value='Départements',  # initial value displayed when page first loads
                        clearable=False)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),

], fluid=True)


@app.callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Input(dropdown, 'value')
)
def update_graph(column_name):  

    fig = px.choropleth_mapbox(df,
                    geojson=departements, 
                    color="Gagnant",
                    mapbox_style='open-street-map',
                    locations='Code du département', 
                    featureidkey="properties.code",
                    center={"lat": 47.0000, "lon": 2}, 
                    zoom = 4.5, 
                    opacity = 0.5
                   )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig, '# '+column_name  


# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)
