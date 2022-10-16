import sys
import os
import time
import csv

sys.path.append("./ABAGAIL.jar")

import opt.example.FlipFlopEvaluationFunction as FlipFlopEvaluationFunction
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.SingleCrossOver as SingleCrossOver
import dist.DiscreteDependencyTree as DiscreteDependencyTree
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.prob.MIMIC as MIMIC
from array import array


def run(algo_funcname, iters=10000, trials=10):
    N = 80
    fill = [2] * N
    ranges = array('i', fill)
        
    ef = FlipFlopEvaluationFunction()
    problem_name = "flipflop"

    for t in range(1, trials+1):
        odd = DiscreteUniformDistribution(ranges)
        nf = DiscreteChangeOneNeighbor(ranges)
        mf = DiscreteChangeOneMutation(ranges)
        cf = SingleCrossOver()
        df = DiscreteDependencyTree(.1, ranges)
        hcp = GenericHillClimbingProblem(ef, odd, nf)
        gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
        pop = GenericProbabilisticOptimizationProblem(ef, odd, df)

        if algo_funcname == "RHC":
            rhc = RandomizedHillClimbing(hcp)
            algo_funcfunc = rhc
        elif algo_funcname == "SA":
            sa = SimulatedAnnealing(100, .95, hcp)
            algo_funcfunc = sa
        elif algo_funcname == "GA":
            gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
            ga = StandardGeneticAlgorithm(200, 100, 20, gap)
            algo_funcfunc = ga
        elif algo_funcname == "MIMIC":
            pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
            mimic = MIMIC(200, 5, pop)
            algo_funcfunc = mimic
        else:
            return

        # ef.resetFunctionEvaluationCount()
        # fit = ConvergenceTrainer(algo_funcfunc)
        fit = FixedIterationTrainer(algo_funcfunc, 10)
        FILE_NAME="{}_{}_{}.csv".format(algo_funcname, problem_name, str(t))
        OUTPUT_FILE = os.path.join("results/csv", FILE_NAME)
        with open(OUTPUT_FILE, "wb") as results:
            writer= csv.writer(results, delimiter=',')
            writer.writerow(["iters","fevals","fitness"])
            for i in range(0, iters, 10):
                fit.train()
                #print str(i) + ", " + str(ef.getFunctionEvaluations()) + ", " + str(ef.value(algo_funcfunc.getOptimal()))
                writer.writerow([i, ef.getFunctionEvaluations()-i, ef.value(algo_funcfunc.getOptimal())])
        
        print algo_funcname + " trial #" + str(t)
        print algo_funcname + ": " + str(ef.value(algo_funcfunc.getOptimal()))
        print "Function Evaluations: " + str(ef.getFunctionEvaluations()-iters)
        print "Iters: " + str(iters)
        print "####"




run("RHC")
run("SA")
run("GA")
run("MIMIC")
