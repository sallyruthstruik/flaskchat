FROM python:3.6

RUN pip install pipenv

COPY Pipfile /app/
COPY Pipfile.lock /app/

WORKDIR /app

RUN pipenv install

COPY ./ /app/

CMD ["pipenv", "run", "uwsgi", "--http", ":5000", "--gevent", "256", "--http-websockets", "--master", "--gevent-monkey-patch", "--wsgi-file", "server.py", "--callable", "application"]
