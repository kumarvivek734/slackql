from sqlalchemy import create_engine
from app.config import settings
from contextlib import contextmanager

def get_engine():
    engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={"options": f"-c statement_timeout={settings.DB_QUERY_TIMEOUT_SECONDS * 1000}"},
    )
    return engine

@contextmanager
def get_connection():
    connection = get_engine().connect()
    try:
        yield connection
    finally:
        connection.close()
