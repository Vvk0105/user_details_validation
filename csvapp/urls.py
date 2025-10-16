from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.CsvUploadAPiView.as_view(), name='upload'),
    path('upload_file/', views.upload_file, name='upload_file')
]