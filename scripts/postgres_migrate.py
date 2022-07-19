import os

from src.adapters.postgres.db import PostgresDatabase
from src.utils.postgres_database import ensure_store_table_is_created


def _list_modules_in_systems() -> list:
    """
        It will list modules from src/helpers/systems, filtering by modules python that
    ends with .py and not is double underscore.

    @return: List[str]
    """
    try:
        modules = os.listdir("src/features/systems")
    except FileNotFoundError:
        modules = os.listdir("../src/features/systems")

    return [
        system.replace(".py", "")
        for system in modules
        if (
            "base" not in system
            and "__" not in system
            and "base" not in system
            and system.endswith(".py")
        )
    ]


def _create_schema_google():
    with PostgresDatabase("stores") as db:
        conn = db.conn
        cursor = conn.cursor()
        cursor.execute("CREATE SCHEMA IF NOT EXISTS google;")
        conn.commit()


def _create_table_stores():
    with PostgresDatabase("stores") as db:
        conn = db.conn
        cursor = conn.cursor()
        try:
            cursor = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS google.stores (
                id serial PRIMARY KEY,
                store_name TEXT NOT NULL,
                store_ref TEXT UNIQUE NOT NULL,
                status VARCHAR(1) NOT NULL,
                store_id INTEGER DEFAULT 0,
                platform TEXT,
                store_table TEXT,
                seller_default TEXT NOT NULL,
                subdomain_platform TEXT,
                url TEXT NOT NULL
            );
            """
            cursor.execute(query)
            conn.commit()
        except Exception as err:
            print(err)
            conn.rollback()
        cursor.close()


def _create_product_search():
    with PostgresDatabase("product_search") as db:
        conn = db.conn
        cursor = conn.cursor()
        try:
            cursor = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS google.product_search (
                id serial PRIMARY KEY,
                ean TEXT NOT NULL,
                date timestamp NOT NULL,
                status TEXT NOT NULL,
                url TEXT NOT NULL
            );
            """
            cursor.execute(query)
            conn.commit()
        except Exception as err:
            print(err)
            conn.rollback()
        cursor.close()


def _create_table_data_quality():
    with PostgresDatabase("data_quality") as db:
        conn = db.conn
        cursor = conn.cursor()
        try:
            cursor = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS google.data_quality (
                ean BIGINT,
                product_name TEXT,
                brand TEXT,
                image TEXT,
                model TEXT,
                provider TEXT,
                color TEXT,
                voltage TEXT,
                PRIMARY KEY(ean, provider, color, voltage)
            );
            """
            cursor.execute(query)
            conn.commit()
        except Exception as err:
            print(err)
            conn.rollback()
        cursor.close()


def _migrate_stores():
    with PostgresDatabase("stores") as db:
        conn = db.conn
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO
                google.stores (
                    store_name,
                    store_ref,
                    status,
                    store_id,
                    platform,
                    store_table,
                    seller_default,
                    url
                )
            VALUES
                ('MAGAZINE LUIZA', 'Magazine Luiza', 'S', 89, 'magazineluiza', 'magazineluiza', 'MAGAZINELUIZA', 'https://magazineluiza.com.br'),
                ('CASASBAHIA', 'Casas Bahia', 'S', 96, 'casasbahia', 'cnova', 'CASASBAHIA.COM.BR', 'https://casasbahia.com.br'),
                ('PONTOFRIO', 'Pontofrio.com', 'S', 94, 'pontofrio', 'cnova', 'PONTOFRIO.COM.BR', 'https://pontofrio.com.br'),
                ('EXTRA', 'Extra.com.br', 'S', 93, 'extra', 'cnova', 'EXTRA.COM.BR', 'https://extra.com.br')

            ON CONFLICT (store_ref) DO NOTHING;
            """
            cursor.execute(query)
            conn.commit()
        except Exception as err:
            print(err)
            conn.rollback()
        cursor.close()


def _migrate_schemas():
    with PostgresDatabase("stores") as db:
        cursor = db.conn.cursor()
        for table_name in ["bw2", "cnova", "magazineluiza"]:
            ensure_store_table_is_created(database=db, store_table=table_name)
        cursor.close()


def migrate():
    _create_schema_google()
    _create_table_stores()
    _create_table_data_quality()
    _create_product_search()
    _migrate_stores()
    _migrate_schemas()


if __name__ == "__main__":
    print("Starting...")
    migrate()
    print("Migrate with success!")
