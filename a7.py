import pandas as pd
from dash import Dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
#import chardet  # For detecting file encoding# Load the data from the CSV file with the correct encoding
df = pd.read_csv('scores.csv', encoding='latin1')

# Clean the data
df = df.dropna(subset=['Year', 'Winners', 'Runners-up'])

# Create a list of unique countries that have won the World Cup
unique_winners = df['Winners'].unique()

# Create a dictionary to count the number of wins for each country
win_counts = df['Winners'].value_counts().to_dict()

# Create a Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard"),
    
    dcc.Tabs([
        dcc.Tab(label='World Cup Winners', children=[
            html.H2("Countries that have won the World Cup"),
            dcc.Graph(id='choropleth-map'),
        ]),
        
        dcc.Tab(label='Country Wins', children=[
            html.H2("Select a country to view the number of times it has won the World Cup"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in unique_winners],
                value=unique_winners[0]
            ),
            html.Div(id='country-wins-output')
        ]),
        
        dcc.Tab(label='Yearly Winners and Runners-up', children=[
            html.H2("Select a year to view the winner and runner-up"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in df['Year'].unique()],
                value=df['Year'].unique()[0]
            ),
            html.Div(id='year-output')
        ])
    ])
])

@app.callback(
    Output('choropleth-map', 'figure'),
    Input('choropleth-map', 'id')
)
def update_choropleth_map(_):
    fig = px.choropleth(df, locations="Winners", locationmode="country names", color="Winners",
                        hover_name="Winners", projection="natural earth",
                        title="Countries that have won the World Cup")
    return fig

@app.callback(
    Output('country-wins-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_wins(selected_country):
    wins = win_counts.get(selected_country, 0)
    return f"{selected_country} has won the World Cup {wins} times."

@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_output(selected_year):
    row = df[df['Year'] == selected_year].iloc[0]
    winner = row['Winners']
    runner_up = row['Runners-up']
    return f"In {selected_year}, {winner} won the World Cup and {runner_up} was the runner-up."

if __name__ == '__main__':
    app.run(debug=True)
