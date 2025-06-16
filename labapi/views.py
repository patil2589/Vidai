from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    def get_queryset(self):
        return Patient.objects.filter(tenant=self.request.tenant)
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class TestRequestViewSet(viewsets.ModelViewSet):
    serializer_class = TestRequestSerializer
    def get_queryset(self):
        return TestRequest.objects.filter(tenant=self.request.tenant)
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

    @action(detail=True, methods=['post'])
    def upload_result(self, request, pk=None):
        tr = self.get_object()
        tr.result_json = request.data.get('result_json')
        tr.save()
        return Response({'status': 'uploaded'})

    @action(detail=True, methods=['get'])
    def download_result(self, request, pk=None):
        return Response(self.get_object().result_json)

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    def get_queryset(self):
        return Invoice.objects.filter(tenant=self.request.tenant)
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

class AnalyticsViewSet(ViewSet):
    def list(self, request):
        tenant = request.tenant
        return Response({
            'total_tests': TestRequest.objects.filter(tenant=tenant).count(),
            'total_revenue': Invoice.objects.filter(tenant=tenant, paid=True).aggregate(models.Sum('total_amount'))['total_amount__sum'] or 0,
            'pending_invoices': Invoice.objects.filter(tenant=tenant, paid=False).count()
        })
