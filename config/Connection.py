from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'.format(
    username='root', password=1234, host='127.0.0.1', port=3306, db_name='payhere'
))

db_session = scoped_session(session_factory=sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
