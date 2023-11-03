from django.urls import path


from recipes import views


urlpatterns = [
    path('home/', views.home),
    path("recipes/<int:id>/", views.recipe),
]
