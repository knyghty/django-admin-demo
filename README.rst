django-admin-demo
=================

This is just a sample project for demoing / developing the Django Admin.

The main use-cases are:

1. Testing against the admin.
2. Aiding django admin development.
3. Aiding development of django admin customisations.

Running
-------

1. Clone this repo.
2. ``pip install -r requirements.txt``
3. ``./manage.py migrate`` -- may not be necessary.
4. ./manage.py runserver

You can create your own superuser or use the one already existing:

- Username: ``admin``
- Password: ``correcthorsebatterystaple``

There is already a database included with data. If you want to add more data,
there is a manageent command for getting data from the Spotify API:

``./manage.py import_data <artist_id_1> <artist_id_2> ...``

To use this you need to set up a Spotify app on their website and set the
following environment variables:

- ``SPOTIPY_CLIENT_ID``
- ``SPOTIPY_CLIENT_SECRET``

It can take a while and it might be a good idea to fetch only one artist at
a time to avoid rate limits or other issues. Not every album / track will be
downloaded -- just whatever is on the first page of results for each.

The URLs are internationalized, with English as the default language.
This is useful for testing right-to-left styling.
If you want to quickly switch to RTL styling and translations,
change the URL prefix to an RTL language code (e.g., `ar`):

``http://127.0.0.1:8000/ar/admin/``

You can also see the congrats page, also in any language:

``http://localhost:8000/congrats/``

``http://localhost:8000/nl/congrats/``

Deployment
----------

This project is designed to be run locally, but if you do want to deploy,
set the following environment variables to reasonable settings:

- ``DEBUG``
- ``SECRET_KEY``
- ``ALLOWED_HOSTS``

To Do
-----

- Use more of the admin's features.
- Use more of the admin's widgets - as we're only running SQLite there are
  widgets we can't use for Postgres specific fields, but it should be
  possible to fake them.
