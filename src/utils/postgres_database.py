def ensure_store_table_is_created(database, store_table: str):
    cursor = database.conn.cursor()
    try:
        query = f"""
            CREATE TABLE IF NOT EXISTS google.{store_table} (
                ean BIGINT NOT NULL,
                sku TEXT NOT NULL,
                product_reference TEXT,
                url TEXT NOT NULL,
                status TEXT default 'N',
                attribute_name TEXT,
                attribute_value TEXT,
                seller_name TEXT,
                store_id INTEGER NOT NULL,
                url_raw TEXT,
                PRIMARY KEY(ean, sku, store_id)
            );
        """
        cursor.execute(query)
        database.conn.commit()
    except Exception as err:
        print(f"Error creating new store table -> {err}")
        database.conn.rollback()
    cursor.close()
