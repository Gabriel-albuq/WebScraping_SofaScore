import os
import sys
import json
import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_dir)

from src.utils.create_engine_postgres import create_engine_postgres

def update_json_postgres(table_name, schema, json_path):
    engine = create_engine_postgres(see_echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = MetaData(schema=schema)
    Json_Table = Table(table_name, metadata, autoload_with=engine)

    parent_folder = os.path.basename(os.path.dirname(json_path))
    file_name = f"{parent_folder}/{os.path.basename(json_path)}"

    with open(json_path, "r", encoding="utf-8") as f:
        file_json = json.load(f)

    try:
        with Session() as session:
            session.execute(
                Json_Table.insert().values(
                    name_file=file_name,
                    file_json=file_json
                )
            )
            session.commit()

    except SQLAlchemyError as e:
        print(f"Erro ao inserir ou atualizar dados: {e}")
        session.rollback()

    finally:
        session.close()

if __name__ == "__main__":
 a = 1