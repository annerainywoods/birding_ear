from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


#the unchanging bird info, like name and bird call
class Bird(models.Model):
    name = models.CharField("common name", max_length=50)
    narration = models.CharField("narrated name", max_length=255)
    bird_call = models.CharField("bird call", max_length=255)
    states = models.ManyToManyField('State', verbose_name="states", blank=True, null=True)
    bird_type = models.ForeignKey('BirdType', verbose_name="type of bird", blank=True, null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Bird, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


#list of U.S. states. Used by Bird and Mix
class State(models.Model):
    name = models.CharField("U.S.State", max_length=3)

    def __unicode__(self):
        return self.name


#list of 22 categories of birds (owls, hawks, etc). Used by Bird and Mix
class BirdType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


#UserBird is created when user registers. It extends Bird.
class UserBird(models.Model):
    BIRD_PILE = (
        ('N', 'New'),
        ('L', 'Learned'),
        ('M', 'Missed')
    )
    bird = models.ForeignKey('Bird', verbose_name="static bird data", blank=False, null=False)
    bird_pile = models.CharField("bird pile", max_length=1, choices=BIRD_PILE, default='N')
    favorite = models.BooleanField("saved as favorite", default=False)
    excluded = models.BooleanField("excluded from drill", default=False)
    user = models.ForeignKey(User)

#the classes are needed for the list of bird links in the mix_detail template
    def html_classes(self):
        bird = self
        if bird.bird_pile == 'L':
            html_classes = "learned"
        else:
            html_classes = "unlearned"
        if bird.favorite:
            html_classes = html_classes + " favorite"
        if bird.excluded:
            html_classes = html_classes + " excluded"
        return html_classes

#the parent mixes are needed for the list of mixes in the bird_detail template
    def parent_mixes(self):
        bird = self
        user = self.user
        parent_mixes = []
        for m in Mix.objects.filter(user=user):
            for b in m.bird_list():
                if b == bird:
                    parent_mixes.append({
                        "nickname": m.nickname,
                        "slug": m.slug,
                        "description": m.description
                    })
        return parent_mixes


    def __unicode__(self):
        return self.user.username + "-" + self.bird.name


#User chooses states and bird types for a mix, program finds matching birds
class Mix(models.Model):
    COLOR = (
        ('OLV', 'Olive'),
        ('YEL', 'Yellow'),
        ('RUS', 'Rust'),
        ('DKB', 'Dark Brown'),
        ('LTB', 'Light Brown'),
        ('DGY', 'Dark Grey'),
        ('TGY', 'Theme Grey')
    )
    nickname = models.CharField("three-letter name", max_length=3)
    description = models.CharField("short description", max_length=255)
    states = models.ManyToManyField('State', blank=True, null=True, verbose_name="state filters")
    bird_types = models.ManyToManyField('BirdType', blank=True, null=True, verbose_name="bird type filters")
    color = models.CharField("color", max_length=3, choices=COLOR, default='OLV')
    user = models.ForeignKey(User)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        super(Mix, self).save(*args, **kwargs)


#returns "learned" birds matching the mix settings
    def num_learned(self):
        mix = self
        user = self.user
        if mix.bird_types.filter(mix__user=user) and mix.states.filter(mix__user=user):
            bird_list = len(UserBird.objects.filter(user=user).filter(bird__bird_type__in=mix.bird_types.all())\
                .filter(bird__states__in=mix.states.all()).distinct().filter(bird_pile__in='L'))
        elif mix.bird_types.filter(mix__user=user):
            bird_list = len(UserBird.objects.filter(user=user).filter(bird__bird_type__in=mix.bird_types.all()).filter(bird_pile__in='L'))
        elif mix.states.filter(mix__user=user):
            bird_list = len(UserBird.objects.filter(user=user).filter(bird__states__in=mix.states.all()).distinct().filter(bird_pile__in='L'))
        else:
            bird_list = len(UserBird.objects.filter(user=user).filter(bird_pile__in='L'))
        return bird_list

#returns all birds matching the mix settings
    def bird_list(self):
        mix = self
        user = self.user
        if mix.bird_types.filter(mix__user=user) and mix.states.filter(mix__user=user):
            bird_list = UserBird.objects.filter(user=user).filter(bird__bird_type__in=mix.bird_types.all())\
                .filter(bird__states__in=mix.states.all()).distinct()
        elif mix.bird_types.filter(mix__user=user):
            bird_list = UserBird.objects.filter(user=user).filter(bird__bird_type__in=mix.bird_types.all())
        elif mix.states.filter(mix__user=user):
            bird_list = UserBird.objects.filter(user=user).filter(bird__states__in=mix.states.all()).distinct()
        else:
            bird_list = UserBird.objects.filter(user=user)
        return bird_list

    def __unicode__(self):
        return self.user.username + "-" + self.nickname


#user settings for drills
class Drill(models.Model):
    FREQUENCY_NEW = (
        (0, 'None'),
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Very high')
    )
    FREQUENCY_MISSED = (
        (0, 'None'),
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Very high')
    )
    FREQUENCY_LEARNED = (
        (0, 'None'),
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Very high')
    )
    BATCH_SIZE = (
        (10, '10'),
        (20, '20'),
        (30, '30'),
        (40, '40'),
        (50, '50'),
    )
    NEXT_BATCH = (
        (60, '60% learned'),
        (70, '70% learned'),
        (80, '80% learned'),
        (90, '90% learned'),
        (100, '100% learned'),
    )
    DRILL_ORDER = (
        ('RAN', 'Random'),
        ('REL', 'Related')
    )
    #turn off the multiple choice option for hands-free use
    listen_only = models.BooleanField("listen only", default=False)
    #set what percentage of drill questions should be new, learned or missed
    frequency_new = models.SmallIntegerField("% new birds", max_length=1, choices=FREQUENCY_NEW, default=3)
    frequency_learned = models.SmallIntegerField("% learned birds", max_length=1, choices=FREQUENCY_LEARNED, default=2)
    frequency_missed = models.SmallIntegerField("% missed birds", max_length=1, choices=FREQUENCY_MISSED, default=5)
    #set how many birds should be drilled on at once
    batch_size = models.SmallIntegerField("number of birds per batch", max_length=3, choices=BATCH_SIZE, default=30)
    #set what percent of "misses" should create a new batch
    next_batch = models.SmallIntegerField("start new batch at", max_length=3, choices=NEXT_BATCH, default=80)
    #turn off the audio for all three answer options, and only hear the bird to identify
    challenge_level = models.BooleanField("skip audio for answer options", default=False)
    #drill on similar birds in the same batch, or randomize batches
    drill_order = models.CharField("drill order", max_length=3, choices=DRILL_ORDER, default="RAN")
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.username


# class Quiz(models.Model):  # needs user
#     NUM_QUESTIONS = (
#         (5, '5'),
#         (10, '10'),
#         (15, '15'),
#         (20, '20')
#     )
#     LEVELS = (
#         (1, 'Rookie Birder'),
#         (2, 'Advanced Birder'),
#         (3, 'Expert Birder')
#     )
#     MESSAGE = (
#         (1, 'Good job! Keep drilling to learn those birds.'),
#         (2, 'Excellent! Very impressive achievement.'),
#         (3, 'Wow! You have developed quite the birding ear.')
#     )
#     mix = models.OneToOneField('Mix', verbose_name="mix for drill")
#     fav_mix = models.OneToOneField('FavMix', verbose_name="fav mix for drill")
#     partial_credit = models.BooleanField("Credit for last word of bird name", default=True)
#     num_questions = models.SmallIntegerField("number of questions", max_length=2, choices=NUM_QUESTIONS, default=10)
#     levels = models.SmallIntegerField("birding level", max_length=1, choices=LEVELS, default=1)
#     message = models.SmallIntegerField("encouraging message", max_length=1, choices=MESSAGE, default=1)
#     user = models.ForeignKey(User)

#    def __unicode__(mix.nickname):
#        return mix.nickname


#  class QuizQuestion(models.Model):  # needs user
