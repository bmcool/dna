#-*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.models import User

Bad = -10
Normal = 0
Good = 10

EVALUATION_TYPE_CHOICES = (
    (Bad, _('Bad')),
    (Normal, _('Normal')),
    (Good, _('Good')),
)

class Movie(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    year = models.IntegerField(_('Year'))
    
    def set_evaluation(self, user, evaluation):
        instance, new = Evaluation.objects.get_or_create(movie=self, user=user, evaluation=evaluation)
        instance.evaluation = evaluation
        instance.save()
    
    def __unicode__(self):
        return self.name

class Evaluation(models.Model):
    evaluation = models.IntegerField(_("Evaluation"), default=Normal, choices=EVALUATION_TYPE_CHOICES)
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)
    
    class Meta:
        unique_together = ('user', 'movie')
