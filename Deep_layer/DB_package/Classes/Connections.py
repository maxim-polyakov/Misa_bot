import psycopg2
from sqlalchemy import create_engine


class PostgresConnection:
    """

    It is connection class

    """
    def __init__(self):
        # establishes a connection to a remote postgresql database using psycopg2.
        # the connection string includes:
        # username: 'postgres'
        # password: 'gatreskpjx25'
        # host: 'ep-round-paper-091468.us-east-2.aws.neon.tech'
        # database name: 'botsmemory'
        self.conn_remote = psycopg2.connect(
        'postgres://postgres:gaTResKPJX25@ep-round-paper-091468.us-east-2.aws.neon.tech/BotsMemory')
        # creates a sqlalchemy engine for the same remote postgresql database.
        # the engine is used for higher-level database operations, such as executing sql queries
        # and managing database connections in a more abstract way.
        # the connection string is formatted similarly to the one used for psycopg2.
        self.engine_remote = create_engine(
            f'postgresql://postgres:gaTResKPJX25@ep-round-paper-091468.us-east-2.aws.neon.tech/BotsMemory')
