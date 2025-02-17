import os
import pandas as pd

# Define os diretórios fixos
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Diretório raiz
raw_data_dir = os.path.join(base_dir, "data", "raw_data")  # Diretório das amostras CSV
processed_data_dir = os.path.join(base_dir, "data", "processed_data")  # Diretório para salvar o resultado

# Garante que o diretório de saída existe
os.makedirs(processed_data_dir, exist_ok=True)

# Lista todos os arquivos CSV no diretório raw_data
arquivos_csv = [f for f in os.listdir(raw_data_dir) if f.endswith(".csv")]

# Verifica se há arquivos CSV
if not arquivos_csv:
    print("Nenhum arquivo CSV encontrado em 'data/raw_data'.")
else:
    # Lê o primeiro arquivo para obter os nomes das colunas
    primeiro_arquivo = os.path.join(raw_data_dir, arquivos_csv[0])
    print(f"Lendo primeiro arquivo (mantendo cabeçalho): {arquivos_csv[0]}")
    df_base = pd.read_csv(primeiro_arquivo)
    colunas = df_base.columns  # Captura os nomes das colunas

    # Lista para armazenar os DataFrames
    dfs = [df_base]

    # Lê os arquivos restantes, garantindo que tenham as mesmas colunas
    for arquivo in arquivos_csv[1:]:
        caminho_completo = os.path.join(raw_data_dir, arquivo)
        print(f"Lendo arquivo (garantindo colunas consistentes): {arquivo}")
        df = pd.read_csv(caminho_completo, names=colunas, header=0)  # Mantém as colunas consistentes
        dfs.append(df)

    # Concatena todos os DataFrames
    df_final = pd.concat(dfs, ignore_index=True)

    # Define o nome do arquivo de saída
    resultado_csv = os.path.join(processed_data_dir, "resultado.csv")

    # Salva o resultado
    df_final.to_csv(resultado_csv, index=False)

    print(f"Arquivo final salvo em: {resultado_csv}")
