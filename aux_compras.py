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

# Local arquivo vendas
arquivo_vendas = 'C:\\Users\\anton\\OneDrive\\Documents\\GitHub\\aux_compras\\src\\vendas23.xlsx'

# Local arquivo produtos
arquivo_produtos = 'C:\\Users\\anton\\OneDrive\\Documents\\GitHub\\aux_compras\\src\\produtos.xlsx'

# Solicitar ao usuário a marca desejada
marca_escolhida = input("Digite a marca para ver a quantidade de vendas e estoque: ")

# Listar as categorias disponíveis para a marca escolhida
df_produtos = pd.read_excel(arquivo_produtos)
categorias_disponiveis = df_produtos[df_produtos['MARCA'] == marca_escolhida]['CATEGORIA'].unique()

print(f"Categorias disponíveis para a marca {marca_escolhida}: {categorias_disponiveis}")

# Solicitar ao usuário a categoria desejada
categoria_escolhida = input("Digite a categoria para ver a quantidade de vendas: ")

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
total_vendas = contar_vendas_por_marca_categoria(arquivo_vendas, marca_escolhida, categoria_escolhida, periodo)
estoque_total = verificar_estoque_por_marca_categoria(arquivo_produtos, marca_escolhida, categoria_escolhida)

if periodo is None:
    print(f"Total de vendas para a marca {marca_escolhida} na categoria {categoria_escolhida} durante o ano todo: {total_vendas}")
else:
    print(f"Total de vendas para a marca {marca_escolhida} na categoria {categoria_escolhida} no período de {periodo[0]} a {periodo[1]}: {total_vendas}")

print(f"Estoque disponível para a marca {marca_escolhida} na categoria {categoria_escolhida}: {estoque_total}")

# Calcular a projeção de crescimento e a quantidade mínima de peças a comprar
if total_vendas > 0:
    projecao_crescimento = float(input("Digite a projeção de crescimento (%) para o próximo ano: "))
    quantidade_minima_comprar = int(total_vendas * (1 + projecao_crescimento / 100)) - estoque_total
    if quantidade_minima_comprar < 0:
        quantidade_minima_comprar = 0
    print(f"Quantidade mínima de peças a comprar para atingir a projeção de vendas: {quantidade_minima_comprar}")
else:
    print("Não houve vendas para esta categoria no período especificado.")
