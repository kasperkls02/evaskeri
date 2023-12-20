import requests
from bs4 import BeautifulSoup
import json


def get_live(server, session):
    url = server + 'Location/Live5/?App=TUK&session=' + session
    req = requests.Session()
    response = req.get(url)
    return(response.content)

def get_home(server, session): # To be used to retrieve machines currently used by account
    url = server + 'User/Home3/?App=TUK&session=' + session
    req = requests.Session()
    response = req.get(url)
    return(response.content)


def get_machines(server, session):
    content = get_live(server, session)
    soup = BeautifulSoup(content, 'html.parser')

    machines = soup.select('object[data^="' + server + '"]')
    
    timestamp = soup.find('i', string=lambda s: s and s.startswith('Aktualiseret')).text.strip()
    timestamp = timestamp.split(': ')[1]

    machines_with_name = []
    for machine in machines:
        name = machine.next_sibling.next_sibling.text.strip()
        unit = machine.attrs['data'].split('/')[4]
        machine  = machine.attrs['data'].split('/')[5]
        machines_with_name.append([name, unit, machine])

    return(timestamp, machines_with_name)

def get_state(server, unit, machineIdentifier):
    url = server + 'download/' + unit + '/' + machineIdentifier + '/g/200/200.svg'

    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to fetch the SVG content."
    with open('response_content.svg', 'wb') as file:
        file.write(response.content)
    #soup = BeautifulSoup(response.content, 'xml')
    soup = BeautifulSoup(response.content, 'html.parser')
    text_tags = soup.find_all('text')
    
    text_values = [tag.get_text() for tag in text_tags]
    text_values = [text.replace('\n', '') for text in text_values]
    
    return text_values

def get_states(server, session):
    time, objects = get_machines(server, session)
    states = [time,[]]
    for obj in objects:
        states[1].append([obj[0], get_state(server, obj[1], obj[2])])
    return states


def get_statements(server, session): 
    ident = 'User/Statement5/'
    url = server + ident +'?App=TUK&session=' + session
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    xmp_tag = soup.find('xmp')
    json_data = None
    if xmp_tag:
        json_data = json.loads(xmp_tag.text)

    # Find the section with the name "statement"
    for section in json_data['Sections']:
        if section['Name'] == 'statement':
            # Create the new structure
            new_structure = {
                'CurrentPeriod': str(int(float(section['Rows'][1]['Columns2']['Cells'][0].replace(' kr', '').replace(',', '.')) * 100)),
                'LastPeriod': str(int(float(section['Rows'][1]['Columns2']['Cells'][1].replace(' kr', '').replace(',', '.')) * 100))
            }
            # Replace the old structure with the new one
            json_data['Saldo'] = new_structure
            json_data.pop('Sections')

    # Remove the "Cover" field
    if 'Cover' in json_data:
        json_data.pop('Cover')
        
    return(json_data)

def get_saldo(server, session):
    data = get_statements(server, session)
    return data.get('Saldo', None)



