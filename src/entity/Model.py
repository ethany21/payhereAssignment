from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from src.config.Connection import engine

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class UserLogin(Base):
    __tablename__ = 'UserLogin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), nullable=False)
    password = Column(String(256), nullable=False)


class Ledger(Base):
    __tablename__ = "Ledger"
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    memo = Column(String(120), nullable=False)
    user_id = Column(Integer, ForeignKey("UserLogin.id"), nullable = False)
    user = relationship("UserLogin", backref="ledger_userLogin")
