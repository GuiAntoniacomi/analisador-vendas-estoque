import pandas as pd
# Local do arquivo de produtos
arquivo_produtos = 'C:\\Users\\anton\\OneDrive\\Documents\\GitHub\\aux_compras\\src\\produtos.xlsx'

# Escolha da marca
marca_escolhida = input("Digite a marca para ver a quantidade de vendas e estoque: ").strip().capitalize()

# Listar as categorias disponíveis para a marca escolhida
df_produtos = pd.read_excel(arquivo_produtos)
categorias_disponiveis = df_produtos[df_produtos['MARCA'] == marca_escolhida]['CATEGORIA'].unique()

marca_escolhida = input("Digite a marca para ver a quantidade de vendas e estoque: ").strip().capitalize()
print(f"Marca escolhida: {marca_escolhida}")

print(f"Categorias disponíveis para a marca {marca_escolhida}:")
print("Todas")
for categoria in categorias_disponiveis:
    print(categoria)
