from budget.fixtures import movement_category_fixtures


def populate(db='default'):
    mv_categories_data = movement_category_fixtures.populate(db)
