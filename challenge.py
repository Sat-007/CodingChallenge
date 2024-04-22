import json
import os
import sys
import xml.etree.ElementTree as ET
import csv

def xmlInput(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []
        for entity in root.findall('ENTITY'):
            for element in entity.findall('ENT'):
                entity_data = {}
                for child in element:
                    value = child.text.strip() if child.text else None
                    if value:
                        entity_data[child.tag.lower()] = value
                data.append(entity_data)
        json_data = json.dumps(data, indent=2)
        return json_data
    except Exception as e:
        return f"error: {e}"

def txtInput(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    data = []
    current_address = {}
    for line in lines:
        line = line.strip()
        if line == "":
            if current_address:
                data.append(current_address)
                current_address = {}
        else:
            if 'name' not in current_address:
                current_address['name'] = line
            elif 'address' not in current_address:
                current_address['address'] = line
            else:
                if "COUNTY" in line:
                    current_address['county'] = line
                else:
                    city_state = line.split(', ')
                    if len(city_state) == 2:
                        current_address['city'] = city_state[0]
                        state_zip = city_state[1].split(' ')
                        if len(state_zip) == 2:
                            current_address['state'] = state_zip[0]
                            current_address['zip_code'] = state_zip[1].strip('-')
    if current_address:
        data.append(current_address)
    return data



def tsvInput(file_path):
    with open(file_path, 'r') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        data = []
        for row in reader:
            name_parts = [row.get('first', ''), row.get('middle', ''), row.get('last', '')]
            name = ' '.join(filter(None, name_parts))

            address = {
                "name": name.strip() if name else None,
                "organization": row.get('organization', '').strip(),
                "street": row.get('address', '').strip(),
                "city": row.get('city', '').strip(),
                "state": row.get('state', '').strip().upper(),
                "zip": row.get('zip', '').strip()
            }
            address = {k: v for k, v in address.items() if v is not None}
            if address.get('name') and address.get('organization'):
                del address['organization']
            elif address.get('name') is None:
                address.pop('name', None)
            data.append(address)
        json_data = json.dumps(data, indent=2)
    return json_data






if __name__ == "__main__":
    print("Command-line arguments:", sys.argv)
    if len(sys.argv) != 3:
        print('Command-line usuage: python challenge.py filepath fileformat')
        sys.exit(1)
    file_path = sys.argv[1]
    file_format = sys.argv[2]
    try:
        if file_format == 'xml':
            entities = xmlInput(file_path)
            print(entities)

        elif file_format == 'txt':
            entities = txtInput(file_path)
            for address in entities:
                address_json = {
                    "name": address.get('name', ''),
                    "street": address.get('address', ''),
                    "city": address.get('city', ''),
                    "state": address.get('state', ''),
                    "county": address.get('county', ''),
                    "postal_code": address.get('zip_code', '')
                }
                address_json = {k: v for k, v in address_json.items() if v}
                print(json.dumps(address_json, indent=2))
        elif file_format == 'tsv':
            entities = tsvInput(file_path)
            print(entities)
        else:
            raise ValueError("Unsupported file format")
        
    except Exception as e:
        print(f"Error: {e}")







