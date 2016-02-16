#!/bin/bash

SAMPLEDIR=/tmp/scheduler_sample/

rm -rf $SAMPLEDIR
mkdir $SAMPLEDIR
mkdir $SAMPLEDIR/input
mkdir $SAMPLEDIR/refine_output
mkdir $SAMPLEDIR/refine_conf

cp -R ../modules/data_refine/sample/input $SAMPLEDIR
cp -R ../modules/data_refine/sample/conf/* $SAMPLEDIR/refine_conf/
cp db_loader.conf $SAMPLEDIR/db_loader.conf
cp sample_sequence.json ../etl_sequences

echo "Now you can execute the sample etl sequence with the folling command:"
echo python -c "from scheduler import start_etl; start_etl.delay(etl_run_name='sample_sequence')"

