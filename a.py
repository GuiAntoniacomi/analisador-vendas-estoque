import pandas as pd

# Nome do arquivo Excel que contém as vendas
arquivo_excel = 'src\\vendas23.xlsx'

# Carrega o arquivo Excel em um DataFrame
df = pd.read_excel(arquivo_excel)

# Exibe as colunas presentes no DataFrame
print("Colunas presentes no DataFrame:")
print(df.columns)
