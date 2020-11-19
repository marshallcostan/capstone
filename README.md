# Casting Agency API Backend

In an effort to help better manage the relationships involved in a generic casting agency this API was created. 
It allows for the creation, updating, accessing and deletion of both actors and movies. The creation of casts using existing actors and movies 
can be done as well.

All backend code follows PEP8 style guidelines, thanks developers!

## Getting Started

### Installing Dependencies

For developers working on this project Python3, pip, and PostgreSQL should be installed on their local machines.

#### Python 3

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

It is recommended to work within a virtual environment when using Python for projects. 

#### Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/capstone` directory and running:

```bash
pip install -r requirements.txt
```

*Verify the current version of Werkzeug is installed to avoid errors.*

## Database Setup

Start the Postgres server, create a database named "capstone" and tables will later be created upon app execution. 

## Setting environmental variables

*If running locally be sure to replace ```DATABASE_URL``` in ```setup.sh``` with your database address.*

To load environmental variables from the `Capstone` directory:

```bash
source setup.sh
```
`setup.sh` includes authorization tokens for three different roles used by the casting agency, executive producer, casting director and casting assistant. 


## Running the server

To run the server, from within the `Capstone` directory execute the following commands:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

These commands direct the app to use the file app.py as well as setting the app development mode. In development mode the server will automatically
restart if any changes are made to the code.

The default URL the app runs on is: http://127.0.0.1:5000/

## Testing

*The first time the tests are run omit the dropdb and createdb commands.*

To run the tests, run

```
dropdb capstone
createdb capstone
python test_app.py
```

## Error Handling

Errors are returned as JSON objects using the following format:
```bash
{
"success": False,
"error": 422,
"message": "unprocessable"
}
```

This API will return these error types when requests fail:

- 400: Bad Request
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable
- 500: Internal server error

## RBAC

Roles:
- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All permissions a Casting has and
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All permissions a Casting Director has and
    - Add or delete a movie from the database
    - Create casts for movies

If using a REST client such as Postman to test API endpoints the authorization tokens can be found in `setup.sh`.


## Endpoints


### GET /actors 

   General:
        
   - Returns a dictionary of all actors and attibutes as key:value pairs and a success value.
        
   Sample:  
         
   http://127.0.0.1:5000/actors
```bash 
{
    "actors": [
        {
            "age": 37,
            "gender": "male",
            "id": 2,
            "name": "Jonah Hill"
        }
    ],
    "success": true
}
```

### GET /movies

General:

   - Returns a dictionary of all movies and attributes as key:value pairs and a success value.

```
{
    "created": {
        "id": 7,
        "release_date": "Fri, 17 Aug 2007 00:00:00 GMT",
        "title": "Superbad"
    },
    "success": true
}

```

### DELETE /actor/<id>  &  /movie/<id>

General:

   - These endpoints delete an actor/movie of a given ID.
   
   - Returns a success value and the ID of the deleted entry. 
``` 
{
    "deleted": 3,
    "success": true
}
```

### PATCH /actor/<id>

General:
    
   - Updates an existing actor of a given ID by submitting a JSON object containing a new entry such as:
```
{
    'age': 35
}
```
   - Returns a success value and the updated object.
```
{
    "success": true,
    "updated": {
        "age": 35,
        "gender": "male",
        "id": 2,
        "name": "Jonah Hill"
    }
}
```

### PATCH /movie/<id>

General:
    
   - Updates an existing movie of a given ID by submitting a JSON object containing a new entry such as:
```
{
    "release_date": "January 1 1999"
}
```
   - Returns a success value and the updated object.
```
{
    "success": true,
    "updated": {
        "id": 3,
        "release_date": "Fri, 01 Jan 1999 00:00:00 GMT",
        "title": "Superbad"
    }
}
```

### POST /actor

General:
    - Creates a new actor by passing a JSON object such as:
    ```
{
"name":"Jonah Hill",
"age": 32,
"gender":"male"
}
    ```
    - Returns a success value and the newly created object.
    
```
{
    "created": {
        "age": 32,
        "gender": "male",
        "id": 3,
        "name": "Jonah Hill"
    },
    "success": true
}
```


### POST /movie

General:
    - Creates a new actor by passing a JSON object such as:
    ```
{
    "title":"Superbad",
    "release_date":"08/17/2007"
}
    ```
    - Returns a success value and the newly created object.
    
```
{
    "created": {
        "id": 7,
        "release_date": "Fri, 17 Aug 2007 00:00:00 GMT",
        "title": "Superbad"
    },
    "success": true
}
```

### POST /casting

General:
    
   - Creates a cast stored as an association in the database. The association is created by supplying a JSON object containing an existing movie ID
    and an actor ID.
    
   - Returns a success value and a message stating the name of the actor added to the given movie.
```
{
    "movie_id": 7,
    "actor_id": 2
}
```

Returns:

```
{
    "cast member added": " Jonah Hill added to the Superbad cast.",
    "success": true
}

```

### Heroku testing

To test endpoints non-locally via the Heroku hosted app use the base url:
https://casting-agency.herokuapp.com/