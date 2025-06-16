from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register('tenants', TenantViewSet)  # This is fine
router.register('patients', PatientViewSet, basename='patients')
router.register('test-requests', TestRequestViewSet, basename='test-requests')
router.register('invoices', InvoiceViewSet, basename='invoices')
router.register('analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
]
