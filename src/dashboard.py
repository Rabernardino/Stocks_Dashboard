

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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

# Dados
file_path = os.path.dirname('__file__')

path = os.path.join(file_path, 'data/processed/stock_market_v3.csv')

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
    template="ggplot2",
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
    template="ggplot2",
    autosize= True,
    margin= go.Margin(l=0, r=0, t=0, b=0),
    showlegend= False,
    mapbox_style = 'carto-darkmatter'
)


variation_df = cleaned_data[(cleaned_data['Year'] == 2023) & (cleaned_data['Company_Name'] == 'Apple')]

# Criando a figura
fig3 = go.Figure()

# Adicionando a linha com a variação diária do fechamento
fig3.add_trace(go.Scatter(x=variation_df['Day'], y=variation_df['Daily_Closing_Variation'], mode='lines', name='Daily Closing Variation'))


fig3.update_traces(hovertemplate=None)

# Atualizando o layout para definir o eixo X na linha zero
fig3.update_layout(
    #title='Variação Diária do Fechamento ao Longo do Tempo',
    hovermode='x',
    template="ggplot2",
    xaxis_title='Day',
    yaxis_title='Daily Closing Variation',
    shapes=[dict(type='line', x0=variation_df['Day'].min(), x1=variation_df['Day'].max(), y0=0, y1=0, line=dict(color='black', width=2))]
    )



groupedby_df = cleaned_data[cleaned_data['Day'] == '2023-12-26'].groupby(['Company_Name','Stock_Code'])['Volume'].max().nlargest(5).reset_index()

colors = ['#EAA1B0', '#C8C990', '#A1D5B8', '#9ECDEE', '#C99EEE']

fig4 = go.Figure()

fig4.add_trace(go.Bar(x=groupedby_df['Company_Name'], y=groupedby_df['Volume'], marker=dict(color=colors),
                        hovertemplate=
                            '<br>Company Name:<br> %{x}' + '<br>Stock Volume:</br> %{y:f}MM<extra></extra>',showlegend=False))



fig4.update_layout(
    template="ggplot2",
    autosize= True,
    margin= go.Margin(l=5, r=10, t=10, b=5),
    xaxis=dict(
        title=dict(text="")
    ),
    yaxis=dict(
        title=dict(text="")
    ),
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
                        html.Div([
                        html.Img(id='logo', src=app.get_asset_url('logo_dark.png'), height=20),
                        html.H4('Stock Market Analysis', style={'text-align':'center', 'margin-top':'50px','margin-bottom':'10px'}),
                        ]),
                        #html.Img(src="/docs/logo_dark.png", style={"width": "100px", "margin": "20px 0"}),



                        # Seletor de variável e data
                        html.Div(
                            [
                                html.Label("Select the stock:"),
                                dcc.Dropdown(
                                    id="acao-seletor",
                                    options= [{'label':j, 'value':i} for j,i in selected_columns_stocks.items()],
                                    value='AAPL',
                                    style={"marginBottom": "20px"} 
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
                                    style={"marginBottom": "20px"}
                                ),
                            ]
                        ),

                        html.Div(
                            [
                                html.Label("Select the day:"),
                                dcc.DatePickerSingle(
                                    id="data-seletor",
                                    date=f"{cleaned_data['Day'].min()}",
                                    min_date_allowed=f"{cleaned_data['Day'].min()}",
                                    max_date_allowed=f"{cleaned_data['Day'].max()}",
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
                                                html.H5("Opening", className="card-title"),
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
                                                html.H5("Closing", className="card-title"),
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
                            html.Div([dbc.Row([
                                html.H6('')
                            ])])
                        ]),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Highest", className="card-title"),
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
                                                html.H5("Lowests", className="card-title"),
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
                        #html.H4("Stock Prices Behavior", style={"textAlign": "center", "margin": "20px 0"}),
                        dcc.Graph(id="grafico-box", style=GRAPH_STYLE, figure=fig2),
                    ],
                    width=4,
                    style={"padding": "20px","borderRight": "1px solid #dee2e6"}
                ),
                dbc.Col(
                    [html.H4("Daily Closing Evolution", style={"textAlign": "center", "margin": "20px 0"}),
                        dbc.Row([
                            dbc.Col([
                                # Gráfico de Linha
                                #html.H4("Daily Closing Evolution", style={"textAlign": "center", "margin": "20px 0"}),
                                dcc.Graph(id="grafico-one", style=GRAPH_STYLE, figure=fig3),

                            ], md=6),

                            dbc.Col([
                                # Gráfico de Colunas
                                #html.H4("Top Five Volume Negotiated", style={"textAlign": "center", "margin": "20px 0"}),
                                dcc.Graph(id="grafico-two", style=GRAPH_STYLE, figure=fig4),

                            ], md=6),

                        ]),

                        dbc.Row([
                            dbc.Col([
                                # Gráfico Candle
                                #html.H4("Candle Chart", style={"textAlign": "center", "margin": "20px 0"}),
                                dcc.Graph(id="grafico-candle", style=GRAPH_STYLE, figure=fig1),
                            ], md=12)
                        ])
                        
                    ],
                    width=8,
                    style={"padding": "20px"}
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
    [Input("acao-seletor", "value"), Input("year-seletor","value")]
)
def update_candle_chart(stock,year):

    #Creating a dataframe to filter the candle
    candle_df = cleaned_data[cleaned_data['Year'] == year]

    # Lógica para gerar o gráfico de candle
    fig1 = go.Figure(data= [go.Candlestick(

    x = candle_df['Day'],
    open = candle_df[candle_df['Company_Name'] == stock]['Opening_Value'],
    high = candle_df[candle_df['Company_Name'] == stock]['Highest_Value'],
    low = candle_df[candle_df['Company_Name'] == stock]['Lowest_Value'],
    close = candle_df[candle_df['Company_Name'] == stock]['Closing_Value']

        )])

    fig1.update_layout(
        xaxis_rangeslider_visible = False,
        template="ggplot2",
        autosize= True,
        margin= go.Margin(l=0, r=0, t=70, b=0),
        showlegend= False,
        mapbox_style = 'carto-darkmatter',
        title=dict(
            text=f'Candle Chart - {stock}',
            font=dict(
            size=16,
            color="black"
            )
        )
        )

    return fig1


