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
        produtos_marca_escolhida = produtos_marca_escolhida[df_produtos['CATEGORIA'] == categoria_escolhida]
    
    # Calcular o estoque total para a marca escolhida e, se especificada, para a categoria escolhida
    estoque_total = produtos_marca_escolhida['ESTOQUE'].sum()
    
    return estoque_total

# Local do arquivo de vendas
arquivo_vendas = 'C:\\Users\\anton\\OneDrive\\Documents\\GitHub\\aux_compras\\src\\vendas23.xlsx'

# Local do arquivo de produtos
arquivo_produtos = 'C:\\Users\\anton\\OneDrive\\Documents\\GitHub\\aux_compras\\src\\produtos.xlsx'

# Escolha da marca
marca_escolhida = input("Digite a marca para ver a quantidade de vendas e estoque: ").strip().title()

# Listar as categorias disponíveis para a marca escolhida
df_produtos = pd.read_excel(arquivo_produtos)
categorias_disponiveis = df_produtos[df_produtos['MARCA'] == marca_escolhida]['CATEGORIA'].unique()

print(f"Categorias disponíveis para a marca {marca_escolhida}:")
print("Todas")
for categoria in categorias_disponiveis:
    print(categoria)

# Solicitar ao usuário a categoria desejada
categoria_escolhida = input("Digite a categoria para ver a quantidade de vendas (ou 'Todas' para todas as categorias): ").strip().capitalize()

# Solicitar ao usuário se deseja ver as vendas do ano todo ou definir um período específico
opcao_periodo = input("Deseja ver as vendas do ano todo (A) ou definir um período específico (P)? ").strip().upper()

if opcao_periodo == 'P':
    # Solicitar ao usuário o período específico
    data_inicio = input("Digite a data de início (no formato YYYY-MM-DD): ").strip()
    data_fim = input("Digite a data de fim (no formato YYYY-MM-DD): ").strip()
    periodo = (data_inicio, data_fim)
else:
    periodo = None

# Chamar as funções para calcular o número de vendas e o estoque disponível e imprimir os resultados
if categoria_escolhida.lower() == 'todas':
    tabela_resultados = []
    projecao_crescimento = float(input("Digite a projeção de crescimento (%) para todas as categorias: ").strip())
    for categoria in categorias_disponiveis:
        total_vendas = contar_vendas_por_marca_categoria(arquivo_vendas, marca_escolhida, categoria, periodo)
        estoque_total = verificar_estoque_por_marca_categoria(arquivo_produtos, marca_escolhida, categoria)
        quantidade_minima_comprar = int(total_vendas * (1 + projecao_crescimento / 100)) - estoque_total
        vendas_projecao = total_vendas + int(total_vendas * projecao_crescimento / 100)
        if quantidade_minima_comprar < 0:
            quantidade_minima_comprar = 0
        tabela_resultados.append([categoria, total_vendas, estoque_total, vendas_projecao, quantidade_minima_comprar])

    # Imprimir tabela de resultados
    print("\nCategoria                                        | Total Vendas 23 | Estoque Atual | Vendas com Projeção | Quantidade Mínima para Comprar")
    for linha in tabela_resultados:
        print("{:<50} | {:<12} | {:<7} | {:<30} | {:<20}".format(*linha))

else:
    total_vendas = contar_vendas_por_marca_categoria(arquivo_vendas, marca_escolhida, categoria_escolhida, periodo)
    estoque_total = verificar_estoque_por_marca_categoria(arquivo_produtos, marca_escolhida, categoria_escolhida)
    projecao_crescimento = float(input("Digite a projeção de crescimento (%) para a categoria escolhida: ").strip())
    vendas_projecao = total_vendas + int(total_vendas * projecao_crescimento / 100)
    quantidade_minima_comprar = max(0, int(total_vendas * (1 + projecao_crescimento / 100)) - estoque_total)

    # Imprimir tabela de resultados
    print("\nCategoria                                        | Total Vendas 23 | Estoque Atual | Vendas com Projeção | Quantidade Mínima para Comprar")
    print("{:<50} | {:<12} | {:<7} | {:<30} | {:<20}".format(categoria_escolhida, total_vendas, estoque_total, vendas_projecao, quantidade_minima_comprar))

# Perguntar ao usuário se deseja salvar os resultados em um arquivo Excel
opcao_salvar_excel = input("Deseja salvar os resultados em um arquivo Excel? (S/N): ").strip().upper()
if opcao_salvar_excel == 'S':
    if categoria_escolhida.lower() == 'todas':
        nome_arquivo_excel = input("Digite o nome do arquivo Excel para salvar os resultados (incluindo .xlsx): ").strip()
    else:
        nome_arquivo_excel = f"{categoria_escolhida.lower().replace(' ', '_')}_{marca_escolhida.lower().replace(' ', '_')}.xlsx"

    df_resultados = pd.DataFrame(tabela_resultados if categoria_escolhida.lower() == 'todas' else [[categoria_escolhida, total_vendas, estoque_total, vendas_projecao, quantidade_minima_comprar]], columns=["Categoria", "Total Vendas 23", "Estoque Atual", "Vendas com Projeção", "Quantidade Mínima para Comprar"])
    df_resultados.to_excel(nome_arquivo_excel, index=False, engine='openpyxl')
    print(f"Os resultados foram salvos no arquivo {nome_arquivo_excel}.")
