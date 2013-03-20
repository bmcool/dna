#-*- encoding: utf-8 -*-

from django.contrib import admin

from dna.models import *

class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    list_filter = ('year', )

class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'evaluation')
    list_filter = ('movie', 'user', 'evaluation')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Evaluation, EvaluationAdmin)