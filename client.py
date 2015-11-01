import suds.client
import suds.wsse


API_URL = 'https://tt.poczta-polska.pl/Sledzenie/services/Sledzenie?wsdl'
API_PUBLIC_USERNAME = 'sledzeniepp'
API_PUBLIC_PASSWORD = 'PPSA'


class ParcelEvent(object):
    def __init__(self):
        self.time = None
        self.event_type = None
        self.ending = None

    @classmethod
    def from_soap_object(cls, o):
        self = cls()
        self.time = o.czas
        self.event_type = (o.kod, o.nazwa)
        self.ending = o.konczace
        return self

    def __str__(self):
        return "{}: {}{}".format(self.time, self.event_type[1],
                                 " ENDING" if self.ending else "")


class Parcel(object):
    def __init__(self):
        self.events = []

    @classmethod
    def from_soap_object(cls, o):
        self = cls()
        for (_, zdarzenie) in o.danePrzesylki.zdarzenia:
            # thank mr soap
            zdarzenie = zdarzenie[0]
            e = ParcelEvent.from_soap_object(zdarzenie)
            self.events.append(e)
        return self

    def get_status(self):
        """Returns last status received.
        @return: (time, (type, name), ending)
        """
        if self.events == []:
            return (None, None, False)
        e =  self.events[-1]
        return (e.time, e.event_type, e.ending)


class Client(object):
    def __init__(self):
        self.client = None

    def connect(self, username=API_PUBLIC_USERNAME,
                password=API_PUBLIC_PASSWORD):
        security = suds.wsse.Security()
        token = suds.wsse.UsernameToken(username, password)
        security.tokens.append(token)
        client = suds.client.Client(API_URL)
        client.set_options(wsse=security)
        self.client = client

    def get_tracking(self, identifier):
        if self.client is None:
            raise Exception("lol not connected")
        t = self.client.service.sprawdzPrzesylke(identifier)
        p = Parcel.from_soap_object(t)
        return p

