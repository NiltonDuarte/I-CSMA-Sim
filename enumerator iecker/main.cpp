#include <iostream>	// cout
#include <stdint.h>	// uint64_t
#include <stdio.h>
#include <fstream>	// ifstream, ofstream
#include <iomanip>      // std::setprecision
#include <ctime>	// clock

#include "Enumerator.h"

#define NETWORKS_PATH "networks/"
typedef unsigned __int128 uint128_t;

using namespace std;

int main(int argc, char** argv)
{
	if(argc != 2)
	{
		cout << "Missing arguments!" << endl;
		cout << "USAGE: ./main <file name>" << endl;
		return 0;
	}	

        string file = argv[1];

	string name = "networks/teste.dat";

	ofstream outfile;
	ifstream infile;

	Network* network;
	Enumerator* enumerator;

	uint64_t links, fsets, delta;
	double objfn;

	network = new Network(file);
	links = network->get_links().size();
	delta = network->get_delta();

	cout << "rede criada" << endl;
	if(links == 0) {
		return 0;
	}
	
	if(links > 128) {
		return 0;
	}

	remove(name.c_str());
	outfile.open(name, ios::binary | ios::out);
			       	
	enumerator = new Enumerator(network, &outfile);
	enumerator->find_fset_entry();
	fsets = enumerator->get_fset();
	
	cout << fsets << endl;
		
	outfile.close();
			
	delete enumerator;
	delete network;

	return 0;
}
