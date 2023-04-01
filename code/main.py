"""
Autor: Humberto C. Araújo
Project: Otimização de etapas em cartografia de paisagens
"""

#imports
import functions as fun
import pandas as pd


df_abertura = pd.read_csv(r'C:\TCC_ETL_CART_PAISAGENS\CSV_TCC_V0013.csv', sep=',',encoding='utf-16')

#df_abertura = fun.open_csv()

print(df_abertura.head(4))



df_validado = fun.validar_dados_df(df_abertura)

print(df_validado.head(5))

fun.creat_shape(df_validado)