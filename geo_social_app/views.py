import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt 

from geo_social_app.models import Person, Note, Activity, Place
from geo_social_app import activities_util

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

    # Create activity in user outbox, need to handle saving to audience inbox
    activity_object = activity['object']
    if activity['type'] == "Create":
        content_type = activity_object['type']
        if content_type == 'Note':
            content = activity['object']['content']
            note = Note(content=content, person=person)
            note.save()
            activity['object']['id'] = note.uris.id 
        elif content_type == 'Place':
            place = Place(name=activity_object['name'], longitude=activity_object['longitude'], latitude=activity_object['latitude'], person=person)
            place.save()
            activity['object']['id'] = place.uris.id

        new_activity_id = activity['object']['id']
        payload = bytes(json.dumps(activity), "utf-8")
        activity = Activity(payload=payload, person=person)
        activity.save()
        return HttpResponseRedirect(new_activity_id)

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
