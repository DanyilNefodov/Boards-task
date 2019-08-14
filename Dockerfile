FROM python:3.6
ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /tmp/requirements.txt
# RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
