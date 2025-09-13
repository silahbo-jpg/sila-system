import os

IGNORED = ['node_modules', '.git', '__pycache__', '.idea', '.vscode']

def print_tree(root, indent=""):
    for item in sorted(os.listdir(root)):
        path = os.path.join(root, item)
        if item in IGNORED or item.endswith('.pyc'):
            continue
        print(indent + item + ("/" if os.path.isdir(path) else ""))
        if os.path.isdir(path):
            print_tree(path, indent + "  ")

if __name__ == "__main__":
    print_tree(".")

