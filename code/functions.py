"""
Autor: Humberto C. Araújo
Project: Otimização de etapas em cartografia de paisagens
"""

#imports
import pandas as pd
import geopandas as gpd
from shapely.geometry import point

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

    geometry = [Point(xy) for xy in zip(df_entrada['longitude'], df_entrada['latitude'])]

    gdf_point = gpd.GeoDataFrame(df_entrada, geometry= geometry)

    gdf_point.to_file(r'C:\Users\beto\Desktop\Estudos_ETL\projeto\shape_teste\arquivo_shapefile.shp', driver='ESRI Shapefile')


df_teste = pd.read_csv( r'C:\Users\beto\Desktop\Estudos_ETL\projeto\teste_shape.csv',sep=';',encoding='ISO-8859-1')

creat_shape(df_teste)

