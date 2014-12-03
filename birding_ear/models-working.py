from django.db import models


class Bird(models.Model):
    name = models.CharField(max_length=50)
    narration = models.CharField(max_length=255)
    bird_call = models.CharField(max_length=255)
    state = models.ManyToManyField('State')
    bird_type = models.ForeignKey('Bird_type')
    excluded = models.BooleanField(default=False)
    played = models.BooleanField(default=False)
    learned = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=2)

    def __unicode__(self):
        return self.name


class Bird_type(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name