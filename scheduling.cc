#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <glpk.h>
#include "scheduling.h"
#include <lemon/matching.h>
#include <lemon/smart_graph.h>
#include <lemon/concepts/graph.h>
#include <lemon/concepts/maps.h>

using namespace std;
using namespace lemon;

// Procedure that returns each input parameter
int paramCount = 0;
char* getParam(int argc, char** argv) {
  paramCount++;
  return argv[paramCount];
}

// Procedure that generates a uniform random number between 0 and 1
double uniform() {
  double r = rand()/((double)RAND_MAX+1);
  return r;
}

// Procedure that reads all input parameters
void readParams(int argc, char** argv) {

  // Number of nodes in the area
  numNodes = atoi(getParam(argc, argv)); 

  // Square area side size (meters)
  areaSide = atof(getParam(argc, argv)); 

  // Central frequency (Hz)
  freq = 2400e06; 

  // Bandwidth (Hz)
  bandwidth = 20e06;

  // Noise-floor (dBm)
  // noise-floor = k*T*B, where: 
  //    k=1380e-23 mW/sK,
  //    T=290K, 
  //    B=bandwidth
  noiseFloor = 1380e-23*290*bandwidth;

  noiseFloordBm = 10*log10(noiseFloor);

  // Path loss exponent of log-distance propagation model
  alpha = atof(getParam(argc, argv)); 

  // Reference distance of log-distance propagation model (meters)
  d0 = 1.0; 

  // L0 -> Loss in dB at the reference distance (d0) using free-space model;
  // Pt/Pr = (4*PI*f*/c*d)**2
  // L0dB = 20*log10(4*M_PI*freq*d0/3e8);

  // This means Pr(d<=d0)=Pt;
  L0dB=0.0;

  // Minimum SINR needed to decode a transmission (in dB)
  betadB = atof(getParam(argc, argv)); 
  // Converting to ratio
  beta = pow(10,betadB/10.0);

  PtmW = atof(getParam(argc, argv));

  PtdBm = 10*log10(PtmW);
  
  // Loss in dB at the distance d
  // L = 10*alpha*log10(d/d0)
  // So, Pt (dBm) = L(dB) + noiseFloor(dBm) + beta(dB) + L0(dB) 
  //PtdBm = 10*alpha*log10(maxRange/d0) + noiseFloordBm + betadB + L0dB;

  maxRange = d0*pow(10,(PtdBm-noiseFloordBm-betadB-L0dB)/(10*alpha));

  // Loss in dB at the distance d
  // L = 10*alpha*log10(d/d0)
  // So, Pt (dBm) = L(dB) + noiseFloor(dBm) + beta(dB) + L0(dB) 
  // PtdBm = 10*alpha*log10(maxRange/d0) + noiseFloordBm + betadB + L0dB;

  // Plotting parameters
  // fprintf(stderr,"Pt=%lf (dBm) PtmW=%lf (mW) beta=%lf (dB) alpha=%lf (dimensionless) d0=%lf (m) noiseFloor=%lf (dBm) maxRange=%lf (m)\n", PtdBm, PtmW, betadB, alpha, d0, noiseFloordBm, maxRange);

  delta_mi = atof(getParam(argc, argv));
  
  outputfile1 = getParam(argc, argv); // Name of the output file 1

  outputfile2 = getParam(argc, argv); // Name of the output file 2
  
  run = atoi(getParam(argc, argv)); // Number of simulation run

  // Setting the seed of random number generator as the simulation run
  srand(run);
}

void placeNodes() {

  int i;

  for (i=0; i < numNodes; ++i) {
    posX[i]= uniform()*areaSide;
    posY[i]= uniform()*areaSide;
  }
}

// Procedure that generate matrices needed by the scheduling algorithms
void generateStructures() {

  // Generating the distance and the power reception matrices
  // and links

  int i,j;
  float PrdBm;

  edges=0;
  for (i = 0; i < numNodes; i++) {
    grau[i]=0;
    for (j = 0; j < numNodes; j++) {
      if (i!=j) {
	dist[i][j] = sqrt(pow(posX[i]-posX[j],2) + pow(posY[i]-posY[j],2));
	if (dist[i][j] > d0) {
	  PrdBm = PtdBm - L0dB - 10*alpha*log10(dist[i][j]/d0);
	  PrmW[i][j] = pow(10.0, PrdBm/10.0);
	} else {
	  PrdBm = PtdBm - L0dB;
	  PrmW[i][j] = pow(10.0, PrdBm/10.0);
	}
	if (dist[i][j] <= maxRange) {
	  if (i<j) {
	    links[edges].sender = i;
	    links[edges].recver = j;
	    links[edges].weight = 0.0;
	    links[edges].scheduled = 0;
	    ++edges;
	    ++grau[i];
	  }
	}
      }	else {
	PrmW[i][j] = 0.0;
	dist[i][j] = 0.0;
      }
    }
  }

  if (edges > 0) {
    fprintf(stderr,"nr of edges: %d\n",edges);
    for (i = 0; i < edges; i++) {
      fprintf(stderr,"link %d: %d-%d - on=%d - w=%f\n",i, links[i].sender, links[i].recver, links[i].weight, links[i].scheduled);
    }
  } else {
    exit(0);
  }
}

