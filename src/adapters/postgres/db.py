from logging import getLogger
from os import getenv
from typing import Dict, List, Union

import psycopg2
import psycopg2.extras

POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
POSTGRES_DATABASE = getenv("POSTGRES_DATABASE", "postgres")
POSTGRES_USER = getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "postgres")
LOGGER_LEVEL = getenv("LOGGER_LEVEL", "DEBUG")

logger = getLogger()
logger.setLevel(LOGGER_LEVEL)


class PostgresDatabase:
    _conn = None

    def __init__(self, table_name, schema="public"):
        self.table_name = f"{schema}.{table_name}"
        self.__setup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__teardown()

    def __del__(self):
        self.__teardown()

    def __setup(self):
        if not self.conn:
            self.conn = psycopg2.connect(
                host=POSTGRES_HOST,
                database=POSTGRES_DATABASE,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
            )

    def __teardown(self):
        if self.conn and not self.conn.closed:
            try:
                self.conn.close()
            except Exception as err:
                print(err)

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, value: psycopg2.connect):
        self._conn = value

    def find_one(self, filter_query: Union[str, dict] = None) -> dict:
        return self._find(filter_query, first=True)

    def find(
        self, filter_query: Union[str, dict] = None, skip: int = 0, limit: int = 1000
    ) -> List[dict]:
        """
        Use this method to find rows on database.

        ===== CAUTION USING TIPPING BELOW, or you can drop down our database =====

            -> Use `limit=-1` to get all rows in a table from the database

        ==========================================================================
        @param filter_query: DICT
        @param skip: int
        @param limit: int
        @return: List
        """
        return self._find(filter_query, first=False, skip=skip, limit=limit)

    def update_one(self, where_dict: dict, update_dict: dict):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        result_operation = None
        try:
            set_it = self.__build_constraint(
                list(update_dict.keys()), list(update_dict.values()),
            )
            where = self.__where_from_dict(where_dict)
            query = f"""
                UPDATE {self.table_name}
                SET {set_it}
                {where}
                RETURNING *;
            """

            logger.debug(f"{query}\n")
            cursor.execute(query)
            result_operation = cursor.fetchone()
            self.conn.commit()
        except Exception as err:
            logger.error(f"UPDATE_ONE ERROR -> {err}")
            self.conn.rollback()
        finally:
            cursor.close()
            return result_operation

    def insert_update(
        self, fields: List[str], values: List[str], field_filter: str = None
    ):
        len_fields = len(fields)
        len_values = len(values)

        if len_fields == len_values and len_values > 0 and len_fields > 0:
            constraint = self.__build_constraint(fields, values)
            on_conflict_do = (
                f"""
                    ON CONFLICT ({field_filter})
                    DO
                        UPDATE SET {constraint}
                """
                if field_filter
                else ""
            )

            join_values = ", ".join(
                f"'{value}'" if isinstance(value, str) else str(value)
                for value in values
            )
            join_fields = ", ".join(fields)

            query = f"""
                INSERT INTO
                    {self.table_name} ({join_fields})
                VALUES
                    ({join_values})
                {on_conflict_do}
                RETURNING *;
            """
            return self._update(query)

    def insert_one(self, fields: List[str], values: List[str]):
        len_fields = len(fields)
        len_values = len(values)

        if len_fields == len_values and len_values > 0 and len_fields > 0:
            join_values = ", ".join(
                f"'{value}'" if isinstance(value, str) else str(value)
                for value in values
            )
            join_fields = ", ".join(fields)

            query = f"""
                INSERT INTO
                    {self.table_name} ({join_fields})
                VALUES
                    ({join_values})
                RETURNING *;
            """
            return self._update(query)

    def insert_many(self, list_data: List[dict]):
        fields = list(list_data[0].keys())
        join_fields = ", ".join(fields)
        joint_values = []
        for item in list_data:
            join_values = ", ".join(
                f"'{value}'" if isinstance(value, str) else str(value)
                for value in item.values()
            )
            joint_values.append(f"({join_values})")

        query = f"""
                    INSERT INTO
                        {self.table_name} ({join_fields})
                    VALUES
                        {', '.join(joint_values)};
                """
        return self._update(query)

    def _update(self, query: str):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        result_operation = ""
        try:
            logger.debug(f"{query}\n\n\n")
            cursor.execute(query)
            result_operation = (
                cursor.fetchall() if "returning" in query.lower() else True
            )
            self.conn.commit()
        except Exception as err:
            if "duplicate key value" not in str(err):
                logger.error(f"Update error: {err}")
            self.conn.rollback()
        finally:
            cursor.close()
            return result_operation

    def _find(
        self,
        filter_query: Union[str, dict] = None,
        first: bool = True,
        skip=0,
        limit=10,
    ) -> Union[dict, List[dict]]:

        row = {} if first else []

        if isinstance(filter_query, str):
            if not (
                filter_query.startswith("WHERE") or filter_query.startswith("where")
            ):
                filter_query = "WHERE " + filter_query
            where = filter_query
        elif isinstance(filter_query, dict):
            where = self.__where_from_dict(filter_query)
        else:
            where = ""

        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        skip = f"offset {skip}" if skip > 0 else ""
        limit = f"limit {limit}" if limit > 0 else ""

        try:
            query = f"SELECT * FROM {self.table_name} {where} {skip} {limit}"
            cursor.execute(query)
            if first:
                fetch = cursor.fetchone()
                row = dict(fetch) if fetch else {}
            else:
                row = [dict(r) for r in cursor.fetchall()]
        except Exception as err:
            logger.critical(err)
        finally:
            cursor.close()
            return row

    @staticmethod
    def __where_from_dict(
        filter_dict: Dict[str, Union[str, int, bool]], condition: str = "AND"
    ):
        if condition.upper() not in ("AND", "OR"):
            raise ValueError("Condition must be AND/OR")

        if not filter_dict:
            return ""

        clause = f" {condition} ".join(
            [
                f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}"
                for k, v in filter_dict.items()
            ]
        )

        return f"WHERE {clause}"

    @staticmethod
    def __build_constraint(fields: list, values: list):
        return ", ".join(
            [
                f"{field}='{value}'" if isinstance(value, str) else f"{field}={value}"
                for field, value in zip(fields, values)
            ]
        )


if __name__ == "__main__":
    with PostgresDatabase("stores") as db:
        print(
            db.find_one(
                {
                    "store_name": "CASAS BAHIA",
                    "store_ref": "Casas Bahia",
                    "system": "casasbahia",
                }
            )
        )
        print()
        print(db.find_one(filter_query="store_name='GAZIN' AND system='gazin'"))
        print()
        print(db.find("WHERE system LIKE 'ka%'"))
