"""Day 7 challenges."""
# pylint: disable=invalid-name
# Imports
import os

# Read the input data
path = os.path.join('.', 'data', 'day7_command_history.txt')
with open(path, 'r', encoding='utf8') as f:
    logs = f.read().splitlines()

# %% Challenge 1
class mockDir():
    """Mock directory."""

    def __init__(self, parent):
        """Init."""
        self.parent = parent
        self.children = {}
        self.files = {}
        self.size = 0

    def add_child(self, child_name):
        """Add a child folder."""
        if child_name not in self.children:
            self.children[child_name] = mockDir(self)

    def add_file(self, file_name, size):
        """Add a file to folder."""
        if file_name not in self.files:
            self.files[file_name] = mockFile(self, size)
            self.size += size

            # Update parent size
            if self.parent is not None:
                self.parent._update(size)  # pylint: disable=protected-access

    def _update(self, size):
        """Recursively update size of folders"""
        self.size += size
        if self.parent is not None:  # Update parent unless we're in root
            self.parent._update(size)  # pylint: disable=protected-access

    def get_child(self, child_name):
        """Get the child object."""
        return self.children[child_name]

    def get_parent(self):
        """Get the parent object."""
        return self.parent

class mockFile():  # pylint: disable=too-few-public-methods
    """Mock file."""

    def __init__(self, parent, size: int):
        """Init."""
        self.parent = parent
        self.size = size

# Generate the file tree
root = mockDir(None)  # Root directory "/"
current_dir = root
for log in logs:
    parsed_log = log.lstrip("$").split()
    # Since we parse line by line, ls is essentially useless
    if parsed_log[0] == "ls":
        continue

    # Move into new directory
    if parsed_log[0] == "cd":
        if parsed_log[1] == "/":
            current_dir = root
        elif parsed_log[1] == "..":
            current_dir = current_dir.get_parent()
        else:
            current_dir = current_dir.get_child(parsed_log[1])

    # Create new directory
    elif parsed_log[0] == "dir":
        current_dir.add_child(parsed_log[1])

    # Create new file
    elif parsed_log[0].isnumeric():
        current_dir.add_file(file_name=parsed_log[1], size=int(parsed_log[0]))

    else:
        print(f'WARNING: Unproccesed log line: {log}')

# Check which folders are smaller than 100000
small_sizes = []
def check_size(folder: mockDir):
    """Check size of folder and all its subfolders"""
    if folder.size <= 100000:
        small_sizes.append(folder.size)
    for child in folder.children:
        check_size(folder.get_child(child))
check_size(root)
print(f"Total size of /: {root.size}")
print(f"Sum of folders with size less than 100000: {sum(small_sizes)}")

# %% Challenge 2
max_size = 70000000
req_size = 30000000
free_size = max_size - root.size
smallest_delete_size = req_size - free_size

def get_smallest_delete(folder: mockDir, current_smallest: int):
    """Check size of folder and all its subfolders"""
    if smallest_delete_size <= folder.size < current_smallest:
        current_smallest = folder.size
    for child in folder.children:
        current_smallest = get_smallest_delete(folder.get_child(child), current_smallest)
    return current_smallest
delete_size = get_smallest_delete(root, root.size)
print(f"Smallest theoretical folder to delete has size {smallest_delete_size}")
print(f"Smallest single folder to delete for enough space has size {delete_size}")
