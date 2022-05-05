class Node:
    def __init__(self,type,children=None,leaf=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf

    def __str__(self):
        s = "Type: " + str(self.type) + "\n"
        s += "Leaf: " + str(self.leaf) + "\n"
        s += "".join( ["C: " + str(c) + "\n" for c in self.children])
        return s
