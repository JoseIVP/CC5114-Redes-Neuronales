import random


class Generator:

    def __init__(self, internals, terminals, depth=0, terminal_prob=0):
        self.internals = internals
        self.terminals = terminals
        self.depth = depth
        self.terminal_prob = terminal_prob

    def generate(self):
        """Generate a random tree, returning the root."""

        # Select the list from which to pick the root node.
        nodes = self.terminals if random.random() < self.terminal_prob else self.internals
        rand_index = random.randint(0, len(nodes) - 1)
        root = nodes[rand_index]()  # Pick the root node
        if not root.is_terminal():
            root.generate_children(self.internals, self.terminals, self.depth,
                                self.terminal_prob)
        return root
