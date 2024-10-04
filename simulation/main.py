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

    plot = max(0, min(1, run_conf['plot']))

    simu, [network_param, model_param] = mod.run(cwd, conf)

    ut.save_plot(network_param, model_param, simu, plot)


if __name__ == "__main__":
    main()
