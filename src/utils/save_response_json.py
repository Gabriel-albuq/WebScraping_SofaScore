import os
import json

def save_response_to_json(data, path, title):
    """
    Salva dados em formato JSON no caminho especificado com o título dado.

    :param data: dict ou qualquer objeto serializável - Os dados a serem salvos no formato JSON.
    :param path: str - O caminho do diretório onde o arquivo será salvo.
    :param title: str - O título (nome) do arquivo JSON.
    """
    path_bronze = os.path.join(path, "bronze")

    # Garante que o caminho exista
    os.makedirs(path_bronze, exist_ok=True)
    
    # Concatena o caminho com o título e a extensão .json
    file_path = os.path.join(path_bronze, f"{title}.json")
    
    # Salva os dados como JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Arquivo JSON salvo com sucesso em: {file_path}")