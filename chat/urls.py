from django.conf.urls import url
from chat.views import IndexView, loginView, registerView, chat_room
from django.contrib.auth.decorators import login_required
# As of Django 1.10 it is impossible to reference views as: 'django.contrib.auth.views.logout' but is required to call
# them directly.
from django.contrib.auth.views import logout

# Updated for Django 2.0 to fix namespace exception from the inc
app_name='chat'

urlpatterns = [
    # redirect_field_name=None prevents Django from redirecting back to where it was called from.
    url(r'^$', login_required(IndexView.as_view(),redirect_field_name=None), name= 'index'),
    url('^login/$', loginView, name= 'login'),
    url('^register/$', registerView, name= 'register'),
    # The use of builtin logout allows the use of 'next_page' which automatically redirects.
    url(r'^logout/$', logout, name= 'logout', kwargs={'next_page': '/chat/'}),
	# url(r'^logout/$', 'django.contrib.auth.views.logout', name= 'logout', kwargs={'next_page': '/chat/'}),
    url(r'^(?P<user_id>[0-9]+)/$', chat_room, name= 'room'),
]