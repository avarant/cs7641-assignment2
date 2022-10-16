# cs7641-assigment2

This project uses [ABAGAIL Github](https://github.com/pushkar/ABAGAIL) with jython to analyze local random search algorithms, namely randomized hill climbing, simulated annealing, a genetic algorithm, MIMIC.

## Generating graphs

Install jython. If you're on Ubuntu or another Debian based distro you can run.
```
sudo apt-get install jython
```

Create and activate a python virtual env. I use Python 3.10.6.
```
python -m venv .venv
source .venv/bin/activate
```

Install packages
```
pip install -r requirements.txt
```

Generate csv results and graphs.
```
./run.sh
```
