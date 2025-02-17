import os

# Define os diretórios
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Diretório raiz
processed_data_dir = os.path.join(base_dir, "data", "processed_data")  # Dados processados
normalized_data_dir = os.path.join(base_dir, "data", "normalized_data")  # Dados normalizados

dirs = [processed_data_dir, normalized_data_dir]

for dir in dirs:
    files = os.listdir(dir)
    for file in files:
        if file == "resultado.csv":
            file_path = os.path.join(dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removido: {file_path}")
            else:
                print(f"Arquivo não encontrado: {file_path}")