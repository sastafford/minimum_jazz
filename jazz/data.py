from faker import Faker
import xml.etree.ElementTree as ET
import random
from pathlib import Path
import time

def generate_xml() -> str:
    faker = Faker()
    pi = ET.ProcessingInstruction("version", "1.0")
    root = ET.Element('MESSAGE')
    ET.PI(pi)
    metadata = ET.SubElement(root, 'METADATA')
    original_date = ET.SubElement(metadata, "ORIGINAL_DATE")
    original_date.text = faker.date()
    delivery_date = ET.SubElement(metadata, 'DELIVERED_DATE')
    delivery_date.text = faker.date()
    classification = ET.SubElement(metadata, "CLASSIFICATION")
    classification.text = random.choice(["OPEN", "SENSITIVE", "PROPRIETARY"])
    subject = ET.SubElement(root, 'SUBJECT')
    subject.text = faker.sentence()
    body = ET.SubElement(root, "BODY")
    body.text = faker.paragraph(nb_sentences=10)
    
    # supported in Python 3.10
    # ET.indent(root) 

    # create a new XML file with the results
    return ET.tostring(root)

def save_file(path, data):
    myfile = open(path, "w")
    myfile.write(data.decode('UTF-8'))

def generate(path, number_files):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    print("generating " + str(number_files) + " files")
    tic = time.perf_counter()
    for i in range(number_files):
        xml = generate_xml()
        xml_path = str(path) + "/sample-" + str(i) + ".xml"
        save_file(xml_path, xml)
    toc = time.perf_counter()
    print(f"Total Processing Time {toc - tic:0.4f} seconds")

