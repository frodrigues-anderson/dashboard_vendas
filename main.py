import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from dash_bootstrap_templates import ThemeSwitchAIO
import plotly.graph_objects as go
import plotly.express as px
import calendar
import locale


# Variaveis de apoio___________________________________________________________________________________
dark_tema = 'darkly'
vapor_tema='vapor'
url_dark = dbc.themes.DARKLY
url_vapor = dbc.themes.GRID



#Importando dados ______________________________________________________________________________________

df = pd.read_csv('bases/dados_completo.csv')

df['dt_Venda'] = pd.to_datetime(df['dt_Venda'])

df['Mês'] = df['dt_Venda'].dt.strftime('%b').str.upper()

df['Categorias'] = df['Categorias'].str.upper()

df['Loja'] = df['Loja'].str.upper()

df['Produto'] = df['Produto'].str.upper()

df['Quantidade'] = df['Quantidade']

# Listas de apoio_______________________________________________________________________________________

lista_meses = []

for mes in df['Mês'].unique():
    lista_meses.append({
        'label': mes,
        'value': mes
    })
    
lista_meses.append({'label': 'Ano Completo', 'value' : 'ano'})

lista_categoria = []

for categoria in df['Categorias'].unique():
    lista_categoria.append({
        'label': categoria,
        'value': categoria
    })
    
lista_categoria.append({'label': 'Todas as Categorias', 'value' : 'Categorias'})

lista_loja = []

for loja in df['Loja'].unique():
    lista_loja.append({
        'label': loja,
        'value': loja
    })

lista_loja.append({'label': 'Todas as Lojas', 'value' : 'Lojas'})
  
lista_produto = []

for produto in df['Produto'].unique():
    lista_produto.append({
        'label': produto,
        'value': produto
    })

lista_produto.append({'label': 'Todos os Produtos', 'value' : 'Produtos'})


lista_quantidade = []

for quantidade in df['Quantidade'].unique():
    lista_quantidade.append({
        'label': quantidade,
        'value': quantidade
    })

lista_quantidade.append({'label': 'Quantidade de Produtos por Lojas', 'value' : 'Quantidade'})


# Fim **************************************************************************************************
# Função de apoio ______________________________________________________________________________________

def filtro_cliente(cliente_selecionado):
    if cliente_selecionado is None:
      return pd.Series(True, index=df.index)  
    else:
        return df['Cliente'] == cliente_selecionado
 


def filtro_mes(mes_selecionado):
    if mes_selecionado is None:
        return pd.Series(True, index=df.index)
    elif mes_selecionado =='ano':
        return df['Mês']
    return df['Mês'] == mes_selecionado



def filtro_categoria(categoria_selecionado):
    if categoria_selecionado is None:
        return pd.Series(True, index=df.index)
    elif categoria_selecionado =='Categorias':
        return df['Categorias']
    return df['Categorias'] == categoria_selecionado


def filtro_produto(produto_selecionado):
    if produto_selecionado is None:
        return pd.Series(True, index=df.index)
    elif produto_selecionado =='Produtos':
        return df['Produtos']
    return df['Produtos'] == produto_selecionado


def filtro_lojas(loja_selecionado):
    if loja_selecionado is None:
        return pd.Series(True, index=df.index)
    elif loja_selecionado =='Loja':
        return df['Loja']
    return df['Loja'] == loja_selecionado


def filtro_quantidade(quantidade_selecionada):
    if quantidade_selecionada is None:
        return pd.Series(True, index=df.index)
    elif quantidade_selecionada =='Lojas':
        return df['Quantidade']
    return df['Quantidade'] == quantidade_selecionada

# Criando App __________________________________________________________________________________________

app = dash.Dash(__name__)




# Montando Layout _______________________________________________________________________________________

linha_cabecalho = html.Div([
    html.Div([
        dcc.Dropdown(id='dropdown_clientes',
                    options=df['Cliente'].unique(),
                    placeholder='Selecione o nome do cliente',
                    style={
                        'font-family': 'Fira Code',
                        'color': '#101010'
                    }
            
        )
    ], style={'width': '25%'}),
    
    html.Div(
        html.Legend(
            'Miner Store', 
            style={'font-size': '150%', 'text-align' : 'center'}
        ),
        style={'width': '50%'}
    ),
    
    html.Div(ThemeSwitchAIO(
        aio_id='theme',
        themes=[
            url_dark, 
            url_vapor
            ]
    ), style={'width': '25%'}
             
    )
], style={
    'text-align': 'center',
    'display' : 'flex',
    'justify-content': 'center',
    'align-items' : 'center',
    'margin-top' : '20px'
})
    

