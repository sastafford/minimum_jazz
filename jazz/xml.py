from faker import Faker
import xml.etree.ElementTree as ET

def get_random_name():
    faker = Faker()
    return faker.name()

def generate_xml(path):
    root = ET.Element('MESSAGE')
    metadata = ET.SubElement(root, 'METADATA')
    delivery_date = ET.SubElement(root, 'DeliveredDate')
    subject = ET.SubElement(root, 'SUBJECT')
    body = ET.SubElement(root, "BODY")
    classification = ET.SubElement(root, "CLASSIFICATION")
    ET.indent(root)

    # create a new XML file with the results
    mydata = ET.tostring(root)
    print(mydata)
    myfile = open(path, "w")
    myfile.write(mydata.decode('UTF-8'))
