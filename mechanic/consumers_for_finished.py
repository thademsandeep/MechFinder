import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import helps_finished
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels.generic.websocket import WebsocketConsumer

instances = []

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        global instances

        instances.append(self)

        self.send(json.dumps({'message': helps_finished.get_all_objects(helps_finished)}, sort_keys=True, indent=1, cls=DjangoJSONEncoder))

    def disconnect(self, close_code):

        global instances

        instances.remove(self)

        self.close()


@receiver(post_save, sender=helps_finished)
@receiver(post_delete, sender=helps_finished)
def get_model_objects(sender, **kwargs):
    print(helps_finished.get_all_objects(helps_finished))

    for instance in instances:
        instance.send(json.dumps({'message': helps_finished.get_all_objects(helps_finished)}, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
