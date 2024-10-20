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
    if 'mode' not in run_conf:
        raise ValueError("The 'mode' key is missing in run.yaml.")

    mode = run_conf['mode']
    plot = max(0, min(1, run_conf['plot']))
    iteration = run_conf['iteration']
    keep = max(0, min(1,run_conf['keep']))

    match mode:
        case "dynamic":
            if 'parameters' not in run_conf:
                raise ValueError("The 'parameters' key is missing in run.yaml.")

            param = run_conf['parameters']

            mod.run_dyn(cwd, conf, param)

        case "single":
            sims = []

            for _ in range(iteration):
                simu, [network_param, model_param], avg_degree = mod.run_single(cwd, conf)
                sims.append(simu)

            sim_mean = [sum(sim[i] for sim in sims) / len(sims) for i in range(len(sims[0]))]
            sims.append(sim_mean)

            ut.save_plot(network_param, model_param, sims, iteration, avg_degree, plot)

        case _:
            raise ValueError(f"The mode {mode} is not a possible value for mode. Change it inside run.yaml,value can "
                             f"be either 'dynamic' or 'single'.")

    if os.path.exists(ut.SAVE_PATH) and not keep:
        os.remove(ut.SAVE_PATH)


if __name__ == "__main__":
    main()
