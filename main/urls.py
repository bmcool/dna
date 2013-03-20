from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from mezzanine.core.views import direct_to_template
from main.views import *

admin.autodiscover()

urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    
    url("^$", direct_to_template, {"template": "index.html"}, name="home"),
    
    ("^", include("mezzanine.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler500 = "mezzanine.core.views.server_error"
handler404 = "mezzanine.core.views.page_not_found"
