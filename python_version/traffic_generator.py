"""
    python traffic_generator.py
    Traffic generator class to generates traffic for N nodes using Poisson distribution for a load in Erlang.
    
    Author: Shrinivas Petale (@srpetale)
    Please cite our work:
    @article{petale2022tra,
    title={{TRA}: an efficient dynamic resource assignment algorithm for {MCF}-based {SS-FONs}},
    author={Petale, Shrinivas and Zhao, Juzi and Subramaniam, Suresh},
    journal={Journal of Optical Communications and Networking},
    volume={14},
    number={7},
    pages={511--523},
    year={2022},
    publisher={Optica Publishing Group}
    }
"""

from typing import List
import random
import math

class NetworkTrafficGenerator:
    """
    This class generates the network traffic using Poisson distribution. In each iteration,
    it generates arrival time and holding time. The load (in erlangs) is used as a variable
    \lambda to generate these values using exponential function. 
    """
    def __init__(self,
                number_of_nodes: int,
                list_of_datarates: List[float],
                lambda_in_poisson_distribution: int,
                mean_holding_time: int):
        self.nodes_set: set(int) = set([i for i in range(0, number_of_nodes)])
        self.datarates_set: set(float) = set(list_of_datarates)
        self.lambda_in_poisson_distribution: int = lambda_in_poisson_distribution
        self.mean_holding_time: int = mean_holding_time
        self.current_time: float = 0.0
    
    def generate_connection_data(self):
        source: int = random.sample(self.nodes_set, 1)
        self.nodes_set.remove(source[0])
        destination: int = random.sample(self.nodes_set, 1)
        self.nodes_set.add(source[0])

        datarate: int = random.sample(self.datarates_set, 1)
        
        return source[0], destination[0], datarate[0]

    def generate_arrival_event(self):
        time: float = self.random_exponential(denominator = self.lambda_in_poisson_distribution)
        self.current_time += time
        
        return self.random_exponential(denominator = self.mean_holding_time)
    
    def random_exponential(self, denominator: int):
        pV = 1.0
        while pV == 1.0:
            pV = random.uniform(0.0, 1.0)
        
        pV = (-1.0 / denominator) * math.log(1.0 - pV)
        
        return pV
    
    def get_connection(self):
        source, destination, datarate = self.generate_connection_data()

        return source, destination, datarate, self.current_time, self.generate_arrival_event()