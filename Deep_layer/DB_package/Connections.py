import psycopg2
from sqlalchemy import create_engine

class PostgresConnection:

    engine = create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost:5432/MisaMemory')
    conn = psycopg2.connect(
        'dbname=MisaMemory user=postgres password=postgres')