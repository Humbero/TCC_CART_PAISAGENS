"""
Autor: Humberto C. Araújo
Project: Otimização de etapas em cartografia de paisagens
"""

#imports
import functions as fun
import pandas as pd


df_abertura = pd.read_csv(r'C:\TCC\TCC_CART_PAISAGENS\CSV_TCC_V0013.csv', sep=',',encoding='utf-16')

#df_abertura = fun.open_csv()

print(df_abertura.head(4))



df_validado = fun.validar_dados_df(df_abertura)

print(df_validado.head(5))
print(df_validado.dtypes)

df_nomeado = fun.paisagem_nome(df_validado)

print(df_nomeado.head(5))
df_nomeado.to_csv('C:\TCC\TCC_CART_PAISAGENS\df_nomeado.csv', index=False)
