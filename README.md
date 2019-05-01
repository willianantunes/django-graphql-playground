# Django GraphQL Playground

[![Build status](https://dev.azure.com/willianantunes/python/_apis/build/status/Django%20GraphQL%20Playground)](https://dev.azure.com/willianantunes/python/_build/latest?definitionId=1)
[![Maintainability](https://api.codeclimate.com/v1/badges/90f0ed08e9d576f7c602/maintainability)](https://codeclimate.com/github/willianantunes/django-graphql-playground/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/90f0ed08e9d576f7c602/test_coverage)](https://codeclimate.com/github/willianantunes/django-graphql-playground/test_coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

An honest place to play with this fantastic framework with GraphQL with help of [Graphene](https://github.com/graphql-python/graphene).

## Preparing your dev environment

This project uses `pipenv`, so you must have it (see how [here](https://pipenv.readthedocs.io/en/latest/#install-pipenv-today)). [It is the recommended tool to work with dependency management by python.org](https://packaging.python.org/guides/tool-recommendations/).

At the root of project, issue the following command:

    pipenv install --dev --ignore-pipfile

Then do the following commands:

    pipenv run python manage.py makemigrations
    pipenv run python manage.py migrate

Run it:

    pipenv run python manage.py runserver
    
Or if you prefer:

    docker-compose up

## Tests

I did some integration tests to see if [Grafene Testing Tools](https://docs.graphene-python.org/en/latest/testing/#testing-tools) is who he really says he is.

Execute the following to test everything:

    pipenv run pytest 

Useful links:

- https://docs.graphene-python.org/en/latest/testing/#testing-tools
- https://pytest-django.readthedocs.io/en/latest/helpers.html
