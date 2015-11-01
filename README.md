Poczta Polska JSON API Proxy
============================

Still a better lovestory than SOAP.

Installation
------------

    virtualenv venv
    venv/bin/pip install -r requirements.txt

Deployment
----------

Development:

    virtualenv/bin/python api.py

Production:

    virtualenv/bin/uwsgi -s socket.sock --module api --callable app

Usage
-----

This does only tracking for now, via one endpoint:

    /api/1/parcel/<identifier>.json


