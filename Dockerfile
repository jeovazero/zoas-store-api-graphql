FROM python:3.7.3-alpine

RUN apk add make postgresql-dev gcc musl-dev python3-dev

WORKDIR /zoas-api

COPY ./flaskr /zoas-api/flaskr
COPY ./requeriments.txt /zoas-api
COPY ./Makefile /zoas-api

RUN make _install

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flaskr.app:app"]
