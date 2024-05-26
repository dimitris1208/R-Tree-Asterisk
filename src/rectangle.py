import math

class Rectangle:
    def __init__(self , min_point , max_point):
        self.min_point = min_point
        self.max_point = max_point

    def intersects(self, other):
        return all(self.min_point[i] <= other.max_point[i] and self.max_point[i] >= other.min_point[i] for i in range(len(self.min_point)))
    
    def area(self):
        return math.prod(self.max_point[i] - self.min_point[i] for i in range(len(self.max_point)))
    
    def distance(self):
        return 2 * sum(self.max_point[i] <= self.min_point[i] for i in range(len(self.min_point)))
    
    def enlargement(self , other):
        enlarged_rectangle = Rectangle([min(self.min_point[i] , other.min_point[i]) for i in range(len(self.min_point))],
                                       [max(self.max_point[i], other.max_point[i]) for i in range(len(self.max_point))])     
        
        return enlarged_rectangle.area() - self.area()
    
    def contains(self, other):
        return all(self.min_point[i] <= other.min_point[i] and self.max_point[i] >= other.min_point[i] for i in range(len(self.min_point)))