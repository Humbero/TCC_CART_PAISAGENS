"""
Autor: Humberto C. Araújo
Project: Otimização de etapas em cartografia de paisagens
"""

#imports
import pandas as pd
import pandera as pa
import re
import geopandas as gpd
from shapely.geometry import Point

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#função para abertura do arquivo csv e carga do DataFrame no main
def open_csv():

    #variáveis de uso
    df_main = 0
    validador = True
    caminho_final = 0

    #definição e teste do caminho e nome do arquivo a ser carregado
    while  validador == True:

        print('Para a carga do arquivo .CSV precisaremos de algumas informações, favor preecher com atenção!')
        caminho_temp = input('Digite o caminho da pasta onde o arquivo foi armazenado, exempo de caminho: C:\pasta_de_joão\desktop\pasta_projeto \nDigite o caminho da pasta:  ')
        nome_arquivo = input('Forneca o nome do arquivo com sua extensão, exemplo: arquivo_x.csv \nDigite o nome do arquivo: ')

        #confirmação dos dados
        print('Favor confirme se o caminh do arquivo é: '+caminho_temp+' e o nome do arquivo é:  '+nome_arquivo)

        confirma = input('Digite C para confirmar ou  A para alterar os dados: ')

        if confirma in 'Cc':

            #utilizada a função r'{}'.format para tornar o o caminho final do tipo string real, sem que a barra invertida pudesse comprometer o resutlado de construção do código
            caminho_final =r'{}'.format(caminho_temp  +'/'+ nome_arquivo) 
            
            validador = False

    #carga do csv em um DataFrame 
    #OBS: foi utilizado o encoding ISO-8859-1 pois o utf-8 não estava conseguindo decodificar os caracteres especiais da língua portuguesa.
    df_main = pd.read_csv(caminho_final, encoding='ISO-8859-1', sep=';')

    #retornando ao main o dataframe carregado
    return df_main

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Função para criação de arquivo do tipo shapefile baseando-se em um dataframe existente que será passado como parâmetro de entrada
def creat_shape(df_entrada):

    #Criação da geometria a ser utilizada na produção do arquivo shape, neste caso a geometria é do tipo Point, onde são passados como x,y respectivamente as coordenadas de longitude e latitude
    #extraidas do csv (OBS: o nome das colunas deve ser igual ao nome apresentado na coluna do dataframe de entrada, por isso utilizar o arquivo csv definido como padrão de entrada no programa)
    geometry = [Point(xy) for xy in zip(df_entrada['LONGITUDE'], df_entrada['LATITUDE'])]

    #criação de dataframe contendo dados geográficos passando os parâmetros de geometria e dataframe de entrada da função
    gdf_point = gpd.GeoDataFrame(df_entrada, geometry= geometry)

    #chamada do método .to_file para criação do arquivo com base no geodataframe criado anteriormente
    gdf_point.to_file(r'C:\TCC_ETL_CART_PAISAGENS\teste_abertura_csv.shp', driver='ESRI Shapefile')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Função para validar os dados do data frame
def validar_dados_df(df_validacao):


    #Alteração dos dados de latitude e longitude para adoção do ponto como marcador de unidade no dataframe fornecido a função
    df_validacao['Longitude'] = df_validacao['Longitude'].str.replace(',','.')


    schema = pa.DataFrameSchema(

        columns= {
        
            'Parcela': pa.Column(pa.Int),
            'Latitude': pa.Column(pa.Float),
            'Longitude': pa.Column(pa.Float),
            'Fisionomia': pa.Column(pa.String),
            'Complementos': pa.Column(pa.String),
            'Ambiente': pa.Column(pa.String),
            'Lenhosa dominante': pa.Column(pa.String),
            'Herbacea dominante': pa.Column(pa.String),
            'Estiagem': pa.Column(pa.String, nullable=True),
            'Erosao': pa.Column(pa.String, nullable=True),
            'Fogo': pa.Column(pa.String, nullable=True),
            'Desmatamento': pa.Column(pa.String, nullable=True),
            'Pastoreio/herbivoria': pa.Column(pa.String, nullable=True),
            'Inundacao': pa.Column(pa.String, nullable=True),
            'Observacao': pa.Column(pa.String, nullable=True)
        
            }


    )



#trecho de código exclusivamente utilizado para testas as funções implementadas
df_teste = pd.read_csv( r'C:\TCC_ETL_CART_PAISAGENS\teste_abertura_csv.csv',sep=',',encoding='ISO-8859-1')

df_teste['LONGITUDE'] = df_teste['LONGITUDE'].str.replace(',', '.')
df_teste['LATITUDE'] = df_teste['LATITUDE'].str.replace(',', '.')




