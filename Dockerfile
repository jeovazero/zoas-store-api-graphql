FROM python:3.7.3-alpine as pyimage

FROM pyimage as build

RUN apk add --virtual build-dependencies make postgresql-dev gcc musl-dev python3-dev \
        && apk add libpq

FROM build as deps

WORKDIR /packages

COPY ./requirements.txt .

RUN pip3.7 install -r requirements.txt --prefix=/packages --no-warn-script-location


FROM pyimage

COPY --from=deps /packages /usr/local
COPY --from=deps /usr/lib/ /usr/lib/

WORKDIR /zoas-api

COPY ./flaskr /zoas-api/flaskr
COPY ./Makefile /zoas-api/Makefile

RUN apk add make

EXPOSE 5000

CMD ["make", "run_gunicorn"]
