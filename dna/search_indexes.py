
from haystack import indexes

from dna.models import *
from django.contrib.auth.models import User

class DNAIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    good = indexes.CharField()
    normal = indexes.CharField()
    bad = indexes.CharField()
    
    def prepare_good(self, obj):
        result = ''
        for evaluation in obj.evaluation_set.filter(evaluation=Good):
            result += evaluation.movie.name + '/'
        return result
    
    def prepare_normal(self, obj):
        result = ''
        for evaluation in obj.evaluation_set.filter(evaluation=Normal):
            result += evaluation.movie.name + '/'
        return result
    
    def prepare_bad(self, obj):
        result = ''
        for evaluation in obj.evaluation_set.filter(evaluation=Bad):
            result += evaluation.movie.name + '/'
        return result
    
    def get_model(self):
        return User
