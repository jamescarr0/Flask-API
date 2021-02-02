# Flask-RESTful API - Work in progress

## Installation
```
pip install -r requirements.txt
FLASK_APP=api. # Set environment variable according to os: eg: 'set FLASK_APP=api', '$env:FLASK_APP=api
flask run

```

## Features

### JWT Authentication
- Access tokens.
- Refresh tokens.
- Revoke tokens. (Blacklisting)
- Customised error responses

### Password hashing
- Argon2

## Endpoints

### GET
   - /items
   - /items/<user_id>
   - /item/<name>
   - /stores
 
### POST
 - /register
 - /login
 - /logout
 - /item/<name>
  - /store/<id>
  
### PUT
- /item/<name>

### DELETE
- /user/<user_id>
- /item/<name>
- /store/<id>
