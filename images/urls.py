from django.urls import path
from .views import ImageUploadView, ImageListView, ImageChangeView

urlpatterns = [
    path('', ImageListView.as_view(), name='image_list'),
    path('create', ImageUploadView.as_view(), name='image_create'),
    path('resize/<pk>', ImageChangeView.as_view(), name='image_change')
]
