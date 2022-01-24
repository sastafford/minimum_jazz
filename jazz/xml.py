from faker import Faker
import xml.etree.ElementTree as ET
import random

def generate_xml(path):
    faker = Faker()
    root = ET.Element('MESSAGE')
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
    ET.indent(root)

    # create a new XML file with the results
    mydata = ET.tostring(root)
    print(mydata)
    myfile = open(path, "w")
    myfile.write(mydata.decode('UTF-8'))
