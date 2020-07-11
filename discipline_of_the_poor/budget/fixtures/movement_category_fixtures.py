from budget.models.movement_category import MovementCategory

movement_categories_list = [
    {
        "unique_name": "income",
        "description": "Income movement, adds to the budget",
    },
    {
        "unique_name": "expense",
        "description": "Expense movement, substracts from the budget",
    },
]


def populate(db='default'):

    mv_categories = {}
    for mc_data in movement_categories_list:
        try:
            mv_category = MovementCategory.objects.using(db).get(
                unique_name=mc_data.get('unique_name'))
            for key, value in mc_data.items():
                setattr(mv_category, key, value)

        except MovementCategory.DoesNotExist:
            mv_category = MovementCategory(**mc_data)

        mv_category.save(using=db)
        mv_categories[mv_category.unique_name] = mv_category

    return mv_categories
