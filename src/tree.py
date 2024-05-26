import math
import heapq
from .rectangle import Rectangle
from .node import Node
from .entry import Entry

class Tree:
    def __init__(self , max_entries=4 , min_entries =2 , dimension = 2 ) :
        self.max_entries = max_entries
        self.min_entries = min_entries
        self.dimension = dimension
        self.root = Node(is_leaf = True)

    def insert(self , rectangle , record_id):
        leaf = self._choose_leaf(self.root, rectangle)
        leaf.entries.append(Entry(rectangle, record_id=record_id))
        if len(leaf.entries) > self.max_entries:
            self._split_node(leaf)
        if self.root.is_leaf and len(self.root.entries) > self.max_entries:
            self._split_root()

    def _choose_leaf(self, node, rectangle):
        if node.is_leaf:
            return node
        min_enlargement = float('inf')
        chosen_entry = None
        for entry in node.entries:
            enlargement = entry.rectangle.enlargement(rectangle)
            if enlargement < min_enlargement:
                min_enlargement = enlargement
                chosen_entry = entry
        return self._choose_leaf(chosen_entry.child, rectangle)

    def _split_node(self, node):
        seeds = self._pick_seeds(node.entries)
        group1 = [seeds[0]]
        group2 = [seeds[1]]
        entries = [e for i, e in enumerate(node.entries) if i not in seeds]
        while entries:
            if len(group1) + len(entries) == self.min_entries:
                group1.extend(entries)
                break
            if len(group2) + len(entries) == self.min_entries:
                group2.extend(entries)
                break
            next_entry = self._pick_next(entries, group1, group2)
            group1_area_increase = self._group_area_increase(group1, next_entry)
            group2_area_increase = self._group_area_increase(group2, next_entry)
            if group1_area_increase < group2_area_increase:
                group1.append(next_entry)
            else:
                group2.append(next_entry)
        if node.is_leaf:
            node.entries = group1
            new_node = Node(is_leaf=True)
            new_node.entries = group2
        else:
            node.entries = [Entry(self._compute_mbr(group1), child=e.child) for e in group1]
            new_node = Node(is_leaf=False)
            new_node.entries = [Entry(self._compute_mbr(group2), child=e.child) for e in group2]
        if node == self.root:
            new_root = Node(is_leaf=False)
            new_root.entries = [Entry(self._compute_mbr(group1), child=node),
                                Entry(self._compute_mbr(group2), child=new_node)]
            self.root = new_root
        return new_node

    def _split_root(self):
        entries = self.root.entries
        seeds = self._pick_seeds(entries)
        group1 = [entries[seeds[0]]]
        group2 = [entries[seeds[1]]]
        entries = [e for i, e in enumerate(entries) if i not in seeds]
        while entries:
            if len(group1) + len(entries) == self.min_entries:
                group1.extend(entries)
                break
            if len(group2) + len(entries) == self.min_entries:
                group2.extend(entries)
                break
            next_entry = self._pick_next(entries, group1, group2)
            group1_area_increase = self._group_area_increase(group1, next_entry)
            group2_area_increase = self._group_area_increase(group2, next_entry)
            if group1_area_increase < group2_area_increase:
                group1.append(next_entry)
            else:
                group2.append(next_entry)
        new_root = Node(is_leaf=False)
        new_root.entries = [Entry(self._compute_mbr(group1), child=self.root),
                            Entry(self._compute_mbr(group2), child=self._split_node(group2))]
        self.root = new_root

    def _compute_mbr(self, entries):
        min_point = [min(e.rectangle.min_point[i] for e in entries) for i in range(self.dimension)]
        max_point = [max(e.rectangle.max_point[i] for e in entries) for i in range(self.dimension)]
        return Rectangle(min_point, max_point)

    def _pick_seeds(self, entries):
        max_d = float('-inf')
        seed1, seed2 = None, None
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                d = self._rectangle_distance(entries[i].rectangle, entries[j].rectangle)
                if d > max_d:
                    max_d = d
                    seed1, seed2 = i, j
        return seed1, seed2

    def _pick_next(self, entries, group1, group2):
        max_diff = float('-inf')
        next_entry = None
        for entry in entries:
            group1_area_increase = self._group_area_increase(group1, entry)
            group2_area_increase = self._group_area_increase(group2, entry)
            diff = abs(group1_area_increase - group2_area_increase)
            if diff > max_diff:
                max_diff = diff
                next_entry = entry
        entries.remove(next_entry)
        return next_entry

    def _group_area_increase(self, group, entry):
        group_mbr = self._compute_mbr(group)
        return group_mbr.enlargement(entry.rectangle)

    def _rectangle_distance(self, rect1, rect2):
        return sum(max(0, max(rect1.min_point[i], rect2.min_point[i]) - min(rect1.max_point[i], rect2.max_point[i])) for i in range(len(rect1.min_point)))

    def range_query(self, rectangle):
        result = []
        self._range_search(self.root, rectangle, result)
        return result

    def _range_search(self, node, rectangle, result):
        if node.is_leaf:
            for entry in node.entries:
                if entry.rectangle.intersects(rectangle):
                    result.append(entry.record_id)
        else:
            for entry in node.entries:
                if entry.rectangle.intersects(rectangle):
                    self._range_search(entry.child, rectangle, result)





