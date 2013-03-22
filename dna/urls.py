from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('dna.views',
    url("^match/", 'match_view', name="match_view"),
)
