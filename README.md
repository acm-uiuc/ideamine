Ideamine
========

Ideamine is a Django powered web application for sharing and launcing ideas
into fully featured projects. Ideamine lets users find ideas they might be
interested in working on or create their own and find other interested people
to help turn their dream into a real project.

##Setup

###Under Django Development Server

Setting up a running instance of Ideamine is easy! Just follow these steps:

1. Checkout the master branch of Ideamine into a local directory
2. Install Django, version 1.2.3 or greater
3. Copy settings.py.example to settings.py.
4. Change the secret key in settings.py to something randomly generated.
5. Update the ADMINS field in settings.py to have the correct administrators.
6. Update the database information in settings.py.
7. Run "./manage.py syncdb" to set up first time run database information.
8. Run "./manage.py runserver PORT" where PORT is the desired port to run on.

