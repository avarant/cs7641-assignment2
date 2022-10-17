# cs7641-assigment2

See https://github.com/avarant/cs7641-assignment2

This project uses [ABAGAIL](https://github.com/pushkar/ABAGAIL) with jython to analyze the following local random search algorithms.

1. randomized hill climbing
2. simulated annealing
3. a genetic algorithm
4. MIMIC


## Problems

| Problem      | Optimal algorithm |
| ------------ | ----------- |
| continuous peaks     | SA       |
| knapsack     | MIMIC        |
| traveling salesman   | GA        |


## Part 1: Generating graphs

Make sure you have java installed.

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


## Part 2: Generating results for part 2

Train and test a perceptron using RHC, SA and GA

code: `ABAGAIL/src/opt/test/BreastCancerTest.java`

data: `ABAGAIL/data/`

```
cd ABAGAIL
java -cp ABAGAIL.jar opt.test.BreastCancerTest
```
