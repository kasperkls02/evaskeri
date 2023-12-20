import json
import nortec
# Load the secrets from secrets.json
with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

url = secrets['url']

states = nortec.get_states(url)
print(states[0])
for i in states[1]:
    print(i[0], i[1])


'''
16:35
Vaskemaskine 1 [' 32:46', ' 60° Normal', ' Hovedvask', ' ', ' OPTAGET', ' ']
Vaskemaskine 2 [' 17:33', ' 40° Normal', ' Skyl', ' ', ' OPTAGET', ' ']
Vaskemaskine 3 [' 32:57', ' 60° Normal', ' Hovedvask', ' ', ' OPTAGET', ' ']
Vaskemaskine 4 [' 21:49', ' 40° Normal', ' Skyl', ' ', ' OPTAGET', ' ']
Vaskemaskine 5 [' 21:55', ' 40° Normal', ' Skyl', ' ', ' OPTAGET', ' ']
Vaskemaskine 6 [' 10:44', ' 40° Normal', ' Centrifugering', ' ', ' OPTAGET', ' ']
Tørretumbler 7 [' ', ' ', ' ', ' ', ' FRI', ' ']
Tørretumbler 8 [' ', ' ', ' ', ' ', ' FRI', ' ']
Tørretumbler 9 [' 10:55', ' 55° Medium', ' Opvamning', ' ', ' OPTAGET', ' ']
Tørretumbler 10 [' ', ' ', ' ', ' ', ' FRI', ' ']
'''
