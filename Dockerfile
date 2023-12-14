FROM python:3.11
WORKDIR .
RUN pip install --upgrade pip
COPY ./requirements.txt .
ENV LIBRARY_PATH=/lib:/usr/lib
RUN python3 -m pip install -r requirements.txt --no-cache-dir
COPY . .
