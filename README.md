# PlanetLabsCodeTest
*A REST service that can be used to store, fetch, and update user records.*

##### To install dependencies
```bash
$ pip install pipreqs
```

##### To run tests
``` bash
$ python tests.py
```

##### To start server
```bash
$ python run.py

```
The app will be available at http://127.0.0.1:5000

## API

A user record is represented in a JSON hash like so:

```json
{
    "first_name": "Joe",
    "last_name": "Smith",
    "userid": "jsmith",
    "groups": ["admins", "users"]
}
```


The service provides the following endpoints and semantics:

```
GET /users/<userid>
    Returns the matching user record or 404 if none exist.
```

```
POST /users
    Creates a new user record. The body of the request should be a valid user
    record. POSTs to an existing user should be treated as errors and flagged
    with the appropriate HTTP status code.
```

```
DELETE /users/<userid>
    Deletes a user record. Returns 404 if the user doesn't exist.
```

```
PUT /users/<userid>
    Updates an existing user record. The body of the request should be a valid
    user record. PUTs to a non-existant user should return a 404.
```

```
GET /groups/<group name>
    Returns a JSON list of userids containing the members of that group. Should
    return a 404 if the group doesn't exist.
```

```
POST /groups
    Creates a empty group. POSTs to an existing group should be treated as
    errors and flagged with the appropriate HTTP status code. The body should contain
    a `name` parameter
```

```
PUT /groups/<group name>
    Updates the membership list for the group. The body of the request should 
    be a JSON list describing the group's members.
```

```
DELETE /groups/<group name>
    Deletes a group.
```

## Database Schema
![Database Schema](http://i.imgur.com/VnZKeNQ.png)   
P.S. This application is developed with python2.7
