

from dash import Dash, dcc, Output, Input  
import dash_bootstrap_components as dbc    
import plotly.express as px
import pandas as pd                        
import json
import numpy as np

df_departements = pd.read_excel("data/departements_2ndturn_results.xlsx")
df_communes = pd.read_excel("data/cities_2ndturn_results.xlsx")

f = open('data/departements.geojson')
departements = json.load(f)

f = open('data/COMMUNEidf_light.geojson')
communes_idf = json.load(f)


app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='# Résultat du second tour des éléctions présidentielles françaises')
graph_dep = dcc.Graph(figure={})
graph_com = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=['Gagnant','Abstentions'],
                        value='Gagnant',
                        clearable=False)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center',style={'textAlign':'center'}),
    dbc.Row([
        dbc.Col([graph_dep], width=8),
        dbc.Col([graph_com], width=4)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ],justify='center'),

], fluid=True)


@app.callback(
    Output(graph_dep, 'figure'),
    Output(graph_com, 'figure'),
    Input(dropdown, 'value')
)
def update_graph(column_name):  

    fig_dep = px.choropleth_mapbox(df_departements,
                    geojson=departements, 
                    color=column_name,
                    mapbox_style='open-street-map',
                    locations='Code du département', 
                    featureidkey="properties.code",
                    center={"lat": 47.0000, "lon": 2}, 
                    zoom = 4.5, 
                    opacity = 0.5
                   )
    fig_dep.update_geos(fitbounds="locations", visible=False)
    fig_dep.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig_com = px.choropleth_mapbox(df_communes, 
                    geojson=communes_idf,
                    color=column_name,
                    mapbox_style='open-street-map',
                    locations='Code', 
                    featureidkey="properties.INSEE_COM",
                    center={"lat": 48.8566, "lon": 2.5}, 
                    zoom = 6.7, 
                    opacity = 0.5
                   )
    fig_com.update_geos(fitbounds="locations", visible=False)
    fig_com.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig_dep,fig_com 


# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)
