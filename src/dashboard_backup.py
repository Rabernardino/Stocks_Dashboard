

import os
from dotenv import load_dotenv
import dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from datetime import date
from filter_obj import selected_columns_stocks, selected_columns_month,selected_metrics,selected_year

# Inicializar a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Dados
file_path = os.path.dirname('__file__')

path = os.path.join(file_path, 'data/processed/stock_market_v2.csv')

cleaned_data = pd.read_csv(path)

#Charts

fig1 = go.Figure(data= [go.Candlestick(

    x = cleaned_data[cleaned_data['Day'] == '2024-05-17'],
    open = cleaned_data[cleaned_data['Company_Name'] == 'Apple']['Opening_Value'],
    high = cleaned_data[cleaned_data['Company_Name'] == 'Apple']['Highest_Value'],
    low = cleaned_data[cleaned_data['Company_Name'] == 'Apple']['Lowest_Value'],
    close = cleaned_data[cleaned_data['Company_Name'] == 'Apple']['Closing_Value']

        )])

fig1.update_layout(
    xaxis_rangeslider_visible = False,
    paper_bgcolor = '#242424',
    autosize= True,
    margin= go.Margin(l=0, r=0, t=0, b=0),
    showlegend= False,
    mapbox_style = 'carto-darkmatter'
)


#Boxplot with the selected company
fig2 = go.Figure()

df_boxplot = cleaned_data[(cleaned_data['Company_Name'] == 'Apple') & (cleaned_data['Year'] == '2023')]

for metric in cleaned_data.columns[8:12]:
    fig2.add_trace(go.Box(
        y=df_boxplot[metric],
        name=metric,
        boxmean=True  # Adiciona uma linha para a média
    ))


fig2.update_layout(
    paper_bgcolor = '#242424',
    autosize= True,
    margin= go.Margin(l=0, r=0, t=0, b=0),
    showlegend= False,
    mapbox_style = 'carto-darkmatter'
)


# Estilização
CARD_STYLE = {
    "margin": "10px 20px",
    "padding": "10px",
    "textAlign": "center",
    "height":"100px"
}

GRAPH_STYLE = {
    "margin": "20px 0"
}


# Layout do dashboard
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Logo da empresa
                        html.Img(src="/docs/logo.png", style={"width": "100px", "margin": "20px 0"}),

                        html.H4('Stock Market Analysis', style={'text-align':'center', 'margin-bottom':'30px'}),


                        # Seletor de variável e data
                        html.Div(
                            [
                                html.Label("Select the stock:"),
                                dcc.Dropdown(
                                    id="acao-seletor",
                                    options= [{'label':j, 'value':i} for j,i in selected_columns_stocks.items()],
                                    value='AAPL',
                                    style={"marginBottom": "20px", "backgroundColor": "#242424"} 
                                ),
                            ]
                        ),


                        html.Div(
                            [
                                html.Label("Select the year:"),
                                dcc.Dropdown(
                                    id="year-seletor",
                                    options= [{'label':j, 'value':i} for j,i in selected_year.items()],
                                    value='2023',
                                    style={"marginBottom": "20px", "backgroundColor": "#242424"}
                                ),
                            ]
                        ),

                        html.Div(
                            [
                                html.Label("Selecione o Dia:"),
                                dcc.DatePickerSingle(
                                    id="data-seletor",
                                    date=f"{cleaned_data['Day'].min()}",
                                    display_format="YYYY-MM-DD",
                                    style={"margin-letf":"30px","marginBottom": "20px", "padding":"10px", "b" 'display': 'inline-block'}
                        ),
                            ]
                        ),

                        # Cards de informações
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Abertura", className="card-title"),
                                                html.P(id="valor-abertura", className="card-text"),
                                            ],
                                            style=CARD_STYLE
                                        )
                                    ),
                                    width=6,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Fechamento", className="card-title"),
                                                html.P(id="valor-fechamento", className="card-text"),
                                            ],
                                            style=CARD_STYLE
                                        )
                                    ),
                                    width=6
                                ),
                            ]
                            
                        ),

                        dbc.Row([
                            html.Hr()
                        ]),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Maior Valor", className="card-title"),
                                                html.P(id="valor-maior", className="card-text"),
                                            ],
                                            style=CARD_STYLE
                                        )
                                    ),
                                    width=6
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Menor Valor", className="card-title"),
                                                html.P(id="valor-menor", className="card-text"),
                                            ],
                                            style=CARD_STYLE
                                        )
                                    ),
                                    width=6
                                ),
                            ]
                        ),

                        # Gráfico de barras
                        html.H4("Gráfico de Barras", style={"textAlign": "center", "margin": "20px 0"}),
                        dcc.Graph(id="grafico-box", style=GRAPH_STYLE, figure=fig2),
                    ],
                    width=4,
                    style={"padding": "20px", "backgroundColor": "#242424", "borderRight": "1px solid #dee2e6"}
                ),
                dbc.Col(
                    [
                        dbc.Row([
                            dbc.Col([
                                # Gráfico de candle
                                html.H4("Chart One", style={"textAlign": "center", "margin": "20px 0"}),
                                dcc.Graph(id="grafico-one", style=GRAPH_STYLE),

                            ], md=6),

                            dbc.Col([
                                # Gráfico de linha
                                html.H4("Chart Two", style={"textAlign": "center", "margin": "20px 0"}),
                                dcc.Graph(id="grafico-two", style=GRAPH_STYLE),

                            ], md=6),

                        ]),

                        dbc.Row([
                            dbc.Col([
                                # Outro gráfico
                                html.H4("Candle Chart", style={"textAlign": "center", "margin": "20px 0"}),
                                dcc.Graph(id="grafico-candle", style=GRAPH_STYLE, figure=fig1),
                            ], md=12)
                        ])
                        
                    ],
                    width=8,
                    style={"padding": "20px", "backgroundColor": "#242424"}
                ),
            ]
        )
    ],
    fluid=True,
)