void initialize(void) {

  int i,j;
  
  for(i = 0; i < numNodes; i++) {
    for(j = 0; j < numNodes; j++) {
      K[i][j]=0;
      interference[j]=0.0;
    }
  }
}

void adjustInterference(int sender, int recver) {

  int i;
  
  for(i = 0; i < numNodes; i++) {
    if ( i != sender && i != recver ) {
      interference[i] = interference[i] + PrmW[sender][i];
    }
  }		
}

int addLink(int id) {

  int i, j;

  // Is the links(id) feasible in this slot?

  for(i = 0; i < numNodes; i++) {
    for(j = 0; j < numNodes; j++) {
      // foreach edge scheduled in this slot...
      if (K[i][j] == 1) {
	// if links(id) has same endpoint...
	if (links[id].sender == i || links[id].sender == j || links[id].recver == i || links[id].recver == j) {
	  // is not feasible
	  //fprintf(stderr, "%d: %d-%d is not feasible - same endpoint that %d-%d \n",id,links[id].sender, links[id].recver, i, j);
	  return false;
	} else {
	  // or if links(id) power at some receiver added to interference is greater than minSINR or vice-versa
	  if (PrmW[i][j]/(interference[j] + PrmW[links[id].sender][j])  < beta  || PrmW[links[id].sender][links[id].recver]/interference[links[id].recver] < beta )  {
	    // is not feasible
	    //fprintf(stderr, "%d: %d-%d is not feasible - PrmWij[%d,%d] = %e - PrmWe[%d,%d] = %e, interference[%d] = %e, PrmWsenderj = %e \n",id,links[id].sender, links[id].recver,i,j,PrmW[i][j], links[id].sender, links[id].recver,PrmW[links[id].sender][links[id].recver], j, interference[j], PrmW[links[id].sender][j]);
	    return false;
	  } else {
	    // fprintf(stderr, "%d: %d-%d is feasible\n",id,links[id].sender, links[id].recver);
	  }
	}
      }
    }
  }
  // otherwise is feasible
  return true;
}

int isFeasible() {
	 
  int i,j;

  initialize();

  for(i = 0; i < edges; i++) {
    
    if (links[i].scheduled) {
      K[links[i].sender][links[i].recver]=1;
      adjustInterference(links[i].sender, links[i].recver);
    
      for (j = 0; j < edges; j++) {
      
	if (links[j].scheduled && (i!=j)) {
	  if (addLink(j)) {   
	    K[links[j].sender][links[j].recver]=1;
	    adjustInterference(links[j].sender, links[j].recver);
	  } else 
	    return false;
	}
      }
      return true;
    }
  }
  return true;
}

glp_prob* generateLPProblem() {

  glp_prob* lp;

  int i;

  char buf[100];

  // create problem
  lp = glp_create_prob();
  glp_set_prob_name(lp, "multicoloring");

  // maximization
  glp_set_obj_dir(lp, GLP_MAX);

  // number of edges/columns
  glp_add_cols(lp, edges);

  for (i=1; i<=edges; i++) {
    sprintf(buf,"%s%d","x",i);
    glp_set_col_name(lp, i, buf);
    
    glp_set_obj_coef(lp, i, 1.0);
    glp_set_col_bnds(lp, i, GLP_FR, 0.0, 0.0);
  }

  return lp;
}

