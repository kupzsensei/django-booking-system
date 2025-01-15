from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Schedule
from .serializers import ScheduleSerializer , SchedulePostSerializer

from django.db.models import Q
from django.core.exceptions import ValidationError

# Create your views here.

class ScheduleView(APIView):

    def validate_schedule(self , data):
        validate_schedule = Schedule.objects.filter(
            Q(room=data['room']) & (
            (Q(start_time__lte=data['start_time']) & Q(end_time__gte=data['start_time'])) |
            (Q(start_time__lte=data['end_time']) & Q(end_time__gte=data['end_time'])) |
            (Q(start_time__gte=data['start_time']) & Q(end_time__lte=data['end_time']))
        ))
        return validate_schedule

    def get(self, request):
        data = Schedule.objects.all().order_by('-id')
        serializer = ScheduleSerializer(data , many=True)
        return Response({"ok": True , "data": serializer.data})
        
    def post(self, request):
        data = request.data
        
        if self.validate_schedule(data):
            return Response({"ok": False , "errors": "Overlapping timeline" })
         
        if data['start_time'] >= data['end_time']:
            return Response("start time cannot be greater than your end time.")
        
        serializer = SchedulePostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"ok": True , "data": serializer.data})
        return Response({"ok": False , "errors": serializer.errors})
        
    def patch(self, request):
        pass
        
    def delete(self, request):
        pass
        

