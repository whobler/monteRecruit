from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Events


class EventView(APIView):
    def get(self, request):
        # events = Events.objects.all()
        # return Response({"Events": events})
        pass


# class TicketView(APIView):
#     def get(self, request):
#         pass
