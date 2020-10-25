from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_list", views.create, name="create"),
    path("active_list", views.active_list, name="active_list"),
    path("categories", views.categories, name="categories"),
    path("item/<str:name>", views.item, name="item"),
    path("comments", views.comments, name="comments"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.category, name="category"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("showwatchlist",views.showwatchlist,name="showwatchlist"),
    path("removeWatchlist",views.removeWatchlist,name="removeWatchlist"),
    path("close",views.close,name="close"),
    path("bid",views.bid,name="bid"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
