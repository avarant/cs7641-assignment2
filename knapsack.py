import sys
import os
import time
import csv

sys.path.append("./ABAGAIL.jar")

import java.io.FileReader as FileReader
import java.io.File as File
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.Distribution as Distribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.HillClimbingProblem as HillClimbingProblem
import opt.NeighborFunction as NeighborFunction
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction
import opt.ga.CrossoverFunction as CrossoverFunction
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.ga.MutationFunction as MutationFunction
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.ga.UniformCrossOver as UniformCrossOver
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import opt.prob.ProbabilisticOptimizationProblem as ProbabilisticOptimizationProblem
import shared.FixedIterationTrainer as FixedIterationTrainer
import shared.ConvergenceTrainer as ConvergenceTrainer
import opt.example.KnapsackEvaluationFunction as KnapsackEvaluationFunction

from array import array

# Random number generator */
random = Random()
# The number of items
NUM_ITEMS = 40
# The number of copies each
COPIES_EACH = 4
# The maximum weight for a single element
MAX_WEIGHT = 50
# The maximum volume for a single element
MAX_VOLUME = 50
# The volume of the knapsack 
KNAPSACK_VOLUME = MAX_VOLUME * NUM_ITEMS * COPIES_EACH * .4


def run(algo_funcname, iters=10000, trials=10):
    # create copies
    fill = [COPIES_EACH] * NUM_ITEMS
    copies = array('i', fill)

    # create weights and volumes
    fill = [0] * NUM_ITEMS
    weights = array('d', fill)
    volumes = array('d', fill)
    for i in range(0, NUM_ITEMS):
        weights[i] = random.nextDouble() * MAX_WEIGHT
        volumes[i] = random.nextDouble() * MAX_VOLUME


    # create range
    fill = [COPIES_EACH + 1] * NUM_ITEMS
    ranges = array('i', fill)

    ef = KnapsackEvaluationFunction(weights, volumes, KNAPSACK_VOLUME, copies)
    problem_name = "knapsack"

    for t in range(1, trials+1):
        odd = DiscreteUniformDistribution(ranges)
        nf = DiscreteChangeOneNeighbor(ranges)
        mf = DiscreteChangeOneMutation(ranges)
        cf = UniformCrossOver()
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
            ga = StandardGeneticAlgorithm(200, 150, 25, gap)
            algo_funcfunc = ga
        elif algo_funcname == "MIMIC":
            pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
            mimic = MIMIC(200, 100, pop)
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
