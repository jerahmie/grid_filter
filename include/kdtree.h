#ifndef _KDTREE_H_
#define _KDTREE_H_

std::tuple<nodeData, int> median_point_id(const std::vector<nodeData> &nd);

class KDTree {
  private:
    int depth;
    
  public:
    KDTree();
    ~KDTree();
  //  friend median_point_id(
};

#endif /* _KDTREE_H_ */
