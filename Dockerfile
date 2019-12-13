FROM python:3.6-alpine3.8

MAINTAINER fs714 <fs714@163.com>

RUN mkdir -p /root/.pip
ADD ./requirements.txt /home
ADD ./resources/pip.conf /root/.pip/

RUN echo 'http://mirrors.aliyun.com/alpine/v3.8/community/' > /etc/apk/repositories && \
    echo 'http://mirrors.aliyun.com/alpine/v3.8/main/' >> /etc/apk/repositories

RUN apk update && \
    apk add --no-cache make && \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers libffi-dev postgresql-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir setuptools && \
#     pip install --no-cache-dir --no-use-pep517 -r /home/requirements.txt && \
    pip install --no-cache-dir -r /home/requirements.txt && \
    apk --purge del .build-deps && \
    rm -rf /tmp/*

RUN mkdir -p /etc/pymsboot
RUN mkdir -p /var/log/pymsboot

WORKDIR /home/pymsboot

CMD ["/bin/sh"]

