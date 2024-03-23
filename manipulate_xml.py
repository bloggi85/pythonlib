import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import os
import pytest

# Implementation of functions
def find_element_by_hierarchy(root: Element, hierarchy: str) -> Element:
    elements = hierarchy.split('.')
    current_element = root
    for elem in elements:
        current_element = current_element.find(elem)
        if current_element is None:
            raise ValueError(f"Element '{elem}' in hierarchy '{hierarchy}' not found.")
    return current_element

def replace_substring(path_to_file: str, hierarchy: str, needle: str, replace: str):
    tree = ET.parse(path_to_file)
    root = tree.getroot()
    
    target_element = find_element_by_hierarchy(root, hierarchy)
    if needle not in target_element.text:
        return  # No update if needle not in element text
    
    target_element.text = target_element.text.replace(needle, replace)
    tree.write(path_to_file)

def set_string_in_file(path_to_file: str, hierarchy: str, needle: str, replace: str):
    tree = ET.parse(path_to_file)
    root = tree.getroot()
    
    target_element = find_element_by_hierarchy(root, hierarchy)
    if target_element.text != needle:
        return  # No update if needle does not match element text exactly
    
    target_element.text = replace
    tree.write(path_to_file)

# Unit tests with pytest
def create_test_xml_file(file_path: str, content: str):
    with open(file_path, 'w') as file:
        file.write(content)

@pytest.fixture
def setup_xml_file(tmp_path):
    file_path = tmp_path / "test.xml"
    content = """<root>
    <child>Original</child>
    <child>Replaceable Text</child>
    <!-- This is a comment -->
</root>"""
    create_test_xml_file(file_path, content)
    return file_path

def test_replace_substring(setup_xml_file):
    replace_substring(setup_xml_file, 'root.child', 'Replaceable', 'Replaced')
    tree = ET.parse(setup_xml_file)
    root = tree.getroot()
    assert 'Replaced Text' in root.find('child').text

def test_set_string_in_file_no_change(setup_xml_file):
    original_text = 'Original'
    set_string_in_file(setup_xml_file, 'root.child', 'Nonexistent', 'New Value')
    tree = ET.parse(setup_xml_file)
    root = tree.getroot()
    assert original_text == root.find('child').text

def test_set_string_in_file_replace(setup_xml_file):
    set_string_in_file(setup_xml_file, 'root.child', 'Original', 'Replaced')
    tree = ET.parse(setup_xml_file)
    root = tree.getroot()
    assert 'Replaced' == root.find('child').text

# Ensure pytest is installed in your environment: `pip install pytest`
