from django.urls import path
from . import views

app_name = "boulders"
urlpatterns = [
    path("api/lights/", views.proxy_lights, name="proxy_lights"),
    # Boulder URLs
    path("", views.IndexView.as_view(), name="index"),
    path("new/", views.NewBoulderView.as_view(), name="new_boulder_view"),
    path("<int:pk>/", views.BoulderView.as_view(), name="boulder_view"),
    path("<int:pk>/edit/", views.EditBoulderView.as_view(), name="edit_boulder_view"),
    path("<int:pk>/logascent/", views.LogBoulderAscentView.as_view(), name="log_boulder_ascent"),

    # Circuit URLs
    path("circuits/", views.CircuitListView.as_view(), name="circuit_list"),
    path("circuits/new/", views.NewCircuitView.as_view(), name="new_circuit"),
    path("circuits/<int:pk>/", views.CircuitView.as_view(), name="circuit_view"),
    path("circuits/<int:pk>/edit/", views.EditCircuitView.as_view(), name="edit_circuit"),

    # Log in / out 
    path("login/", views.BouldersLoginView.as_view(), name='login'),
    path("logout/", views.BouldersLogoutView.as_view(), name='logout'),
    path("register/", views.BouldersRegisterView.as_view(), name='register')
    ]
