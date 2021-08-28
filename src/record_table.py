from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    MetaData,
    Date,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

DB_NAME = "testdb"
USER = "jaccouille"
PASS = "root"

Base = declarative_base()

class DailyRecord(Base):
    __tablename__ = "daily_record"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    rank = Column(Integer)
    played = Column(Integer)
    rating = Column(Integer)
    lastChange = Column(Integer)
    date = Column(Date, nullable=False)

    __table_args__ = (UniqueConstraint("name", "date", name="_name_date_uc"),)


def drop_table(conn, tablename, engine):
    meta = MetaData(engine)
    table = Table(tablename, meta, autoload_with=engine)
    table.drop(checkfirst=True)

def init_table(engine):
    DailyRecord.__table__.create(engine, checkfirst=True)

def insert_daily_daily_record(daily_record):
    engine = create_engine(f"postgresql+psycopg2://{USER}:{PASS}@localhost/{DB_NAME}")
    if not database_exists(engine.url):
        create_database(engine.url)

    with engine.connect() as conn:
        conn.execute(DailyRecord.__table__.inert(), daily_record)