# Callback para atualizar os valores dos cards
@app.callback(
    [
        Output("valor-abertura", "children"),
        Output("valor-fechamento", "children"),
        Output("valor-maior", "children"),
        Output("valor-menor", "children"),
    ],
    [Input("acao-seletor", "value"), Input("data-seletor", "date")]
)
def update_cards(acao, data):
    filtered_df = cleaned_data[(cleaned_data['Company_Name'] == acao) & (cleaned_data['Day'] == data)]
    if not filtered_df.empty:
        abertura = filtered_df.iloc[0]['Opening_Value']
        fechamento = filtered_df.iloc[0]['Closing_Value']
        maior = filtered_df.iloc[0]['Highest_Value']
        menor = filtered_df.iloc[0]['Lowest_Value']
    else:
        abertura = fechamento = maior = menor = "N/A"
    
    return f"R$ {abertura}", f"R$ {fechamento}", f"R$ {maior}", f"R$ {menor}"



#Callback para atualizar o gráfico de candle
@app.callback(
    Output("grafico-candle", "figure"),
    [Input("acao-seletor", "value")]
)
def update_candle_chart(acao):
    # Lógica para gerar o gráfico de candle
    fig1 = go.Figure(data= [go.Candlestick(

    x = cleaned_data['Day'],
    open = cleaned_data[cleaned_data['Company_Name'] == acao]['Opening_Value'],
    high = cleaned_data[cleaned_data['Company_Name'] == acao]['Highest_Value'],
    low = cleaned_data[cleaned_data['Company_Name'] == acao]['Lowest_Value'],
    close = cleaned_data[cleaned_data['Company_Name'] == acao]['Closing_Value']

        )])

    fig1.update_layout(xaxis_rangeslider_visible = False)

    return fig1


# Callback para atualizar o gráfico de box
@app.callback(
    Output("grafico-box", "figure"),
    [Input("acao-seletor", "value"), Input("year-seletor","value")]
)


def update_box_chart(acao,year):
    # Lógica para gerar o gráfico boxplot

    df_boxplot = cleaned_data[(cleaned_data['Company_Name'] == acao) & (cleaned_data['Year'] == year)]

    #Creating a dataframe to filter the selected data
    fig2 = go.Figure()

    for metric in df_boxplot.columns[8:12]:
        fig2.add_trace(go.Box(
            y=df_boxplot[metric],
            name=metric,
            boxmean=True  # Adiciona uma linha para a média
        ))


    fig2.update_layout(
    paper_bgcolor = '#242424',
    autosize= True,
    margin= go.Margin(l=0, r=0, t=0, b=0),
    showlegend= False,
    mapbox_style = 'carto-darkmatter',
    font_color='#F7FFF7'
    )

    return fig2


# Callback para atualizar o gráfico de linha
@app.callback(
    Output("grafico-linha", "figure"),
    [Input("acao-seletor", "value"), Input("data-seletor", "value")]
)

def update_line_chart(variavel, data):
    # Lógica para gerar o gráfico de linha
    fig = go.Figure()
    fig.update_layout(title=f"Gráfico de Linha - {variavel} em {data}")
    return fig

# Callback para atualizar outro gráfico
@app.callback(
    Output("grafico-outro", "figure"),
    [Input("variavel-seletor", "value"), Input("data-seletor", "value")]
)
def update_other_chart(variavel, data):
    # Lógica para gerar outro gráfico
    fig = go.Figure()
    fig.update_layout(title="Outro Gráfico")
    return fig


# Rodar a aplicação
if __name__ == "__main__":
    app.run_server(debug=True, port='8080')