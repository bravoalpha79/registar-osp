from django.urls import path
from . import views

urlpatterns = [
    path("safety_objects/", views.SafetyObjectsApiView.as_view(), name="safety_objects"),
    path("safety_objects/<int:object_id>", views.SafetyObjectApiView.as_view(), name="safety_object"),
]
