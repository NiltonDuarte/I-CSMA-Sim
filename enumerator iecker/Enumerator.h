/*
** Enumerator class implementing an algorithm that enumerates all feasible sets of links
** Author: Guilherme Iecker Ricardo
** Institute: Systems Engineering and Computer Science Program - COPPE/UFRJ
*/

#pragma once

#include <iostream>	// cout, endl
#include <stdint.h>	// uint64_t
#include <math.h>	// pow, log
#include <vector>	// vector
#include <fstream>	// ifstream

#include "Node.h"
#include "Link.h"
#include "Network.h"

#define MAX 2331756040 // a=8000,n=117,r=390,m=40

typedef unsigned __int128 uint128_t;

using namespace std;

class Enumerator
{
private:
	uint64_t n, m, f, stop;
	vector<Node*> cset;
	Network* network;
	ofstream* outfile;

	void add_link(uint64_t);
	double calculate_interference(Node*, Node*);
	bool is_feasible();
	bool primary_test();
	double calculate_sinr(Link*);
	void del_link(uint64_t);

public:
	Enumerator(Network*, ofstream*);
	void find_fset_entry();
	void find_fset(uint128_t);
	uint64_t get_fset();
	void print_cset();
};

uint64_t log2(uint128_t x) {
        uint64_t count = 0;
        while((x & 1) == 0) {
                x = x >> 1;
                count++;
        }
        return count;
}

uint128_t pow2(uint64_t x) {
        uint128_t res = 1;
        res = res << x;
        return res;
}

void Enumerator::find_fset_entry() {
	uint64_t limit = m;
	uint128_t numero;
	for (uint64_t i = 0; i < limit; i++) {
		numero = pow2(i);
		find_fset(numero);
	}
}

void Enumerator::find_fset(uint128_t x) {
	/*if (f >= stop) {
		f = 0;
		stop = 0;
		return;
	}*/
	uint64_t limit = log2(x);
	add_link(limit);
	
	if (is_feasible()) {
		outfile->write((char*)&x, sizeof(uint128_t));
		print_cset();
		f++;
		for (uint64_t i = 0; i < limit; i++) find_fset(x + pow2(i));
	}
	del_link(limit);
}

void Enumerator::add_link(uint64_t index)
{
	cset.push_back(network->get_node(index));
}

double Enumerator::calculate_interference(Node* a, Node* b)
{
	double dist = a->distance(*b);
	if (dist > network->d0)
		return pow(10.0, ((network->tpower_dBm - network->l0_dB - 10 * network->alpha*log10(dist / network->d0)) / 10.0));
	else
    		return pow(10.0, network->tpower_dBm - network->l0_dB / 10.0);
}

bool Enumerator::is_feasible()
{
	if(cset.size() < 2)
		return true;
	if(primary_test()/*secondary_test()*/)
		return true;
	return false;
}

bool Enumerator::primary_test()
{
	for (vector<Node*>::iterator i = cset.begin(); i != cset.end(); ++i)
	{
		for (vector<Node*>::iterator j = i + 1; j != cset.end(); ++j) {				
			if(network->there_is_link(*(*i), *(*j))) return false;
		}
	}
	return true;
}

double Enumerator::calculate_sinr(Link* l)
{
    return l->get_rpower() / (network->noise_mW + l->clc_interf());
}

void Enumerator::del_link(uint64_t index)
{
	cset.pop_back();
}

Enumerator::Enumerator(Network* g, ofstream* file):
	n(g->get_nodes().size()), m(g->get_links().size()), network(g), outfile(file)
{
	stop = (uint64_t) (MAX/m);
	f = 0;
}

uint64_t Enumerator::get_fset()
{
	return f;
}

void Enumerator::print_cset() {
	//cout << "cset: ";
	for (vector<Node*>::iterator i = cset.begin(); i != cset.end(); ++i) {
		cout << (*i)->get_id() << " ";
	}
	cout << endl;
}
