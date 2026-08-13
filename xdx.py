class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []  # List to hold child nodes

    def add_child(self, child_node):
        """Adds a child node to the current node."""
        self.children.append(child_node)

    def print_tree(self, level=0):
        """Helper method to visually print the tree using indentation."""
        indent = "   " * level
        print(f"{indent}└── {self.data}")
        for child in self.children:
            child.print_tree(level + 1)


# Create the root node
root = TreeNode("Electronics")

# Create first-level children
laptop = TreeNode("Laptops")
phone = TreeNode("Cell Phones")

# Create second-level children
macbook = TreeNode("MacBook")
thinkpad = TreeNode("ThinkPad")
iphone = TreeNode("iPhone")

# Build the tree structure
root.add_child(laptop)
root.add_child(phone)

laptop.add_child(macbook)
laptop.add_child(thinkpad)
phone.add_child(iphone)

# Print the final hierarchy
root.print_tree()

print(type({}))
