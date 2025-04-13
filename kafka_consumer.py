import json
from kafka import KafkaConsumer
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geo_social.settings")
django.setup()

from geo_social_app.models import Person, Note, Place

KAFKA_BROKERS = ["localhost:9092","localhost:9093", "localhost:9094"]
KAFKA_TOPIC = "test"
KAFKA_GROUP = "activity_group"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    group_id=KAFKA_GROUP,
    bootstrap_servers=KAFKA_BROKERS,
    auto_offset_reset="earliest"
)

def process_message(message):
    try:
        activity = message['activity']
        username = message['username']
        person = Person.objects.get(username=username)

        if activity['type'] == "Create":
            content_type = activity['object']['type']

            if content_type == 'Note':
                note = Note(content=activity['object']['content'], person=person)
                note.save()
            elif content_type == 'Place':
                place = Place(
                    name=activity['object']['name'],
                    longitude=activity['object']['longitude'],
                    latitude=activity['object']['latitude'],
                    person=person
                )
                place.save()
    except Person.DoesNotExist:
        print(f"Person with username {activity['username']} does not exist.")
    except Exception as e:
        print(f"Error processing activity: {str(e)}")

def consume_messages():
    for msg in consumer:
        if msg is None:
            continue

        try:
            message = json.loads(msg.value.decode("utf-8"))
            process_message(message)
        except Exception as e:
            print(f"Error deserializing message: {str(e)}")

if __name__ == "__main__":
    consume_messages()