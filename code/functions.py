"""
Autor: Humberto C. Araújo
Project: Otimização de etapas em cartografia de paisagens
"""

#imports
import pandas as pd
import math
import geopandas as gpd
from shapely.geometry import Point
import PySimpleGUI as sg

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#função para abertura do arquivo csv e carga do DataFrame no main
#Entradas da função: nenhuma
#Retorno da função: dataframe codificado em utf-8
def open_csv(caminho_e_nome_r):

    #carga do csv em um DataFrame 
    df_main = pd.read_csv(caminho_e_nome_r, encoding='utf-8', sep=';')

    #retornando ao main o dataframe carregado
    return df_main

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Função para criação de arquivo do tipo geopackge baseando-se em um dataframe existente que será passado como parâmetro de entrada
#entradas da função: dataframe contendo colunas 'latitude' e 'longitude'
#Retrono da função: mensagem de confirmação
def creat_geopackge(df_entrada,caminho_e_nome_w):

    #Criação da geometria a ser utilizada na produção do arquivo shape, neste caso a geometria é do tipo Point, onde são passados como x,y respectivamente as coordenadas de longitude e latitude
    #extraidas do csv (OBS: o nome das colunas deve ser igual ao nome apresentado na coluna do dataframe de entrada, por isso utilizar o arquivo csv definido como padrão de entrada no programa)
    geometry = [Point(xy) for xy in zip(df_entrada['longitude'], df_entrada['latitude'])]

    #criação de dataframe contendo dados geográficos passando os parâmetros de geometria e dataframe de entrada da função
    gdf_point = gpd.GeoDataFrame(df_entrada, geometry= geometry)

    #chamada do método .to_file para criação do arquivo com base no geodataframe criado anteriormente
    gdf_point.to_file(r'{}'.format(caminho_e_nome_w+'.gpkg'), driver='GPKG', encoding= 'utf-8')

    

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Função para validar os dados do data frame
#Entrada fa função: dataframe
#Retorno da função: dataframe padrinizado
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

