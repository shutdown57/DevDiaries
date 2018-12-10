FROM python:3.6-alpine

RUN adduser -D link

WORKDIR /home/link

COPY link/requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./link link
COPY link/manage.py ./link

ENV FLASK_APP manage.py

RUN chown -R link:link ./
USER link

# CMD sh link/presetup.sh
# CMD python link/manage.py db init
# CMD python link/manage.py init_db
# CMD python link/manage.py db upgrade
# CMD python link/manage.py set_env

EXPOSE 5000
CMD python link/server.py
