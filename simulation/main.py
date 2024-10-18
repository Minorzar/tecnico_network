import Network.Networks as nw
import Models.Model as mod
import utils.utils as ut

import os
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import numpy as np


def main():
    cwd = ut.CWD
    conf = ut.CONFIG_PATH

    run_conf = ut.load_yaml(conf)
    if 'plot' not in run_conf:
        raise ValueError("The 'plot' key is missing in run.yaml.")
    if 'iteration' not in run_conf:
        raise ValueError("The 'iteration' key is missing in run.yaml.")
    if 'keep' not in run_conf:
        raise ValueError("The 'keep' key is missing in run.yaml.")

    plot = max(0, min(1, run_conf['plot']))
    iteration = run_conf['iteration']
    keep = run_conf['keep']

    sims = []

    for _ in range(iteration):
        simu, [network_param, model_param], avg_degree = mod.run(cwd, conf)
        sims.append(simu)

    sim_mean = [sum(sim[i] for sim in sims) / len(sims) for i in range(len(sims[0]))]
    sims.append(sim_mean)

    ut.save_plot(network_param, model_param, sims, iteration, avg_degree, plot)

    if os.path.exists(ut.SAVE_PATH) and not keep:
        os.remove(ut.SAVE_PATH)


if __name__ == "__main__":
    main()
