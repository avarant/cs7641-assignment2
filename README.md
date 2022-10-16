# cs7641-assigment2

This project uses [ABAGAIL](https://github.com/pushkar/ABAGAIL) with jython to analyze local random search algorithms, namely randomized hill climbing, simulated annealing, a genetic algorithm, MIMIC.


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

Generate csv results and graphs.
```
./run.sh
```


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
