"""Задача 8.
Что нужно сделать
В программе реализована структура BinaryTreeNode, а также функция walk_tree, которая обходит бинарное дерево по уровням, при этом записывая в логи номер посещаемого узла и номера его потомков.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами в виде строки, а возвращает корень восстановленного бинарного дерева.

Гарантируется, что все значения, хранящиеся в бинарном дереве, уникальны.

Пример построения бинарного дерева



root = BinaryTreeNode(1)
root.left = node2 = BinaryTreeNode(2)
root.right = BinaryTreeNode(3)
node2.left = BinaryTreeNode(4)
node2.right = BinaryTreeNode(5)
Советы и рекомендации
Создайте словарь {node_value: node_object}. Это позволит быстро получить нужный узел по его значению.
Существует два основных алгоритма обхода графа: поиск в глубину (Depth-First Search, DFS) и поиск в ширину (Breadth-First Search, BFS).
Что оценивается
Функция restore_tree возвращает корень бинарного дерева в виде объекта BinaryTreeNode.
Все узлы дерева из логов обходятся только один раз.
"""
from collections import deque


class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def restore_tree(log_file_path):
    nodes = {}
    children = set()
    logs = []

    with open(log_file_path, 'r') as f:
        logs = f.readlines()

    relations = []
    for line in logs:
        tokens = line.strip().replace(':', '').replace('=', ' ').split()
        parent = int(tokens[1])
        left = tokens[3]
        right = tokens[5]
        left_val = int(left) if left != 'None' else None
        right_val = int(right) if right != 'None' else None
        relations.append((parent, left_val, right_val))
        if parent not in nodes:
            nodes[parent] = BinaryTreeNode(parent)

        if left_val is not None and left_val not in nodes:
            nodes[left_val] = BinaryTreeNode(left_val)
        if right_val is not None and right_val not in nodes:
            nodes[right_val] = BinaryTreeNode(right_val)

        if left_val is not None:
            children.add(left_val)
        if right_val is not None:
            children.add(right_val)

    for parent, left_val, right_val in relations:
        node = nodes[parent]
        node.left = nodes[left_val] if left_val is not None else None
        node.right = nodes[right_val] if right_val is not None else None

    all_nodes = set(nodes.keys())
    root_candidates = all_nodes - children
    root_val = root_candidates.pop()
    return nodes[root_val]


def print_tree_by_levels(root):
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is not None:
            print(node.value, end=' ')
            queue.append(node.left)
            queue.append(node.right)


root = restore_tree('logs.txt')
print_tree_by_levels(root)


def print_tree_preorder(node):
    if node:
        print(node.value, end=' ')
        print_tree_preorder(node.left)
        print_tree_preorder(node.right)


print('\n')
print('Последовательность обхода в консоли:')
root = restore_tree('logs.txt')
print_tree_preorder(root)
