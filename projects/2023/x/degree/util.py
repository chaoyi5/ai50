class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1] # 最後一個值
            self.frontier = self.frontier[:-1] # 排除最後一個值以外的所有值
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            # 手動拋出異常：http://c.biancheng.net/view/2360.html
            raise Exception("empty frontier")
        else:
            node = self.frontier[0] # 第一個值
            self.frontier = self.frontier[1:] # 排除第一個值以外的所有值
            return node
