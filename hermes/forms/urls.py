from django.urls import path

from . import views

urlpatterns = [
    # Site
    path("", views.SiteListView.as_view(), name="site-list"),
    path("create/", views.SiteCreateView.as_view(), name="site-create"),
    path("<int:pk>/", views.SiteUpdateView.as_view(), name="site-update"),
    path("<int:pk>/delete/", views.SiteDeleteView.as_view(), name="site-delete"),
    # Forms
    path("forms/create/", views.FormCreateView.as_view(), name="form-create"),
    path("<int:site_pk>/forms/", views.FormListView.as_view(), name="form-list"),
    path(
        "<int:site_pk>/forms/create/",
        views.FormCreateView.as_view(),
        name="form-site-create",
    ),
    path(
        "<int:site_pk>/forms/<int:pk>/",
        views.FormUpdateView.as_view(),
        name="form-update",
    ),
    path(
        "<int:site_pk>/forms/<int:pk>/delete/",
        views.FormDeleteView.as_view(),
        name="form-delete",
    ),
]
