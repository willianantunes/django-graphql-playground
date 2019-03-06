# Django GraphQL Playground

An honest place to play with this fantastic framework with GraphQL with help of [Graphene](https://github.com/graphql-python/graphene).

## Running it

If you're new to Python, do not forget to create your virtual environment:

    python -m venv .venv
    
Switch to the context and install all the dependencies needed:

    source .venv/bin/activate
    pip install -r requirements_dev.txt

Then do the following commands:

    python manage.py makemigrations
    python manage.py migrate

Run it:

    python manage.py runserver

## Tests

I did some integration tests to see if [Grafene Testing Tools](https://docs.graphene-python.org/en/latest/testing/#testing-tools) is who he really says he is.

Execute the following to test everything:

    python -m pytest 

Useful links:

- https://docs.graphene-python.org/en/latest/testing/#testing-tools
- https://pytest-django.readthedocs.io/en/latest/helpers.html
