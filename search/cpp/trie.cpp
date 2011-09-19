
#include <string>
#include <vector>
#include <algorithm>

#include <cstdio>


using namespace std;

class Node {
  
  public:
    int label;
    bool is_value;

    Node(const int& label, bool is_value): label(label), is_value(is_value) {}
    ~Node() {}

    bool operator==(const int& label) { return this->label == label; }
    bool operator!=(const int& label) { return this->label != label; }
};


class Element {
  
  public:
    Node node;
    vector<Node> child;

    Element(const Node& n): node(n) {}
    ~Element() {}
};


class Trie {
  
  public:
    vector<Element> g;

    void build(const vector<int>& keys) {

      for (int i = 0; i < keys.size()-1; ++i) {
        
        const int term = keys[i];
        const int next_term = keys[i+1];

        const vector<Element>::iterator g_begin = g.begin();
        const vector<Element>::iterator g_end = g.end();
        
        vector<Element>::iterator g_current = g.begin();

        while (g_current != g_end) {

          if (g_current->node.is_value == false && g_current->node.label == term) {

            /// Node:term を持つ Element:g_current に対するnext_termにマッチする子ノードの探索.
            vector<Node>::iterator it_child = g_current->child.begin();
            for ( ; it_child != g_current->child.end(); ++it_child) {

              if (it_child->label == next_term) { break; }
            }
            if (it_child == g_current->child.end()) {
              g_current->child.push_back(Node(next_term, false));
            }
          }
          ++g_current;
        }

        if (g_current == g_end) {
          g.push_back(Element(Node(term, false)));
          (--g.end())->child.push_back(Node(next_term, false));
        }
      }

      g.push_back(Element(Node(keys[keys.size()-1], true)));
    }

    bool search(const vector<int>& query) {

      int term = query[0];
      
      vector<Element>::iterator i = g.begin();
      
      vector<Node>::iterator current_node = g.end()->child.end();

      vector<Node>::iterator find_result;
      while (i != g.end()) {

        find_result = find(i->child.begin(), i->child.end(), term);
        if (find_result != i->child.end()) {

          current_node = find_result;
          break;
        }
        ++i;
      }

      if (current_node == g.end()->child.end()) { return false; }

      for (int k = 1; k < query.size(); ++k) {

        i = g.begin();
        while (i != g.end()) {
          find_result = find(i->child.begin(), i->child.end(), query[k]);
          if (find_result != i->child.end()) {
            current_node = find_result;
            break;
          }
          ++i;
        }
      }
      if (i != g.end()) {
        printf("Found.\n");
        return true;
      }
      return false;
    }
};


int main(int argc, char* argv[]) {

  Trie trie;

  vector<int> keys;
  keys.push_back(1);
  keys.push_back(2);
  keys.push_back(3);
  
  trie.build(keys);

  keys.clear();
  keys.push_back(1);
  keys.push_back(4);
  keys.push_back(5);
  keys.push_back(6);
  
  trie.build(keys);

  //printf("%d\n", trie.g.size());

  for (int i = 0; i < trie.g.size(); ++i) {

    printf("%d\n", trie.g[i].node.label);
    for (vector<Node>::iterator it = trie.g[i].child.begin(); it != trie.g[i].child.end(); ++it) {
      printf("%d ", it->label);
    }
    printf("\n\n");
  }

  vector<int> query;
  query.push_back(2);
  query.push_back(3);

  trie.search(query);

  query.clear();
  query.push_back(-1);
  trie.search(query);
  
  query.clear();
  query.push_back(4);
  query.push_back(5);
  trie.search(query);
 
  return 0;
}

