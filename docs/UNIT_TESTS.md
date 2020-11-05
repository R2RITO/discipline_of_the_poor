# Unit test docs

The unit tests are created using the django test suite, trying to use as
much as possible from the framework tools available in order to ease the
maintenance, since from experience, the more complicated the tests are,
the less likely future developers are to maintain them. So using easy to
google tools should help in the ease of modifying, running and adding new
tests.

### Fixture creation

The fixtures are created using the commands:

    
    python manage.py dumpdata budget.budget --format=json --indent=4 > budget/tests/fixtures/budget.json
    python manage.py dumpdata budget.movementcategory --format=json --indent=4 > budget/tests/fixtures/movement_category.json
    python manage.py dumpdata budget.periodicmovement --format=json --indent=4 > budget/tests/fixtures/periodic_movement.json
    python manage.py dumpdata budget.movement --format=json --indent=4 > budget/tests/fixtures/movement.json
    python manage.py dumpdata dotp_users.dotpuser --natural-foreign --format=json --indent=4 > budget/tests/fixtures/dotp_user.json