void addConstraints2C(glp_prob* lp,int id,double *e) {

  fprintf(stderr,"Adding constraint %d to C\n",id);

  int l,m;
  int ja[1+edges];
  double ar[1+edges];

  l=1;
  for (m=1; m<=edges; m++) {
    ja[m] = l, ar[m] =  e[m-1];
    // fprintf(stderr,"%d: 1,%d --> %f\n", m,l,ar[m]);
    ++l;
  }

  // new row
  glp_add_rows(lp, 1);

  // variable with upper bound
  glp_set_row_bnds(lp, id, GLP_UP, 0.0, 1.0);

  char buf[100];
  sprintf(buf,"%s%d","c",id);
  glp_set_row_name(lp, id, buf);

  glp_set_mat_row(lp, id, edges, ja, ar);
}

int addConstraints2D(glp_prob* lp,int id,double *e,double mi) {

  fprintf(stderr,"Adding constraint %d to D - mi = %f\n",id,mi);

  int l,m;
  int ja[1+edges];
  double ar[1+edges];
  
  l=1;
  for (m=1; m<=edges; m++) {
    ja[m] = l, ar[m] =  e[m-1];
    // fprintf(stderr,"%d: 1,%d --> %f\n", m,l,ar[m]);
    ++l;
  }

  // new row
  glp_add_rows(lp, 1);

  // variable with upper bound
  glp_set_row_bnds(lp, id, GLP_UP, 0.0, mi);

  char buf[100];
  sprintf(buf,"%s%d","c",id);
  glp_set_row_name(lp, id, buf);

  glp_set_mat_row(lp, id, edges, ja, ar);
}

int remConstraintsFromD(glp_prob* lp, int count, int *rows) {

  fprintf(stderr,"Removing %d constraints from D\t",count);
  int i;
  for (i=1; i<=count; i++) {
    fprintf(stderr,"%d\t", rows[i]);
  }
  fprintf(stderr,"\n");

  glp_del_rows(lp, count, rows);
}

int heuristic(double weight) {

  int i,j;
  unsigned int ok = false;
  unsigned int none = true;
  double w;

  for (i = 0; i < edges; i++) {
    if (links[i].scheduled) {
      fprintf(stderr,"heuristic: removing link %d\n",i);
      links[i].scheduled = 0;
      for (j = 0; j < edges; j++) {
	if (links[j].scheduled) {
	  none = false;
	  break;
	}
      }
      if (isFeasible() && !none) {
	w=0.0; none = true;
	for (j = 0; j < edges; j++) {
	  if (links[j].scheduled)
	    w += links[j].weight;
	}
	if (w > 1.0 && w < weight) {
	  fprintf(stderr,"heuristic: weight - %1.20f %f\n", w, weight);
	  ok = true;
	  break;
	}
      }
    }
  }
  
  return ok;
}

void print_results(glp_prob* lp) {

  fprintf(stderr,"========= Printing results ========\n");

  int i, j, len, ind[1+1000];

  double val[1+1000];
  
  int m=0;

  int status = glp_get_dual_stat(lp);
  
  if (status == GLP_FEAS) {

    int nr_rows = glp_get_num_rows(lp);
    fprintf(stderr,"nr of rows %d\n",nr_rows);
    for (i=1; i<=nr_rows; i++) {
      if ((glp_get_row_stat(lp,i) == GLP_NU) && (glp_get_row_dual(lp, i))) {
	++m;
	fprintf(stderr,"matching %d: %f\n",m, glp_get_row_dual(lp, i));
	len = glp_get_mat_row(lp,i,ind,val);
	fprintf(stderr,"links:");
	for (j=1; j<=len; j++) 
	  fprintf(stderr,"\t%d",ind[j]-1);
	fprintf(stderr,"\n");
      }
    }
    glp_print_sol(lp, outputfile1);

    FILE* f1 = fopen(outputfile2, "w+");

    // unbuffered mode
    setvbuf (f1, NULL, _IONBF, 0);

    double gain = m * 1.0/edges;
    fprintf(f1, "%d %d %d %f\n", numNodes, edges, m, gain);

    fclose(f1);
    
  } else if (status = GLP_UNDEF)
    fprintf(stderr,"Undefined Solution\n");
}

