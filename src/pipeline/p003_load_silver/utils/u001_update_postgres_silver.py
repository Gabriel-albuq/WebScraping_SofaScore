import pandas as pd
import sys
import os
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from unidecode import unidecode

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.utils.create_engine_postgres import create_engine_postgres

def update_table_postgres(table_name, schema, df):
    engine = create_engine_postgres(see_echo=False)

    Session = sessionmaker(bind=engine)
    
    metadata = MetaData(schema=schema)
    table = Table(table_name, metadata, autoload_with=engine)

    key_columns = [col.name for col in table.primary_key.columns]

    try:
        for index, row in df.iterrows():
            session = Session()
            session.begin()
            try:
                # Substituir 'nan' por None
                row = row.apply(lambda x: None if str(x).lower() == 'nan' else x)
                
                # Criar a condição de filtro baseada nas chaves
                conditions = [table.c[col] == row[col] for col in key_columns]
                registro = session.query(table).filter(*conditions).first()

                if registro:
                    session.execute(
                        table.update()
                        .where(*conditions)
                        .values({col: unidecode(str(row[col])) if row[col] else row[col] for col in row.index})
                    )
                else:
                    session.execute(
                        table.insert().values(
                            {col: unidecode(str(row[col])) if row[col] else row[col] for col in row.index}
                        )
                    )
                session.commit()
            
            except Exception as e:
                print(f"Erro ao inserir ou atualizar o registro {row.to_dict()}: {e}")
                session.rollback()
                continue

    except SQLAlchemyError as e:
        print(f"Erro ao inserir ou atualizar dados: {e}")
        session.rollback()

    finally:
        session.close()
