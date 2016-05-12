from django.db import models

class Thing(models.Model):
    name = models.CharField(max_length=500)
    create_datetime = models.DateTimeField(
        auto_now_add=True,
    )
    archived = models.BooleanField(
        default=False,
    )
