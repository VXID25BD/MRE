import psycopg2
from psycopg2.pool import ThreadedConnectionPool


class DBManager:
    _pool_connection: ThreadedConnectionPool = None

    def __init__(self, schema: str, user: str, password: str, host: str, port: str, pool_size: int) -> None:
        self._dsn = f"postgresql://{user}:{password}@{host}:{port}/{schema}"
        self._pool_size = pool_size

        if self._pool_connection is None:
            self._create_connection_pool()

        self._create_tables()

    def _create_tables(self) -> None:
        connection = self.get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS wallets
            (
                id SERIAL PRIMARY KEY,
                address CHARACTER VARYING(10000) NOT NULL UNIQUE
            );""")
        self.put_connection(connection=connection)

    def get_connection(self):
        connection = self._pool_connection.getconn()
        connection.autocommit = True
        return connection

    def put_connection(self, connection) -> None:
        self._pool_connection.putconn(connection)

    def _create_connection_pool(self) -> None:
        self._pool_connection: ThreadedConnectionPool = ThreadedConnectionPool(
            1,
            maxconn=self._pool_size,
            dsn=self._dsn
        )
