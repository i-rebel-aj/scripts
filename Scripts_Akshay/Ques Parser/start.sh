#!/bin/bash
mkdir -p htmlDump
rm config.txt result.json result.csv
for entry in "./htmlDump"/*
do
  echo "$entry">>config.txt
done


python3 parser.py