from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# dataframe de pandas
df = pd.read_excel('Vendas.xlsx')

# plotly
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
fig2 = px.scatter(df, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)

# lista_marcas = ["Treinamentos", "Programação", "Todas"]
lista_marcas = list(df["Marca"].unique())
lista_marcas.append("Todas")

lista_paises = list(df["País"].unique())
lista_paises.append("Todos")

# Layout 
app.layout = html.Div(children=[
    html.H1(children='Meu Dashboard'),

    html.Div(children='''
        Dashboard de Vendas em Python
    '''),

    html.H3(children="Vendas de cada Produto por Loja", id="subtitulo"),

    dcc.RadioItems(options=lista_marcas, value="Todas", id="selecao_marcas", inline=True),

    html.Div(children=[
        dcc.Dropdown(options=lista_paises, value="Todos", id="selecao_pais"),   
    ], style={"width": "50%", "margin": "auto"}),

    dcc.Graph(
        id='vendas_por_loja',
        figure=fig
    ),

    dcc.Graph(
        id='distribuicao_vendas',
        figure=fig2
    ),


], style={"text-align": "center"})


@app.callback(
    Output("selecao_pais", "options"),
    Input("selecao_marcas", "value"),
)
def opcoes_pais(marca):
    # criar logica que diga qual a lista de países que ele vai pegar
    if marca == "Todas":
        nova_lista_paises = list(df["País"].unique())
        nova_lista_paises.append("Todos")
    else:
        df_filtrada = df.loc[df["Marca"]==marca, : ]
        nova_lista_paises = list(df_filtrada["País"].unique())
        nova_lista_paises.append("Todos")
    return nova_lista_paises

# callbacks

@app.callback(
    Output("subtitulo", "children"),
    Output("vendas_por_loja", "figure"),
    Output("distribuicao_vendas", "figure"),
    Input("selecao_marcas", "value"),
    Input("selecao_pais", "value"),
)
def selecionar_marca(marca, pais):
    if marca == "Todas" and pais == "Todos":
        texto = "Vendas de cada Produto por Loja"
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig2 = px.scatter(df, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)
    else:
        df_filtrada = df
        if marca != "Todas":
            df_filtrada = df_filtrada.loc[df_filtrada['Marca'] == marca, : ]
            # filtrar de acordo com a marca
        if pais != "Todos":
            df_filtrada = df_filtrada.loc[df_filtrada["País"] == pais, : ]
            # filtrar de acordo com o país


        texto = f"Vendas de cada Produto por Loja da Marca {marca} e do País {pais}"
        fig = px.bar(df_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
        fig2 = px.scatter(df_filtrada, x="Quantidade", y="Valor Final", color="Produto", size="Valor Unitário", size_max=60)
    return texto, fig, fig2


# colocando o site no ar
if __name__ == '__main__':
    app.run(debug=True, port=8050)
