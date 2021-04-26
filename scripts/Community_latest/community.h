// File: community.h
// -- community detection header file
//-----------------------------------------------------------------------------
// Community detection
// Based on the article "Fast unfolding of community hierarchies in large networks"
// Copyright (C) 2008 V. Blondel, J.-L. Guillaume, R. Lambiotte, E. Lefebvre
//
// This program must not be distributed without agreement of the above mentionned authors.
//-----------------------------------------------------------------------------
// Author   : E. Lefebvre, adapted by J.-L. Guillaume
// Email    : jean-loup.guillaume@lip6.fr
// Location : Paris, France
// Time	    : February 2008
//-----------------------------------------------------------------------------
// see readme.txt for more details

#ifndef COMMUNITY_H
#define COMMUNITY_H

#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <map>
#include <cmath>

#include "graph_binary.h"

using namespace std;

//#define lambda1 0.5
//#define lambda2 0//0.7
//#define N       200

class Community {
 public:
  vector<double> neigh_weight;
  vector<unsigned int> neigh_pos;
  unsigned int neigh_last;

  Graph g; // network to compute communities for
  int size; // nummber of nodes in the network and size of all vectors
  vector<int> n2c; // community to which each node belongs
  vector<double> in,tot; // used to compute the modularity participation of each community
  vector<int> sizeForComm;

  // number of pass for one level computation
  // if -1, compute as many pass as needed to increase modularity
  int nb_pass;
  int SIZE;

  int N;
  double lambda1;
  double lambda2;

  // a new pass is computed if the last one has generated an increase 
  // greater than min_modularity
  // if 0. even a minor increase is enough to go for one more pass
  double min_modularity;
  int nc;

  // constructors:
  // reads graph from file using graph constructor
  // type defined the weighted/unweighted status of the graph file
  Community (char *filename, char *filename_w, int type, int nb_pass, double min_modularity, int N, double lambda1, double lambda2);
  // copy graph
  Community (Graph g, int nb_pass, double min_modularity, int N, double lambda1, double lambda2);

  // initiliazes the partition with something else than all nodes alone
  void init_partition(char *filename_part);

  // display the community of each node
  void display();

  // remove the node from its current community with which it has dnodecomm links
  inline void remove(int node, int comm, double dnodecomm);

  // insert the node in comm with which it shares dnodecomm links
  inline void insert(int node, int comm, double dnodecomm);

  // compute the gain of modularity if node where inserted in comm
  // given that node has dnodecomm links to comm.  The formula is:
  // [(In(comm)+2d(node,comm))/2m - ((tot(comm)+deg(node))/2m)^2]-
  // [In(comm)/2m - (tot(comm)/2m)^2 - (deg(node)/2m)^2]
  // where In(comm)    = number of half-links strictly inside comm
  //       Tot(comm)   = number of half-links inside or outside comm (sum(degrees))
  //       d(node,com) = number of links from node to comm
  //       deg(node)   = node degree
  //       m           = number of links
  inline double modularity_gain(int node, int comm, double dnodecomm, double w_degree);

  // compute the set of neighboring communities of node
  // for each community, gives the number of links from node to comm
  void neigh_comm(unsigned int node);

  // compute the modularity of the current partition
  double modularity();

  // displays the graph of communities as computed by one_level
  void partition2graph();
  // displays the current partition (with communities renumbered from 0 to k-1)
  void display_partition();

  // generates the binary graph of communities as computed by one_level
  Graph partition2graph_binary();

  // compute communities of the graph for one level
  // return true if some nodes have been moved
  bool one_level();

  int H(int nc);
};

inline void
Community::remove(int node, int comm, double dnodecomm) {
  assert(node>=0 && node<size);

  tot[comm] -= g.weighted_degree(node);
  in[comm]  -= 2*dnodecomm + g.nb_selfloops(node);
  n2c[node]  = -1;
}

inline void
Community::insert(int node, int comm, double dnodecomm) {
  assert(node>=0 && node<size);

  tot[comm] += g.weighted_degree(node);
  in[comm]  += 2*dnodecomm + g.nb_selfloops(node);
  n2c[node]=comm;
}

inline double
Community::modularity_gain(int node, int comm, double dnodecomm, double w_degree) {
  assert(node>=0 && node<size);

  double totc = (double)tot[comm];
  double degc = (double)w_degree;
  double m2   = (double)g.total_weight;
  double dnc  = (double)dnodecomm;
  double Wi = in[comm];
  double WiPlus  = in[(comm + 1) % size];
  double WiMinus = in[(comm - 1) % size];

  double sizeBalance = 0.0, loadBalance = 0.0;
  //cout << lambda2 << endl;
  //double regu = lambda1*(fabs(Wi - WiPlus) + fabs(Wi - WiMinus))/m2 + temp * (new_nc - old_nc)/(SIZE - N);
  return (1.0/(2*m2))*(dnc - totc*degc/m2);
}

inline int
Community::H(int nc) {

	if (nc > N) {
		return 1;
	} else {
		return 0;
	}
}
#endif // COMMUNITY_H
