import pandas as pd

def contar_vendas_por_marca_categoria(arquivo_vendas, marca_escolhida, categoria_escolhida=None, periodo=None):
    # Ler o arquivo de vendas
    df_vendas = pd.read_excel(arquivo_vendas)
    
    # Filtrar as vendas para a marca escolhida
    vendas_marca_escolhida = df_vendas[df_vendas['Marca'] == marca_escolhida]
    
    # Se uma categoria foi especificada, filtrar as vendas para essa categoria
    if categoria_escolhida is not None:
        vendas_marca_escolhida = vendas_marca_escolhida[vendas_marca_escolhida['Categoria'] == categoria_escolhida]
    
    # Se um período foi especificado, filtrar as vendas para esse período
    if periodo is not None:
        vendas_marca_escolhida = vendas_marca_escolhida[(vendas_marca_escolhida['Data'] >= periodo[0]) & (vendas_marca_escolhida['Data'] <= periodo[1])]
    
    # Contar o número de vendas para a marca escolhida e, se especificada, para a categoria escolhida
    total_vendas = len(vendas_marca_escolhida)
    
    return total_vendas

def verificar_estoque_por_marca_categoria(arquivo_produtos, marca_escolhida, categoria_escolhida=None):
    # Ler o arquivo de produtos
    df_produtos = pd.read_excel(arquivo_produtos)
    
    # Filtrar os produtos para a marca escolhida
    produtos_marca_escolhida = df_produtos[df_produtos['MARCA'] == marca_escolhida]
    
    # Se uma categoria foi especificada, filtrar os produtos para essa categoria
    if categoria_escolhida is not None:
        produtos_marca_escolhida = produtos_marca_escolhida[produtos_marca_escolhida['CATEGORIA'] == categoria_escolhida]
    
    # Calcular o estoque total para a marca escolhida e, se especificada, para a categoria escolhida
    estoque_total = produtos_marca_escolhida['ESTOQUE'].sum()
    
    return estoque_total

# Substitua 'caminho/para/seu/arquivo_vendas.xlsx' pelo caminho do seu arquivo de vendas Excel
arquivo_vendas = 'C:\\Users\\anton\\OneDrive\\Documents\\GitHub\\aux_compras\\src\\vendas23.xlsx'

# Substitua 'caminho/para/seu/arquivo_produtos.xlsx' pelo caminho do seu arquivo de produtos Excel
arquivo_produtos = 'C:\\Users\\anton\\OneDrive\\Documents\\GitHub\\aux_compras\\src\\produtos.xlsx'

# Solicitar ao usuário a marca desejada
marca_escolhida = input("Digite a marca para ver a quantidade de vendas e estoque: ")

# Listar as categorias disponíveis para a marca escolhida
df_produtos = pd.read_excel(arquivo_produtos)
categorias_disponiveis = df_produtos[df_produtos['MARCA'] == marca_escolhida]['CATEGORIA'].unique()

print(f"Categorias disponíveis para a marca {marca_escolhida}:")
print("Todas")
for categoria in categorias_disponiveis:
    print(categoria)

# Solicitar ao usuário a categoria desejada
categoria_escolhida = input("Digite a categoria para ver a quantidade de vendas (ou 'Todas' para todas as categorias): ")

# Solicitar ao usuário se deseja ver as vendas do ano todo ou definir um período específico
opcao_periodo = input("Deseja ver as vendas do ano todo (A) ou definir um período específico (P)? ").upper()

if opcao_periodo == 'P':
    # Solicitar ao usuário o período específico
    data_inicio = input("Digite a data de início (no formato YYYY-MM-DD): ")
    data_fim = input("Digite a data de fim (no formato YYYY-MM-DD): ")
    periodo = (data_inicio, data_fim)
else:
    periodo = None

# Chamar as funções para calcular o número de vendas e o estoque disponível e imprimir os resultados
if categoria_escolhida.lower() == 'todas':
    tabela_resultados = []
    projecao_crescimento = float(input("Digite a projeção de crescimento (%) para todas as categorias: "))
    for categoria in categorias_disponiveis:
        total_vendas = contar_vendas_por_marca_categoria(arquivo_vendas, marca_escolhida, categoria, periodo)
        estoque_total = verificar_estoque_por_marca_categoria(arquivo_produtos, marca_escolhida, categoria)
        quantidade_minima_comprar = int(total_vendas * (1 + projecao_crescimento / 100)) - estoque_total
        if quantidade_minima_comprar < 0:
            quantidade_minima_comprar = 0
        tabela_resultados.append([categoria, total_vendas, estoque_total, quantidade_minima_comprar])

    # Imprimir tabela de resultados
    print("\nCategoria | Total Vendas | Estoque | Quantidade Mínima para Comprar")
    for linha in tabela_resultados:
        print("{:<40} | {:<12} | {:<7} | {:<30}".format(*linha))
else:
    total_vendas = contar_vendas_por_marca_categoria(arquivo_vendas, marca_escolhida, categoria_escolhida, periodo)
    estoque_total = verificar_estoque_por_marca_categoria(arquivo_produtos, marca_escolhida, categoria_escolhida)
    projecao_crescimento = float(input(f"Digite a projeção de crescimento (%) para a categoria {categoria_escolhida}: "))
    quantidade_minima_comprar = int(total_vendas * (1 + projecao_crescimento / 100)) - estoque_total
    if quantidade_minima_comprar < 0:
        quantidade_minima_comprar = 0
    print(f"Total de vendas para a marca {marca_escolhida} na categoria {categoria_escolhida}: {total_vendas}")
    print(f"Estoque disponível para a marca {marca_escolhida} na categoria {categoria_escolhida}: {estoque_total}")
    print(f"Quantidade mínima de peças a comprar para atingir a projeção de vendas: {quantidade_minima_comprar}")

