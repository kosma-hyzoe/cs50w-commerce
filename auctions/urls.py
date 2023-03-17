from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("archive", views.archive, name="archive"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("user/<str:user_id>", views.user_view, name="user"),
    path("categories", views.categories_view, name="categories"),
    path("categories/<str:abbreviation>", views.category_view, name="category"),
    path("<str:listing_id>", views.listing_view, name="listing")
]
