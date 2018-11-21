from django.db import models

from apps.common.models import TimeStampedModel


class Sequence(TimeStampedModel):

    code = models.CharField('Code', max_length=100, unique=True)
    value = models.PositiveIntegerField('Value', default=0)

    class Meta:
        ordering = ('code',)

    def __unicode__(self):
        return '{}: {}'.format(self.code, self.value)

    @classmethod
    def get_next_value(cls, code):
        sequence, created = cls.objects.get_or_create(code=code.lower())
        sequence.value += 1
        sequence.save()
        return sequence.value
