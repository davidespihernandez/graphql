from enum import Enum

from django.db import models


class Status(Enum):
    OPEN = 0
    CLOSED = 1


class Master(models.Model):
    name = models.CharField(max_length=255)
    status = models.IntegerField(
        choices=[(c.value, c.name) for c in Status],
        default=Status.OPEN,
    )
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.name


class Detail(models.Model):
    master = models.ForeignKey(
        to=Master,
        related_name="details",
        on_delete=models.deletion.CASCADE,
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.name
