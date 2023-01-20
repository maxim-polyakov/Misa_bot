import Deep_layer.DB_package as db
class PostgresConnection:

    engine = db.create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost:5432/MisaMemory')
    conn = db.psycopg2.connect(
        'dbname=MisaMemory user=postgres password=postgres')