#Função para composição de sugestões de nomenclatura as parcelas coletadas em campo seguindo o método constante no livro de cartografia de paisagens (Cavalcanti,L.C.S, 2018)
#Entrada da função: Dataframe
#retorno da função: dataframe com adição da coluna paisagem com as sugestões de nomenclatura da paisagem
def paisagem_nome(df_entrada):

    df_nomear = df_entrada

    #etapa 01 criação de coluna no dataframe para acomodação da composição do nome da paisagem
    df_nomear['paisagem'] = None

    #etapa 02 preenchimento do data frame como a composição do nome da paisagem
    for i, row in df_nomear.iterrows():

        
        #Validando que a paisagem possua as informações mínimas a composição da paisagem em cada coluna de acordo com o padrão da ficha de campo e seus respectivos itens de menor tamaho
        if pd.isna(df_nomear['fisionomia'][i]) or len(df_nomear['fisionomia'][i]) < 7 or pd.isna(df_nomear['complementos'][i]) or len(df_nomear['complementos'][i]) < 5 or pd.isna(df_nomear['ambiente'][i]) or len(df_nomear['ambiente'][i]) < 4:


            df_nomear.loc[i,'paisagem'] = 'dados insuficentes para nomenclatura'

        else:

            #etapa 03 estrutura de decisão para definição das duas perturbações de maior impacto na paisagem
            
            #estruturação das variaveis do dataframe para montar estrutura de seleção e conversão
            estiagem = df_nomear['estiagem'][i]
            erosao = df_nomear['erosão'][i]
            fogo = df_nomear['fogo'][i]
            desmatamento = df_nomear['desmatamento'][i]
            pastoreio = df_nomear['pastoreio/herbivoria'][i]
            inundacao = df_nomear['inundação'][i]
            perturbacao_final = []

                
            ##teste de classificação para as duas perturbações mais influentes, começando pelo caso 0, onde nenhuma perturbação foi identificada
            if estiagem == 0 and erosao == 0 and fogo == 0 and desmatamento == 0 and pastoreio == 0 and inundacao == 0:

                perturbacao_final = 'sem perturbações visíveis'
            
            else:
                #para facilitar a seleção entre as 6 variáveis foi criado um dicionário que posteriomente será classificado e extraído os dois maiores valores
                seletor = {'estiagem': estiagem, 'erosão': erosao,'fogo': fogo, 'desmatamento': desmatamento, 'pastoreio/herbivoria': pastoreio, 'inundação': inundacao}

                seletor_ordenado = sorted(seletor.items(), key=lambda x: x[1], reverse=True)

                selec_final = seletor_ordenado[:2]
                selec_final_dicionario = dict(selec_final)
            
                #for para percorrer o dicionário contendo as perturbações de maior influência e substituir os valores numéricos da intensidade das pertubações
                #por valores de texto, bem como, adicionar esta composição a variável perturbacao_final
                for chave, n in selec_final_dicionario.items():

                    if n == 1:
                        texto_add = 'leve'
                        
                    elif n == 2:
                        texto_add = 'moderada'
                        
                    elif n == 3:
                        texto_add = 'severa'
                
                    else:
                        texto_add = 'ausente'
                    
                    perturbacao_final.append(f'{chave} {texto_add}')           

            #etapa 04 composição do nome e aplicação no dataframe em sua respectiva coluna 
            df_nomear.loc[i,'paisagem'] = str(df_nomear['fisionomia'][i]) + ' ' + str(df_nomear['complementos'][i]) + ' sobre ambiente ' + str(df_nomear['ambiente'][i]) + ', influenciado por ' + str(perturbacao_final[0])+ ' e '+ str(perturbacao_final[1])
        
    return df_nomear

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#função para coletar dados prévios para abertura de csv
#Entrada da função: nenhuma
#saída da função: caminho do arquivo e nome
def leitura_r():
    
    #variaveis de universo local
    caminho = ''
    nome = ''
    caminho_final = ''
    #layout de abertura
    layout_abertura = [
           [sg.Text('Digite o caminho onde o arquivo está armazenado(ex: C:\Pastas\pasta):')],
           [sg.InputText()],
           [sg.Text('Digite o nome do arquivo e a respectiva extensão:')],
           [sg.InputText()],
           [sg.Button('Ok'), sg.Button('Sair')]
           ]
    
    abertura = sg.Window('Abertura de arquivo CSV',layout_abertura)

    while True:

        event, values = abertura.read()
        if event == sg.WINDOW_CLOSED or event == 'Sair':
            abertura.close()
            break

        elif event == 'Ok':
            caminho = values[0]
            nome = values[1]


        # Executa a função 1 com os valores recebidos
        # Define o layout da segunda tela
        confirmacao = [
                    [sg.Text(f'O caminho do arquivo é: {caminho}')],
                    [sg.Text(f'O nome arquivo é: {nome}')],
                    [sg.Button('Voltar'), sg.Button('Ok')]]
        
        # Cria a janela da segunda tela
        confirma = sg.Window('Tela 2', confirmacao)

        # Loop para capturar as interações do usuário com a segunda tela
        while True:
            event, values = confirma.read()
            if event == sg.WINDOW_CLOSED or event == 'Ok':
                confirma.close()
                break
            elif event == 'Voltar':
                # Fecha a janela da segunda tela e volta para a primeira tela
                confirma.close()
                break
        # Fecha a janela da primeira tela
        abertura.close()

        caminho_final = r'{}'.format(caminho+'/'+nome)
    
        return caminho_final

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#função para coletar dados prévios para salvamento 
#Entrada da função: nenhuma
#saída da função: caminho do arquivo e nome para salvamento
def salvar_w():
    
    #variaveis de universo local
    caminho = ''
    nome = ''

    #layout de abertura
    layout_salvamento = [
           [sg.Text('Digite o caminho onde deseja salvar o arquivo GEOPACKAGE(ex: C:\Pastas\pasta):')],
           [sg.InputText()],
           [sg.Text('Digite o nome que deseja colocar no GEOPACKAGE:')],
           [sg.InputText()],
           [sg.Button('Ok'), sg.Button('Sair')]
           ]
    
    salvamento = sg.Window('Salvar em GEOPACKAGE',layout_salvamento)

    while True:

        event, values = salvamento.read()
        if event == sg.WINDOW_CLOSED or event == 'Sair':
            salvamento.close()
            break

        elif event == 'Ok':
            caminho = values[0]
            nome = values[1]

        # Executa a função 1 com os valores recebidos
        # Define o layout da segunda tela
        confirmacao = [
                    [sg.Text(f'O caminho do arquivo será: {caminho}')],
                    [sg.Text(f'O nome arquivo será: {nome}')],
                    [sg.Button('Voltar'), sg.Button('Ok')]]
        
        # Cria a janela da segunda tela
        confirma = sg.Window('Tela 2', confirmacao)

        # Loop para capturar as interações do usuário com a segunda tela
        while True:
            event, values = confirma.read()
            if event == sg.WINDOW_CLOSED or event == 'Ok':
                confirma.close()
                break
            elif event == 'Voltar':
                # Fecha a janela da segunda tela e volta para a primeira tela
                confirma.close()
                break
        # Fecha a janela da primeira tela
        salvamento.close()

        caminho_final = r'{}'.format(caminho+'/'+nome)
    
        return caminho_final
