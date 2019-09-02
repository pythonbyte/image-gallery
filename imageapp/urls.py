from django.urls import path

from .views import (
    ApprovePhotoListView,
    ListPhotosView,
    LikePhotoView,
    ApprovePhotoView,
    DeletePhotoView,
)

urlpatterns = [
    path("", ListPhotosView.as_view(), name="pictures"),
    path("like-picture", LikePhotoView.as_view(), name="like-picture"),
    path(
        "approve-picture", ApprovePhotoListView.as_view(), name="approve-picture-list"
    ),
    path(
        "approve-picture/<int:id>", ApprovePhotoView.as_view(), name="approve-pictures"
    ),
    path("delete-picture/<int:id>", DeletePhotoView.as_view(), name="delete-pictures"),
]
