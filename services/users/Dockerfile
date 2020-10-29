#FROM tiangolo/uwsgi-nginx-flask:python3.8

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
#ENV STATIC_INDEX 1
# ENV STATIC_INDEX 0

# COPY ./app /app
# base image
FROM python:3.7.2-alpine

# set working directory
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
# ENV PATH /usr/src/app:$PATH


# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app

# run server
# CMD python manage.py run -h 0.0.0.0
# CMD flask run --host=0.0.0.0 --port=5000
# CMD sh