import Network.Networks as nw
import matplotlib as plt
import os
import networkx as nx
import random
import utils.utils as ut
import numpy as np


class SIS:
    def __init__(self, network: nw, beta: float, gamma: float, initial_infected: int):
        self.G = network
        self.beta = beta
        self.gamma = gamma
        self.states = {node: 'S' for node in self.G.G.nodes()}
        self.time_steps = 0
        self.initial_infected = initial_infected

        self.num_nodes = self.G.num_nodes

        if self.num_nodes <= self.initial_infected:
            raise ValueError(f'Number of infected cannot be more or equal to the number of nodes. {self.num_nodes}'
                             f' nodes against {self.initial_infected} initual infected.')

        initial_infected_nodes = random.sample(list(self.G.G.nodes()), initial_infected)

        for node in initial_infected_nodes:
            self.states[node] = 'I'

    def step(self):
        new_states = self.states.copy()

        for node in self.G.G.nodes():
            if self.states[node] == 'I':
                if random.random() < self.gamma:
                    new_states[node] = 'S'
            elif self.states[node] == 'S':
                infected_neighbors = [n for n in self.G.G.neighbors(node) if self.states[n] == 'I']
                if infected_neighbors and random.random() < self.beta:
                    new_states[node] = 'I'

        self.states = new_states
        self.time_steps += 1

    def plot_states(self):
        color_map = ['red' if self.states[node] == 'I' else 'green' for node in self.G.nodes()]
        nx.draw(self.G, node_color=color_map, with_labels=True)
        plt.show()


def run(cwd, config_path):
    run_config = ut.load_yaml(config_path)

    if 'model' not in run_config:
        raise ValueError("The 'model' key is missing in run.yaml.")

    model = run_config['model']
    G, network_param = nw.generate(cwd, config_path)

    match model:
        case 'SIS':
            model_config_path = os.path.join(cwd, f'simulation\\config\\Model\\{model}.yaml')
            model_config = ut.load_yaml(model_config_path)
            model_param = model_config['parameters']
            params = ['num_steps', 'beta', 'gamma', 'initial_infected']

            for p in params:
                if p not in model_param:
                    raise ValueError(f"The '{p}' key is missing in SIS.yaml.")

            print(f"Configuration for model '{model}':")
            print(model_config)

            num_steps = model_param['num_steps']
            beta = model_param['beta']
            gamma = model_param['gamma']
            initial_infected = model_param['initial_infected']

            sim = SIS(G, beta, gamma, initial_infected)

        case _:
            raise ValueError(f"Config file for '{model}' doesn't exist. Please check that in run.yaml, model is set to"
                             f" a possible value: ('SIS', ).")

    infected_count = []

    for _ in range(num_steps):
        sim.step()
        infected_count.append(list(sim.states.values()).count('I') / sim.num_nodes)

    return infected_count, [network_param, model_config]
