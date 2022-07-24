from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from django.urls import path

router = DefaultRouter()
router.register(r'assets', views.AssetViewSet)
router.register(r'contracts', views.ContractViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'reports', views.ReportViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'update-trait', views.update_trait),
]
