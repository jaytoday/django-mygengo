from django.conf.urls.defaults import *

import settings

#from mygengo-plugin import views

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^$', 'mygengo-plugin.views.index'),
    ('^overview/?$', 'mygengo-plugin.views.overview'),
    ('^order/?$', 'mygengo-plugin.views.order'),
    ('^settings/?$', 'mygengo-plugin.views.post_settings'), 
    ('^preview/(?P<job_id>[A-Za-z0-9]+)/?$', 'mygengo-plugin.views.preview'),
    ('^login/?$', 'mygengo-plugin.views.login'),
    ('^logout/?$', 'mygengo-plugin.views.logout'),
    ('^service_quote/?$', 'mygengo-plugin.views.service_quote'),
    ('^review/(?P<job_id>[A-Za-z0-9]+)/?$', 'mygengo-plugin.views.post_review'),
    ('^comment/(?P<job_id>[A-Za-z0-9]+)/?$', 'mygengo-plugin.views.post_comment'),
    ('^static/(?P<path>.*)/?$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT }), # warning: this is inefficient! Use cloudfront or other CDN
)



