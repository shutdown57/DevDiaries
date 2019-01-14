FROM python:3.6-alpine

RUN adduser -D link

WORKDIR /home/link

COPY link/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./link .
COPY link/manage.py .

ENV FLASK_APP manage.py

RUN chown -R link:link .
RUN chmod +x ./presetup.sh
USER link

EXPOSE 5000
CMD ./presetup.sh
