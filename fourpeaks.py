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

from array import array


def run(algo_funcname, iters=10000, trials=10):
    N=200
    T=N/5
    fill = [2] * N
    ranges = array('i', fill)
    ef = FourPeaksEvaluationFunction(T)
    problem_name = "fourpeaks"

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
            algo_func = rhc
        elif algo_funcname == "SA":
            sa = SimulatedAnnealing(1E11, .95, hcp)
            algo_func = sa
        elif algo_funcname == "GA":
            gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
            ga = StandardGeneticAlgorithm(200, 100, 10, gap)
            algo_func = ga
        elif algo_funcname == "MIMIC":
            pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
            mimic = MIMIC(200, 20, pop)
            algo_func = mimic
        else:
            return

        # ef.resetFunctionEvaluationCount()
        # fit = ConvergenceTrainer(algo_func)
        fit = FixedIterationTrainer(algo_func, 10)
        FILE_NAME="{}_{}_{}.csv".format(algo_funcname, problem_name, str(t))
        OUTPUT_FILE = os.path.join("results/csv", FILE_NAME)
        with open(OUTPUT_FILE, "wb") as results:
            writer= csv.writer(results, delimiter=',')
            writer.writerow(["iters","fevals","fitness"])
            for i in range(0, iters, 10):
                fit.train()
                #print str(i) + ", " + str(ef.getFunctionEvaluations()) + ", " + str(ef.value(algo_func.getOptimal()))
                writer.writerow([i, ef.getFunctionEvaluations()-i, ef.value(algo_func.getOptimal())])
        
        print algo_funcname + " trial #" + str(t)
        print algo_funcname + ": " + str(ef.value(algo_func.getOptimal()))
        print "Function Evaluations: " + str(ef.getFunctionEvaluations()-iters)
        print "Iters: " + str(iters)
        print "####"




run("RHC")
run("SA")
run("GA")
run("MIMIC")
