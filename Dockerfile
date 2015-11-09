# Copyright (c) 2015 Sergiusz 'q3k' Bazanski
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# the COPYING file for more details.

FROM ubuntu:14.04

RUN set -e -x ;\
	apt-get -y update ;\
	apt-get -y install python-virtualenv python-dev ;\
	useradd -rm service ;\
	mkdir /srv/service

ADD . /srv/service
RUN chown -R service:service /srv/service

USER service
WORKDIR /srv/service

RUN set -e -x ;\
	virtualenv venv ;\
	venv/bin/pip install -r requirements.txt

CMD ["venv/bin/uwsgi", "--http", "0.0.0.0:8080", "--module", "api", "--callable", "app"]
EXPOSE 8080
