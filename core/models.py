import uuid
from django.db import models


class Core(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    common_fields = ("id", "create_time", "modify_time")

    class Meta:
        abstract = True
