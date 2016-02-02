
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#connstr = 'sqlite:///:memory:'
#connstr = 'sqlite:////tmp/iris.sqlite'
connstr = 'postgresql+psycopg2://data_warehouse_admin:pass@localhost/data_warehouse'

def get_session() :
    engine = create_engine(connstr, echo=True)
    session = sessionmaker()
    session.configure(bind=engine)
    return session()

Base = declarative_base()

class ETLRun(Base):
    __tablename__ = 'etl_run'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)

class ETLModuleRun(Base):
    __tablename__ = 'etl_module_run'
    id = Column(Integer, primary_key=True)
    etlrun_id = Column(Integer)
    task_id = Column(Integer)
    name = Column(String)
    input = Column(string)
    output = Column(string)
    conf = Column(string)
    start = Column(DateTime)
    end = Column(DateTime)
    status = Column(String)


def create_all():
    engine = create_engine(connstr, echo=True)
    Base.metadata.create_all(engine)

 
