# OpenApi docs

Using drf-yasg an OpenApi 2.0 file can be generated, with some rough edges.
The file needs to be further revised to fix some write only and read only
fields, and then uploaded alongside the project to be used in an OpenApi
reader.

### Library usage

The suite uses the drf-yasg library to generate an OpenApi 2.0 file
automatically, based on the views and serializers. To set it up:

    SWAGGER_SETTINGS = {
        'DEFAULT_INFO': 'discipline_of_the_poor.urls.schema_info',
        'USE_SESSION_AUTH': False,
        'SECURITY_DEFINITIONS': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
        },
        'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg_examples.SwaggerAutoSchema',
    }
    
and then, generate the file using the command given in the main README file.
The file is generated statically (instead of the normal drf-yasg usage which
is to provide a web interface to interact with the service) because some manual
editing needs to be done to further improve the documentation file.

### APIView docs

When a generic APIView is used instead of the regular ModelViewSet, the
definition can be specified as shown in the notify_low_budget_amount_view file

### Swagger file

The gotchas about using drf-yasg are subtle and the ones I know are listed as
follow:
 
##### writeOnly tag
The usage of OpenApi 2.0 prevents the writeOnly tag to be used in 
write only fields, such as the ids of the foreign keys passed on POST requests. 
Thus, the endpoints examples in the file show that for a GET request the id is 
also passed, which is not true. 
This is a small problem that should be fixed when either the library is
upgraded or a manual file for OpenApi 3.0 is used.

##### readOnly tag
The drf-yasg library does not automatically detect read only serializer fields,
such as the ###_object used in this project. For example for the movements,
the MovementSerializer has category as a foreign key, and category_object as
a serializer, useful to receive an id as a POST request, and return a fully
serialized object in the response.
To circumvent this problem, the swagger file should be edited to add

    allOf:
        - readOnly: true
        - $ref: '#/definitions/{{definition}}'
        
where the definition is the used object, such as MovementCategory.