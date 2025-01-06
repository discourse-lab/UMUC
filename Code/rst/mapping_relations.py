import dictionaries
import argparse
from pathlib import Path
import lxml.etree as ET
import os


def get_key_by_list_element(d, target_element):
    for k, v_list in d.items(): 
        if target_element in v_list:
            return k


def iterate_files(input_path, output_path, rst_type):
    for file_path in input_path.glob("*.rs3"):
        w = file_path.open()
        rf = w.read()
        tree = parseXML(rf, rst_type)

        # convert tree to an element tree and write into file
        element_tree = ET.ElementTree(tree)
        output_fp = output_path / os.path.basename(file_path)
        output_path.mkdir(parents=True, exist_ok=True)
        element_tree.write(output_fp, pretty_print=True)

    
def parseXML(xml, rst_type):
    tree = ET.fromstring(xml)
    elements = tree.xpath("/rst/header/relations/rel | /rst/body/segment | /rst/body/group")
    for relname in elements:
        if relname.tag == "rel":
            element_to_find = relname.attrib["name"].lower()
            if rst_type == "GUM":
                key = get_key_by_list_element(dictionaries.unsc2gum, element_to_find)
                print("UNSC: ", element_to_find, " GUM: ", key)
                relname.attrib["name"] = key
                assert key is not None
            elif rst_type == "RST-DT":
                key = get_key_by_list_element(dictionaries.unsc2rstdt, element_to_find)
                print("UNSC: ", element_to_find, " RST-DT: ", key)
                relname.attrib["name"] = key
                assert key is not None

        elif relname.tag == "segment" or relname.tag == "group":
            try:
                element_to_find = relname.attrib["relname"].lower()
                if rst_type == "GUM":
                    key = get_key_by_list_element(dictionaries.unsc2gum, element_to_find)
                    # print("UNSC: ", element_to_find, " GUM: ", key)
                    relname.attrib["relname"] = key
                    assert key is not None
                elif rst_type == "RST-DT":
                    key = get_key_by_list_element(dictionaries.unsc2rstdt, element_to_find)
                    print("UNSC: ", element_to_find, " RST-DT: ", key)
                    relname.attrib["relname"] = key
                    assert key is not None
            except:
                continue

    return tree
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rst_type", choices=["GUM", "RST-DT"], required=True)
    parser.add_argument("--path", required=True) # input path
    args = parser.parse_args()

    input_path = Path(args.path)
    rst_type = args.rst_type
    output_path = Path("./dataset/gold_translated_dataset/07_rst_" + rst_type+ "-relations")
    iterate_files(input_path, output_path, rst_type)
    print("Saved in: ", output_path)


if __name__=="__main__":
    main()



