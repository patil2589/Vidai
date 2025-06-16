from django.db import models
import uuid

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)

class Patient(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class Test(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class TestRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='pending')
    result_json = models.JSONField(null=True, blank=True)

class Invoice(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    test_request = models.OneToOneField(TestRequest, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)