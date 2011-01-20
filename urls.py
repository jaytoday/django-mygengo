from django.conf.urls.defaults import *
import views
import settings

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^$', 'views.index'),
    ('^overview/?$', 'views.overview'),
    ('^order/?$', 'views.order'),
    ('^settings/?$', 'views.post_settings'), 
    ('^preview/(?P<job_id>[A-Za-z0-9]+)/?$', 'views.preview'),
    ('^login/?$', 'views.login'),
    ('^logout/?$', 'views.logout'),
    ('^service_quote/?$', 'views.service_quote'),
    ('^review/(?P<job_id>[A-Za-z0-9]+)/?$', 'views.post_review'),
    ('^comment/(?P<job_id>[A-Za-z0-9]+)/?$', 'views.post_comment'),
    ('^static/(?P<path>.*)/?$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT }), # warning: this is inefficient! Use cloudfront or other CDN
)