// Main procedure
int main(int argc, char** argv) {

  int i,c;

  int D_rows[1+10000];
  double edge[1+1000];

  readParams(argc, argv);

  placeNodes();

  generateStructures();

  SmartGraph g;
  SmartGraph::EdgeMap<int> weight(g);

  glp_prob *lp = generateLPProblem();

  // define simplex method
  glp_smcp p;
  glp_init_smcp(&p);
  p.meth = GLP_PRIMAL;

  // adding initial constraints to C: one per link
  for (c = 0; c < edges; c++) {
    for (i = 0; i < edges; i++) {
      if (i == c) edge[i]=1.0;
      else edge[i]=0.0;
    }
    addConstraints2C(lp,c+1,edge);
  }

  // global constraints id
  int c_id = edges+1;

  // number of added constraints to D
  int nr_Dconstraints=0;

  double mi=1.0;
  int D_Vazio=true;
  unsigned int ok;
  double w=0.0;

  double z;

  unsigned int found;

  int solution;

  unsigned int isfeasible;

  int mi_int, w_int;

  SmartGraph::Node n[numNodes];
  SmartGraph::Edge e[edges];

  unsigned int schedlink;

  do {
    
    // removing constraints from D
    if (nr_Dconstraints > 0) {
      remConstraintsFromD(lp,nr_Dconstraints,D_rows);
      D_Vazio = true;
      c_id -=nr_Dconstraints;
      nr_Dconstraints = 0;
    }
    
    ok = false;
    
    while (!ok) {
      
      // running LP
      glp_std_basis(lp);
      solution = glp_simplex(lp, &p);
      if (solution == 0) { //successful
	// primal two-phase simplex method based on exact (rational) arithmetic
	glp_exact(lp,&p);
      }
      
      // getting LP results 
      z = glp_get_obj_val(lp);
      // fprintf(stderr,"\nz = %f;\t",z);
      for (i=1; i<=edges; i++) {
	links[i-1].weight = glp_get_col_prim(lp, i);
	// fprintf(stderr,"x%d = %f\t",i, links[i-1].weight);
      }
      // fprintf(stderr,"\n");

      // calculate weighted matching
      g.clear();
      for (i = 0; i < numNodes; i++) {
	n[i] = g.addNode();
      }
      for (i = 0; i < edges; i++) {
	e[i] = g.addEdge(n[links[i].sender],n[links[i].recver]);
	weight[e[i]] = links[i].weight;
      }
      MaxWeightedMatching<SmartGraph> mwm(g, weight);
      mwm.run();

      // cleaning scheduled links and coefficients of constraints
      for (i = 0; i < edges; i++) {
	links[i].scheduled = 0;
	edge[i]=0.0;
      }

      w=0.0;
      fprintf(stderr,"matching:\t");
      for (SmartGraph::EdgeIt edgeit(g); edgeit != INVALID; ++edgeit) {
	if (mwm.matching(edgeit) == true) {
	  schedlink=g.id(edgeit);
	  fprintf(stderr,"%d %f\t",g.id(edgeit),links[g.id(edgeit)].weight);
	  w += links[g.id(edgeit)].weight;
	  if (links[schedlink].scheduled == 0) {
	    links[schedlink].scheduled = 1;
	    edge[schedlink]=1.0;
	  }
	}
      }
      fprintf(stderr,"\n");
      
      w_int = (int) round(w * 1e5);
      mi_int = (int) round(mi * 1e5);
      
      isfeasible = isFeasible();

      if (w_int <= 1e5) {

	fprintf(stderr,"w <= 1.0 ==> w = %.20f - mi = %.20f\n",w,mi);
	ok = true;
	
      } else if ((w_int > mi_int) && !isfeasible) {
	
	fprintf(stderr,"w > mi and unfeasible ==> w = %.20f - mi = %.20f\n",w,mi);
	addConstraints2D(lp,c_id,edge,mi);
	D_rows[++nr_Dconstraints] = c_id;
	++c_id;
	
	D_Vazio = false;
	
      } else if ((w_int > 1e5) && isfeasible) {
	
	fprintf(stderr,"w > 1.0 and feasible ==> w = %.20f - mi = %.20f\n",w,mi);
	addConstraints2C(lp,c_id,edge);
	++c_id;
	
      } else if ((w_int > 1e5 && w_int <= mi_int) && !isfeasible) {
	
	fprintf(stderr,"w > 1.0 and <= mi and unfeasible ==> w = %.20f - mi = %.20f\n",w,mi);
	found = heuristic(w);
	
	if (!found) {
	  ok = true;
	  fprintf(stderr,"Matching OK not found\n");
	}
	else {
	  for (i = 0; i < edges; i++) {
	    if (links[i].scheduled) {
	      fprintf(stderr,"Heuristic: adding link %d\n",i);
	      edge[i]=1.0;
	    } else
	      edge[i]=0.0;
	  }

	  addConstraints2C(lp,c_id,edge);
	  ++c_id;
	}
      }
    }

    if (!D_Vazio) mi += delta_mi;
    
  } while (!D_Vazio);

  print_results(lp);

  glp_delete_prob(lp);
}
