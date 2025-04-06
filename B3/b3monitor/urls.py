from django.contrib import admin
from django.urls import path
from assets.views import AssetListView, AssetDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AssetListView.as_view(), name='asset-list'),
    path('asset/<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
] 
