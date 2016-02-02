#!/bin/bash

INFILE="$1"

#export PGPASSWORD='pass'; psql -U data_warehouse_admin -h 127.0.0.1 -c "ALTER USER data_warehouse_admin SUPERUSER; COPY iris FROM '$INFILE' DELIMITER ',' CSV; ALTER USER data_warehouse_admin NOSUPERUSER;" data_warehouse
#export PGPASSWORD='pass'; psql -U data_warehouse_admin -h 127.0.0.1 -c "\copy iris (sepal_length,sepal_width,petal_length,petal_width,flower_class) FROM '$INFILE' WITH HEADER DELIMITER ',' CSV;" data_warehouse
export PGPASSWORD='pass'; psql -U data_warehouse_admin -h 127.0.0.1 -c "\copy iris (sepal_length,sepal_width,petal_length,petal_width,flower_class) FROM '$INFILE' WITH DELIMITER ',' CSV HEADER;" data_warehouse


