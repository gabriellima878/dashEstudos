from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# dataframe de pandas
df = pd.read_excel('Vendas.xlsx')

# plotly
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

#css 
app.layout = html.Div(children=[
    html.H1(children='Meu Dashboard'),

    html.Div(children='''
        Dashboard de Vendas em Python
    '''),

    html.H3(children="Vendas de cada Produto por Loja"),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
], style={"text-align": "center"})

# callbacks

# colocando o site no ar
if __name__ == '__main__':
    app.run(debug=True, port=5050)
