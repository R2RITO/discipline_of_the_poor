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
    BUDGET_MEDIA_FOLDER
    ALLOWED_HOSTS
    
    DEFAULT_DATABASE_NAME
    DEFAULT_DATABASE_USER
    DEFAULT_DATABASE_PASSWORD
    DEFAULT_DATABASE_HOST
    DEFAULT_DATABASE_PORT
    
    REGULAR_DATABASE_NAME
    REGULAR_DATABASE_USER
    REGULAR_DATABASE_PASSWORD
    REGULAR_DATABASE_HOST
    REGULAR_DATABASE_PORT
    
    PREMIUM_DATABASE_NAME
    PREMIUM_DATABASE_USER
    PREMIUM_DATABASE_PASSWORD
    PREMIUM_DATABASE_HOST
    PREMIUM_DATABASE_PORT
    
    
Example:

    export BASE_MEDIA_ROOT='/home/fulanito/Projects/dotp_media/'
    export MEDIA_URL='http://10.0.0.207/'
    export BUDGET_MEDIA_FOLDER='budget_media'
    export ALLOWED_HOSTS='0.0.0.0,127.0.0.1'
    
    export DEFAULT_DATABASE_NAME='dotp_db'
    export DEFAULT_DATABASE_USER='dotp_user'
    export DEFAULT_DATABASE_PASSWORD='dotp_user'
    export DEFAULT_DATABASE_HOST='localhost'
    export DEFAULT_DATABASE_PORT=5432
    
    export REGULAR_DATABASE_NAME='regular_dotp_db'
    export REGULAR_DATABASE_USER='regular_dotp_user'
    export REGULAR_DATABASE_PASSWORD='regular_dotp_user'
    export REGULAR_DATABASE_HOST='localhost'
    export REGULAR_DATABASE_PORT=5432
    
    export PREMIUM_DATABASE_NAME='premium_dotp_db'
    export PREMIUM_DATABASE_USER='premium_dotp_user'
    export PREMIUM_DATABASE_PASSWORD='premium_dotp_user'
    export PREMIUM_DATABASE_HOST='localhost'
    export PREMIUM_DATABASE_PORT=5432

## Requirements
Install the requirements

    pip install -r requirements/prod.txt

## Database
Create the databases according to the credentials provided in the environment
variables.

Run migrations

    python manage.py makemigrations
    python manage.py migrate
    
Run populate, substitute DB_USED for the database name to populate

    python manage.py shell
    from prepare_database import populate
    populate(db='DB_USED')

## Translations
Compile messages

    django-admin compilemessages

## Run 

    python manage.py runserver

## Translation note

    Some translations are not directly placed inside the source files, they
    are rather a translation of labels stores in the database, therefore the
    command django-admin makemessages updates the file with comments on those
    lines. They should be uncommented before commiting translation changes

## Documentation

    The folder openapi contains a swagger.yml file, following the OpenApi 2.0
    specification, that documents the endpoints exposed in this project. To
    use it, the file should be loaded into an OpenApi visualizer such as the
    one provided in https://editor.swagger.io/ in order to explore the
    services.
    
    When an endpoint is updated, the file should be re-generated using the
    command
    
    python manage.py generate_swagger swagger.yaml
    
    And then, moved to the openapi folder, this will allow for the version control
    to display the changes and allow for editing unwanted changes
    
    As additional notes, the examples are defined in the serializers of each
    resource, and some of them require the readOnly: true attribute to be set
    manually after generating the file.
    
## Obfuscation

    The file cython_setup.py has the required setup to compile most of the
    source files into .so files, useful to deploy on a server where the code
    is going to be used but should not be available for inspection.
    
    To compile the project, run the command:
    
    python cython_setup.py build_ext
    
    This will create a folder called build, inside of which the compiled
    project will be located, then, the required files can be moved to the
    desired project location and the project can be run as normal with the
    compiled files.
    
    When a new directory, or file that requires special attention is created,
    the cython_setup.py file should be updated to include it in the compiled
    sources.