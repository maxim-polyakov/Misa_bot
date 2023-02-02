import psycopg2
from sqlalchemy import create_engine

class PostgresConnection:
    engine_remote = create_engine(
        f'postgresql://postgres:gaTResKPJX25@ep-round-paper-091468.us-east-2.aws.neon.tech/SistersMemory')
    conn_remote = psycopg2.connect(
        'postgres://postgres:gaTResKPJX25@ep-round-paper-091468.us-east-2.aws.neon.tech/SistersMemory')