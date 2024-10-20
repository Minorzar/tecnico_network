import Network.Networks as nw
import matplotlib.pyplot as plt
import os
import networkx as nx
import random
import utils.utils as ut
import numpy as np
import datetime


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


def run_dyn(cwd, config_path, run_param):
    run_config = ut.load_yaml(config_path)
    date_str = datetime.datetime.now().strftime("%d-%m-%Y")
    time_str = datetime.datetime.now().strftime("%H-%M-%S")

    os.makedirs(f"out/{date_str}", exist_ok=True)

    if 'model' not in run_config:
        raise ValueError("The 'model' key is missing in run.yaml.")

    if 'keep' not in run_config:
        raise ValueError("The 'keep' key is missing in run.yaml.")

    if 'iteration' not in run_config:
        raise ValueError("The 'iteration' key is missing in run.yaml.")

    model = run_config['model']
    keep = run_config['keep']
    num_iteration = run_config['iteration']

    G, network_param, avg_degree = nw.generate(cwd, config_path, keep)

    treshold = 1/(avg_degree + 1)

    match model:
        case 'SIS':
            model_config_path = os.path.join(cwd, f'simulation\\config\\Model\\{model}.yaml')
            model_config = ut.load_yaml(model_config_path)

            if 'parameters' not in model_config:
                raise ValueError(f"The 'parameters' key is missing in SIS.yaml.")

            model_param = model_config['parameters']

            model_params = ['num_steps', 'initial_infected']
            params = ['range', 'step']

            for p in model_params:
                if p not in model_param:
                    raise ValueError(f"The '{p}' key is missing in parameters in SIS.yaml.")

            for p in params:
                if p not in run_param:
                    raise ValueError(f"The '{p}' key is missing in parameters in run.yaml.")

            [start, end] = map(int, run_param['range'].split('-'))
            step = run_param['step']
            num_steps = model_param['num_steps']
            initial_infected = model_param['initial_infected']

            diff = np.zeros((int((end - start + step) / step), int((end - start + step) / step)))

            beta_values = np.arange(start, end + step, step)
            gamma_values = np.arange(start, end + step, step)

            for i, beta in enumerate(beta_values):
                for j, gamma in enumerate(gamma_values):
                    delta_I = []

                    for it in range(num_iteration):
                        sim = SIS(G, beta, gamma, initial_infected)
                        infected_count = [initial_infected]

                        if not os.path.exists(ut.SAVE_PATH):
                            ut.network_save(G.G)

                        for _ in range(num_steps):
                            sim.step()
                            infected_count.append(list(sim.states.values()).count('I'))

                        final_infected = infected_count[-1]
                        delta_I.append((final_infected - initial_infected)/sim.num_nodes)

                    diff[i, j] = sum(delta_I)/len(delta_I)

            plt.figure(figsize=(10, 6))
            plt.xlim(-(start + step), end + step)
            plt.ylim(-(start + step), end + step)
            contour = plt.contourf(beta_values, gamma_values, diff, levels=[-1, -0.3, 0, 0.3, 1], alpha=0.7)
            plt.colorbar(contour, label="Infected variation (ΔI)")

            y = beta_values / treshold
            plt.plot(beta_values, y, label=f'treshold')

            plt.xlabel('Transmission rate (β)')
            plt.ylabel('Healing rate (γ)')
            plt.title(f'Infected evolution on SIS model with γ and β in a range of {start} to {end} for {G.type} '
                      f'network')
            plt.savefig(f'out/{date_str}/{time_str}.pdf', format='pdf')
            plt.show()


def run_single(cwd, config_path):
    run_config = ut.load_yaml(config_path)

    if 'model' not in run_config:
        raise ValueError("The 'model' key is missing in run.yaml.")

    if 'keep' not in run_config:
        raise ValueError("The 'keep' key is missing in run.yaml.")

    model = run_config['model']
    keep = run_config['keep']

    G, network_param, avg_degree = nw.generate(cwd, config_path, keep)

    match model:
        case 'SIS':
            model_config_path = os.path.join(cwd, f'simulation\\config\\Model\\{model}.yaml')
            model_config = ut.load_yaml(model_config_path)
            model_param = model_config['parameters']
            params = ['num_steps', 'beta', 'gamma', 'initial_infected']

            for p in params:
                if p not in model_param:
                    raise ValueError(f"The '{p}' key is missing in parameters in SIS.yaml.")

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

    infected_count = [initial_infected / sim.num_nodes]

    for _ in range(num_steps):
        sim.step()
        infected_count.append(list(sim.states.values()).count('I') / sim.num_nodes)

    return infected_count, [network_param, model_config], avg_degree
