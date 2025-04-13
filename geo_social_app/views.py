import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt 
from kafka import KafkaProducer
from kafka_consumer import KAFKA_BROKERS, KAFKA_TOPIC

from geo_social_app.models import Person, Note, Activity, Place
from geo_social_app import activities_util

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    linger_ms=50,
    batch_size=32768,
    compression_type='gzip',
    retries=5,
    acks='all',
    # enable_idempotence=True
)

@csrf_exempt
def outbox(request, username):
    person = get_object_or_404(Person, username=username)

    # Fetch all ordered activities pertaining to user
    if request.method == "GET":
        objects = person.activities.order_by('-created_at')
        collection = activities_util.OrderedCollection(objects)
        return JsonResponse(collection.to_json(context=True))

    payload = request.body.decode("utf-8")
    activity = json.loads(payload)

    try:
        message = {'activity': activity, 'username': username}
        producer.send(KAFKA_TOPIC, message)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"status": "queued", "activity": activity}, status=202)

def note_detail(request, username, id):
    note = get_object_or_404(Note, id=id)
    return JsonResponse(activities_util.Note(note).to_json(context=True))

def place_detail(request, username, id):
    place = get_object_or_404(Place, id=id)
    return JsonResponse(activities_util.Place(place).to_json(context=True))
    
def activity_detail(request, username, id):
    activity = get_object_or_404(Activity, id)
    return JsonResponse(activities_util.Activity(activity).to_json(context=True))

def person(request, username):
    person = get_object_or_404(Person, username=username)
    return JsonResponse(activities_util.Person(person).to_json(context=True))
