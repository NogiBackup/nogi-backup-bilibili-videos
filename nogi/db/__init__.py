import sqlalchemy
from sqlalchemy import create_engine, types
from sqlalchemy.schema import MetaData


def create_engine_and_metadata(engine_url: str):
    settings = dict(encoding='utf8')
    engine = create_engine(engine_url, **settings)
    metadata = MetaData(bind=engine)
    return engine, metadata


class BaseModel:
    def __init__(self, engine, metadata, table, role='reader'):
        self.engine = engine
        self.metadata = metadata
        self.table = table
        self.role = role

    def execute(self, stmt: str):
        return self.engine.execute(stmt)
