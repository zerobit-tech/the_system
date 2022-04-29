the_system
===============

This app can be installed and used in your django project by:

.. code-block:: bash

    $ pip install realpython-django-receipts


Edit your `settings.py` file to include `'the_system'` in the `INSTALLED_APPS`
listing.

.. code-block:: python

    INSTALLED_APPS = [
        ...

        'the_system',
    ]



    MIDDLEWARE = [
        ...
        'the_system.middleware.TheSystemMiddleware',
        'the_system.middleware.CurrentUserMiddleware',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',

                    ...

                    'the_system.context_processor.SystemConfigContextProcessor',  ## <<<
                    
                    ...

                    'django.template.context_processors.static',
                
                ],
            },
        },
    ]

    REST_FRAMEWORK = {
    ...
    'EXCEPTION_HANDLER': 'the_system.drf_utils.exception_handler',
    ...
    }


Edit your project `urls.py` file to import the URLs:


.. code-block:: python

    url_patterns = [
        ...

        path('system/', include('the_system.urls')),
    ]


Finally, add the models to your database:


.. code-block:: bash

    $ ./manage.py makemigrations the_system


The "project" Branch
--------------------

The `master branch <https://github.com/realpython/django-receipts/tree/master>`_ contains the final code for the PyPI package. There is also a `project branch <https://github.com/realpython/django-receipts/tree/project>`_ which shows the "before" case -- the Django project before the app has been removed.


 