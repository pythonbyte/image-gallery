from django.urls import path

from .views import ApprovePhotoListView, ListPhotosView, LikePhotoView

urlpatterns = [
    path('', ListPhotosView.as_view(), name='pictures'),
    path('like-picture', LikePhotoView.as_view(), name='like-picture'),
    path('approve-picture', ApprovePhotoListView.as_view(), name='approve-picture'),
]