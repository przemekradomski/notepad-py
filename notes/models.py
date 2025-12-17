from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
        verbose_name = 'Timestamped Model'
        verbose_name_plural = 'Timestamped Models'


class TitleNote(TimestampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class ContentNote(TimestampedModel):
    content = models.TextField()

    def __str__(self):
        return self.content[:50]


class DataNote(TimestampedModel):
    data = models.JSONField()

    def __str__(self):
        return str(self.data)
