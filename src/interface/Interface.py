from sqlalchemy.orm import Session


class Interface:
    def __init__(self, db: Session):
        self.db = db


class AppService(Interface):
    pass


class AppRepository(Interface):
    pass
