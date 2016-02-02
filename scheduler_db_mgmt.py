
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

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
    etl_run_id = Column(Integer, ForeignKey('etl_run.id'))
    #etl_run = relationship("ETLRun", back_populates="modules")
    task_id = Column(String)
    
    name = Column(String)
    input = Column(String)
    output = Column(String)
    conf = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    status = Column(String)


def create_all():
    engine = create_engine(connstr, echo=True)
    Base.metadata.create_all(engine)

 
