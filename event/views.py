from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from event.models import Event
from event.serializers import EventSerializer


def health(request):
    return HttpResponse("Health Api")


class EventView(APIView):

    def post(self, request):
        serializer_class = EventSerializer(data={
            "type": request.data.get("type"),
            "public": request.data.get("public"),
            "repo_id": request.data.get("repo_id"),
            "actor_id": request.data.get("actor_id"),
        })
        if not serializer_class.is_valid():
            data = {"message": "Data is invalid"}
            return Response(data=data, status=HTTP_400_BAD_REQUEST)
        type_data = request.data.get("type")

        if type_data not in ('PushEvent', 'ReleaseEvent', 'WatchEvent'):
            data = {"message": "Topic is invalid"}
            return Response(data=data, status=HTTP_400_BAD_REQUEST)
        serializer_class.save()
        return Response(serializer_class.data, status=HTTP_201_CREATED)

    def get(self, request):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


@api_view(('GET',))
def get_event_by_repo_id(self, repo_id):
    event = Event.objects.filter(repo_id=repo_id)
    serializer = EventSerializer(event, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(('GET',))
def get_event_by_user_id(self, user_id):
    event = Event.objects.filter(actor_id=user_id)
    serializer = EventSerializer(event, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(('GET',))
def get_event_by_event_id(self, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        serializer = EventSerializer(event, many=False)
        return Response(serializer.data, status=HTTP_200_OK)
    except ObjectDoesNotExist:
        data = {"message": "Event id not exist"}
        return Response(data=data, status=HTTP_400_BAD_REQUEST)
