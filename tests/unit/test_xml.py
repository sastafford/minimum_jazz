from jazz.data import generate_xml, generate
from pathlib import Path

def test_xml_file_exists(tmpdir):
    xml_string = generate_xml()
    assert(xml_string.startswith("<?xml version='1.0'"))
    assert(xml_string.endswith("</MESSAGE>"))
    

def test_generate_files(tmpdir):
    generate(tmpdir, 3)
    for i in range(3):
        xml_path = tmpdir + "/sample-" + str(i) + ".xml"
        path = Path(xml_path)
        assert(path.is_file())
    
