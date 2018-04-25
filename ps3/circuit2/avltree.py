class Node(object):
    def __init__(self, key):
        self.left = None
        self.right = None
        self.parent = None
        self.key = key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key


class AVLNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.height = 1

    def __str__(self):
        return str(self.key) + ', ' + str(self.height)

    def as_list(self, first_key, last_key, result):
        """
        Add corresponding nodes to result recursively and return with main call.
        returns: list of correspondent keys at subtree
        """

        if first_key <= self.key <= last_key:
            result.append(self.key)

        self.left and self.left.as_list(first_key, last_key, result)
        self.right and self.right.as_list(first_key, last_key, result)

        return result

    def update_height(self):
        left_height = (self.left and self.left.height) or 0
        right_height = (self.right and self.right.height) or 0
        self.height = 1 + max(left_height, right_height)

    def balance(self):
        left_height = (self.left and self.left.height) or 0
        right_height = (self.right and self.right.height) or 0
        return (left_height - right_height)


class AVLTree(object):
    """
    Tree Property: left_child <= node < right_child
    Written for MIT6.006 ps3.
    """

    def __init__(self):
        self.root = None

    def insert(self, key):
        node = AVLNode(key)

        if self.root is None:
            self.root = node
            return node

        parent = self.root
        # crawl to right spot
        while True:
            if node > parent:
                if parent.right is None:
                    node.parent = parent
                    parent.right = node
                    break
                else:
                    parent = parent.right

            else:
                if parent.left is None:
                    node.parent = parent
                    parent.left = node
                    break
                else:
                    parent = parent.left

        self.update_heights(node)
        self.rebalance(node)

    def delete(self, key):
        """
        Deletes first node with the key, else raises ValueError.
        returns: deleted node
        """

        # find node
        node = self.root
        while node and node.key != key:
            if key > node.key:
                node = node.right
            elif key < node.key:
                node = node.left

        if not node:
            return None

        # if has 2 child
        if node.right and node.left:
            # crawl to smallest node of right subtree
            smallest_node = node.right
            while smallest_node and smallest_node.left:
                smallest_node = smallest_node.left

            balancing_node = smallest_node.parent

            # replace smallest_node with node in tree
            smallest_node.parent.left = None
            smallest_node.parent = node.parent
            if not node.parent:
                pass
            elif node.parent < node:
                node.parent.right = smallest_node
            else:
                node.parent.left = smallest_node

        # if has 1 child
        elif node.right or node.left:
            balancing_node = node.parent
            if node.right:
                child = node.right
            else:
                child = node.left

            child.parent = node.parent
            if not node.parent:
                self.root = child
            elif node.parent < node:
                node.parent.right = child
            else:
                node.parent.left = child

        # no child
        else:
            balancing_node = node.parent
            if not node.parent:
                self.root = None
            else:
                if node.parent < node:
                    node.parent.right = None
                else:
                    node.parent.left = None

        balancing_node and self.rebalance(balancing_node)
        node.left, node.right, node.parent = [None] * 3
        return node

    def lca(self, first_key, last_key):
        """
        returns: Least Common Ancestor
        """

        lca = self.root
        while lca and not first_key <= lca.key <= last_key:
            if last_key < lca.key:
                lca = lca.left
            elif first_key > lca.key:
                lca = lca.right
        
        return lca

    def as_list(self, first_key, last_key):
        # find lca
        node = self.lca(first_key, last_key)
        if node is None:
            return []

        # return list
        return node.as_list(first_key, last_key, [])

    @staticmethod
    def update_heights(avlnode): 
        """
        Crawls from current node to root node

        In current algorithms with rotations, the node is always z.
        That's because z is the 'youngest' child who could be effected by rotations.
        """
        
        update_block = avlnode
        while update_block:
            update_block.update_height()
            update_block = update_block.parent

    def rotate_right(self, node):
        z, y = node, node.left

        # base pointer swaps
        if self.root is z:
            self.root = y
        z.left, y.right= y.right, z
        
        # arranging parent
        y.parent = z.parent
        z.parent = y
        if y.parent:
            if y.parent < y:
                y.parent.right = y
            else:
                y.parent.left = y

        self.update_heights(z) 

    def rotate_left(self, node):
        z, y = node, node.right

        # base pointer swaps
        if self.root is z:
            self.root = y
        z.right, y.left = y.left, z
        
        # arranging parent
        y.parent = z.parent
        z.parent = y
        if y.parent is not None:
            if y.parent < y:
                y.parent.right = y
            else:
                y.parent.left = y

        self.update_heights(z)
       
    def rebalance(self, node):
        """
        Let w be the inserted node and z is the first unbalanced node
        while traveling up. y is child of z and x is grandchild of z.

        Rotations determined by z, y, x
        """

        w = node

        # w.parent and w.parent.parent is for deletion rebalance exception for 2 nodes
        x, y, z = w, w.parent, w.parent and w.parent.parent

        # crawl to unbalanced node
        while z and abs(z.balance()) < 2:
            x, y, z = x.parent, y.parent, z.parent
            
        # not unbalanced   
        if not z:
            return True
        
        if z.balance() < 0:
            if x < y:
                self.rotate_right(y)
            self.rotate_left(z)
        else:
            if x > y:
                self.rotate_left(y)
            self.rotate_right(z)

