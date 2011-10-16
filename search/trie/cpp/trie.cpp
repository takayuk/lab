
#include <string>
#include <vector>
#include <algorithm>

#include <cstdio>
#include <fstream>
#include <sstream>
#include <iostream>

using namespace std;

class Node {
  
  public:
    int label;
    bool is_value;
    vector<int> docids;

    int bros_;

    /// Specified Label, BrosID, is-Value? .
    //Node(const int& label, bool is_value): label(label), is_value(is_value) {}
    Node(const int& label, const int& bros, bool is_value): label(label), bros_(bros), is_value(is_value) {}
   
    /// Specified Label only.
    //Node(const int& label): label(label) {
    Node(const int& label, const int& bros): label(label), bros_(bros) {
      is_value = false;
    }

    /// Specified Label, DocID.
    //Node(const int& label, const int& doc_id): label(label), is_value(true) {
    Node(const int& label, const int& bros, const int& doc_id): label(label), bros_(bros), is_value(true) {
      docids.push_back(doc_id);
    }

    ~Node() {}

    bool operator==(const int& label) { return this->label == label; }
    bool operator==(const Node& lhs) {
      return (this->label == lhs.label) && (this->bros_ == lhs.bros_);
    }
    
    bool operator!=(const int& label) { return this->label != label; }
};


class Element {
  
  public:
    Node node;
    vector<Node> child;

    Element(const Node& n): node(n) {}
    Element(const Node& n, const Node& c): node(n) {
      child.push_back(c);
    }
    ~Element() {}

    bool operator==(const int& label) { return this->node.label == label; }
    bool operator==(const Element& lhs) {
      return (this->node.label == lhs.node.label) && (this->node.bros_ == lhs.node.bros_);
    }
};


class Trie {
  
  public:
    vector<Element> g;


    void build_testing(const vector<int>& keys, const int& doc_id) {

      /// Regist Elements.
      for (int i = 0; i < keys.size(); ++i) {
        
        const int term = keys[i];
        int prev_term;
        if (i == 0) { prev_term = 0; }
        else { prev_term = keys[i-1]; }

        Element e( Node(term, prev_term) );
        vector<Element>::iterator elem = find(g.begin(), g.end(), e);
        if (elem == g.end()) {
          g.push_back(e);
        }
      }

      /// Regist child node.
      for (int i = 0; i < keys.size()-1; ++i) {
        
        const int term = keys[i];
        const int next_term = keys[i+1];
        int prev_term;
        if (i == 0) { prev_term = 0; }
        else { prev_term = keys[i-1]; }

        Element e( Node(term, prev_term) );

        vector<Element>::iterator elem = find(g.begin(), g.end(), e);

        vector<Node>::iterator child = find(elem->child.begin(), elem->child.end(), next_term);
        if (child == elem->child.end()) {
          elem->child.push_back( Node(next_term, prev_term) );
        }
      }

      const int term = keys[keys.size()-1];
      const int prev_term = keys[keys.size()-2];

      Element e( Node(term, prev_term) );
      vector<Element>::iterator elem = find(g.begin(), g.end(), e);
      
      vector<Node>::iterator nd = find(elem->child.begin(), elem->child.end(), term);

      //nd->docids.push_back(doc_id);

      /*
      const int t = keys[keys.size()-2];
      const int nt = keys[keys.size()-1];

      vector<Element>::iterator elem = find(g.begin(), g.end(), t);
      vector<Node>::iterator nd = find(elem->child.begin(), elem->child.end(), nt);
      nd->docids.push_back(doc_id);
      */
 
    }

    void build(const vector<int>& keys, const int& doc_id) {

      for (int i = 0; i < keys.size(); ++i) {

        const int term = keys[i];

        vector<Element>::iterator elem = find(g.begin(), g.end(), term);
        if (elem == g.end()) {
          
          //g.push_back( Element(Node(term)) );
          if (i == 0) {
            g.push_back( Element(Node(term, 0)) );
          }
          else {
            g.push_back( Element(Node(term, keys[i-1])) );
          }
        }
      }

      for (int i = 0; i < keys.size()-1; ++i) {

        
        const int term = keys[i];
        const int next_term = keys[i+1];

        vector<Element>::iterator elem = find(g.begin(), g.end(), term);

        vector<Node>::iterator child = find(elem->child.begin(), elem->child.end(), next_term);
        if (child == elem->child.end()) {
          
          //elem->child.push_back( Node(next_term) );
          if (i == 0) {
            elem->child.push_back( Node(next_term, 0) );
          }
          else {
            elem->child.push_back( Node(next_term, keys[i-1]) );
          }
        }
      }

      const int t = keys[keys.size()-2];
      const int nt = keys[keys.size()-1];

      vector<Element>::iterator elem = find(g.begin(), g.end(), t);
      vector<Node>::iterator nd = find(elem->child.begin(), elem->child.end(), nt);
      nd->docids.push_back(doc_id);
    }


    vector<int> search(const vector<int>& query) {

      vector<int> search_result;

      const int term = query[query.size()-2];
      const int end_term = query[query.size()-1];

      int k = 0;
      while (true) {
        const int node = query[k];

        vector<Element>::iterator n = find(g.begin(), g.end(), node);
        if (n == g.end()) {
          break;
        }
        
        ++k;
      }

      return search_result;
    }
};


bool read(const string& file_path, vector< vector<int> >& dataset) {

  ifstream ifs(file_path.c_str());

  string buffer;
  int doc_j = 0;

  while (ifs && getline(ifs, buffer)) {

    dataset.push_back(vector<int>());

    stringstream ss(buffer);
    int id;
    
    while (ss >> id) {
      dataset[doc_j].push_back(id);
    }
    ++doc_j;
  }

  return true;
}


int main(int argc, char* argv[]) {

  vector< vector<int> > dataset;
  read(argv[1], dataset);

  for (vector< vector<int> >::iterator i = dataset.begin(); i != dataset.end(); ++i) {
    for (vector<int>::iterator j = i->begin(); j != i->end(); ++j) {
      cout << *j << " ";
    }
    cout << endl;
  }

  Trie trie;

  int doc_id = 0;
  for (vector< vector<int> >::iterator i = dataset.begin(); i != dataset.end(); ++i) {
    //trie.build(*i, doc_id);
    trie.build_testing(*i, doc_id);
    doc_id++;
  }

  printf("\n");
  for (vector<Element>::iterator i = trie.g.begin(); i != trie.g.end(); ++i) {

    printf("%d\t", i->node.label);

    printf("__%d__", i->node.bros_);

    for (vector<Node>::iterator c = i->child.begin(); c != i->child.end(); ++c) {
      printf("%d ", (*c).label);

      printf("[");
      for (vector<int>::iterator j = c->docids.begin(); j != c->docids.end(); ++j) {
        printf(" %d", *j);
      }
      printf("]\t");
    }
    printf("\n");
  }

  return 0;
}

