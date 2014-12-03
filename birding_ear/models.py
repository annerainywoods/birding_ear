from django.db import models


class Bird(models.Model):
    name = models.CharField(max_length=50)
    narration = models.CharField(max_length=255)
    bird_call = models.CharField(max_length=255)
    state = models.ManyToManyField('State')
    bird_type = models.ForeignKey('Bird_type')
    excluded = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    bird_pile = models.ForeignKey('Bird_pile', blank=True, null=True)

    def __unicode__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=2)

    def __unicode__(self):
        return self.name

class Bird_type(models.Model):
    name = models.CharField(max_length=100, default='All')

    def __unicode__(self):
        return self.name

class Bird_pile(models.Model):
    name = models.CharField(max_length=10, default='unplayed')

    def __unicode__(self):
        return self.name

class Mix(models.Model):
    nickname = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    state = models.ManyToManyField('State')
    bird_type = models.ManyToManyField('Bird_type')
    color = models.ForeignKey('Color', blank=True, null=True)

    def __unicode__(self):
        return self.nickname

#There is a special mix for Favorites. It has a nickname and a description that are constants.

class Color(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Drill(models.Model):
    listen_only = models.BooleanField(default=False) #this form control is at the level of the question, so this setting can change while drill is in progress
    frequency_unplayed = models.ForeignKey('Frequency', to_field='unplayed', related_name='+', blank=True, null=True)
    frequency_learned = models.ForeignKey('Frequency', to_field='learned', related_name='+', blank=True, null=True)
    frequency_missed = models.ForeignKey('Frequency', to_field='missed', related_name='+', blank=True, null=True)
    batch = models.ForeignKey('Batch', to_field='quantity', related_name='+', blank=True, null=True)
    percent_learned = models.ForeignKey('Batch', to_field='percent_learned', related_name='+', blank=True, null=True)
    bird_name_withheld = models.BooleanField(default=False)
    related_birds = models.BooleanField(default=False)
    mix = models.ForeignKey(Mix, to_field='id')

    def __unicode__(self):
        return self.mix

class Frequency(models.Model):
    unplayed = models.CharField(max_length=9, default='Medium', unique=True)
    learned = models.CharField(max_length=9, default='Very Low', unique=True)
    missed = models.CharField(max_length=9, default='High', unique=True)

    def __unicode__(self):
        return self.unplayed

class Batch(models.Model):
    quantity = models.SmallIntegerField(max_length=2, default=30, unique=True)
    percent_learned = models.SmallIntegerField(max_length=2, default=80, unique=True)#Does this have to be exactly what is in the form? Form will say 80% learned

    def __unicode__(self):
        return self.batch