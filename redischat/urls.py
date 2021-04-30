from django.urls import path, include
from . import views

app_name = 'redischat'
urlpatterns = [
	path('', views.page_index, name='index'),
	path('rooms', views.page_room_list, name='room_list'),
	path('new', views.page_room_new, name='room_new'),
	path('create', views.compute_room_create, name='room_create'),
	path('tmp', views.page_tmp, name='tmp'),
	path('rooms/<int:room_id>/', views.page_room, name='room'),
]
