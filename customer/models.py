from django.db import models

# Create your models here.

class Principal(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Shipper(models.Model):
    principal = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name="shippers")
    name = models.CharField(max_length=50, blank=True, default='')
    address = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return self.name