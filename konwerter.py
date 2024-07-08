import sys
import json
import xml.etree.ElementTree as ET
import yaml

def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return elem_to_dict(root)

def elem_to_dict(elem):
    d = {elem.tag: {} if elem.attrib else None}
    children = list(elem)
    if children:
        dd = {}
        for dc in map(elem_to_dict, children):
            for k, v in dc.items():
                if k in dd:
                    if not isinstance(dd[k], list):
                        dd[k] = [dd[k]]
                    dd[k].append(v)
                else:
                    dd[k] = v
        d = {elem.tag: dd}
    if elem.attrib:
        d[elem.tag].update(('@' + k, v) for k, v in elem.attrib.items())
    if elem.text:
        text = elem.text.strip()
        if children or elem.attrib:
            if text:
                d[elem.tag]['#text'] = text
        else:
            d[elem.tag] = text
    return d

def write_xml(data, file_path):
    root = dict_to_elem(data)
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

def dict_to_elem(d):
    tag, body = next(iter(d.items()))
    elem = ET.Element(tag)
    if isinstance(body, dict):
        for k, v in body.items():
            if k.startswith('@'):
                elem.set(k[1:], v)
            elif k == '#text':
                elem.text = v
            else:
                elem.append(dict_to_elem({k: v}))
    else:
        elem.text = body
    return elem

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def write_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.safe_dump(data, file, default_flow_style=False)

def convert(input_path, output_path):
    input_format = input_path.split('.')[-1].lower()
    output_format = output_path.split('.')[-1].lower()

    if input_format == 'xml':
        data = read_xml(input_path)
    elif input_format == 'json':
        data = read_json(input_path)
    elif input_format in ['yml', 'yaml']:
        data = read_yaml(input_path)
    else:
        raise ValueError(f'Unsupported input format: {input_format}')

    if output_format == 'xml':
        write_xml(data, output_path)
    elif output_format == 'json':
        write_json(data, output_path)
    elif output_format in ['yml', 'yaml']:
        write_yaml(data, output_path)
    else:
        raise ValueError(f'Unsupported output format: {output_format}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        convert(input_path, output_path)
        print(f'Successfully converted {input_path} to {output_path}')
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)