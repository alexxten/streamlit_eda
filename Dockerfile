FROM python:3.11-alpine
# set work directory
WORKDIR .
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN apk add build-base jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
# copy project
COPY . .
