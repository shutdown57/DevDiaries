FROM python:3.6-alpine

RUN adduser -D app

WORKDIR /home/app

COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./app app
COPY app/app.py ./

ENV FLASK_APP app.py

RUN chown -R app:app ./
USER app

RUN ls -al

EXPOSE 5001
CMD python app/server.py
