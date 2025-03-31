import pandas as pd
import sys
import os
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.pipeline.p002_load_bronze.utils.u001_update_postgres_bronze import update_json_postgres

if __name__ == "__main__":
    batch_dir = r'data\outputs\bronze\2025-03-30_17-37-36'
    schema = "s001_bronze"

    print('-------------------------------- Sports --------------------------------')
    path_table_name = 'Sports'
    table_name = 't001_sports'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    for json_path in json_files:
        print(json_path)
        update_json_postgres(table_name, schema, json_path)

    print('\n-------------------------------- Countries --------------------------------')
    path_table_name = 'Countries'
    table_name = 't002_countries'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    for json_path in json_files:
        print(json_path)
        update_json_postgres(table_name, schema, json_path)

    print('\n-------------------------------- Tournaments --------------------------------')
    path_table_name = 'Tournaments'
    table_name = 't003_tournaments'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    for json_path in json_files:
        print(json_path)
        update_json_postgres(table_name, schema, json_path)

    print('\n-------------------------------- Seasons --------------------------------')
    path_table_name = 'Seasons'
    table_name = 't004_seasons'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    for json_path in json_files:
        print(json_path)
        update_json_postgres(table_name, schema, json_path)

    print('\n-------------------------------- Rounds --------------------------------')
    path_table_name = 'Rounds'
    table_name = 't005_rounds'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    for json_path in json_files:
        print(json_path)
        update_json_postgres(table_name, schema, json_path)

    print('\n-------------------------------- Matches --------------------------------')
    path_table_name = 'Matches'
    table_name = 't006_matches'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    for json_path in json_files:
        print(json_path)
        update_json_postgres(table_name, schema, json_path)

    print('\n-------------------------------- Matches Statistics --------------------------------')
    path_table_name = 'Matches Statistics'
    table_name = 't007_matches_statistics'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    for json_path in json_files:
        print(json_path)
        update_json_postgres(table_name, schema, json_path)

    print('\n-------------------------------- Lineups --------------------------------')
    path_table_name = 'Lineups'
    table_name = 't008_lineups'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    for json_path in json_files:
        print(json_path)
        update_json_postgres(table_name, schema, json_path)

    print('\n-------------------------------- Lineups Statistics --------------------------------')
    path_table_name = 'Lineups Statistics'
    table_name = 't009_lineups_statistics'
    
    json_files = glob.glob(os.path.join(batch_dir, path_table_name, "*.json"))
    for json_path in json_files:
        print(json_path)
        update_json_postgres(table_name, schema, json_path)

    
