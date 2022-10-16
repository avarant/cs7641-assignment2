#!/bin/bash

mkdir -p results/plot

# # four peaks
# echo "four peaks"
# python plot.py "fourpeaks"

# knapsack
echo "knapsack"
# jython knapsack.py
python plot.py "knapsack"

# # flipflop
# echo "flipflop"
# python plot.py "flipflop"

# continuouspeaks
echo "continuouspeaks"
python plot.py "continuouspeaks"

# travelingsalesman
echo "travelingsalesman"
python plot.py "travelingsalesman"
