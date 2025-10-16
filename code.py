#!/bin/python3
import os

# #################################### #
# Traversals and helpers used by main  #
# #################################### #
def _balance(node):
    if not node:
        return 0
    left = node.left.height if node.left else 0
    right = node.right.height if node.right else 0
    return left - right

def _formatter(node):
    return f"{node.value}(BF={_balance(node)})"

def _inorder(node):
    result = []
    if node is not None:
        result += _inorder(node.left)
        result.append(_formatter(node))  # ?or print with end=" "
        result += _inorder(node.right)
    return result

def _postorder(node):
    result = []
    if node is not None:
        result.append(_formatter(node))
        result += _postorder(node.left)
        result += _postorder(node.right)
    return result

# #################################### #
# Class Definitions and Solution code  #
# #################################### #

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def compute_height(self, node):
        return 1 + max(self.height(node.left), self.height(node.right))

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def make_balance(self, root):
        balance = self.balance(root)
        # Left rotation
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)
        # Right rotation
        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)
        # Left-Right rotation
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Right-Left rotation
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def insert(self, root, value):
        if not root:
            return Node(value)
        elif value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)
        root.height = self.compute_height(root)
        return self.make_balance(root)

    def delete(self, root, value):
        if not root:
            return root
        if value < root.value:
            root.left = self.delete(root.left, value)
        elif value > root.value:
            root.right = self.delete(root.right, value)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            temp = self.min_value_node(root.right)
            root.value = temp.value
            root.right = self.delete(root.right, temp.value)

        if not root:
            return root
        root.height = self.compute_height(root)
        return self.make_balance(root)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = self.compute_height(z)
        y.height = self.compute_height(y)
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = self.compute_height(z)
        y.height = self.compute_height(y)
        return y

    def min_value_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    def search(self, root, value):
        if not root or root.value == value:
            return root
        if root.value < value:
            return self.search(root.right, value)
        return self.search(root.left, value)

    def insert_value(self, value):
        self.root = self.insert(self.root, value)

    def delete_value(self, value):
        self.root = self.delete(self.root, value)

    def search_value(self, value):
        return self.search(self.root, value)


def solve(tree: AVLTree, value: int) -> Node:
    tree.insert_value(value)
    return tree.root

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    num_initial = int(input().strip())
    arr = list(map(int, input().split()))
    additional = int(input().strip())
    tree = AVLTree()
    for val in arr:
        tree.insert_value(val)
    result = solve(tree, additional)
    ordering = _inorder(result)
    fptr.write(' '.join(ordering))
    fptr.write('\n')
    ordering = _postorder(result)
    fptr.write(' '.join(ordering))
    fptr.write('\n')
    fptr.close()
