
# DATA-GRID-SURFACE
SDK to communicate with data-grid API service.
It uses the API service and it's end-points to determine if the given emails or passwords have been compromised.


## Installation

Install data-grid-surface SDK:

```
pip install data-grid-surface
```

## Using data-grid-access sdk

Import DataGrid class from library

```
from data_grid_surface.data_grid import DataGrid
```

You will need to provide username and password parameters to DataGrid class constructor. These are credentials for data-grid API service.

### DataGrid methods

DataGrid methods return dictionary as a result.

**Methods:**
* check_email(email) -> email as string parameter
* check_password(password) -> password as string parameter

**Use example:**

```
from data_grid_surface.data_grid import DataGrid

dataGrid = DataGrid(username='testuser', password='testpassword')
response = dataGrid.checkEmail('email@example.com')
print(response)
```

**Response examples:**

```
{
    'status': 'success', 
    'data': {
        'emails': [
            {
                '_id': '6033927de534be1225cd4052', 
                'email': 'email@example.com'
            }
        ]
    }
}
```

```
{
    'status': 'fail', 
    'message': 'Not Found'
}
```