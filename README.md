# TreeVisualizer

Using tkinter to recursively generate a tree of nodes to visualize user input.
Expects binary trees in the format [int, [tree], [tree]].
An example tree is [8,[1],[2]], which corresponds to a tree with 8 as its root, 1 as the left child, and 2 as the right child.
Another example is [8,[], [2,[3],[4]]], where 8 is the root, there is no left child, and the right child is 2, which itself has 3 as a left child and 4 as a right child.
