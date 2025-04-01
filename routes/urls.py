from django.urls import path
from . import views
from .views import register_view, login_view, logout_view, home, create_route, user_routes, edit_route, remove_point

urlpatterns = [
    path("", home, name="home"),  # ← Ustawia stronę główną
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("my_routes/", user_routes, name="user_routes"),
    path('create_route/', create_route, name='create_route'),
    path('edit_route/<int:route_id>/', edit_route, name='edit_route'),
    path('remove_point/<int:route_id>/<int:point_id>/', views.remove_point, name='remove_point'),
]