linha_1 = html.Div([
    
    html.Div([
        html.H4(id='output_client'),
        dcc.Graph(id='Visual01')
    ],
    style={'text-align': 'center', 'width':'65%'}
    ), 
    
    html.Div([
        dbc.RadioItems(
        id='radio_meses',
        options=lista_meses,
        inline=True
    ),
    dbc.RadioItems (
        id='radio_categoria',
        options=lista_categoria,
        inline=True
    )
    ], style={
    'display': 'flex',
    'flex-direction' : 'column',
    'width': '30%',
    'justify-content' :'space-around'
    })

], style={
    
    'margin-top': '40px',
    'display' : 'flex',
    'justify-content' : 'space-around',
    'height': '300px'}
)


linha_2 = html.Div([
    
        dcc.Graph(id='visual02', style={'width' : '65%'}),
        dcc.Graph(id='visual03', style={'width' : '30%'})

], style={
    'display':'flex',
    'justify-content' : 'space-around',
    'height': '300px'
})



app.layout = html.Div([
    linha_cabecalho,
    linha_1,
    linha_2

])

# Callbacks _____________________________________________________________________________________________

@app.callback(
    Output('output_client', 'children'),
    Input('dropdown_clientes','value')
    
)

def atualizar_txt(cliente_selecionado):
    if cliente_selecionado:
        return f'Top5 Produtos comprados por: {cliente_selecionado}'
    return 'Top5 Produtos Vendidos!'
        

@app.callback(
    Output('Visual01', 'figure'),
    [
        Input('dropdown_clientes','value'),
        Input('radio_meses', 'value'),
        Input('radio_categoria', 'value'),
        Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
    ]
)


def visual01(cliente, mes,categoria,toggle):
    
    template = dark_tema if toggle else vapor_tema
    
    # if toggle:
    #     template = dark_tema
    # else:
    #     template =vapor_tema
    
    nome_cliente = filtro_cliente(cliente)
    nome_mes = filtro_mes(mes)
    nome_categoria = filtro_categoria(categoria)
    
    filtros = nome_cliente & nome_mes & nome_categoria
    
    df1 = df.loc[filtros]
    
    
    df_grupo = df1.groupby(['Produto', 'Categorias'])['Total'].sum().reset_index()
    df_top5 = df_grupo.sort_values(by='Total', ascending=False).head(5)
    
    fig1 = px.bar(
        df_top5,
        x='Produto',
        y='Total',
        text='Total',
        color_continuous_scale='Blues',
        height=280,
        template=template
    ) 
    
    fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    
    fig1.update_layout(
        margin={'t': 0},
        xaxis={'showgrid': False},
        yaxis={'showgrid': False,
               'range' : [ df_top5['Total'].min() * 0, df_top5['Total'].max() * 1.2]
        }, 
        xaxis_title=None,
        yaxis_title=None, 
        xaxis_tickangle=-15,
        font={'size':13},
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig1


@app.callback(
    Output('Visual02', 'figure'),
    [
        Input('loja', 'value'),
        Input('Quantidade', 'value'),
        Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
    ]
)


def visual02(loja,Quantidade,toggle):
    
    template = dark_tema if toggle else vapor_tema
    
    # if toggle:
    #     template = dark_tema
    # else:
    #     template =vapor_tema
    
    nome_loja = filtro_categoria(loja)
    
    filtros = nome_loja
    
    df2 = df.loc[filtros]
    
    
    df_grupo1 = df2.groupby(['Loja', 'Quantidade'])['Total'].sum().reset_index()
    df_top5 = df_grupo1.sort_values(by='Total', ascending=False).head(5)
    
    fig2 = px.bar(
        df_top5,
        x='Loja',
        y='Quantidade',
        text='Total',
        color_continuous_scale='Blues',
        height=280,
        template=template
    ) 
    
    fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    
    fig2.update_layout(
        margin={'t': 0},
        xaxis={'showgrid': False},
        yaxis={'showgrid': False,
               'range' : [ df_top5['Total'].min() * 0, df_top5['Total'].max() * 1.2]
        }, 
        xaxis_title=None,
        yaxis_title=None, 
        xaxis_tickangle=-15,
        font={'size':13},
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig2
# Subindo servidor_______________________________________________________________________________________

if __name__ =='__main__' : app.run_server(debug=True)