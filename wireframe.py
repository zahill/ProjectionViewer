import math
import numpy as np

def translationMatrix(dx=0, dy=0, dz=0):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]
    ])

def scaleMatrix(sx=0, sy=0, sz=0):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def rotateXMatrix(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])

def rotateYMatrix(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])

def rotateZMatrix(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

class Node:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.w = 1

    def __str__(self):
        return "({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)

class Edge:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __str__(self):
        return "{} to {}".format(self.start, self.stop)

class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(Node(node))

    def addEdges(self, edgeList):
        for (start, stop) in edgeList:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))

    def outputNodes(self):
        print("---Nodes---")
        for i, node in enumerate(self.nodes):
            print("{:d}: {}".format(i, node))

    def outputEdges(self):
        print("---Edges---")
        for i, edge in enumerate(self.edges):
            print("{:d}: {}".format(i, edge))

    def translate(self, axis, d):
        if axis in ['x','y','z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)

    def scale(self, center, scale):
        center_x, center_y = center
        for node in self.nodes:
            node.x = center_x + scale*(node.x - center_x)
            node.y = center_y + scale*(node.y - center_y)
            node.z *= scale

    def findCenter(self):
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes])/num_nodes
        meanY = sum([node.y for node in self.nodes])/num_nodes
        meanZ = sum([node.z for node in self.nodes])/num_nodes

        return (meanX, meanY, meanZ)

    def rotateX(self, center, radians):
        cx, cy, cz = center
        for node in self.nodes:
            z = node.z - cz
            y = node.y - cy
            d = math.hypot(y,z)
            theta = math.atan2(y,z) + radians
            node.z = cz + d*math.cos(theta)
            node.y = cy + d*math.sin(theta)
    
    def rotateY(self, center, radians):
        cx, cy, cz = center
        for node in self.nodes:
            x = node.x - cx
            z = node.z - cz
            d = math.hypot(z,x)
            theta = math.atan2(z,x) + radians
            node.x = cx + d*math.cos(theta)
            node.z = cz + d*math.sin(theta)
    
    def rotateZ(self, center, radians):
        cx, cy, cz = center
        for node in self.nodes:
            x = node.x - cx
            y = node.y - cy
            d = math.hypot(y,x)
            theta = math.atan2(y,x) + radians
            node.x = cx + d*math.cos(theta)
            node.y = cy + d*math.sin(theta)

    def transform(self, matrix):
        self.nodes = np.dot(self.nodes,matrix)

if __name__=="__main__":
    cube_nodes = [(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)]
    cube = Wireframe()
    cube.addNodes(cube_nodes)
    cube.addEdges([(n,n+4) for n in range(0,4)])
    cube.addEdges([(n,n+1) for n in range(0,8,2)])
    cube.addEdges([(n,n+2) for n in (0,1,4,5)])
    cube.outputNodes()
    cube.outputEdges()
