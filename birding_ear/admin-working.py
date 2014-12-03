from django.contrib import admin
from .models import Bird, State, Bird_type

admin.site.register(Bird)
admin.site.register(State)
admin.site.register(Bird_type)
