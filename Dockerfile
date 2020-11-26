FROM python:3.7.3-slim-stretch

# In order to have OUTPUT from Heroku
RUN apt-get update && apt-get install curl -y

RUN groupadd --system app-user && adduser --system --ingroup app-user app-user

WORKDIR /app

RUN chown app-user:app-user /app

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir --upgrade pip pipenv

RUN pipenv install --system --deploy --ignore-pipfile && \
    pip uninstall --yes pipenv

USER app-user

COPY --chown=app-user:app-user . /app

RUN rm Pipfile Pipfile.lock

CMD gunicorn -cfile:gunicorn_config.ini -b 0.0.0.0:${PORT} django_graphql_playground.wsgi
