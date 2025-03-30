import os
import pandas as pd

def save_dataframe_to_csv(df, path, title):
    """
    Salva um DataFrame como CSV no caminho especificado com o título dado.

    :param df: pd.DataFrame - O DataFrame a ser salvo.
    :param path: str - O caminho do diretório onde o arquivo será salvo.
    :param title: str - O título (nome) do arquivo CSV.
    """
    title_path = title.split(" - ")[0]
    datetime_now = title.rsplit(" - ", 1)[-1]
    path_silver = os.path.join(path, "silver", datetime_now, title_path)

    os.makedirs(path_silver, exist_ok=True)
    file_path = os.path.join(path_silver, f"{title}.csv")
    
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"Arquivo salvo com sucesso em: {file_path}")