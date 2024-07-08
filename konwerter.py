import sys
import json
import xml.etree.ElementTree as ET
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

def parse_args(args):
    if len(args) == 3:
        input_path = args[1]
        output_path = args[2]
        convert(input_path, output_path)
        sys.exit(0)
    elif len(args) != 1:
        print("Usage: program.exe [input_path output_path]")
        sys.exit(1)

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

def verify_json(data):
    if not isinstance(data, dict):
        raise ValueError("JSON data is not a valid dictionary")
    # Add more validation checks as necessary

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
        verify_json(data)
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

def save_data_to_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print(f"Data successfully saved to {file_path}")

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel('Select a file to convert', self)
        self.layout.addWidget(self.label)

        self.btnInput = QPushButton('Select Input File', self)
        self.btnInput.clicked.connect(self.selectInputFile)
        self.layout.addWidget(self.btnInput)

        self.btnOutput = QPushButton('Select Output File', self)
        self.btnOutput.clicked.connect(self.selectOutputFile)
        self.layout.addWidget(self.btnOutput)

        self.btnConvert = QPushButton('Convert', self)
        self.btnConvert.clicked.connect(self.convertFile)
        self.layout.addWidget(self.btnConvert)

        self.btnSaveJson = QPushButton('Save Data to JSON', self)
        self.btnSaveJson.clicked.connect(self.saveDataToJson)
        self.layout.addWidget(self.btnSaveJson)

        self.setLayout(self.layout)
        self.input_path = None
        self.output_path = None
        self.data = None

    def selectInputFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", 
                                                  "All Files (*);;XML Files (*.xml);;JSON Files (*.json);;YAML Files (*.yaml *.yml)", options=options)
        if fileName:
            self.input_path = fileName
            self.label.setText(f'Selected input file: {fileName}')

    def selectOutputFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", 
                                                  "All Files (*);;XML Files (*.xml);;JSON Files (*.json);;YAML Files (*.yaml *.yml)", options=options)
        if fileName:
            self.output_path = fileName
            self.label.setText(f'Selected output file: {fileName}')

    def convertFile(self):
        if self.input_path and self.output_path:
            try:
                self.data = convert(self.input_path, self.output_path)
                self.label.setText(f'Successfully converted {self.input_path} to {self.output_path}')
            except Exception as e:
                self.label.setText(f'Error: {e}')
        else:
            self.label.setText('Please select both input and output files')

    def saveDataToJson(self):
        if self.data:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save Data to JSON File", "", 
                                                      "JSON Files (*.json)", options=options)
            if fileName:
                try:
                    save_data_to_json_file(self.data, fileName)
                    self.label.setText(f'Successfully saved data to {fileName}')
                except Exception as e:
                    self.label.setText(f'Error: {e}')
        else:
            self.label.setText('No data available to save')

if __name__ == '__main__':
    parse_args(sys.argv)
    
    app = QApplication(sys.argv)
    ex = ConverterApp()
    ex.setWindowTitle('File Converter')
    ex.resize(400, 200)
    ex.show()
    sys.exit(app.exec_())