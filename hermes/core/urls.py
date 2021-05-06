from django.urls import path

from hermes.core import views

urlpatterns = [path("", views.IndexView.as_view(), name="index")]
