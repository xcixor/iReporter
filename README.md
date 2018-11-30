[![Build Status](https://travis-ci.org/xcixor/iReporter.svg?branch=ft-logout-162185351)](https://travis-ci.org/xcixor/iReporter)
[![Coverage Status](https://coveralls.io/repos/github/xcixor/iReporter/badge.svg?branch=develop)](https://coveralls.io/github/xcixor/iReporter?branch=ft-logout-162185351)
[![Maintainability](https://api.codeclimate.com/v1/badges/b86067db9823606adfed/maintainability)](https://codeclimate.com/github/xcixor/iReporter/maintainability)
## iReporter
iReporter is an a whistle blowing application that enables people to raise concerns about issues that are affecting them to the authorities.
## Preliquisites
- python 3*
- Unix based OS
- Git
- venv
## Setting up app for development
=> This setup assumes you are using a unix based OS
### Step #1
- Create the directory where you want to clone the repository. For this purpose I shall use ireporter
- move into that directory and clone the repository as shown below
- mkdir ireporter
- cd ireporter/
- git clone https://github.com/xcixor/iReporter.git
## Step #2 create a virtual environment and install the requirements
- python3 -m venv ireporter
- source ireporter/bin/activate (to activate virtual env)
- pip install -r requirements.txt (install app dependencies)
## Step #3 set up .env variables
- There are no variable at the moment
## Step #4 start the app
- To start the app run the command below
- - python run.py
## Step 5 Test
- To tes the app run the command below
- - py.test
### Endpoints
|Resource urls                                    | Method     | Description               |
|-------------------------------------------------|------------|---------------------------|
| /api/v1/incident                                |   POST     | Create an Incident        |
| /api/v1/incident                                |   GET      | Get all incidences        |
##### This are enough to get you started
## Contrbuting
My friends at Andela35
## Licenses
None

## Hosting
The app is hosted at [heroku](https://i-reporter.herokuapp.com/)

## Documentation
The documentation can be found [here](https://ireporter.docs.apiary.io/)

The Front end is hosted [here](https://xcixor.github.io/iReporter/)