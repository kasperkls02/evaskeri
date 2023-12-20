# Nortec.py

## Description
A brief description of what the `nortec.py` script does.

## Installation
Instructions on how to install any dependencies required by the script.


## Getting the server and session string
It has not yet been possible to get the session string directly from a request on the server, so we first have to fetch that manually using DevTools. 
Login to https://e-vaskeri.dk/ or a similar Nortec page. 
Now open the DevTool F12 and open the Network tab and select only 'Fetch/XHR'
Either reload the page or wait for refresh. It should be named along the lines of ".../?App=TUK@session=..."
Open the request and copy copy the request url it should be along the lines of: 
https://backend.nortec1.dk/User/Refresh1/?App=TUK&session=asdasdadasdasdddas&tabid=&tick=1703096297554&native=false&.json

We need 
* server: https://backend.nortec1.dk
* session: asdasdadasdasdddas

## Functions and examples
### get_machines(server, session):
The ```get_machines(server, session)``` function return a list that contains the timestamp provided by the server when the request was made and a second list containing information about the site. 

The response is on the form:
```
(Timestamp, [[MachineName, unit, machineIdentifier],
             [MachineName, unit, machineIdentifier]])
```

```Python
>>> print(get_machines(server, session))
('18:48', [['Vaskemaskine 1', 'unit5', 'asddas'], ['Vaskemaskine 2', 'unit5', 'adsfgf'], ['Vaskemaskine 3', 'unit5','jgudjg']]) 
```

### get_state(server, unit, machineIdentifier)
The ```get_state(server, unit, machineIdentifier)``` function return the state of a machine. The response is on the form:
```
['time remaining', 'program', 'state (e.g. "Hovedvask")', '?', 'status (e.g. "OPTAGET")', '?']
```
```Python
>>> print(get_state(server, unit, machineIdentifier))
['9:41', '40° Normal', 'Centrifugering', '', 'OPTAGET', '']
```



### get_states(server, session)
The ```get_states(server,session)``` function is a combination of the above two function. It therefore returns a list that contains the timestamp provided by the server when the request was made and a second list containing information about all machines associated with the site.

The response is on the form: 
```
[Time, 
    [
        [MachineName, 
            [time remaining, 
            program, 
            state (e.g. "Hovedvask"), 
            ?, 
            status (e.g. "OPTAGET"), 
            ?]
        ]
    ]
]
```

```python
>>> print(get_states('https://backend.nortec1.dk', 'asdasdadasdasdddas'))
['18:46', [['Vaskemaskine 1', ['', '40° Normal', '', '', 'FÆRDIG', '']], ['Vaskemaskine 2', ['', '', '', '', 'FRI', '']]]]
```


### get_statements(server, session): 
The ```get_statements(server, session)``` function return a list of receipts and the current saldo and previus saldo. The output represents a JSON structure of the following properties:
- `Receipts`: A list of receipt objects.
  - `LocationId`: The ID of the location.
  - `Title`: The date of the receipt.
  - `Description`: Address of the site.
  - `Lines`:
    - `UnitId`: The ID of the unit.
    - `Time`: The time of the wash/drying
    - `Unit`: The unit name.
    - `Text`: The selected program
    - `Amount`: The amount of the line.
    - `Tag`: The tag of the line.
    - `Returned`: Indicates if the line is returned.
  - `LinesTotal`: The total amount of the lines.
  - `LinesVat`: The VAT amount of the lines.
  - `PaymentsTotal`: The total amount of payments.
  - `Saldo`: The saldo amount.
- `Rate`: The rate.
- `ReturnTime`: The return time.
- `ServerId`: The ID of the server.
- `Session`: The session string.
- `Return`: The return value.
- `Saldo`: The saldo object.
  - `CurrentPeriod`: The saldo of the current period.
  - `LastPeriod`: The saldo of the last period.

```Python
>>> print(nortec.get_statements(server, session))
{'Receipts': [{'LocationId': 125, 'Title': 'Onsdag 13.  december 2023', 'Description': [''], 'Lines': [{'UnitId': 6, 'Time': '19:01', 'Unit': 'Vaskemaskine 6', 'Text': 'Program 4 Normal 40°, forvask, kulørt sæbe, meget snavset', 'Amount': 1200, 'Tag': 1, 'Returned': False}], 'LinesTotal': 1200, 'LinesVat': 0, 'PaymentsTotal': 0, 'Saldo': -1200},], 'Rate': 0, 'ReturnTime': 235, 'ServerId': 1, 'Session': '', 'Return': 100, 'Saldo': {'CurrentPeriod': '-1200', 'LastPeriod': '-3600'}}
```

### get_saldo(server, session)

The ```get_saldo(server, session)``` is a function that extracts the current and previus saldo from the ```get_statemants``` function. 
```Python
>>> print(get_saldo(server, session))
{'CurrentPeriod': '-1200', 'LastPeriod': '-3600'}
```




## Contributing
Information on how others can contribute to the development of the `nortec.py` script.

## License
Information about the license under which the `nortec.py` script is distributed.

## Contact
How to get in touch with the author or maintainers of the `nortec.py` script.
