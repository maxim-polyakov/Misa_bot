import os
import threading

from sqlalchemy import create_engine


class PostgresConnection:
    """

    It is connection class

    """
    _engine_remote = None
    _engine_lock = threading.Lock()

    def __init__(self):
        # One process-wide SQLAlchemy engine keeps a small pool of PostgreSQL
        # connections instead of opening a new TCP/TLS connection per query.
        if self.__class__._engine_remote is None:
            with self.__class__._engine_lock:
                if self.__class__._engine_remote is None:
                    database_url = os.getenv(
                        'DATABASE_URL',
                        'postgresql://postgres:gaTResKPJX25@ep-round-paper-091468.us-east-2.aws.neon.tech/BotsMemory',
                    )
                    self.__class__._engine_remote = create_engine(
                        database_url,
                        pool_size=5,
                        max_overflow=5,
                        pool_pre_ping=True,
                        pool_recycle=900,
                    )
        self.engine_remote = self.__class__._engine_remote
