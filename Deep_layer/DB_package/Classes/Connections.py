import psycopg2
from sqlalchemy import create_engine


class PostgresConnection:
    """

    It is connection class

    """
    def __init__(self):
        self.conn_remote = psycopg2.connect(
        'postgres://postgres:gaTResKPJX25@ep-round-paper-091468.us-east-2.aws.neon.tech/BotsMemory')
        self.engine_remote = create_engine(
            f'postgresql://postgres:gaTResKPJX25@ep-round-paper-091468.us-east-2.aws.neon.tech/BotsMemory')
