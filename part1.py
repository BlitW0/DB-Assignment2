import bisect
import sys

TREE_ORDER = 3


class Node():
    '''
    Base node object.
    
    Each node stores keys and pointers. Pointers point to its child nodes.

    Attributes:
        order (int): The maximum number of keys the node can hold.
    '''
    def __init__(self, order):
        self.is_leaf = True
        self.keys = []
        self.ptrs = []
        self.next = None
        self.order = order

    def split(self):
        '''
        Splits the node into two and returns a key that floats upwards to the parent node, along with the right half of the split
        '''
        right_sib = Node(self.order)
        
        mid = len(self.keys) // 2
        key_mid = self.keys[mid]

        if not self.is_leaf:
            right_sib.is_leaf = False

            right_sib.keys = self.keys[mid + 1:]
            right_sib.ptrs = self.ptrs[mid + 1:]

            self.keys = self.keys[:mid]
            self.ptrs = self.ptrs[:mid + 1]
        else:
            right_sib.keys = self.keys[mid:]
            self.keys = self.keys[:mid]

            right_sib.next = self.next
            self.next = right_sib
        
        return key_mid, right_sib


class B_Plus_Tree():
    '''
    B+ tree object, consisting of nodes.
    
    Nodes will automatically be split into two once it is full. When a split
    occurs, a key will 'float' upwards and be inserted into the parent node to
    act as a pivot.
    
    Attributes:
        order (int): The maximum number of keys each node can hold.
    '''
    def __init__(self, order):
        self._root = Node(order)
        self.order = order

    def insert(self, key):
        '''
        Inserts key into B+ tree
        '''
        key_mid, right_sib = self._insert_utility(key, self._root)
        if key_mid:
            new_root = Node(self.order)
            new_root.is_leaf = False
            new_root.keys = [key_mid]
            new_root.ptrs = [self._root, right_sib]
            self._root = new_root

    def _insert_utility(self, key, node):
        '''
        Inserts key into subtree rooted at node=node
        '''
        if node.is_leaf:
            bisect.insort_right(node.keys, key)
            if len(node.keys) > self.order:
                return node.split()
            return None, None

        key_mid, right_sib = self._insert_utility(key, node.ptrs[bisect.bisect_right(node.keys, key)])

        if key_mid:
            idx = bisect.bisect_right(node.keys, key_mid)
            node.keys.insert(idx, key_mid)
            node.ptrs.insert(idx + 1, right_sib)

            if len(node.keys) > self.order:
                return node.split()
            return None, None
        
        return None, None

    def point_query(self, key, node):
        '''
        Returns leftmost leaf which contains key=key
        '''
        if node.is_leaf:
            return node
        return self.point_query(key, node.ptrs[bisect.bisect_left(node.keys, key)])

    def count(self, key_min, key_max=None):
        '''
        Returns number of keys(in leaves) lying in the range [key_min, key_max]
        '''
        node = self.point_query(key_min, self._root)
        if key_max is None:
            key_max = key_min

        count = 0
        while node:
            if node.keys and (node.keys[0] > key_max or node.keys[-1] < key_min):
                break
            count += bisect.bisect_right(node.keys, key_max) - bisect.bisect_left(node.keys, key_min)
            node = node.next
        
        return count


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: part1.py <filepath>')
        exit(1)

    filepath = sys.argv[1]
    query_list = open(filepath).readlines()
    
    tree = B_Plus_Tree(TREE_ORDER)

    for query in query_list:
        query = query.split()
        query_type = query[0]
        x = int(query[1])
        if len(query) > 2:
            y = int(query[2])
        
        if query_type == 'INSERT':
            tree.insert(x)
        elif query_type == 'FIND':
            print('YES' if tree.count(x) > 0 else 'NO')
        elif query_type == 'COUNT':
            print(tree.count(x))
        elif query_type == 'RANGE':
            print(tree.count(x, y))
        else:
            print('QueryTypeError:', query_type, 'is not supported')
