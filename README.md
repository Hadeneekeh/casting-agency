# Casting Agency
##### Udacity Full stack Nanodegree Capstone Project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## API URL 
- **Heroku:** [base URL](https://fsnd-casting-capstone.herokuapp.com/)
- **Localhost:** base URL is localhost:5000


## Features
- Create and manage ators as well as movies

## Authentication and Authorisation
Authentication is implemented in the form of Role Based Access Control using Auth0
#### Roles
- Executive Producer
- Casting Director
- Casting Assistance

[Login](https://casting-auth.auth0.com/authorize?audience=casting&response_type=token&client_id=ZxcJivQqX87uY1D9yfGha68zdJ2tN0Od&redirect_uri=https://127.0.0.1:8080/login-result) using the credentials provided for each roles.

## Technologies and Services used
- Python
- Flask
- Flask-CORS
- Flask-Migrate
- Unittest
- SQLAlchemy
- Autopep8
- Auth0
- PostgreSQL

## Installation and Database Setup
Clone the repo by running 

```bash
git clone https://github.com/Hadeneekeh/casting-agency.git
```
### Dependencies
#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the ptoject directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Environmental Variables
Follow the **.env-sample** to create a .env file for your local setup

### Database Setup
- Create two databases for **testing** and **development**
- Generate database tables from the migration files included by executing: 
  `python manage.py db upgrade`
- Add dummy data by executing:
  `python manage.py seed`
  
## Running the Server
From within the project directory first ensure you are working using your created virtual environment.

- To run the **development** server, execute:
`bash setup.sh` then 
`flask run`
- To run the **test**, add fresh token for each of the roles specified above under roles. Then execute:
`bash testing.sh` 

***Note** Remember to stop the development server before running the test

## Endpoints
```
# Movies

GET '/movies'
POST '/movies'
PATCH '/movies/<id>'
DELETE '/movies/<id>'

GET '/movies'
- Fetches all movies on the platform
- Request Arguments: None
- Allowed users: Executive Producer, Casting Assistant and casting Director
- Required permission (get:movies)
- Response
{
  "movies": [
    {
      "id": 3,
      "release_date": "Thu, 23 Jun 2005 00:00:00 GMT",
      "title": "A fall from Grace"
    },
    {
      "id": 1,
      "release_date": "Thu, 28 Jun 2000 00:00:00 GMT",
      "title": "Jumanji"
    }
  ],
  "success": True
}

POST '/movies'
- Creates a new movie with the provided parameters
- Request Arguments: None
- Allowed users: Executive Producer
- Required permission (add:movies)
- Request Body: {
	"title": "Slap of the Century"
	"release_date": "2/26/1996"
}

- Response
{
  "movie": {
    "id": 4,
    "release_date": "Mon, 26 Feb 1996 00:00:00 GMT",
    "title": "Slap of the Century"
  },
  "success": true
}


PATCH '/movies/<id>'
- Updates a specific movie with the provided parameters
- Request Arguments: movie_id (The ID of the movie to update)
- Allowed users: Executive Producer, Casting Director
- Required permission (edit:movies)
- Request Body: {
	"title": "Silicon Valley"
}

- Response
{
  "movie": {
    "id": 4,
    "release_date": "Thu, 26 Feb 2004 00:00:00 GMT",
    "title": "Silicon Valley"
  },
  "success": true
}

DELETE '/movies/<id>'
- Deletes a specific movie
- Request Arguments: movie_id (The ID of the movie to delete)
- Allowed users: Executive Producer
- Required permission (delete:movie)
- Response
{
  "delete": id,
  "success": true
}



# Actors

GET '/actors'
POST '/actors'
PATCH '/actors/<id>'
DELETE '/actors/<id>'

GET '/actors'
- Fetches all actors on the platform
- Request Arguments: None
- Allowed users: Executive Producer, Casting Assistant and casting Director
- Required permission (get:actors)
- Response
{
  "actors": [
    {
      "age": 25,
      "gender": "male",
      "id": 3,
      "name": "Kevin Hart"
    },
    {
      "age": 20,
      "gender": "male",
      "id": 1,
      "name": "Desmond Elliot"
    }
  ],
  "success": true
}

POST '/actors'
- Creates a new actor with the provided parameters
- Request Arguments: None
- Allowed users: Executive Producer and casting Director
- Required permission (add:actors)
- Request Body: {
	"name": "Kunle Afolayan",
	"age": 20,
	"gender": "male"
}

- Response
{
  "actor": {
    "age": 20,
    "gender": "female",
    "id": 4,
    "name": "Kunle Afolayan"
  },
  "success": true
}


PATCH '/actors/<id>'
- Updates a specific actor with the provided parameters
- Request Arguments: actor_id (The ID of the actor to update)
- Allowed users: Executive Producer and Casting Director
- Required permission (edit:actor)
- Request Body: {
	"name": "RMD",
}

- Response
{
  "actor": {
    "age": 28,
    "gender": "female",
    "id": 4,
    "name": "RMD"
  },
  "success": true
}

DELETE '/actors/<id>'
- Deletes a specific actor
- Request Arguments: actor_id (The ID of the actor to delete)
- Required permission (delete:actors)
- Response
{
  "delete": id,
  "success": true
}

Errors 
For errors, the server returns a json object with a description of the type of error. Find the description below:

400 (Bad Request)
  {
    "success": False, 
    "error": 400,
    "message": "bad request, please check your input"
  }

401 (Unauthorised)
  {
    "success": False, 
    "error": 401,
    "message": "authorisation error"
  }

403 (Forbiddden request)
  {
    "success": False, 
    "error": 403,
    "message": "You are not allowed to access this resource"
  }

404 (Resource Not Found)
  {
    "success": False, 
    "error": 404,
    "message": "resource not found"
  }

405 (Method not allowed)
  {
    "success": False, 
    "error": 405,
    "message": "Method not allowed"
  }

422 (Unprocessable entity)
  {
    "success": False, 
    "error": 422,
    "message": "unprocessable"
  }

500 (Internal server error)
  {
    "success": False, 
    "error": 500,
    "message": "Server error
  }
```