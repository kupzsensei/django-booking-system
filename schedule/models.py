from django.db import models
from room.models import Room
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

# Create your models here.
class Schedule(models.Model):
    room = models.ForeignKey(Room , on_delete=models.CASCADE )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.room} - {self.start_time}/{self.end_time} | {self.user}"
    




    def clean(self):
        validate_schedule = Schedule.objects.filter(
            Q(room=self.room) & (
            (Q(start_time__lte=self.start_time) & Q(end_time__gte=self.start_time)) |
            (Q(start_time__lte=self.end_time) & Q(end_time__gte=self.end_time)) |
            (Q(start_time__gte=self.start_time) & Q(end_time__lte=self.end_time))
        ))


        if validate_schedule:
            print("error catch")
            raise ValidationError("overlapping")
        

        if self.start_time >= self.end_time:
            raise ValidationError("start time cannot be greater than your end time.")
        