"""
Autor: Humberto C. Araújo
Project: Otimização de etapas em cartografia de paisagens
"""

#imports
import pandas as pd
#import pandera as pa
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
    df_main = pd.read_csv(caminho_final, encoding='utf-16', sep=',')

    #retornando ao main o dataframe carregado
    return df_main

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Função para criação de arquivo do tipo shapefile baseando-se em um dataframe existente que será passado como parâmetro de entrada
def creat_shape(df_entrada):

    #Criação da geometria a ser utilizada na produção do arquivo shape, neste caso a geometria é do tipo Point, onde são passados como x,y respectivamente as coordenadas de longitude e latitude
    #extraidas do csv (OBS: o nome das colunas deve ser igual ao nome apresentado na coluna do dataframe de entrada, por isso utilizar o arquivo csv definido como padrão de entrada no programa)
    geometry = [Point(xy) for xy in zip(df_entrada['longitude'], df_entrada['latitude'])]

    #criação de dataframe contendo dados geográficos passando os parâmetros de geometria e dataframe de entrada da função
    gdf_point = gpd.GeoDataFrame(df_entrada, geometry= geometry)

    #obetenção do nome do arquivo
    caminho_shp = input('Digite o caminho onde deseja salvar o arquivo, ex: C:\pasta_x\pasta_b: ')
    nome_shp = input('Digite o nome que deseja dar ao arquivo do tipo shapefile: ')

    #chamada do método .to_file para criação do arquivo com base no geodataframe criado anteriormente
    gdf_point.to_file(r'{}'.format(caminho_shp + '/'+ nome_shp), driver='ESRI Shapefile', encoding= 'utf-16-le', bom=True)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Função para validar os dados do data frame
def validar_dados_df(df_validacao):

    df_valido = df_validacao

    #etapa 01: colocar todos os títulos de colunas em letras minúsculas para evitar problemas de processamento futuro
    df_valido.columns = [col.lower() for col in df_valido.columns]

    #etapa 02: converter todos as ',' em '.' nas colunas latitude e longitude
    df_valido['longitude'] = df_valido['longitude'].str.replace(',','.')
    df_valido['latitude'] = df_valido['latitude'].str.replace(',','.')

    #etapa 03: garantir que as colunas latitude e longitude esejam do tipo float e que a coluna parcela seja do tipo inteiro
    df_valido['longitude'] = df_valido['longitude'].astype(float)
    df_valido['latitude'] = df_valido['latitude'].astype(float)
    df_valido['parcela'] = df_valido['parcela'].astype(int)

    #etapa 04: colocar todos os dados do tipo string do data frame em letras minúsculas
    df_valido = df_valido.applymap(lambda s: s.lower() if type(s) == str else s)

    return df_valido

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




#trecho de código exclusivamente utilizado para testas as funções implementadas




