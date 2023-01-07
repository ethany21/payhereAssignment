import logging
from contextlib import contextmanager, AbstractContextManager
from typing import Callable

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

username = config("username")
password = config("password")
host = config("host")
port = config("port")
db_name = config("db_name")

engine = create_engine('mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'.format(
    username='root', password=password, host=host, port=port, db_name=db_name
))

db_session = scoped_session(session_factory=sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
