class Point:
    def __init__(self, coordinit: list):
        self.coord = coordinit
        self.size = len(coordinit)
        
    def euclid_distance(self, secondPoint) -> float:
        d = 0
        for index in range(self.size):
            d += (self.coord[index] - secondPoint.coord[index])**2
        return d**0.5

    def display_with_parentheses(self) -> str:
        coordStr = ''
        for index in range(self.size - 1):
            coordStr += str(self.coord[index]) + ', '
        coordStr += str(self.coord[-1])
        return ''.join('(' + coordStr + ')')
    
    def display(self) -> str:
        coordStr = ''
        for index in range(self.size - 1):
            coordStr += str(self.coord[index]) + ', '
        coordStr += str(self.coord[-1])
        return ''.join(coordStr)

def calculate_midpoint_of_list(listPoints: list) -> list():
    midpoint = list()
    pointSize = listPoints[0].size
    for iCoord in range(pointSize):
        curr = 0
        for point in listPoints:
            curr += point.coord[iCoord]
        midpoint.append(curr/len(listPoints))
    return Point(midpoint)
        
def compare_two_point(a: Point, b: Point) -> int:
    if a.size != b.size:
        return 0
    for iCoordA in range(len(a.coord)):
        if a.coord[iCoordA] - b.coord[iCoordA] != 0:
            return 0
    return 1

