#-*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _

from dna.models import *

class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    list_filter = ('year', )
    actions = ['to_good', 'to_normal', 'to_bad']
    
    def to_good(self, request, queryset):
        for movie in queryset:
            movie.set_evaluation(request.user, Good)
    to_good.short_description = _('Set good')
    
    def to_normal(self, request, queryset):
        for movie in queryset:
            movie.set_evaluation(request.user, Good)
    to_normal.short_description = _('Set normal')
    
    def to_bad(self, request, queryset):
        for movie in queryset:
            movie.set_evaluation(request.user, Good)
    to_bad.short_description = _('Set bad')

class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'evaluation')
    list_filter = ('movie', 'user', 'evaluation')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Evaluation, EvaluationAdmin)