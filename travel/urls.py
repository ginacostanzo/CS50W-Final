from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("plan", views.plan, name="plan"),
    path("trip/<int:trip_id>", views.trip_view, name="trip_view"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("tag/<str:tag_name>", views.tags, name="tags"),
    path("browse", views.browse, name="browse"),
    path("random_trip", views.random_trip, name="random_trip"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("lists_view/<str:list_name>", views.lists_view, name="lists_view"),
    path("search", views.search, name="search"),
    path("addToList", views.addToList, name="addToList"),
    path("removeFromList/<str:list_name>/<int:trip_id>", views.removeFromList, name="removeFromList"),
    path("captions", views.captions, name="captions"),
    path("edit_trip/<int:trip_id>", views.edit_trip, name="edit_trip"),

    # API Routes
    path("all_been", views.all_been, name="all_been")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)