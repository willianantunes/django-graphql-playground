# Django GraphQL Playground

[![Build status](https://vsrm.dev.azure.com/willianantunes/_apis/public/Release/badge/5674f3e0-ef67-4b72-9d1b-1baf81d589c7/1/6)](https://vsrm.dev.azure.com/willianantunes/_apis/public/Release/badge/5674f3e0-ef67-4b72-9d1b-1baf81d589c7/1/6)
[![Maintainability](https://api.codeclimate.com/v1/badges/90f0ed08e9d576f7c602/maintainability)](https://codeclimate.com/github/willianantunes/django-graphql-playground/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/90f0ed08e9d576f7c602/test_coverage)](https://codeclimate.com/github/willianantunes/django-graphql-playground/test_coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

An honest place to play with this fantastic framework with GraphQL with help of [Graphene](https://github.com/graphql-python/graphene).

## Run NOW with Docker

Simply execute:

    docker run -itd --name django-graphql-playground \
    -p 8000:80 \
    willianantunes/django-graphql-playground \
    /bin/bash /app/start.sh

Access on your browser: http://localhost:8000/admin/

See the logs:

    docker logs -f django-graphql-playground

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

    PIPENV_DONT_LOAD_ENV=1 pipenv run pytest --ignore-glob='**/pubsub/**/*.py' 

Useful links:

- https://docs.graphene-python.org/en/latest/testing/#testing-tools
- https://pytest-django.readthedocs.io/en/latest/helpers.html
- https://gist.github.com/JamesMGreene/cdd0ac49f90c987e45ac

## Issues

- [Pipeline for Django fails with: No module named '_sqlite3'](https://developercommunity.visualstudio.com/content/problem/574733/pipeline-for-django-fails-with-no-module-named-sql.html)
- [GitHubInstallationTokenSignatureSecret](https://developercommunity.visualstudio.com/content/problem/564582/githubinstallationtokensignaturesecret-does-not-ex.html)
- [Azure DevOps Output Variable](https://github.com/microsoft/azure-pipelines-agent/blob/master/docs/preview/outputvariable.md)
