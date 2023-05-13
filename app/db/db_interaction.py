from typing import List

import psycopg2

from app.db.db_manager import DBManager


class DBInteraction(DBManager):
    def __init__(self, schema: str, user: str, password: str, host: str, port: str, pool_size: int) -> None:
        super().__init__(schema, user, password, host, port, pool_size)

    @staticmethod
    def wallet_exists(connection, address: str) -> bool:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM wallets WHERE address = %s", (address, ))
            results: List[str] = cursor.fetchall()

        return bool(len(results))

    @staticmethod
    def add_wallet(
            address: str,
            connection
    ) -> None:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO wallets (address) VALUES (%s)", (address, ))
