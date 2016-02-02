#!/bin/bash

INFILE="$1"
OUTFILE="$2"

#INFILE="/tmp/dummy.csv"
#OUTFILE="/tmp/dummy_out.csv"

cp $INFILE $OUTFILE

echo "Dummy file copied from" $INFILE "to" $OUTFILE
