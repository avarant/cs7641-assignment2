# cs7641-assigment2

See https://github.com/avarant/cs7641-assignment2

This project uses [ABAGAIL](https://github.com/pushkar/ABAGAIL) with jython to analyze the following local random search algorithms.

1. randomized hill climbing
2. simulated annealing
3. a genetic algorithm
4. MIMIC


## Generating graphs

Install jython. If you're on Ubuntu or another Debian based Linux distro you can run.
```
sudo apt-get install jython
```

Create and activate a python virtual env. I use Python 3.10.6.
```
python -m venv .venv
source .venv/bin/activate
```

Install packages.
```
pip install -r requirements.txt
```

Generate csv results.
```
./run.sh
```

Generate graphs.
```
./plot.sh
```

## Problems

| Problem      | Optimal algorithm |
| ------------ | ----------- |
| continuous peaks     | SA       |
| knapsack     | MIMIC        |
| traveling salesman   | GA        |


## Notes
convergence plot: fitness v iters
choosing convergence criteria is important

try different problem size and see how performance changes
does not need to be a plot. table is acceptable

analyze wallclock time
fevals per iteration
fevals per wallclock time


for NN
learning curve
compare backprop with randomized optimization
