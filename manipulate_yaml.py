import yaml
import pytest

def find_value_by_hierarchy(data, hierarchy):
    """
    Navigate the nested YAML data to find a value by its hierarchy.
    Hierarchy is given in a dot-separated string format: 'parent.child.subchild'.
    """
    elements = hierarchy.split('.')
    current_data = data
    for elem in elements:
        if elem not in current_data:
            raise ValueError(f"Key '{elem}' in hierarchy '{hierarchy}' not found.")
        current_data = current_data[elem]
    return current_data

def replace_substring_in_yaml(path_to_file: str, hierarchy: str, needle: str, replace: str):
    """
    Replaces substring 'needle' within the value of 'hierarchy' with 'replace' in a YAML file.
    """
    with open(path_to_file) as file:
        data = yaml.safe_load(file)
    
    current_data = data
    elements = hierarchy.split('.')
    for elem in elements[:-1]:
        if elem not in current_data:
            raise ValueError(f"Key '{elem}' in hierarchy '{hierarchy}' not found.")
        current_data = current_data[elem]
    
    # Replace substring
    if needle in current_data[elements[-1]]:
        current_data[elements[-1]] = current_data[elements[-1]].replace(needle, replace)
        with open(path_to_file, 'w') as file:
            yaml.safe_dump(data, file)

def set_string_in_yaml(path_to_file: str, hierarchy: str, needle: str, replace: str):
    """
    Replaces value of key at 'hierarchy' with 'replace' if it matches 'needle' in a YAML file.
    """
    with open(path_to_file) as file:
        data = yaml.safe_load(file)
    
    current_data = data
    elements = hierarchy.split('.')
    for elem in elements[:-1]:
        if elem not in current_data:
            raise ValueError(f"Key '{elem}' in hierarchy '{hierarchy}' not found.")
        current_data = current_data[elem]
    
    # Set new value
    if current_data[elements[-1]] == needle:
        current_data[elements[-1]] = replace
        with open(path_to_file, 'w') as file:
            yaml.safe_dump(data, file)

# Unit tests for YAML functions
def create_test_yaml_file(file_path: str, content: dict):
    with open(file_path, 'w') as file:
        yaml.safe_dump(content, file)

@pytest.fixture
def setup_yaml_file(tmp_path):
    file_path = tmp_path / "test.yaml"
    content = {
        'root': {
            'child': 'Original',
            'another_child': 'Replaceable Text'
        }
    }
    create_test_yaml_file(file_path, content)
    return file_path

def test_replace_substring_in_yaml(setup_yaml_file):
    replace_substring_in_yaml(setup_yaml_file, 'root.another_child', 'Replaceable', 'Replaced')
    with open(setup_yaml_file) as file:
        data = yaml.safe_load(file)
    assert 'Replaced Text' == data['root']['another_child']

def test_set_string_in_yaml_no_change(setup_yaml_file):
    original_text = 'Original'
    set_string_in_yaml(setup_yaml_file, 'root.child', 'Nonexistent', 'New Value')
    with open(setup_yaml_file) as file:
        data = yaml.safe_load(file)
    assert original_text == data['root']['child']

def test_set_string_in_yaml_replace(setup_yaml_file):
    set_string_in_yaml(setup_yaml_file, 'root.child', 'Original', 'Replaced')
    with open(setup_yaml_file) as file:
        data = yaml.safe_load(file)
    assert 'Replaced' == data['root']['child']

# You can install them using pip: `pip install pyyaml pytest`
