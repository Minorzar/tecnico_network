import yaml
import os
import networkx as nx
import matplotlib.pyplot as plt

CWD = os.getcwd()
CONFIG_PATH = os.path.join(CWD, r'simulation\config\run.yaml')


def VAL_ERROR(network_type):
    raise ValueError(f"Config file for '{network_type}' doesn't exist. Please check that in run.yaml, network is set to"
                     f" a possible value: ('BA', 'lattice', 'minimal' or 'random').")


def STRUCT_ERROR(struct):
    raise ValueError(f"Structure '{struct}' doesn't exist. Please check that in minimal.yaml, structure is set to a"
                     f" possible value: ('path', 'tree', 'small_conn').")


def load_yaml(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)


class Network:
    def __init__(self, config):
        self.type = config['type']
        param = config['parameters']
        match self.type:
            case 'BA':
                m = param['m']
                num_nodes = param['num_nodes']
                self.G = nx.barabasi_albert_graph(num_nodes, m)
            case 'lattice':
                dim = param['dimension']
                self.G = nx.grid_2d_graph(dim, dim)
            case 'minimal':
                num_nodes = param['num_nodes']
                structure = param['structure']
                match structure:
                    case 'path':
                        self.G = nx.path_graph(num_nodes)
                    case 'tree':
                        self.G = nx.random_tree(num_nodes)
                    case 'small_conn':
                        self.G = nx.random_regular_graph(3, num_nodes)
                    case _:
                        raise STRUCT_ERROR(structure)
            case 'random':
                num_nodes = param['num_nodes']
                conn = param['connectivity']
                self.G = nx.erdos_renyi_graph(num_nodes, conn)
            case _:
                VAL_ERROR(self.type)

    def plot(self):
        nx.draw(self.G)
        plt.show()


def run():
    run_config = load_yaml(CONFIG_PATH)

    if 'network' not in run_config:
        raise ValueError("The 'network' key is missing in run.yaml.")

    network_type = run_config['network']
    network_config_path = os.path.join(CWD, f'simulation\\config\\network\\{network_type}.yaml')

    if os.path.exists(network_config_path):
        network_config = load_yaml(network_config_path)

        print(f"Configuration for network '{network_type}':")
        print(network_config)

        return Network(network_config)

    else:
        VAL_ERROR(network_type)
