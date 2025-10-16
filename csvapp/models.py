from django.db import models

# Create your models here.

class UserDetails(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(db_index=True)
    age = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name