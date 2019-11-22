import random


class AbstractNode:

    def __init__(self, parent=None, key=None):
        self.parent = parent
        self.key = key

    def eval(self, var_dic={}):
        pass

    def copy(self):
        pass

    def serialize(self, node_list: list):
        pass

    def is_terminal(self):
        pass


class AbstractInternal(AbstractNode):

    def __init__(self, parent=None, key=None, left=None, right=None):
        super().__init__(parent, key)
        self.set_children(left, right)

    def set_children(self, left, right):
        self.children = {
            'left': left,
            'right': right,
        }
        for key, child in self.children.items():
            if child is None:
                continue
            child.parent = self
            child.key = key

    def eval(self, var_dic={}):
        """Evaluate the children of the node and return a dictionary of values."""

        self.children_eval = {}
        for key, child in self.children.items():
            self.children_eval[key] = child.eval(var_dic=var_dic)
        return self.children_eval

    def copy(self):
        """Make a copy of the node and its children, returning the copy of
        the node."""

        children_copy = {}
        for key, child in self.children.items():
            children_copy[key] = child.copy()

        return type(self)(**children_copy)

    def serialize(self, node_list: list):
        """Fill the list with all the nodes in the tree, with the first element as
        the root node."""

        node_list.append(self)
        for child in self.children.values():
            child.serialize(node_list)

    def generate_children(self, internals: list, terminals: list, depth: int,
                          terminal_prob: float):
        """Randomly generate the children of the node from the internals and
        terminals lists."""

        self.children = {}
        children_keys = ['left', 'right']
        for key in children_keys:
            # Select the list from which to pick the next child.
            nodes = terminals if depth == 0 or random.random() < terminal_prob else internals
            rand_index = random.randint(0, len(nodes) - 1)
            # Pick the child.
            child = nodes[rand_index](parent=self, key=key)
            self.children[key] = child
            # Keep generating nodes.
            if not child.is_terminal():
                child.generate_children(internals, terminals, depth - 1,
                                        terminal_prob)

    def is_terminal(self):
        return False


class AbstractTerminal(AbstractNode):

    def __init__(self, value, parent=None, key=None):
        super().__init__(parent, key)
        self.value = value

    def eval(self, var_dic={}):
        """Return the value of the terminal."""

        return self.value

    def copy(self):
        """Return a new instance of the terminal."""

        return type(self)()

    def serialize(self, node_list: list):
        """Append this node to the list."""

        node_list.append(self)

    def is_terminal(self):
        return True


def binary_operation_node(operation):

    class BinaryOpNode(AbstractInternal):

        def eval(self, var_dic={}):
            children_eval = super().eval(var_dic=var_dic)
            return operation(children_eval['left'], children_eval['right'])

    return BinaryOpNode


def value_node(value_generator):

    class ValueNode(AbstractTerminal):

        def __init__(self, parent=None, key=None):
            value = value_generator()
            super().__init__(value, parent=parent, key=key)

    return ValueNode
