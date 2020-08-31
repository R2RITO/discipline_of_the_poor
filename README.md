# discipline_of_the_poor

# About

This is a showcase project, useful to serve both as a way to show what can I
do, and to have a reference when I want to check how to do something nice that
I did previously

The project is about a budget organizer API, in which a user is able to create
budgets and movements.

A budget is a deposit of funds, destined for something specific, such as rent
budget, food budget, studies budget, savings budget and such.

A movement is a change in a budget's available amount. There are single and
periodic movements. A single movement is applied instantly and a periodic
movement is applied on the specified date, every fixed time cycle such as
daily, weekly, or monthly. A movement can either be an income or an expense,
and should be used to reflect both planned and unexpected changes in the
budget.

# Walkthrough

To serve as both a showcase and a reference guide, this project contains a
folder **docs** which explains some features of interest of this API

# Setup

## Clone
Clone the project

    git clone https://github.com/R2RITO/discipline_of_the_poor.git

## Virtualenv
Use a python 3 virtual environment, for example:

    virtualenv -p python3 venv
    source venv/bin/activate

## Environment variables
Set up the environment variables

    BASE_MEDIA_ROOT
    MEDIA_URL
    SESSION_MEDIA_FOLDER
    DATABASE_NAME
    DATABASE_USER
    DATABASE_PASSWORD
    DATABASE_HOST
    DATABASE_PORT
    ALLOWED_HOSTS
    
Example:

    export BASE_MEDIA_ROOT='/home/fulanito/Projects/dotp_media/'
    export MEDIA_URL='http://10.0.0.207/'
    export SESSION_MEDIA_FOLDER='session_media'
    export DATABASE_NAME='dotp_db'
    export DATABASE_USER='dotp_user'
    export DATABASE_PASSWORD='dotp_user'
    export DATABASE_HOST='localhost'
    export DATABASE_PORT=5432
    export ALLOWED_HOSTS='0.0.0.0'

## Requirements
Install the requirements

    pip install -r requirements/prod.txt

## Database
Create the database according to the credentials provided in the environment
variables.

Run migrations

    python manage.py makemigrations
    python manage.py migrate
    
Run populate

    python manage.py shell
    from prepare_database import populate
    populate()

## Translations
Compile messages

    django-admin compilemessages

## Run 

    python manage.py runserver
