import dash
from dash import dcc, Input, Output
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO
import random

# Inicializando o aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

url_theme1 = dbc.themes.LITERA
url_theme2 = dbc.themes.VAPOR
template_theme1 = 'litera'
template_theme2 = 'vapor'

# Carregando os dados do arquivo CSV
df = pd.read_csv('nba_novo.csv', sep=",")

# Obtenha a lista de times únicos
teams = df['Tm'].unique()

# Crie um dicionário que mapeia times para cores aleatórias
team_colors = {team: f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})' for team in teams}

# Definindo o layout da aplicação
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
            # Título da página
            dcc.Markdown("## Estatistica NBA"),
            # Dropdown para seleção do time
            dcc.Dropdown(
                id='Team',
                value=[],  
                multi=True,  
                options=[{'label': team, 'value': team} for team in teams],
            ),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            # Gráfico de barras para exibir a comparação de PTS
            dcc.Graph(id='bar_graph_pts')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            # Gráfico para exibir a porcentagem de 3P% por jogador selecionado
            dcc.Graph(id='percentage_graph')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            # Gráfico para exibir as tentativas de 3 pontos (3PA) por jogador selecionado
            dcc.Graph(id='threepa_graph')
        ])
    ])
])

# Callback para atualizar os gráficos com base na seleção de times
@app.callback(
    Output('bar_graph_pts', 'figure'),
    Output('percentage_graph', 'figure'),
    Output('threepa_graph', 'figure'),
    [Input('Team', 'value')],
)
def update_graphs(selected_teams):
    if not selected_teams:
        # Se nenhum time for selecionado, exiba gráficos vazios
        return go.Figure(), go.Figure(), go.Figure()

    # Filtrar o DataFrame para os dados dos times selecionados
    team_df = df[df['Tm'].isin(selected_teams)]

    # Classificar o DataFrame por pontos (PTS) em ordem decrescente
    team_df_sorted = team_df.sort_values(by='PTS', ascending=False)

    # Gráfico de barras para PTS
    bar_fig_pts = go.Figure(go.Bar(
        x=team_df_sorted['Player'],
        y=team_df_sorted['PTS'],
        text=team_df_sorted['PTS'],
        textposition='auto',
        marker_color=[team_colors.get(team, 'gray') for team in team_df_sorted['Tm']]
    ))
    bar_fig_pts.update_layout(
        title='Número de PTS por Jogador',
        xaxis_title='Jogador',
        yaxis_title='Número de PTS'
    )

    # Gráfico de porcentagem de 3P%
    percentage_fig = go.Figure(go.Bar(
        x=team_df_sorted['Player'],
        y=team_df_sorted['3P%'],
        text=team_df_sorted['3P%'],
        textposition='auto',
        marker_color=[team_colors.get(team, 'gray') for team in team_df_sorted['Tm']]
    ))
    percentage_fig.update_layout(
        title='Porcentagem de 3P% por Jogador',
        xaxis_title='Jogador',
        yaxis_title='Porcentagem de 3P%'
    )

    # Gráfico de tentativas de 3 pontos (3PA)
    threepa_fig = go.Figure(go.Bar(
        x=team_df_sorted['Player'],
        y=team_df_sorted['3PA'],
        text=team_df_sorted['3PA'],
        textposition='auto',
        marker_color=[team_colors.get(team, 'gray') for team in team_df_sorted['Tm']]
    ))
    threepa_fig.update_layout(
        title='Tentativas de 3P (3PA) por Jogador',
        xaxis_title='Jogador',
        yaxis_title='Tentativas de 3P (3PA)'
    )

    return bar_fig_pts, percentage_fig, threepa_fig

# Iniciando o servidor da aplicação
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
