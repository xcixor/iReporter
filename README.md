## iReporter
iReporter is an a whistle blowing application that enables people to raise concerns about issues that are affecting them to the authorities.
## Motivation
Poor services in the private and public sector, increasing national debt and poor leadership have derailed the progress of this country. iReporter provides a platform for citizens to take part in the improvement of this situation.
## Prerequisites
- python 3*
- Unix based OS
- Git
- venv
## Build Status
[![Build Status](https://travis-ci.org/xcixor/iReporter.svg?branch=develop)](https://travis-ci.org/xcixor/iReporter)
## Maintenance
[![Coverage Status](https://coveralls.io/repos/github/xcixor/iReporter/badge.svg?branch=chore-update-readme-162337742)](https://coveralls.io/github/xcixor/iReporter?branch=devlop)
[![Maintainability](https://api.codeclimate.com/v1/badges/b86067db9823606adfed/maintainability)](https://codeclimate.com/github/xcixor/iReporter/maintainability)
## Built with
- Python
- Postgres
- HTML, CSS
- Javascript
## Installation
=> This setup assumes you are using a linux based OS
### Step #1
- Create the directory where you want to clone the repository. For this purpose I shall use ireporter
- move into that directory and clone the repository as shown below
- mkdir ireporter
- cd ireporter/
- git clone https://github.com/xcixor/iReporter.git
### Step #2 create a virtual environment and install the requirements
- python3 -m venv ireporter
- source ireporter/bin/activate (to activate virtual env)
- pip install -r requirements.txt (install app dependencies)
### Step #3 set up .env variables
- There are no variable at the moment
### Step #4 start the app
- To start the app run the command below
- - python run.py
- - Test the endpoints in the next section with Postman
## Testing
- To test the app run the command below
- - py.test --cov=app test/ (to test and give coverage)
- You should see an image like below
![alt Tests image](/repo_images/test.png)
### Endpoints
|Resource urls                                    | Method     | Description               |
|-------------------------------------------------|------------|---------------------------|
| /api/v1/incident                                |   POST     | Create an Incident        |
| /api/v1/incident                                |   GET      | Get all incidences        |
| /api/v1/incident/id                             |   GET      | Get an Incident by Id     |
| /api/v1/incident/id                             |   DELETE   | Delete an incident        |
| /api/v1/incident/id/comments                    |   PATCH    | Edit an incident comment  |
| /api/v1/incident/id/location                    |   PATCH    | Edit an incident location |
| /api/v1/auth/signup                             |   POST     | Signup a user             |
| /api/v1/auth/login                              |   POST     | Login a user              |
| /api/v1/auth/logout                             |   POST     | Sigout a user             |

##### These are enough to get you started

## Contributing
My friends at Andela35
## Licenses
None

## Hosting
The app is hosted at [heroku](https://i-reporter.herokuapp.com/api/v1)

## Documentation
The documentation can be found [here](https://ireporter.docs.apiary.io/)

The Front end is hosted [here](https://xcixor.github.io/iReporter/)

## Owner
This app was built by [pndungu54@gmail.com](https://github.com/xcixor)