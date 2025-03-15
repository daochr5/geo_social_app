import json

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from geo_social_app.models import Person, Note, Activity, uri
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
    if activity['type'] == "Create":
        content = activity['object']['content']
        note = Note(content=content, person=person)
        note.save()

        activity['object']['id'] = note.uris.id 
        payload = bytes(json.dumps(activity), "utf-8")
        activity = Activity(payload=payload, person=person)
        activity.save()
        return HttpResponseRedirect(note.uris.id)

def note_detail(request, username, id):
    note = get_object_or_404(Note, id=id)
    return JsonResponse(activities_util.Note(note).to_json(context=True))
    
def activity_detail(request, username, id):
    activity = get_object_or_404(Activity, id)
    return JsonResponse(activities_util.Activity(activity).to_json(context=True))

def person(request, username):
    person = get_object_or_404(Person, username=username)
    return JsonResponse(activities_util.Person(person).to_json(context=True))
