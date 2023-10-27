from django.urls import path
from recipes.views import my_view


urlpatterns = [
    path('', my_view)
]
