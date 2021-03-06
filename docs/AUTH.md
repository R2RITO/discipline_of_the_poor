# Authentication and permissions

### Authentication

This project uses the standard authentication system provided by django,
along with the simple-jwt library to provide token authentication for users
to access the resources. No personal information is encoded on the token.

To activate it, set the settings variables:

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=150),
    }
    
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ]
    }

### Authorization

The authorization process comes in two stages, resource and object permissions.

##### Resource permissions

For the resource permissions, the normal authentication provided by guardian
is used, which is based on the regular django permission ecosystem as follows:

The table django_content_type holds the model labels for each app, useful to
link the model to a user with permissions

The table auth_permission has, for each content type, the available permissions
created, such as read or delete from a model.

But instead of using the regular auth_user_user_permissions table from django, 
the custom table dotp_users_dotpuser_user_permissions is used. This table is
created from the custom auth model inheriting from GuardianUserMixin, thus
being the one used to check for permissions on resources.

When a user is created, permissions for each model are assigned in the view,
and are generated from budget/models/permission_signals/generate_permissions
function.

##### Object permissions

To check per object permissions, the guardian-rest-framework library is used,
which allows for easy object filtering based on ownership. This is, a check is
performed to see if the user has permissions to view/alter the object.

To perform this check, the table guardian_userobjectpermission is used, in
which the necessary relationship between the object pk, the content type
(which is essentially the model), the user_id and the permission is stored.

To create said relationship, a post_save signal is used, to assign permissions
to each object when it is created.

The function budget/models/permission_signals/owner_permissions checks that the
created model object has an owner attribute, sets it to the current user and
assigns permissions to the owner.


To activate it, set the settings variables:

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
            'discipline_of_the_poor.permissions.CustomObjectPermissions'
        ],
        'DEFAULT_FILTER_BACKENDS': [
            'rest_framework_guardian.filters.ObjectPermissionsFilter',
        ],
    }

    GUARDIAN_RAISE_403 = True
    ANONYMOUS_USER_NAME = None
    GUARDIAN_MONKEY_PATCH = False
    
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'guardian.backends.ObjectPermissionBackend',
    ]

### Object sharing

Since each object has an owner, for some models the suite allows the owner to
assign permissions to another user to grant the ability to view or edit said
object.
