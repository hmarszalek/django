from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, RouteForm, RoutePointForm
from .models import BackgroundImage, Route, RoutePoint

def home(request):
    return render(request, "routes/home.html")

def register_view(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "routes/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "routes/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def create_route(request):
    if request.method == 'POST':
        background_id = request.POST.get("background")
        background = BackgroundImage.objects.get(id=background_id)
        route_name = request.POST.get("name")
        route = Route.objects.create(user=request.user, name=route_name, background=background)
        return redirect("edit_route", route.id)
    backgrounds = BackgroundImage.objects.all()
    return render(request, "routes/create_route.html", {"backgrounds": backgrounds})

@login_required
def edit_route(request, route_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    points = route.points.all()  # Pobierz wszystkie punkty trasy
    if request.method == 'POST':
        form = RoutePointForm(request.POST)
        if form.is_valid():
            point = form.save(commit=False)
            point.route = route
            point.save()
            return redirect("edit_route", route_id=route.id)
    else:
        form = RoutePointForm()
    return render(request, "routes/edit_route.html", {"route": route, "points": points, "form": form})

@login_required
def remove_point(request, route_id, point_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    point = get_object_or_404(RoutePoint, id=point_id, route=route)
    point.delete()
    return redirect('edit_route', route_id=route.id)

def user_routes(request):
    routes = Route.objects.filter(user=request.user)
    return render(request, "routes/user_routes.html", {"routes": routes})