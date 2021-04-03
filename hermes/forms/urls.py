from django.urls import path

from . import views

urlpatterns = [
    path("sites/create/", views.SiteCreateView.as_view(), name="site-create"),
    path("", views.FormListView.as_view(), name="form-list"),
    path("create/", views.FormCreateView.as_view(), name="form-create"),
    path("delete/<int:pk>", views.FormDeleteView.as_view(), name="form-delete"),
    path("<int:pk>", views.FormUpdateView.as_view(), name="form-update"),
]
