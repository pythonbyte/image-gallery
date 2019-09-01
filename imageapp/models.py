from django.utils import timezone
from djongo import models

class Photo(models.Model):
    approved = models.BooleanField(default=False)
    date_taken = models.DateField(default=timezone.now)
    friends_name = models.CharField(max_length=150, null=False, blank=False)
    image_file = models.ImageField(null=True)
    likes = models.PositiveIntegerField(default=0, null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return f'{self.name} - {self.date_taken}'
