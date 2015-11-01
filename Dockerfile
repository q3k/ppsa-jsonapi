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

CMD ["venv/bin/uwsgi", "--http", "8080", "--module", "api", "--callable", "app"]
EXPOSE 8080
