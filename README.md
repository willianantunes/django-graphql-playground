# Django GraphQL Playground

[![Build Status](https://travis-ci.org/willianantunes/django-graphql-playground.svg?branch=master)](https://travis-ci.org/willianantunes/django-graphql-playground)
[![Maintainability](https://api.codeclimate.com/v1/badges/90f0ed08e9d576f7c602/maintainability)](https://codeclimate.com/github/willianantunes/django-graphql-playground/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/90f0ed08e9d576f7c602/test_coverage)](https://codeclimate.com/github/willianantunes/django-graphql-playground/test_coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

---

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
