#include <iostream>
#include <vector>
#include <cstdio>
#include <cstdlib>

#include <fstream>

using namespace std;

#include "traverse.hpp"


void ccd() {
}


int main(int argc, char* argv[]) {

  ifstream ifs(argv[1]);


  const int N = 10;
  vector< vector<int> > graph(N);

  srand(time(NULL));
  for (int i = 0; i < N; ++i) {

    const int M = rand() % N;
    graph[i] = vector<int>(M);
    for (int j = 0; j < M; ++j) {
      const int m = rand() % N;
      if (i == m) { continue; }
      graph[i][j] = m;
    }
  }

  for (int i = 0; i < N; ++i) {

    for (int j = 0; j < graph[i].size(); ++j) {

      printf("%d ", graph[i][j]);
    }
    printf("\n");
  }


  return 0;
}

