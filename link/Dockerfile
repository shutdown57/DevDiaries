FROM python:3.6-alpine

RUN adduser -D link

WORKDIR /home/link

COPY link/requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./link link
COPY link/app.py ./

ENV FLASK_APP app.py

RUN chown -R link:link ./
USER link

EXPOSE 5000
CMD python link/server.py
