from django.conf.urls import url

form . import views

urlpatterns = [
	url(r'^$',views.index,name='index'),
]
