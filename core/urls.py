from django.urls import path
from . import views
urlpatterns = [path('top-artists/', views.get_top_artists, name='top-artists')]