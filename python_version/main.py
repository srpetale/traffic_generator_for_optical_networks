"""
    python main.py
    Generates traffic for N nodes using Poisson distribution for a load in Erlang.
    
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
from traffic_generator import NetworkTrafficGenerator

'''
Constants
'''
number_of_nodes: int = 14
list_of_datarates: List[float] = [40, 100, 400]
number_of_connections: int = 10
load_in_erlang: int = 600
mean_holding_time: int = 1


'''
Generate Network Traffic
'''
traffic_generator = NetworkTrafficGenerator(number_of_nodes=number_of_nodes,
list_of_datarates=list_of_datarates,
lambda_in_poisson_distribution=load_in_erlang,
mean_holding_time=mean_holding_time)

connection_id = 0
while connection_id < number_of_connections:
    source, destination, datarate, arrival_time, holding_time = traffic_generator.get_connection()

    print(f'The connection of datarate {datarate} Gbps arrives at node {source} to node {destination} at {arrival_time} and exists for {holding_time}. It exists from {arrival_time} to {arrival_time+holding_time}.')
    
    connection_id += 1