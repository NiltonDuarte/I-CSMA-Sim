/*
** Network class modeling the entire network with nodes and links
** Author: Guilherme Iecker Ricardo
** Institute: Systems Engineering and Computer Science Program - COPPE/UFRJ
*/


#pragma once

#include <stdint.h>	// uint64_t
#include <iostream>	// cout
#include <vector>		// vector
#include <math.h>		// pow, log10
#include <fstream>
#include <string>

#include "Link.h"
#include "Node.h"

using namespace std;

typedef unsigned __int128 uint128_t;

class Network {
private:
	uint64_t num_nodes, delta;
	double area_side;
	double tpower;

	vector<Node> nodes;
	vector<Link> links;

public:
	const double bandwidth = 20e06;
	const double noise_mW = 1380e-23 * 290 * bandwidth;
	const double noise_dBm = 10 * log10(noise_mW);
	const double d0 = 1.0;
	const double l0_dB = 0.0;
	const double alpha = 4.0;
	const double beta_dB = 25.0;
	const double beta_mW = pow(10, beta_dB / 10.0);
	const double tpower_dBm = 10 * log10(tpower);
	const double max_range = d0*pow(10, (tpower_dBm - noise_dBm - beta_dB - l0_dB) / (10 * alpha));

	Network(uint64_t _n = 100, double _a = 3000.0, double _p = 300.0) : num_nodes(_n), area_side(_a), tpower(_p)
	{
		delta = 0;
		set_nodes();
		set_links();
	}

	Network(string _name) {
		Node* node;
		Link* link;
		int r, s, n, m;

		ifstream _file(_name);
		_file >> n;
		_file >> m;
		for (int i = 0; i < n; i++) {
			node = new Node(i, 1000.0);
			nodes.push_back(*node);
		}
		for (int i = 0; i < m; i++) {
			_file >> r >> s;
			link = new Link(&nodes[r], &nodes[s], i, 0, 0);
			links.push_back(*link);
		}
		_file.close();
		print_links();
		print_nodes();
	}
	vector<Node> get_nodes();
	vector<Link> get_links();

	void set_nodes();
	void set_links();

	Node* get_node(uint128_t);
	void print_links();
	void print_nodes();

	uint64_t get_delta();
	bool there_is_link(Node, Node);
};

#include "Network.h"

vector<Node> Network::get_nodes()
{
	return nodes;
}

vector<Link> Network::get_links()
{
	return links;
}

void Network::set_nodes()
{
	Node* n;
	for (uint64_t i = 0; i < num_nodes; i++)
	{
		n = new Node(i, area_side);
		nodes.push_back(*n);
	}
}

void Network::set_links() {
	double pr, dist;
	uint64_t index = 0;
	for (vector<Node>::iterator i = nodes.begin(); i != nodes.end(); ++i) {
		for (vector<Node>::iterator j = i + 1; j != nodes.end(); ++j) {
			dist = i->distance(*j);
			if (dist <= max_range) {
				i->inc_degree();
				j->inc_degree();
				pr = (dist > d0) ? pow(10.0, ((tpower_dBm - l0_dB - 10*alpha*log10(dist / d0))/10.0)) : pow(10.0, ((tpower_dBm - l0_dB) / 10.0));
				links.push_back(Link(&(*i), &(*j), index++, dist, pr));
			}
		}
	}
	for (vector<Node>::iterator i = nodes.begin(); i != nodes.end(); ++i) {
		delta = (i->get_degree() > delta) ? i->get_degree() : delta;
		i->set_degree(0);
	}
}

Node* Network::get_node(uint128_t idx)
{
	return &(nodes[idx]);
}

void Network::print_links()
{
	cout << "Printing links..." << endl;
	for (vector<Link>::iterator i = links.begin(); i != links.end(); ++i)
		cout << "Link id=" << i->get_id() << " sender(id=" << (*i).get_sender()->get_id() << ", deg=" << (*i).get_sender()->get_degree() << ") receiver(id=" << (*i).get_recver()->get_id() << ", deg=" << (*i).get_recver()->get_degree() << ")" << endl;
}

void Network::print_nodes()
{
	cout << "Printing nodes..." << endl;
	for (vector<Node>::iterator i = nodes.begin(); i != nodes.end(); ++i)
                cout << "Node id=" << i->get_id() << " (" << i->get_x() << "," << i->get_y() << ")" << endl;
}

uint64_t Network::get_delta() { return delta; }

bool Network::there_is_link(Node u, Node v) {
	for (vector<Link>::iterator i = links.begin(); i != links.end(); ++i) {
		if (((i->get_sender()->get_id() == u.get_id())&&(i->get_recver()->get_id() == v.get_id())) ||
                    ((i->get_sender()->get_id() == v.get_id())&&(i->get_recver()->get_id() == u.get_id())))
			return true;
	}
	return false;
}
