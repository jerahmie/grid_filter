/*
 *
 */

#pragma once

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
    std::shared_ptr<KDTreeNode2D> node_left;
    std::shared_ptr<KDTreeNode2D> node_right;
    std::shared_ptr<nodeData> node_data;
  public:
    KDTreeNode2D(std::unique_ptr<KDTreeNode2D>, std::unique_ptr<KDTreeNode2D>,std::unique_ptr<nodeData>);
    //std::shared_ptr<KDTreeNode2D> getLeft(void);
    //std::shared_ptr<KDTreeNode2D> getRight(void);
    nodeData getData(void);
    friend std::ostream& operator<<(std::ostream& os, const KDTreeNode2D& kd2);

    //~KDTreeNode2D();
};

