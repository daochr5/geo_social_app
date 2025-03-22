import json 

from django.db.models import Model, ForeignKey, CharField, TextField, ManyToManyField, CASCADE, BinaryField, DateField, DecimalField

from django.conf import settings
from django.urls import reverse


def uri(name, *args):
    domain = settings.DOMAIN
    path   = reverse(name, args=args)
    return f"http://{domain}{path}"

class URIs(object):

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

class Person(Model):
    username  = CharField(max_length=100)
    name      = CharField(max_length=100, null=True)
    following = ManyToManyField('self', symmetrical=False, related_name='followers')

    @property
    def uris(self):
        return URIs(
            id=uri("person", self.username),
            # following=uri("following", self.username),
            # followers=uri("followers", self.username),
            outbox=uri("outbox", self.username),
            # inbox=uri("inbox", self.username),
        )

    def to_activitystream(self):
        return {
            "type": "Person",
            "id": self.uris.id,
            "name": self.name,
            "preferredUsername": self.username,
        }

class Note(Model):
    ap_id   = TextField(null=True)
    person  = ForeignKey(Person, related_name='notes', on_delete=CASCADE, db_constraint=True)
    content = CharField(max_length=500)

    @property
    def uris(self):
        ap_id = uri("note_detail", self.person.username, self.id)
        return URIs(id=ap_id)

    def to_activitystream(self):
        uri_id = self.person.uris.id
        return {
            "type": "Note",
            "id": self.uris.id,
            "content": self.content,
            "actor": uri_id,
        }

class Place(Model):
    ap_id   = TextField(null=True)
    person  = ForeignKey(Person, related_name='places', on_delete=CASCADE, db_constraint=True)
    name = CharField(max_length=100, null=True)
    longitude = DecimalField(max_digits=9, decimal_places=6, null=True) 
    latitude = DecimalField(max_digits=9, decimal_places=6, null=True)

    @property
    def uris(self):
        ap_id = uri("place_detail", self.person.username, self.id)
        return URIs(id=ap_id)

    def to_activitystream(self):
        uri_id = self.person.uris.id
        return {
            "type": "Place",
            "id": self.uris.id,
            "name": self.name,
            "longitude": self.longitude,
            "latitude": self.latitude,
        }
    

class Activity(Model):
    ap_id      = TextField()
    payload    = BinaryField()
    created_at = DateField(auto_now_add=True)
    person     = ForeignKey(Person, related_name='activities', on_delete=CASCADE, db_constraint=True)

    @property
    def uris(self):
        ap_id = uri("activity_detail", self.person.username, self.id)
        return URIs(id=ap_id)

    def to_activitystream(self):
        payload = self.payload.decode("utf-8")
        data = json.loads(payload)
        data.update({
            "id": self.uris.id
        })
        return data['object']