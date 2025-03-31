import sys
import os
import glob
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.pipeline.p003_load_silver.utils.u001_update_postgres_silver import update_table_postgres

if __name__ == "__main__":
    batch_dir = r'data\outputs\silver\2025-03-30_17-37-36' \
    ''
    schema = "s002_silver"

    print('-------------------------------- Sports --------------------------------')
    path_table_name = 'Sports'
    table_name = 't001_sports'
    
    csv_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.csv"))
    for csv_path in csv_files:
        print(csv_path)
        df = pd.read_csv(csv_path, encoding='utf-8')
        update_table_postgres(table_name, schema, df)

    print('\n-------------------------------- Countries --------------------------------')
    path_table_name = 'Countries'
    table_name = 't002_countries'
    
    csv_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.csv"))
    print(csv_files)
    for csv_path in csv_files:
        print(csv_path)
        df = pd.read_csv(csv_path, encoding='utf-8')
        update_table_postgres(table_name, schema, df)

    print('\n-------------------------------- Tournaments --------------------------------')
    path_table_name = 'Tournaments'
    table_name = 't003_tournaments'
    
    csv_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.csv"))
    for csv_path in csv_files:
        print(csv_path)
        df = pd.read_csv(csv_path, encoding='utf-8')
        update_table_postgres(table_name, schema, df)

    print('\n-------------------------------- Seasons --------------------------------')
    path_table_name = 'Seasons'
    table_name = 't004_seasons'
    
    csv_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.csv"))
    for csv_path in csv_files:
        print(csv_path)
        df = pd.read_csv(csv_path, encoding='utf-8')
        update_table_postgres(table_name, schema, df)

    print('\n-------------------------------- Rounds --------------------------------')
    path_table_name = 'Rounds'
    table_name = 't005_rounds'
    
    csv_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.csv"))
    for csv_path in csv_files:
        print(csv_path)
        df = pd.read_csv(csv_path, encoding='utf-8')
        df['season_id_round_slug'] = df['season_id_round_slug'].astype(str)
        update_table_postgres(table_name, schema, df)

    print('\n-------------------------------- Matches --------------------------------')
    path_table_name = 'Matches'
    table_name = 't006_matches'
    
    csv_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.csv"))
    for csv_path in csv_files:
        print(csv_path)
        df = pd.read_csv(csv_path, encoding='utf-8')
        df['season_id_round_slug'] = df['season_id_round_slug'].astype(str)
        update_table_postgres(table_name, schema, df)

    print('\n-------------------------------- Matches Statistics --------------------------------')
    path_table_name = 'Matches Statistics'
    table_name = 't007_matches_statistics'
    
    csv_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.csv"))
    for csv_path in csv_files:
        print(csv_path)
        df = pd.read_csv(csv_path, encoding='utf-8')
        update_table_postgres(table_name, schema, df)

    print('\n-------------------------------- Lineups --------------------------------')
    path_table_name = 'Lineups'
    table_name = 't008_lineups'
    
    csv_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.csv"))
    print(csv_files)
    for csv_path in csv_files:
        print(csv_path)
        df = pd.read_csv(csv_path, encoding='utf-8')
        update_table_postgres(table_name, schema, df)

    print('\n-------------------------------- Lineups Statistics --------------------------------')
    path_table_name = 'Lineups Statistics'
    table_name = 't009_lineups_statistics'
    
    csv_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.csv"))
    for csv_path in csv_files:
        print(csv_path)
        df = pd.read_csv(csv_path, encoding='utf-8')
        update_table_postgres(table_name, schema, df)





