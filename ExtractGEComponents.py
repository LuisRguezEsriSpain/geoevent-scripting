import xml.etree.ElementTree as ET

geoEventBackupFile = r'.\GeoEventBackup-2023-02-23.xml'

treeConfigGE = ET.parse(geoEventBackupFile)
root = treeConfigGE.getroot()

inputs = root.findall("./inputs/input")
print("Inputs:")
for input in inputs:
	print('{"label": "' + input.attrib['label'] + '", "name": "' + input.attrib['name'] + '"},')

outputs = root.findall("./outputs/output")
print("Outputs:")
for output in outputs:
	print('{"label": "' + output.attrib['label'] + '", "name": "' + output.attrib['name'] + '"},')

services = root.findall("./geoEventServices/geoEventService")
print("GeoEventServices:")
for service in services:
	print('{"label": "' + service.attrib['label'] + '", "name": "' + service.attrib['name'] + '"},')
