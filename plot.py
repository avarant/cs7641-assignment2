import sys
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

sns.set_theme(style='darkgrid')


def get_data(algo_name, problem):
    dfs = []
    for fp in glob.glob(f'results/csv/{algo_name}_{problem}_*.csv'):
        df = pd.read_csv(fp)
        dfs.append(df)
    avg_df = pd.concat(dfs).groupby(level=0).mean()
    return avg_df

def plot_convergence(problem):
    """convergence plot: fitness v iters
    """
    plt.clf()
    algos = ["RHC", "SA", "GA", "MIMIC"]
    for algo_name in algos:
        df = get_data(algo_name, problem)
        sns_plot=sns.lineplot(x="iters", y="fitness", data=df, legend="full", label=algo_name)
    
    ax = sns_plot.axes
    ax.legend(loc="best")
    sns_plot.set_title(f"{problem} Fitness Convergence")
    fig=sns_plot.get_figure()
    fig.savefig(os.path.join('results/plot', f'{problem}_convergence.png'))

def plot_feval_vs_iters(problem):
    plt.clf()
    algos = ["RHC", "SA", "GA", "MIMIC"]
    for algo_name in algos:
        df = get_data(algo_name, problem)
        sns_plot=sns.lineplot(x="iters", y="fevals", data=df, legend="full", label=algo_name)
    
    ax = sns_plot.axes
    ax.legend(loc="best")
    sns_plot.set_title(f"{problem} Function evaluations vs Iterations")
    fig=sns_plot.get_figure()
    fig.savefig(os.path.join('results/plot', f'{problem}_fevals_v_iters.png'))

def plot_feval_vs_time(problem):
    plt.clf()
    algos = ["RHC", "SA", "GA", "MIMIC"]
    for algo_name in algos:
        df = get_data(algo_name, problem)
        sns_plot=sns.lineplot(x="times", y="fevals", data=df, legend="full", label=algo_name)
    
    ax = sns_plot.axes
    ax.legend(loc="best")
    sns_plot.set_title(f"{problem} Function evaluations vs Time")
    fig=sns_plot.get_figure()
    fig.savefig(os.path.join('results/plot', f'{problem}_fevals_v_time.png'))

def plot_time_vs_iters(problem):
    plt.clf()
    algos = ["RHC", "SA", "GA", "MIMIC"]
    for algo_name in algos:
        df = get_data(algo_name, problem)
        sns_plot=sns.lineplot(x="iters", y="times", data=df, legend="full", label=algo_name)
    
    ax = sns_plot.axes
    ax.legend(loc="best")
    sns_plot.set_title(f"{problem} Time vs Iterations")
    fig=sns_plot.get_figure()
    fig.savefig(os.path.join('results/plot', f'{problem}_time_v_iters.png'))

def plot_log_time_vs_iters(problem):
    plt.clf()
    algos = ["RHC", "SA", "GA", "MIMIC"]
    for algo_name in algos:
        df = get_data(algo_name, problem)
        df['log_times'] = np.log(df['times'])
        sns_plot=sns.lineplot(x="iters", y="log_times", data=df, legend="full", label=algo_name)
    
    ax = sns_plot.axes
    ax.legend(loc="best")
    sns_plot.set_title(f"{problem} Log Time vs Iterations")
    fig=sns_plot.get_figure()
    fig.savefig(os.path.join('results/plot', f'{problem}_log_time_v_iters.png'))

########################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("problem")
    args = parser.parse_args()

    problem = args.problem
    print(f"Plotting {problem} graphs")

    plot_convergence(problem)
    plot_feval_vs_iters(problem)
    plot_feval_vs_time(problem)
    plot_time_vs_iters(problem)
    plot_log_time_vs_iters(problem)
