import requests
from bs4 import BeautifulSoup
import json


def connect(username, password): # Not currently used as the session id it possible to retrieve with basic requests.
    login_url = 'https://backend.nortec1.dk/User/Login4/'
    session = requests.Session()

    # Define the login credentials and other necessary parameters
    payload = {
        'App': 'TUK',
        'session': 'undefined',
        'username': username,
        'password': password,
        'language': 'da',
        'domain': 'https://e-vaskeri.dk',
        'native': 'false',
        # Add other necessary parameters here if needed
    }
    response = session.post(login_url, data=payload)
    if response.status_code == 200:
        print("Login successful")
        return(session)
    else:
        print("Login failed")


def retrieve_machines(session, url):
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    machines = soup.select('object[data^="https://backend.nortec"]')
    timestamp = soup.find('i', string=lambda s: s and s.startswith('Aktualiseret')).text.strip()
    timestamp = timestamp.split(': ')[1]
    machines_with_name = []
    for machine in machines:
        name = machine.next_sibling.next_sibling.text.strip()
        machines_with_name.append((machine, name))

    return(timestamp, machines_with_name)


def get_svg_content(session, svg_url):
    response = session.get(svg_url)
    if response.status_code == 200:
        svg_content = response.content
        return svg_content
    else:
        return "Failed to fetch the SVG content."

#save_svg_content(get_svg_content(kk, objects[0]['data']), 'test.svg')
def extract_text_from_svg(svg_content):
    soup = BeautifulSoup(svg_content, 'xml')
    text_tags = soup.find_all('text')
    text_values = [tag.get_text() for tag in text_tags]
    return text_values


def extract_machinestate(session, svg_url):
    svg_content = get_svg_content(session, svg_url)
    text_values = extract_text_from_svg(svg_content)
    text_values = [text.replace('\n', ' ') for text in text_values]  # Remove line breaks
    return text_values


def get_states(url):
    session = requests.Session()
    time, objects = retrieve_machines(session, url)
    states = [time,[]]
    for obj in objects:
        states[1].append([obj[1], extract_machinestate(session, obj[0]['data'])])
    return states