#!/usr/bin/python

import db_commons

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy import create_engine

Base = declarative_base()

def create_db ():
    # Create DB
    engine = create_engine(db_commons.connstr, echo=True)
    conn = engine.connect()

    conn.execute("COMMIT;")
    conn.execute("CREATE DATABASE data_warehouse;")
    
    # Setup users
    conn.execute("CREATE USER data_warehouse_admin WITH PASSWORD 'pass';")
    conn.execute("GRANT ALL PRIVILEGES ON DATABASE data_warehouse to data_warehouse_admin;")

    conn.close()

def  create_schema ():
    engine = create_engine(connstr, echo=True)
    Base.metadata.create_all(engine)

if __name__ == '__main__' :
    #create_db()
    create_schema()