# Callback para atualizar o gráfico de box
@app.callback(
    Output("grafico-box", "figure"),
    [Input("acao-seletor", "value"), Input("year-seletor","value")]
)


def update_box_chart(stock,year):
    # Lógica para gerar o gráfico boxplot

    df_boxplot = cleaned_data[(cleaned_data['Company_Name'] == stock) & (cleaned_data['Year'] == year)]

    #Creating a dataframe to filter the selected data
    fig2 = go.Figure()

    for metric in df_boxplot.columns[8:12]:
        fig2.add_trace(go.Box(
            y=df_boxplot[metric],
            name=metric,
            boxmean=True  # Adiciona uma linha para a média
        ))

    
    fig2.update_layout(
    template="ggplot2",
    autosize= True,
    margin= go.Margin(l=0, r=0, t=70, b=0),
    showlegend= False,
    mapbox_style = 'carto-darkmatter',
    font_color='#F7FFF7',
    title=dict(
            text=f'Stock Prices Behavior - {stock}',
            font=dict(
            size=16,
            color="black"
            )
        )
    )

    return fig2


# Callback para atualizar o gráfico de linha
@app.callback(
    Output("grafico-one", "figure"),
    [Input("acao-seletor", "value"), Input("year-seletor","value")]
)

def update_line_chart(stock, year):
    
    # Creating the filtered dataframe
    variation_df = cleaned_data[(cleaned_data['Year'] == year) & (cleaned_data['Company_Name'] == stock)]

    # Criando a figura
    fig3 = go.Figure()

    # Adicionando a linha com a variação diária do fechamento
    fig3.add_trace(go.Scatter(x=variation_df['Day'], y=variation_df['Daily_Closing_Variation'], mode='lines', name='Daily Closing Variation', 
                              hovertemplate='%{y:.2f}<extra></extra>',showlegend=False))

    #Modifying the hover template exhibition 
    #fig3.update_traces(hovertemplate=None)

    # Atualizando o layout para definir o eixo X na linha zero
    fig3.update_layout(
        #title='Variação Diária do Fechamento ao Longo do Tempo',
        hovermode='x unified',
        template="ggplot2",
        autosize= False,
        # paper_bgcolor = '#282828',
        margin= go.Margin(l=5, r=10, t=30, b=5),
        # xaxis_title='Day',
        # yaxis_title='Daily Closing Variation',
        shapes=[dict(type='line', x0=variation_df['Day'].min(), x1=variation_df['Day'].max(), y0=0, y1=0, line=dict(color='black', dash='dash', width=2))],
        title=dict(
            text=f'Closing Variation - {stock}',
            font=dict(
            size=16,
            color="black"
            )
        )
    )


    return fig3



@app.callback(
    Output("grafico-two", "figure"),
    [Input("data-seletor", "date")]
)
def update_other_chart(data):
    
    colors = ['#EAA1B0', '#C8C990', '#A1D5B8', '#9ECDEE', '#C99EEE']

    fig4 = go.Figure()

    fig4.add_trace(go.Bar(x=groupedby_df['Company_Name'], y=groupedby_df['Volume'], marker=dict(color=colors),
                        hovertemplate=
                            '<br>%{x}' + '<br>Stock Volume:</br> %{y:,.0f}MM<extra></extra>',showlegend=False))


    # groupedby_df = cleaned_data[cleaned_data['Day'] == data].groupby(['Company_Name','Stock_Code'])['Volume'].max().nlargest(5).reset_index()

    # fig4 = px.bar(groupedby_df, x='Company_Name', y='Volume', color='Stock_Code', color_discrete_sequence=['#EAA1B0', '#C8C990', '#A1D5B8', '#9ECDEE', '#C99EEE'])

    #Cores colunas (#eaa1b0, #c8c990, #a1d5b8, #9ecdee, #c99eee)

    fig4.update_layout(
        template="ggplot2",
        autosize= False,
        margin= go.Margin(l=5, r=10, t=30, b=5),
        xaxis=dict(
        title=dict(text="")
        ),
        yaxis=dict(
            title=dict(text="")
        ),
        showlegend= False,
        mapbox_style = 'carto-darkmatter',
        title=dict(
            text=f'Daily Five Bigest Volume ({data})',
            font=dict(
            size=16,
            color="black"
            )
        )
    )

    return fig4

@app.callback(
    Output("data-seletor", "date"),
    Output("data-seletor", "min_date_allowed"),
    Output("data-seletor", "max_date_allowed"),
    [Input("acao-seletor", "value"), Input("year-seletor","value")]
)

def update_datepicker(stock,year):
    filtered_dates = cleaned_data[(cleaned_data['Company_Name'] == stock) & (cleaned_data['Year'] == year)]['Day']

    date = filtered_dates.min()
    min_date = filtered_dates.min()
    max_date = filtered_dates.max()

    return date, min_date, max_date


# Rodar a aplicação
if __name__ == "__main__":
    app.run_server(debug=True, port='8080')