from jazz.data import generate_xml
from pathlib import Path

def test_xml_file_exists(tmpdir):
    xml_path = tmpdir + "/sample.xml"
    print(xml_path)
    generate_xml(xml_path)
    path = Path(xml_path)
    assert(path.is_file())