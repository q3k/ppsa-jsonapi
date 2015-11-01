import json

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

    return json.dumps({'status': 'ok', 'data' : data})


if __name__ == '__main__':
    app.run(debug=True)
