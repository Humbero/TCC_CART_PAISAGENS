import functions as fc
import pandas as pd

df_inicial = pd.read_csv(r'{}'.format('C:\TCC\PADRAO_DE_CARGA_new.csv'), encoding='UTF-8', sep=';')

print(df_inicial.head(5))
print(2*'\n')

df_padrao = fc.validar_dados_df(df_inicial)

print(df_padrao.head(5))

df_rename = fc.paisagem_nome(df_padrao)

print(3*'\n' + 'df_nomeado\n')
print(df_rename.head(5))