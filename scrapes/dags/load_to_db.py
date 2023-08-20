def load(dataset_name: str, input_filename: str, fields: list, mode: str) -> None:
    import psycopg2
    import os
    import json
    import pandas as pd
    import logging

    logger = logging.getLogger('load')

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    secrets_path = os.path.join(
        base_dir, 'secrets.json'
    )

    with open(secrets_path, "r") as file:
        secrets = json.load(file)

    host = secrets["aws_db"]["endpoint"]
    user = secrets["aws_db"]["user"]
    password = secrets["aws_db"]["password"]
    dbname = secrets["aws_db"]["db_name"]
    port = "5432"

    df = pd.read_csv(input_filename)

    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    cursor = connection.cursor()
    
    if mode == 'append':
        create_table_query = f"CREATE TABLE IF NOT EXISTS {dataset_name} (id SERIAL PRIMARY KEY"

    elif mode == 'replace':
        drop_table_query = f"DROP TABLE IF EXISTS {dataset_name};"
        cursor.execute(drop_table_query)
        connection.commit()
        create_table_query = f"CREATE TABLE {dataset_name} (id SERIAL PRIMARY KEY"
    
    for field in fields:
        field_name = field['name']
        field_type = field['type']
        create_table_query += f", {field_name} {field_type}"
    create_table_query += ");"

    cursor.execute(create_table_query)
    connection.commit()

    # Insert data into the table
    columns = ', '.join([field['name'] for field in fields])
    insert_query = f"INSERT INTO {dataset_name} ({columns}) VALUES %s"
    records = [tuple(row) for row in df.to_numpy()]
    psycopg2.extras.execute_values(cursor, insert_query, records)
    connection.commit()

    cursor.close()
    connection.close()

    logger.info('LOAD COMPLETE')

    
