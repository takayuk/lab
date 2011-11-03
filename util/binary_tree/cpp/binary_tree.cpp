#include <vector>
#include <iostream>


template <typename T>
class Element {

  public:
    Element(): data(0), left(-1), right(-1) {}
    Element(const T& data): data(data), left(-1), right(-1) {}
    ~Element() {}

    const T& node() const { return this->data; }

    void operator=(const T& data) { this->data = data; }
  
    int left;
    int right;
  
  private:
    T data;
};


void build() {

  using namespace std;

  int data[] = { 2, 5, 6, 4, 8, 1, 9, 3, 4, 7 };

  vector< Element<int> > tree(10);

  int sp = -1;
  int empty_index = sp + 1;

  tree[0] = data[0];
  for (int i = 1; i < 10; ++i) {
    tree[i] = data[i];

    int current = 0;
    while (true) {

      int next = -1;
      if (data[i] < tree[current].node()) {
        next = tree[current].left;

        if (next < 0) {
          tree[current].left = i;
          break;
        }
      }
      else {
        next = tree[current].right;

        if (next < 0) {
          tree[current].right = i;
          break;
        }
      }
      current = next;
    }
  }

  for (vector< Element<int> >::iterator i = tree.begin(); i != tree.end(); ++i) {

    cout << i->node() << " --> " << tree[i->left].node() << ", " << tree[i->right].node() << endl;
  }
}


int main(int argc, char* argv[]) {

  build();

  return 0;
}
