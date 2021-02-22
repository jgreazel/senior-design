from django.urls import path

from apiapp import views

urlpatterns = [
    path('hello-view/',views.post_json)
]
