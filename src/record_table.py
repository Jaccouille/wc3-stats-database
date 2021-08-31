from sqlalchemy import (
    create_engine,
    inspect,
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
from logging import getLogger
import os
from dotenv import load_dotenv
import sys

load_dotenv()

try:
    DB_NAME = os.environ['DB_NAME']
    USER = os.environ['DB_USER']
    PASS = os.environ['DB_PASSWORD']
    HOST = os.environ['DB_HOST']
except KeyError as e:
    logger.error(f"Following .env variable's missing : {str(e)}")
    sys.exit()

logger = getLogger(__name__)

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
    try:
        DailyRecord.__table__.create(engine, checkfirst=True)
    except Exception as e:
        logger.error(str(e))
    else:
        logger.info(f"Created table {DailyRecord.__tablename__}")

def init_database(engine):
    try:
        create_database(engine.url)
    except Exception as e:
        logger.error(str(e))
    else:
        logger.info(f"Created database {DB_NAME}")

def insert_daily_record(daily_record):
    engine = create_engine(f"postgresql+psycopg2://{USER}:{PASS}@{HOST}/{DB_NAME}")
    if not database_exists(engine.url):
        init_database(engine)

    if not inspect(engine).has_table(DailyRecord.__tablename__):
        init_table(engine)

    with engine.connect() as conn:
        conn.execute(DailyRecord.__table__.insert(), daily_record)
