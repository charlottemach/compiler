class Node:
    def __init__(self,type,children=None):
        self.type = type
        self.children = children
        self.edges = []

    def __str__(self):
        s = str(self.type) + "- "
        if type(self.children) == list:
            s += "".join( ["[" + str(c) + "]" for c in self.children])
        else:
            s += "[" + str(self.children) + "]"
        return s


    def calculate_edges(self):
        if self.edges == []:
            edges = []
            for child in self.children:
                if type(child) is Node:
                    edges.append((str(self.type)+'('+str(id(self))+')',str(child.type)+'('+str(id(child))+')'))
                    edges.extend(child.calculate_edges())
                else:
                    edges.append((str(self.type)+'('+str(id(self))+')',str(child)+'('+str(id(child))+')'))
            self.edges = edges
        return self.edges
