FROM python:3.8-slim-buster

LABEL maintainer "Github@davelil4"

# set working directory in container
RUN mkdir wd
WORKDIR wd

# Copy and install packages
COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

# Copy app folder to app folder in container
COPY . ./

# Changing to non-root user
RUN useradd -m appUser
USER appUser

# Run locally on port 8050
CMD gunicorn --bind 0.0.0.0:8050 app:server