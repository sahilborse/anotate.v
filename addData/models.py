from django.db import models
from django.contrib.auth.models import User

class DataEntry(models.Model):
    title = models.CharField(max_length=255)  

    def __str__(self) -> str:
        return f"ID: {self.id}, Title: {self.title}"


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
        return f"title_id: {self.title_id}, User: {self.user.username}, Annotate: {self.annotate}"
    
# class SelectedText(models.Model):
#     title_id = models.IntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     selected_text=models.CharField(max_length=255)

#     def __str__(self):
#         return  f"title_id: {self.title_id}, User: {self.user.username}, HighlightedText: {self.selected_text}"
    

class HighlightedText(models.Model):
    title_id = models.IntegerField()  # Store only the title ID instead of a ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title_id: {self.title_id}, User: {self.user.username}, Selected_Text: {self.text[:30]}"
