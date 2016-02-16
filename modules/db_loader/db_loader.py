#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import csv
import re

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, String, UnicodeText, Text, Integer, BigInteger, Float, Boolean, Date, Time, DateTime

import module_base

class DBLoaderModule(module_base.ModuleBase) :
    prog_text   = "db_loader.py"
    desc_text = "Load CSVs to database. The data of the files will be loaded on the database indicated by the name of the file."
    input_text = "Directory where the input CSVs are stored. The tables on the database will be created"
    output_text = "Connection string of the database on which the files will be loaded"
    conf_text = "Configuration"
    epilog = """
    The name of the input files should be of the form TABLE.FOO.BAR.csv where TABLE is the name of the table where the data will be loaded. The section in middle, FOO.BAR is ignored.
    Example:
    ./python db_loader.py --input data.csv \
                          --output "postgresql+psycopg2://user:pass@localhost/db_name" \
                          --conf sample_config.json
    """
    input_required = True
    output_required = True
    conf_required = True

    def implementation(self, input=None, output=None, conf=None) :
        print "Loading files from %s" % input
        print "To connstr %s" % output
        print "Using config file %s" % conf
        
        indir = input
        connstr = output
        conf = json.load(open(conf))
        delimiter = str(conf.get("delimiter", ","))
        
        engine = create_engine(connstr, echo=False)
        conn = engine.connect()
        metadata = MetaData()
        
        col_dtypes = {
            "String" : String(255),
            "UnicodeText" : UnicodeText(255),
            "Text" : Text,
            "Integer" : Integer,
            "BigInteger" : BigInteger,
            "Float" : Float,
            "Boolean" : Boolean,
            "Date" : Date,
            "Time" : Time,
            "DateTime" : DateTime,
        }
        
        def get_col_type(typestr) :
            if col_dtypes.has_key(typestr) :
                return col_dtypes[typestr]
            m = re.match("String\s*\(\s*(\d+)\s*\)", typestr)
            if m and len(m.groups) == 1 :
                return String(m.group(1))
            
            m = re.match("UnicodeText\s*\(\s*(\d+)\s*\)", typestr)
            if m and len(m.groups) == 1 :
                return UnicodeText(m.group(1))

            return None
        
        tables = {}
        table_col_renamer = {}
        for table_desc in conf["table_desc"] :
            table_name = table_desc["name"]
            
            table_col_renamer[table_name] = { col.get("name_orig", col["name"]) : col["name"] for col in table_desc["columns"] }

            cols = [Column(col["name"], get_col_type(col["type"])) for col in table_desc["columns"]]
            if conf["add_pk"] :
                cols = [Column('id', Integer, primary_key=True)] + cols
            tables[table_name] = Table(*([table_name, metadata]+cols))
        
        if conf["create_all"] :
            if conf["clear_all_tables_before_insert"] :
                metadata.drop_all(engine)
            metadata.create_all(engine)
        
        for fn in os.listdir(indir) :
            infpath = os.path.join(os.path.join(indir, fn))
            aux = fn.split(".")
            if len(aux) < 2 or aux[-1] != "csv"  or not aux[0] in tables.keys() :
                continue
            table_name = aux[0]
            
            print "Loading file %s in %s table..." % (infpath, table_name)
            inf = open(infpath)
            row_data = csv.DictReader(inf, delimiter=delimiter)
            row_data = [ {table_col_renamer[table_name][k]:unicode(v, 'utf-8') for (k,v) in row.items() if table_col_renamer[table_name].has_key(k) } for row in row_data]
            conn.execute(tables[table_name].insert(), row_data)
            inf.close()
            "Done"

if __name__ == "__main__" :
    module = DBLoaderModule()
    module.run()
