
import yaml
import os

def load_test_data(filename):
    path = os.path.join("test_data", filename)
    with open(path, "r") as f:
        return yaml.safe_load(f)
    