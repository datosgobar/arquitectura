
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask.ext.jsontools import JsonSerializableBase

engine = create_engine('sqlite:///orm_in_detail.sqlite')

def get_session() :
    engine = create_engine(connstr, echo=True)
    session = sessionmaker()
    session.configure(bind=engine)
    return session()

Base = declarative_base(cls=(JsonSerializableBase,))

class Iris(Base):
    __tablename__ = 'iris'
    id = Column(Integer, primary_key=True)
    sepal_length = Column(Float)
    sepal_width = Column(Float)
    petal_length = Column(Float)
    petal_width = Column(Float)
    flower_class = Column(String)


#connstr = 'sqlite:///:memory:'
#connstr = 'sqlite:////tmp/iris.sqlite'
connstr = 'postgresql+psycopg2://data_warehouse_admin:pass@localhost/data_warehouse'


