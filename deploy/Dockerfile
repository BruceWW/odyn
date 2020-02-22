FROM python:3.7.5

MAINTAINER Lin Luo / Bruce Liu

##############
# set env
##############
# pip env
ENV PIP_NO_CACHE_DIR=off
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple

# apt install
RUN apt-get update
RUN apt-get install -y tcl8.6-dev tk8.6-dev python-tk default-libmysqlclient-dev vim

WORKDIR /opt/www/odyn

# pip install
RUN pip install pipenv

COPY odyn odyn

RUN pipenv install

EXPOSE 80

CMD mkdir -p /var/logs/$HOSTNAME \
RUN pipenv shell
RUN python manage.py migrate --noinput \
RUN uwsgi deploy/uwsgi/crowd_insights_service.ini
