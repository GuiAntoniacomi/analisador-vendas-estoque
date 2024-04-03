import pandas as pd

def obter_sku_filho(sku_pai, arquivo_excel):
    df = pd.read_excel(arquivo_excel)
    sku_filho = df[df['SKU Pai'] == sku_pai]['SKU Filho'].unique()
    return sku_filho

def contar_vendas_por_sku(sku, arquivo_excel):
    df = pd.read_excel(arquivo_excel)
    vendas_sku = df[df['SKU Filho'] == sku]
    return vendas_sku.shape[0]

def data_primeira_venda(sku, arquivo_excel):
    df = pd.read_excel(arquivo_excel)
    vendas_sku = df[df['SKU Filho'] == sku]
    if vendas_sku.empty:
        return "Nenhuma venda encontrada para este SKU Filho."
    primeira_venda = vendas_sku['Data'].min().strftime('%d/%m/%Y')
    return primeira_venda

def data_ultima_venda(sku, arquivo_excel):
    df = pd.read_excel(arquivo_excel)
    vendas_sku = df[df['SKU Filho'] == sku]
    if vendas_sku.empty:
        return "Nenhuma venda encontrada para este SKU Filho."
    ultima_venda = vendas_sku['Data'].max().strftime('%d/%m/%Y')
    return ultima_venda

def calcular_duracao_vendas(sku, arquivo_excel):
    df = pd.read_excel(arquivo_excel)
    vendas_sku = df[df['SKU Filho'] == sku]
    if vendas_sku.empty:
        return "Nenhuma venda encontrada para este SKU Filho."
    primeira_venda = vendas_sku['Data'].min()
    ultima_venda = vendas_sku['Data'].max()
    duracao_vendas = (ultima_venda - primeira_venda).days
    return duracao_vendas

def mostrar_categorias_por_marca(marca, arquivo_excel):
    df = pd.read_excel(arquivo_excel)
    categorias = df[df['Marca'] == marca]['Categoria'].unique()
    if categorias.size > 0:
        return categorias.tolist()
    else:
        return []

    
# Nome do arquivo Excel que contém as vendas
arquivo_excel = 'src\\vendas23.xlsx'

# Pergunta ao usuário se ele deseja procurar pelo SKU Pai ou pela Marca
opcao = input("Deseja procurar por SKU Pai ou por Marca? Digite 'SKU' para SKU Pai ou 'Marca' para Marca: ")

if opcao.lower() == 'sku':
    # SKU Pai que você deseja pesquisar
    sku_pai = int(input("Digite o SKU Pai que deseja pesquisar: "))

    # Obtém os SKU Filho do SKU Pai
    skus_filho = obter_sku_filho(sku_pai, arquivo_excel)

    # Loop para cada SKU Filho
    for sku_filho in skus_filho:
        # Chama a função para calcular a duração das vendas do SKU Filho fornecido
        duracao_vendas_sku_filho = calcular_duracao_vendas(sku_filho, arquivo_excel)

        # Chama a função para contar as vendas do SKU Filho fornecido
        total_vendas_sku_filho = contar_vendas_por_sku(sku_filho, arquivo_excel)

        # Exibe o total de vendas do SKU Filho fornecido
        print(f"Total de vendas do SKU Filho {sku_filho}: {total_vendas_sku_filho}")

        # Exibe a duração das vendas do SKU Filho fornecido
        if isinstance(duracao_vendas_sku_filho, int):
            primeira_venda = data_primeira_venda(sku_filho, arquivo_excel)
            ultima_venda = data_ultima_venda(sku_filho, arquivo_excel)
            print(f"A primeira venda desse produto ocorreu em {primeira_venda} e a última em {ultima_venda}. Duração: {duracao_vendas_sku_filho} dias")
        else:
            print(duracao_vendas_sku_filho)

elif opcao.lower() == 'marca':
    # Marca que você deseja pesquisar
    marca = input("Digite a marca que deseja pesquisar: ")

    # Mostra todas as categorias existentes da marca
    categorias = mostrar_categorias_por_marca(marca, arquivo_excel)
    if categorias:
        print(f"Categorias da marca {marca}: {', '.join(categorias)}")


    else:
        print(f"Nenhuma categoria encontrada para a marca {marca}.")
else:
    print("Opção inválida. Por favor, digite 'SKU' ou 'Marca'.")
