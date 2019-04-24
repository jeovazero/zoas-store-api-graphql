FROM python:3.7.3-alpine

RUN apk add make postgresql-dev gcc musl-dev python3-dev

WORKDIR /zoas-api

COPY ./src /zoas-api
COPY ./requeriments.txt /zoas-api
COPY ./Makefile /zoas-api

RUN make _install

RUN pip3.7 install gunicorn

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
