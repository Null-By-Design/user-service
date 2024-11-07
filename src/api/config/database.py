from contextlib import contextmanager
from typing import Generator

from psycopg2.pool import SimpleConnectionPool

from src.api.config import settings


class DatabasePool:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = SimpleConnectionPool(
                    minconn=1, maxconn=10, dsn=settings.DATABASE_URL
                )
            except Exception as e:
                raise Exception(f"Error creating connection pool: {str(e)}")
        return cls._pool

    @classmethod
    @contextmanager
    def get_connection(cls) -> Generator:
        pool = cls.get_pool()
        conn = pool.getconn()
        try:
            yield conn
        finally:
            pool.putconn(conn)
