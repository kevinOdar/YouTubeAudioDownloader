import os

def generate_directory_diagram(path, indent=""):
    if os.path.basename(path) in ("__pycache__", ".git", ".pytest_cache"):
        return

    print(indent + os.path.basename(path) + "/")
    indent += "    "

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                generate_directory_diagram(entry.path, indent)
            else:
                print(indent + entry.name)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))

    generate_directory_diagram(current_directory)
#sdsds