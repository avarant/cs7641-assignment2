#!/bin/bash

export CLASSPATH=ABAGAIL.jar:$CLASSPATH

rm -rf results
mkdir -p results/csv
mkdir -p results/plot

# four peaks
echo "four peaks"
jython fourpeaks.py
python plot.py fourpeaks

# knapsack
echo "knapsack"
jython knapsack.py
python plot.py knapsack

# flipflop
echo "flipflop"
jython flipflop.py
python plot.py flipflop

# continuouspeaks
echo "continuouspeaks"
jython continuouspeaks.py
python plot.py continuouspeaks

# travelingsalesman
echo "travelingsalesman"
jython travelingsalesman.py
python plot.py travelingsalesman
