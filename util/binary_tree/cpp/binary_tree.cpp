#include <vector>
#include <cstdio>


using namespace std;

const int N = 10;


class Node {

  public:
    int id;
    Node(const int& id): id(id) {}
    Node(): id(-1) {}
};


class Elem {

  public:

    Node node;
    int left;
    int right;

    Elem(const Node& node): node(node), left(-1), right(-1) {}
    Elem(): node(Node()), left(-1), right(-1) {}
};


void binary_tree() {

  vector<Node> nodelist;
  vector<Elem> elem(N);

  for (int i = 0; i < N; ++i) {
    nodelist.push_back(Node(i));
  }

  int root = 0;
  elem[root] = nodelist[0];
  
  for (int i = 1; i < N; ++i) {

    Node n = nodelist[i];
    int current = root;
    
    while (true) {

      if (n.id <= elem[current].node.id) {
        current = elem[current].left;
      }
      else {
        current = elem[current].right;
      }
      
      if (elem[current].left < 0 && elem[current].right < 0) {
        elem[current].right = i;
        break;
      }
    }
  }

  for (int i = 0; i < N; ++i) {
    printf("%d --> %d, %d\n", elem[i].node.id, elem[i].left, elem[i].right);
  }
}


int main(int argc, char* argv[]) {

  binary_tree();

  return 0;
}

