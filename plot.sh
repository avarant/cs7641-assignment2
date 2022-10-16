#!/bin/bash

mkdir -p results/plot

# python plot.py "fourpeaks"
python plot.py "knapsack"
# python plot.py "flipflop"
python plot.py "continuouspeaks"
python plot.py "travelingsalesman"
