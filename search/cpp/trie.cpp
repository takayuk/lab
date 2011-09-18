
#include <string>
#include <vector>
using namespace std;

class node {
  
  public:
    int label;
    bool is_value;

    node(const int&, bool);
    ~node();
};


class element {
  
  public:
    node n;
    vector<int> a;

    element(const node& n);
    ~element();
};


class trie {
  
  public:
    vector<element> g;

    void add(const vector<int>& keys) {


    }

    void search(const vector<int>& key) {

      int pos = 0;
      
      for (int j = 0; j < key.size(); ++j) {

        vector<int>::iterator i = g[pos].a.begin();
        vector<int>::iterator e = g[pos].a.end();

        while (i != e) {
          if (g[*i].n.is_value == false && g[*i].n.label == key[j]) {
            pos = *i;
            break;
          }
          ++i;
        }
        if (i == e) {
          g[pos].a.push_back(g.size());
          g.push_back(element(node(key[j], true)));
        }
      }
    }
};


int main(int argc, char* argv[]) {


  return 0;
}

