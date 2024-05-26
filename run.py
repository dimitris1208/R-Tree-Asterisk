from src import Tree,Rectangle

rtree = Tree()

# Example insertion
rectangle1 = Rectangle([0, 0], [2, 2])
record_id1 = 1
rtree.insert(rectangle1, record_id1)

rectangle2 = Rectangle([1, 1], [3, 3])
record_id2 = 2
rtree.insert(rectangle2, record_id2)

# Example range query
query_rectangle = Rectangle([0, 0], [4, 4])
result = rtree.range_query(query_rectangle)
print("Query result:", result)
