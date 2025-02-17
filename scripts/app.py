import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Definir diretórios
DATA_DIR = "data/processed_data"
NORMALIZED_DIR = "data/normalized_data"

# Criar diretórios caso não existam
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(NORMALIZED_DIR, exist_ok=True)

st.set_page_config(layout="wide")

# Título da aplicação
st.title("ETL de Vendas - Meganium")

# Botões para execução dos scripts
if st.button("Executar Extração"):
    st.write("Executando extração...")
    os.system("python scripts/extraction.py")
    st.success("Extração concluída!")

if st.button("Executar Transformação"):
    st.write("Executando transformação...")
    os.system("python scripts/transformation.py")
    st.success("Transformação concluída!")

if st.button("Limpar arquivos processados"):
    st.write("Executando limpeza...")
    os.system("python scripts/cleanup.py")
    st.success("Limpeza concluída!")

# Carregar dados processados
st.subheader("Visualização dos Dados")
file_path = os.path.join(NORMALIZED_DIR, "resultado.csv")
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    
    # Exibir dados em tabela
    st.write("### Tabela de Dados Normalizados")
    st.dataframe(df)
    
    # Adicionar a coluna net_price
    df["net_price"] = df["total_price"] - df["discount_value"]    

    col1, col2 = st.columns([2, 2])

    with col1:
        # Gráfico de Barras - Quantidade e Preço Total por País de Entrega
        st.write("### Gráfico de Vendas por País de Entrega")
        fig, ax = plt.subplots()
        df_grouped_delivery = df.groupby("delivery_country")[["quantity", "total_price", "net_price"]].sum()
        df_grouped_delivery.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    with col2:
        # Gráfico de Barras - Quantidade e Preço Total por Site
        st.write("### Gráfico de Vendas por Plataforma")
        fig, ax = plt.subplots()
        df_grouped = df.groupby("site")[["quantity", "total_price", "net_price"]].sum()
        df_grouped.plot(kind="bar", ax=ax)
        st.pyplot(fig)
    
else:
    st.warning("Arquivo normalizado não encontrado. Execute a transformação primeiro.")
