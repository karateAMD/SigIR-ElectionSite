from django.contrib import admin

from .models import *

admin.site.register(State)
admin.site.register(Candidate)
admin.site.register(SearchTerm)
admin.site.register(Tweet)
