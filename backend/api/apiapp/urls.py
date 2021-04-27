from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apiapp import views

urlpatterns = [
    path('attack/',csrf_exempt(views.attack_api.as_view())),
    path('attack-defense/',csrf_exempt(views.attack_defense_api.as_view())),
    path('game-theory/',csrf_exempt(views.game_theory_api.as_view()))
]
