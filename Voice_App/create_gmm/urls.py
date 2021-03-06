from django.urls import path
from . import views

urlpatterns = [
        path('createmodel', views.ModelCreateView.as_view(), name="create-model"),
        path('update/<int:pk>/', views.ModelUpdateView.as_view(), name="update-model"),
        path('mymodel/<int:pk>/', views.ModelDetailView.as_view(), name="detail-model"),
        path('delete/<int:pk>/', views.ModelDeleteView.as_view(), name="delete-model"),
        path('list/', views.ModelListView.as_view(), name="list-model"),
        path('aboutmodels/', views.AboutGmm, name="about-model")
        ]

