from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apiapp import views

urlpatterns = [
    path('hello-view/',csrf_exempt(views.api_views.as_view()))
]
