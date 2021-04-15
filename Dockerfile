FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

COPY app/ /app

EXPOSE 8080