# FROM python:3.7.2-alpine
FROM continuumio/anaconda3 
# publysher/alpine-sklearn

# set working directory
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
# ENV PATH /usr/src/app:$PATH

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app

# run server, elija una de las siguientes 3 opciones
# CMD python manage.py run -h 0.0.0.0
# CMD flask run --host=0.0.0.0 --port=5000
# CMD flask run --host=0.0.0.0