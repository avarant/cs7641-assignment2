# traveling salesman algorithm implementation in jython
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
import dist.DiscretePermutationDistribution as DiscretePermutationDistribution
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
import opt.example.TravelingSalesmanEvaluationFunction as TravelingSalesmanEvaluationFunction
import opt.example.TravelingSalesmanRouteEvaluationFunction as TravelingSalesmanRouteEvaluationFunction
import opt.SwapNeighbor as SwapNeighbor
import opt.ga.SwapMutation as SwapMutation
import opt.example.TravelingSalesmanCrossOver as TravelingSalesmanCrossOver
import opt.example.TravelingSalesmanSortEvaluationFunction as TravelingSalesmanSortEvaluationFunction
import shared.Instance as Instance
import util.ABAGAILArrays as ABAGAILArrays

from array import array


# set N value.  This is the number of points
N = 50
random = Random()


def run(algo_name, problem_name, ef, iters=10000, trials=10):
    for t in range(1, trials+1):
        odd = DiscretePermutationDistribution(N)
        nf = SwapNeighbor()
        mf = SwapMutation()
        cf = TravelingSalesmanCrossOver(ef)
        hcp = GenericHillClimbingProblem(ef, odd, nf)
        gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)

        if algo_name == "RHC":
            rhc = RandomizedHillClimbing(hcp)
            algo_func = rhc
        elif algo_name == "SA":
            sa = SimulatedAnnealing(1E12, .999, hcp)
            algo_func = sa
        elif algo_name == "GA":
            gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
            ga = StandardGeneticAlgorithm(2000, 1500, 250, gap)
            algo_func = ga
        elif algo_name == "MIMIC":
            fill = [N] * N
            ranges = array('i', fill)
            odd = DiscreteUniformDistribution(ranges)
            df = DiscreteDependencyTree(.1, ranges)
            pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
            pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
            mimic = MIMIC(500, 100, pop)
            algo_func = mimic
        else:
            return

        # ef.resetFunctionEvaluationCount()
        # fit = ConvergenceTrainer(algo_func)
        fit = FixedIterationTrainer(algo_func, 10)
        FILE_NAME="{}_{}_{}.csv".format(algo_name, problem_name, str(t))
        OUTPUT_FILE = os.path.join("results/csv", FILE_NAME)
        with open(OUTPUT_FILE, "wb") as results:
            writer= csv.writer(results, delimiter=',')
            writer.writerow(["iters","fevals","fitness"])
            for i in range(0, iters, 10):
                fit.train()
                #print str(i) + ", " + str(ef.getFunctionEvaluations()) + ", " + str(ef.value(algo_func.getOptimal()))
                writer.writerow([i, ef.getFunctionEvaluations()-i, ef.value(algo_func.getOptimal())])
        
        print algo_name + " trial #" + str(t)
        print algo_name + " Inverse of Distance: " + str(ef.value(algo_func.getOptimal()))
        print "Route:"

        if algo_name == "MIMIC":
            path = []
            optimal = mimic.getOptimal()
            fill = [0] * optimal.size()
            ddata = array('d', fill)
            for i in range(0,len(ddata)):
                ddata[i] = optimal.getContinuous(i)
            order = ABAGAILArrays.indices(optimal.size())
            ABAGAILArrays.quicksort(ddata, order)
            print order
        else:
            path = []
            for x in range(0,N):
                path.append(algo_func.getOptimal().getDiscrete(x))
            print path


##################


points = [[0 for x in xrange(2)] for x in xrange(N)]
for i in range(0, len(points)):
    points[i][0] = random.nextDouble()
    points[i][1] = random.nextDouble()

ef = TravelingSalesmanRouteEvaluationFunction(points)


run("RHC", "travelingsalesman", ef)
run("SA", "travelingsalesman", ef)
run("GA", "travelingsalesman", ef)


# for mimic we use a sort encoding
ef = TravelingSalesmanSortEvaluationFunction(points)

run("MIMIC", "travelingsalesman", ef)
