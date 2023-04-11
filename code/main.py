"""
Autor: Humberto C. Araújo
Project: Otimização de etapas em cartografia de paisagens
"""

#imports
import functions as fun
import PySimpleGUI as sg

#variáveis do universo
caminho_abertura = ''
caminho_salvamento = ''
df_carga = ''
df_padronizado = ''
df_rename = ''

#interfaces
layout_menu = [
          [sg.Text('Bem vindo a ferramento de otimização de etapas em cartogafia de paisagens')],
          [sg.Text('Escolha uma função:')],
          [sg.Text('Carregar dados do ficha sugerida em CSV e realizar a padronização dos dados:')],
          [sg.Button('Carregar arquivo')],
          [sg.Text('Aplicar sugestões de nome a paisagem baseado na proposta de Cavalcanti,L.C.,2018:')],
          [sg.Button('Sugerir nome da paisagem e salvar')],
          [sg.Text('Cria arquivo GEOPACKGE sem a aplicação da metodologia:')],
          [sg.Button('Salvar como GEOPACKGE direto do arquivo carregado')],
          [sg.Button('Sair')]
          ]

window = sg.Window('Minha janela', layout_menu)



#menu principal com telas
while True:

    event, values = window.read()
    #casos de interrução
    if event == sg.WINDOW_CLOSED or event == 'Sair':
        break
    
    #procedimento de carga do arquivo
    elif event == 'Carregar arquivo':
    
        caminho_abertura = fun.leitura_r()
        df_carga = fun.open_csv(caminho_abertura)
        df_padronizado = fun.validar_dados_df(df_carga)
       
    #salvamento com sugestão de nome
    elif event == 'Sugerir nome da paisagem e salvar':

        df_rename = fun.paisagem_nome(df_padronizado)
        caminho_salvamento = fun.salvar_w()
        fun.creat_geopackge(df_rename,caminho_salvamento)

    #salvamento sem sugestão de nome
    elif event == 'Salvar como GEOPACKGE direto do arquivo carregado':
        
        caminho_salvamento = fun.salvar_w()
        fun.creat_geopackge(df_padronizado,caminho_salvamento)



