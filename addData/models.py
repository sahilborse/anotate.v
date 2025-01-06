from django.db import models
from django.contrib.auth.models import User 

class DataEntry(models.Model):
  
    title:str
    title = models.CharField(max_length=255)  

    def __str__(self) -> str:
        return f"ID: {self.id},  Title: {self.title}"



class Annotation(models.Model):
    title_id = models.IntegerField()  # Assuming `title_id` is an integer representing a unique title
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to the logged-in user
    ANNOTATE_CHOICES = [
        (-1, 'Negative'),
        (0, 'Neutral'),
        (1, 'Positive'),
    ]
    annotate = models.IntegerField(choices=ANNOTATE_CHOICES)

    def __str__(self):
        return f"tittle_id: {self.title_id}, User: {self.user.username}, Annotate: {self.annotate}"