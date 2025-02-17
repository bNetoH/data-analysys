import os
import pandas as pd
import requests
import time
from datetime import datetime

# Define os diretórios
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Diretório raiz
processed_data_dir = os.path.join(base_dir, "data", "processed_data")  # Dados processados
normalized_data_dir = os.path.join(base_dir, "data", "normalized_data")  # Dados normalizados

# Garante que o diretório de saída existe
os.makedirs(normalized_data_dir, exist_ok=True)

# Arquivos de entrada e saída
arquivo_processado = os.path.join(processed_data_dir, "resultado.csv")
arquivo_normalizado = os.path.join(normalized_data_dir, "resultado.csv")

# Verifica se o arquivo processado existe
if not os.path.exists(arquivo_processado):
    print("Erro: O arquivo 'resultado.csv' não foi encontrado em 'data/processed_data'.")
else:
    # Carrega o CSV processado
    df = pd.read_csv(arquivo_processado)

    # Verifica se as colunas esperadas estão presentes
    colunas_necessarias = {"currency", "unit_price", "total_price", "discount_value"}
    if not colunas_necessarias.issubset(df.columns):
        print(f"Erro: O arquivo CSV não contém todas as colunas necessárias: {colunas_necessarias}")
    else:
        # Ordena o DataFrame pela coluna "currency"
        df = df.sort_values(by="currency")

        # Dicionário para armazenar cotações e timestamps
        cotacoes = {}

        # Função para buscar a cotação da moeda
        def obter_cotacao(moeda):
            """Retorna a taxa de conversão para USD e a data de obtenção."""
            if moeda == "USD":  # Se já estiver em dólares, não precisa converter
                return 1.0, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

            if moeda in cotacoes:  # Usa cache se já foi consultado
                return cotacoes[moeda]

            url = f"https://economia.awesomeapi.com.br/last/{moeda}-USD"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    key = f"{moeda}USD"
                    if key in data:
                        taxa = float(data[key]["bid"].replace(".",",")) # Valor de compra
                        timestamp = data[key]["create_date"]  # Data da cotação
                        cotacoes[moeda] = (taxa, timestamp)  # Salva no cache
                        time.sleep(1)  # Evita muitas requisições seguidas
                        return taxa, timestamp
            except Exception as e:
                print(f"Erro ao buscar cotação para {moeda}: {e}")

            return None, None  # Retorna None se não conseguir obter a cotação

        # Criamos três novas colunas
        df["currency_origin"] = df["currency"]  # Mantém a moeda original
        df["taxa"] = None
        df["timestamp_exchange"] = None  # Inicializa a coluna

        # Normaliza os valores monetários
        moeda_atual = None
        taxa_atual = None
        timestamp_atual = None

        for index, row in df.iterrows():
            moeda = row["currency"]

            # Se a moeda mudou, buscamos uma nova cotação
            if moeda != moeda_atual:
                moeda_atual = moeda
                taxa_atual, timestamp_atual = obter_cotacao(moeda)

            # Se conseguiu obter a taxa de conversão, realiza a conversão
            if taxa_atual:
                df.at[index, "unit_price"] = row["unit_price"] / taxa_atual
                df.at[index, "total_price"] = row["total_price"] / taxa_atual
                df.at[index, "discount_value"] = row["discount_value"] / taxa_atual
                df.at[index, "currency"] = "USD"  # Atualiza a moeda
                df.at[index, "taxa"] = taxa_atual
                df.at[index, "timestamp_exchange"] = timestamp_atual  # Salva o timestamp da cotação

        # Salva o novo arquivo normalizado
        df.to_csv(arquivo_normalizado, index=False)
        print(f"Arquivo normalizado salvo em: {arquivo_normalizado}")
