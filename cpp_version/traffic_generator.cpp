/*
    C++ traffic_generator.cpp
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
*/

#include <iostream>
#include <vector>
#include <time.h>
#include <math.h>

using namespace std;

// Global variables
int number_of_nodes = 14;
vector<float> list_of_datarates = { 40, 100, 400 };
int number_of_connections = 10;
int load_in_erlang = 600;
int mean_holding_time = 1;

// Stucts and Class
struct ConnectionRequest {
    int source = 0;
    int destination = 0;
    int datarate = 0;
    double arrival_time = 0.0;
    double holding_time = 0.0;
};

class NetworkTrafficGenerator {
    /*
    This class generates the network traffic using Poisson distribution. In each iteration,
    it generates arrival time and holding time. The load (in erlangs) is used as a variable
    \lambda to generate these values using exponential function. 
    */
   private:
   int number_of_nodes;
   int lambda_in_poisson_distribution;
   int mean_holding_time;
   double current_time;

   ConnectionRequest get_connection_data();
   double generate_arrival_event();
   double random_exponential(double denominator);

   public:
   NetworkTrafficGenerator(int number_of_nodes, int lambda_in_poisson_distribution, int mean_holding_time){
    this->number_of_nodes = number_of_nodes;
    this->lambda_in_poisson_distribution = lambda_in_poisson_distribution;
    this->mean_holding_time = mean_holding_time;
    current_time = 0.0;
   }
   ConnectionRequest get_connection();
};

ConnectionRequest NetworkTrafficGenerator::get_connection_data(){
    ConnectionRequest connection_request;
    connection_request.source = rand() % number_of_nodes;
	do {
		connection_request.destination = rand() % number_of_nodes;
	} while (connection_request.destination == connection_request.source);

    connection_request.datarate = list_of_datarates[rand() % list_of_datarates.size()];
    
    return connection_request;
}

double NetworkTrafficGenerator::generate_arrival_event() {
	current_time += random_exponential(lambda_in_poisson_distribution);
	return random_exponential(mean_holding_time);
}

double NetworkTrafficGenerator::random_exponential(double denominator)
{
	double pV = 1.0;
	while (pV == 1.0) {
		pV = (double)rand() / (double)RAND_MAX;
	}
	pV = (-1.0 / denominator) * log(1 - pV);
	return pV;
}

ConnectionRequest NetworkTrafficGenerator::get_connection() {
    ConnectionRequest connection_request = get_connection_data();

    connection_request.holding_time = generate_arrival_event();
    connection_request.arrival_time = current_time;

    return connection_request;
}

// Main execution
int main(){
    int load_in_erlang = 600;
    srand(time(NULL));
    NetworkTrafficGenerator network_traffic_generator(number_of_nodes, load_in_erlang, mean_holding_time);
    
	int connection_id = 0;
	while (connection_id < number_of_connections) {
        ConnectionRequest connection_request = network_traffic_generator.get_connection();

        cout << "The connection of datarate " << connection_request.datarate << " Gbps arrives at node " << connection_request.source << " to node " << connection_request.destination << " at " << connection_request.arrival_time << " and exists for " << connection_request.holding_time << ". It exists from " << connection_request.arrival_time << " to " << connection_request.arrival_time+connection_request.holding_time << "." << endl;
        
        connection_id += 1;
    }

    return 0;
}