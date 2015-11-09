# Copyright (c) 2015 Sergiusz 'q3k' Bazanski
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import flask

import client


app = flask.Flask(__name__)


@app.route('/api/1/parcel/<identifier>.json')
def api_v1_parcel(identifier):
    c = client.Client()
    c.connect()
    p = c.get_tracking(identifier)
    data = {}
    data['identifier'] = identifier
    data['events'] = []
    for event in p.events:
        e = {}
        e['time'] = event.time
        e['code'] = event.event_type[0]
        e['name'] = event.event_type[1]
        e['ending'] = event.ending
        data['events'].append(e)
    if data['events']:
        data['last'] = data['events'][-1]

    return flask.jsonify(status='ok', data=data)


if __name__ == '__main__':
    app.run(debug=True)
