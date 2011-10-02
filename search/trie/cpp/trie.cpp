
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

    Node(const int& label, bool is_value): label(label), is_value(is_value) {}
    Node(const int& label): label(label) {
      is_value = false;
    }
    Node(const int& label, const int& doc_id): label(label) {
      docids.push_back(doc_id);
    }
    ~Node() {}

    bool operator==(const int& label) { return this->label == label; }
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
};


class Trie {
  
  public:
    vector<Element> g;

    void build(const vector<int>& keys, const int& doc_id) {

      for (int i = 0; i < keys.size(); ++i) {

        const int term = keys[i];
        vector<Element>::iterator elem = find(g.begin(), g.end(), term);
        if (elem == g.end()) {
          g.push_back( Element(Node(term)) );
        }
      }

      for (int i = 0; i < keys.size()-1; ++i) {

        
        const int term = keys[i];
        const int next_term = keys[i+1];

        vector<Element>::iterator elem = find(g.begin(), g.end(), term);

        vector<Node>::iterator child = find(elem->child.begin(), elem->child.end(), next_term);
        if (child == elem->child.end()) {
          elem->child.push_back( Node(next_term) );
        }
      }

      const int t = keys[keys.size()-2];
      const int nt = keys[keys.size()-1];

      vector<Element>::iterator elem = find(g.begin(), g.end(), t);
      vector<Node>::iterator nd = find(elem->child.begin(), elem->child.end(), nt);
      nd->docids.push_back(doc_id);
      /*
      for (int i = 0; i < keys.size()-1; ++i) {

        const bool end_of_document = (i+1) == (keys.size()-1) ? true:false;
        
        const int term = keys[i];
        const int next_term = keys[i+1];

        vector<Element>::iterator elem = find(g.begin(), g.end(), term);
        if (elem != g.end()) {
          
          vector<Node>::iterator child = find(elem->child.begin(), elem->child.end(), next_term);
          if (child == elem->child.end()) {
            if (end_of_document) {
              
              elem->child.push_back( Node(next_term, doc_id) );
              elem->node.docids.push_back(doc_id);
            }
            else {
              elem->child.push_back( Node(next_term) );
            }
          }
        }
        else {
          if (end_of_document) {
            g.push_back( Element(Node(term), Node(next_term)) );
            g.push_back( Element(Node(next_term, doc_id)) );
          }
          else {
            g.push_back( Element(Node(term), Node(next_term)) );
          }
        }
      }
      */
    }


    vector<int> search(const vector<int>& query) {

      vector<int> search_result;

      return search_result;
    }


    /*
    bool search(const vector<int>& query) {

      //vector<Element>::iterator i = g.begin();
      
      //vector<Node>::iterator current_node = g.end()->child.end();

      vector<Node>::iterator find_result;

      for (int k = 0; k < query.size()-1; ++k) {

        //i = g.begin();
        for (vector<Element>::iterator i = g.begin(); i != g.end(); ++i) {

        //vector<Element>::iterator i = g.begin();
        //while (i != g.end()) {
          if (i->node.label == query[k]) {
            printf("F\n");
            find_result = find(i->child.begin(), i->child.end(), query[k+1]);
            //if (find_result == i->child.end()) {
            if (k < query.size()-1 && find_result == i->child.end()) {
              return false;
            }
          }

          //find_result = find(i->child.begin(), i->child.end(), query[k]);
          //find_result = find(i->child.begin(), i->child.end(), query[k+1]);
          //++i;
        }
        //find_result = find(i->child.begin(), i->child.end(), query[k+1]);
      }
      return true;
      //return found;
    }
    */
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
    //trie.build(*i);
    trie.build(*i, doc_id);
    doc_id++;
  }

  printf("\n");
  for (vector<Element>::iterator i = trie.g.begin(); i != trie.g.end(); ++i) {

    printf("%d\t", i->node.label);

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

  /*
  vector<int> query;
  query.push_back(2);
  query.push_back(4);

  const bool result = trie.search(query);
  if (result) { printf("Found.\n"); }
  else { printf("Not found.\n"); }

  query.clear();
  query.push_back(26);
  query.push_back(12);
  query.push_back(13);
  
  if (result) { printf("Found.\n"); }
  else { printf("Not found.\n"); }
  */

  return 0;
}

