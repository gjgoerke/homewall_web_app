from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('ascents/', views.UserAscentListView.as_view(), name='ascents'),
]