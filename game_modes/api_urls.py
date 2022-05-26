from django.urls import path

from game_modes import views


urlpatterns = [
    path('all/', views.GameModeView.as_view(),
         name='preference'),
    path('preference/active/', views.PreferenceView.as_view(),
         name='active'),
    path('preference/inactive/', views.InactivePreferenceView.as_view(),
         name='inactive'),
    path('popular/', views.PopularGameModeView.as_view(),
         name='popular'),
]
