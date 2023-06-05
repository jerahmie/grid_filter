#ifndef _KDTREE_NODE_H_
#define _KDTREE_NODE_H_

struct nodeData {
  double lat;
  double lon;
  int cell_index;
  friend bool operator==(const nodeData& lhs, const nodeData& rhs);
  friend bool operator!=(const nodeData& lhs, const nodeData& rhs);
  friend std::ostream& operator<<(std::ostream& os, const nodeData& nd);
};

// compare node data along dimension
bool compare_node_lat(nodeData n1, nodeData n2);

// compare node data along dimension
bool compare_node_lon(nodeData n1, nodeData n2);

class KDTreeNode2D {
  private:
    KDTreeNode2D* left;
    KDTreeNode2D* right;
    nodeData node_data;
  public:
    KDTreeNode2D(KDTreeNode2D*, KDTreeNode2D*,nodeData);
    KDTreeNode2D* getLeft(void);
    KDTreeNode2D* getRight(void);
    nodeData getData(void);
    friend std::ostream& operator<<(std::ostream& os, const KDTreeNode2D& kd2);

    //~KDTreeNode2D();
};

#endif /* _KDTREE_NODE_H_ */
